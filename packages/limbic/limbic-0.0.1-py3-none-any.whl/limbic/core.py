"""
This is the core of the agent. It is responsible for running the agent and managing the memory.

It uses the ReAct pattern (https://arxiv.org/abs/2210.03629), which is the most common starting pattern for agents.

+-------------------------- ReAct Agent Flow ---------------------------+
|                                                                       |
|                     "Solve using Thought/Action/Observation"          |
|                                                                       |
|    Memory []  <----------------+                                      |
|        |                       |                                      |
|        v                       |                                      |
|  [Prompt + Mem] --> [Call LLM] --> [Parse Tool Calls] --> [Execute]   |
|                          ^                                    |       |
|                      [Loop Back] <-- No ------- [Solved?] <---+       |
|                                                    |                  |
|                                                    v                  |
|                                                   Yes                 |
|                                                    |                  |
|                                                    v                  |
|                                              [Return Result]          |
|-----------------------------------------------------------------------|
"""
import json
import sys
import traceback

from dataclasses import dataclass
from time import time
from typing import List, Any, Tuple

import litellm

from rich.console import Console
from rich.panel import Panel

from limbic.memory import AgentMemory, Memory
from limbic.planning import generate_plan
from limbic.prompts import AGENT_SYSTEM_PROMPT
from limbic.sessions import SessionManager
from limbic.stats import AgentStats, StepStats
from limbic.tools.utils import humanize_tool_descriptions
from limbic.utils import get_quotient_logger

console = Console()
logger = get_quotient_logger()

# LiteLLM call failed: litellm.BadRequestError: AnthropicException - Invalid first message=[]. Should always start with 'role'='user' for Anthropic. System prompt is sent separately for Anthropic. set 'litellm.modify_params = True' or 'litellm_settings:modify_params = True' on proxy, to insert a placeholder user message - '.' as the first message,
litellm.modify_params = True

########################
#### AGENT ############
########################
@dataclass
class AgentConfig:
    """
    Configuration for an agent.
    """
    max_steps: int = 5
    show_steps: bool = False
    tool_choice: str = "auto"
    planning_interval: int = 2  # How often to run planning steps (every N steps)


