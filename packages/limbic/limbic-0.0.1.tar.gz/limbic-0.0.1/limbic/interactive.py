"""
This module contains modifications to the core Agent class to make it better suited
for interactive sessions with continuous user input.
"""
import json
import time

from typing import Any, List

import litellm

from rich.console import Console
from rich.panel import Panel

from limbic.core import Agent, AgentConfig
from limbic.memory import Memory
from limbic.stats import StepStats

console = Console()

class InteractiveAgent(Agent):
    """
    A version of the Agent that's better suited for interactive, conversational use.
    """
    
    def chat(self, user_message: str) -> str:
        """
        Process a user message in conversational mode, returning a response
        without necessarily reaching a "final answer" state.
        
        Args:
            user_message: The user's message
            
        Returns:
            The agent's response
        """
        step_start_time = time.time()
        step_tool_calls = 0
        prompt_tokens = 0
        completion_tokens = 0
        
        # Set task if this is the first message
        if not self.memory.task:
            self.memory.task = "Interactive conversation"
        
        # Create base messages including system prompt and new user message
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Add relevant memories to the context
        memory_context = self.memory.get_relevant_memories(user_message)
        if memory_context:
            memory_message = {
                "role": "assistant", 
                "content": f"Previous relevant memories:\n{memory_context}"
            }
            messages.insert(1, memory_message)
        
        try:
            # Get model response
            response = litellm.completion(
                model=self.model,
                messages=messages,
                tools=[tool.__tool_schema__ for tool in self.tools.values()],
                tool_choice=self.config.tool_choice,
            )
            assistant_message = response.choices[0].message
            
            # Store the assistant's response in messages
            messages.append(assistant_message.to_dict())
            
            prompt_tokens += response.usage.prompt_tokens
            completion_tokens += response.usage.completion_tokens
            
            # Handle tool calls if present
            if assistant_message.tool_calls:
                step_tool_calls = len(assistant_message.tool_calls)
                
                tool_calls = []
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    try:
                        # Call the function and get result
                        function = self.tools[function_name]
                        function_result = function(**function_args)
                        
                        # Record tool call success
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
                        # Record tool call failure
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
                
                # Format the observation for all tool calls
                observation = "\n".join([
                    f"Tool {tool_call['name']} returned: {tool_call['result'] or tool_call['error']}"
                    for tool_call in tool_calls
                ])
                
                memory = Memory(
                    step=self.action_step,
                    timestamp=time.time(),
                    messages=messages.copy(),
                    action=action,
                    observation=observation,
                    tool_calls=tool_calls
                )
                response_text = final_message.content
            else:
                # Direct response without tool calls
                memory = Memory(
                    step=self.action_step,
                    timestamp=time.time(),
                    messages=messages.copy(),
                    action="Direct response",
                    observation=assistant_message.content,
                    tool_calls=None
                )
                response_text = assistant_message.content
            
            # Add to memory and increment step
            self.memory.add_memory(memory)
            self.action_step += 1
            
            # Track stats
            step_stats = StepStats(
                step=self.action_step,
                latency=time.time() - step_start_time,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                tool_calls=step_tool_calls
            )
            self.stats.add_step(step_stats)
            
            if self.config.show_steps:
                step_content = [
                    f"[blue]Chat Step[/blue]: {self.action_step}",
                    f"[blue]Action[/blue]:\n{memory.action}",
                    f"[blue]Response[/blue]:\n{response_text}"
                ]
                console.print(Panel(
                    "\n".join(step_content),
                    border_style="blue",
                    title=f"Chat Step {self.action_step}",
                    expand=False
                ))

            # log to quotient
            logger.log(
                user_query=user_message,
                model_output=response_text,
                message_history=messages,
                tags={
                    "model": self.model,
                    "agent-type": "interactive",
                    "step": self.action_step,
                    "tool_calls": step_tool_calls,
                    **asdict(self.config),
                },
                hallucination_detection=False,
            )
            
            return response_text
        except Exception as e:
            console.print(f"[red]Error in chat: {e}[/red]")
            return f"I encountered an error: {str(e)}" 