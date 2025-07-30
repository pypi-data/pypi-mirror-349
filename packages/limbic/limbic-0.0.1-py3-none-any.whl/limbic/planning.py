import textwrap

from typing import List, Callable
from time import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

import litellm

from limbic.memory import PlanningMemory

console = Console()

# Prompt used during the initial planning step
# TODO: add this back in:
# based on:
# 1. these facts:
# {facts}

# 2. this progress analysis:
# {progress_analysis}

PLANNING_SYSTEM_PROMPT_TEMPLATE = textwrap.dedent("""
You are a world expert at analyzing a situation to derive facts, and plan accordingly towards solving a task.
Below I will present you a task. You will need to 1. build a survey of facts known or needed to solve the task, then 2. make a plan of action to solve the task.

## 1. Facts survey
You will build a comprehensive preparatory survey of which facts we have at our disposal and which ones we still need.
These "facts" will typically be specific names, dates, values, etc. Your answer should use the below headings:

### 1.1. Facts given in the task
List here the specific facts given in the task that could help you (there might be nothing here).

### 1.2. Facts to look up
List here any facts that we may need to look up.
Also list where to find each of these, for instance a website, a file... - maybe the task contains some sources that you should re-use here.

### 1.3. Facts to derive
List here anything that we want to derive from the above by logical reasoning, for instance computation or simulation.

Don't make any assumptions. For each item, provide a thorough reasoning. Do not add anything else on top of three headings above.

## 2. Plan

Then for the given task, develop a step-by-step high-level plan taking into account the above inputs and list of facts.
This plan should involve individual tasks based on the available tools, that if executed correctly will yield the correct answer.
Do not skip steps, do not add any superfluous steps. Only write the high-level plan, DO NOT DETAIL INDIVIDUAL TOOL CALLS.
After writing the final step of the plan, write the '\n<end_plan>' tag and stop there.

You can leverage these tools:
{tool_descriptions}

---
Now begin! Here is your task:
```
{task}
```
First in part 1, write the facts survey, then in part 2, write your plan.
""")


def generate_plan(task: str, remaining_steps: int, model: str, tools: List[Callable]) -> str:
    """
    Generate a plan for the agent to solve a task.
    """
    # show rich progress bar for planning step showing we're in the planning step
    # and processing the task
    # analyze progress against previous plan if it exists
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Planning...", total=None)

        # make a plan incorporating progress analysis
        tool_descriptions = "\n".join(
            "- {name}: {description}".format(
                name=name,
                description=tool.__tool_description__.split('\n')[0]
            )
            for name, tool in tools.items()
        )
        planning_system_prompt = PLANNING_SYSTEM_PROMPT_TEMPLATE.format(
            task=task,
            remaining_steps=remaining_steps,
            tool_descriptions=tool_descriptions,
        )

        plan_response = litellm.completion(
            model=model,
            messages=[{"role": "system", "content": planning_system_prompt}]
        )
        plan = textwrap.dedent(f"""
Here is the plan I will follow in order to solve the task:

{plan_response.choices[0].message.content}
        """)

        # store the planning memories
        # planning_memory = PlanningMemory(
        #     step=0,
        #     timestamp=time(),
        #     facts=None,
        #     plan=plan
        # )

        console.print(Panel(
            f"[blue]Planning Step[/blue]:\n{plan}",
            border_style="blue",
            expand=False,
            title=f"[blue]Planning Step[/blue]:\n{plan}",
        ))

        return plan