class Agent:
    """
    A basic agent that can use tools to solve tasks with periodic planning.
    """
    def __init__(
        self,
        name: str,
        tools: List[callable],
        model: str,
        config: AgentConfig = AgentConfig()
    ):
        self.name = name
        self.tools = {tool.__tool_name__: tool for tool in tools}
        self.model = model
        self.config = config
        self.memory = AgentMemory()
        self.session_manager = SessionManager()

        # steps. used to track the current step in the action and planning loop
        # and to save the session information or load the agent from a session
        self.action_step = 0
        self.planning_step = 0
        self.stats = AgentStats()

    @property
    def system_prompt(self) -> str:
        """
        The system prompt for the agent.
        """
        tool_descriptions = humanize_tool_descriptions(self.tools)
        self.memory.system_prompt = AGENT_SYSTEM_PROMPT.format(tool_descriptions=tool_descriptions)
        return self.memory.system_prompt

    def run(self, task: str) -> Any:
        """
        Run the agent on a task until completion or max steps reached.

        The agent follows this loop:
        ============================
        1. Every planning_interval steps, runs a planning phase to analyze progress
           and update its plan
        2. Gets next action from the model using tools or direct responses
        3. Executes the action and records results in memory
        4. Continues until reaching a final answer or max steps

        Args:
            task (str): The task / question for the agent to work on

        Returns:
            Any: The final result. Usually a string for a final answer, or the
                last observation if max steps reached.
        """
        console.print(Panel(
            "\n".join([
                f"[green]Agent[/green]: {self.name}",
                f"[green]Model[/green]: {self.model}",
                f"[green]Tools[/green]: {', '.join([tool.__tool_name__ for tool in self.tools.values()])}",
            ]),
            border_style="green",
            title="Agent Configuration",
            expand=False
        ))

        console.print(Panel(
            f"[green]Task[/green]: {task}",
            border_style="green",
            title="Task",
            expand=False
        ))

        plan = generate_plan(
            model=self.model,
            tools=self.tools,
            task=task,
            remaining_steps=self.config.max_steps,
        )

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task},
            {"role": "assistant", "content": plan}
        ]

        self.memory.task = task

        try:
            # run until the agent returns a final answer
            while True or self.action_step < self.config.max_steps:
                step_start_time = time()
                step_tool_calls = 0
                prompt_tokens = 0
                completion_tokens = 0

                # Add relevant memories to the context
                memory_context = self.memory.get_relevant_memories(task)
                if memory_context:
                    memory_message = {
                        "role": "assistant",
                        "content": f"Previous relevant memories:\n{memory_context}"
                    }
                    # Update the messages list to include memory context
                    messages.insert(1, memory_message)

                # Get model response
                console.print(Panel(
                    f"Calling {self.model} with {len(messages)} messages",
                    border_style="blue",
                    expand=False,
                    title=f"[blue]Model Call[/blue]"
                ))
                response = litellm.completion(
                    model=self.model,
                     # Use updated messages list with memory context
                    messages=messages,
                    tools=[tool.__tool_schema__ for tool in self.tools.values()],
                    tool_choice=self.config.tool_choice,
                )
                assistant_message = response.choices[0].message

                # Store the assistant's response in messages
                messages.append(assistant_message.to_dict())

                # After getting model response, add:
                prompt_tokens += response.usage.prompt_tokens
                completion_tokens += response.usage.completion_tokens

                # Handle tool calls if present
                if assistant_message.tool_calls:
                    step_tool_calls = len(assistant_message.tool_calls)

                    tool_calls = []
                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        formatted_args = [
                            f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}"
                            for k, v in function_args.items()
                        ]
                        console.print(Panel(
                            f"{function_name}({', '.join(formatted_args)})",
                            border_style="blue",
                            expand=False,
                            title="[blue]Tool Call[/blue]"
                        ))

                        try:
                            # Call the function and get result
                            function = self.tools[function_name]
                            function_result = function(**function_args)

                            # Record tool call success so we can add it to the memory
                            tool_calls.append({
                                "name": function_name,
                                "args": function_args,
                                "result": str(function_result),
                                "error": None,
                            })

                            # Create tool response message
                            tool_message = {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": str(function_result)
                            }
                            messages.append(tool_message)
                        except Exception as e:
                            # Record tool call failure so we can add it to the memory
                            tool_calls.append({
                                "name": function_name,
                                "args": function_args,
                                "result": None,
                                "error": str(e)
                            })
                            # Create error tool response
                            tool_message = {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": f"Error: {str(e)}"
                            }
                            messages.append(tool_message)

                            traceback.print_exc()
                            raise Exception(f"Tool call failed: {str(e)}")

                    # Get final response after tool calls
                    final_response = litellm.completion(
                        model=self.model,
                        messages=messages
                    )
                    final_message = final_response.choices[0].message
                    messages.append(final_message.to_dict())

                    prompt_tokens += final_response.usage.prompt_tokens
                    completion_tokens += final_response.usage.completion_tokens

                    # Format action description for all tool calls
                    tool_actions = []
                    for tool_call in tool_calls:
                        name = tool_call["name"]
                        args = tool_call["args"]
                        formatted_args = [
                            f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}"
                            for k, v in args.items()
                        ]
                        tool_actions.append(f"Tool {name} was called with args: {', '.join(formatted_args)}")

                    action = "\n".join(tool_actions)

                    # and format the observation for all tool calls
                    observation = "\n".join([
                        f"Tool {tool_call['name']} returned:\n{tool_call['result']}"
                        for tool_call in tool_calls
                    ])

                    memory = Memory(
                        step=self.action_step,
                        timestamp=time(),
                        messages=messages.copy(),
                        action=action,
                        observation=observation,
                        tool_calls=tool_calls
                    )
                else:
                    # Handle direct responses (like final answers)
                    memory = Memory(
                        step=self.action_step,
                        timestamp=time(),
                        messages=messages.copy(),
                        action="Did not use any tools",
                        observation=assistant_message.content,
                        tool_calls=None,
                    )

                self.memory.add_memory(memory)
                self.action_step += 1

                # Before creating memory object, add stats:
                step_stats = StepStats(
                    step=self.action_step,
                    latency=time() - step_start_time,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    tool_calls=step_tool_calls
                )
                self.stats.add_step(step_stats)

                if self.config.show_steps:
                    step_content = [
                        f"[blue]Action Step[/blue]: {self.action_step}",
                        f"[blue]Action[/blue]:\n{memory.action}",
                        f"[blue]Observation[/blue]:\n{memory.observation}",
                        f"[blue]Error[/blue]:\n{memory.error}",
                        f"[grey53]\n[Duration: {step_stats.latency:.2f}s | Input Tokens: {step_stats.prompt_tokens} | Output Tokens: {step_stats.completion_tokens}][/grey53] "
                    ]
                    console.print(Panel(
                        "\n".join(step_content),
                        border_style="blue",
                        title=f"Action Step {self.action_step}",
                        expand=False
                    ))

                # log to quotient
                # logger.log(
                #     user_query=task,
                #     model_output=assistant_message.content if assistant_message.content else "",
                #     message_history=messages,
                #     tags={
                #         "model": self.model,
                #         "agent-type": "core-agent",
                #         "step": self.action_step,
                #         "tool_calls": step_tool_calls,
                #         **asdict(self.config),
                #     },
                #     hallucination_detection=False,
                # )
                if memory.is_final_answer():
                    self.stats.complete()

                    console.print(
                        Panel(
                            "\n".join([
                                f"Total Steps: {len(self.stats.steps)}",
                                f"Total Duration: {self.stats.total_duration:.2f}s",
                                f"Total Tokens: {self.stats.total_tokens:,}",
                                f"Total Tool Calls: {self.stats.total_tool_calls}",
                                f"Avg Latency per Step: {self.stats.avg_latency_per_step:.2f}s"
                            ]),
                            border_style="green",
                            title="Execution Stats Summary",
                            expand=False
                        ),
                    )
                    return memory.observation
                else:
                    continue
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            # exit gracefully
            sys.exit(1)
        finally:
            self.session_manager.save_session(self, task)

    @classmethod
    def load_from_session(cls, session_path: str) -> Tuple['Agent', str]:
        """
        Load an agent from a saved session file.
        """
        return SessionManager.load_session(session_path, cls)
