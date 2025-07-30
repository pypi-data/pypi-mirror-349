# Limbic - A Framework for Building AI Agents

Limbic is a Python framework for building AI agents that can use tools, maintain memory, and plan their actions. It's designed to be modular, extensible, and easy to use.

## Features

- 🤖 ReAct pattern implementation for tool use
- 🧠 Memory management for maintaining context
- 📝 Planning capabilities for complex tasks
- 🛠️ Easy tool creation and management
- 📊 Built-in statistics and logging
- 💾 Session management for saving/loading agent state

## Installation

```bash
# Clone the repository
git clone https://github.com/quotient-ai/limbic.git
cd limbic

# Install dependencies using Poetry
poetry install
```

## Quick Start

Here's a simple example of creating and using an agent:

```python
from limbic.core import Agent, AgentConfig
from limbic.tools import calculator, stock_price

# Create an agent with some tools
agent = Agent(
    tools=[calculator, stock_price],
    model="gpt-4o-mini",
    config=AgentConfig()
)

# Run a task
result = agent.run("Calculate the total cost of buying 10 shares of AAPL")
print(result)
```

## Creating Custom Tools

You can create custom tools using the `@tool` decorator:

```python
from limbic.tools import tool

@tool
def my_custom_tool(param1: str, param2: int) -> str:
    """
    A custom tool that does something interesting.

    Parameters:
    -----------
    param1: str
        Description of param1
    param2: int
        Description of param2

    Returns:
    --------
    str
        Description of the return value
    """
    # Your tool implementation here
    return f"Processed {param1} {param2} times"
```

## Agent Configuration

The `AgentConfig` class allows you to customize agent behavior:

```python
from limbic.core import AgentConfig

config = AgentConfig(
    max_steps=10,          # Maximum number of steps before stopping
    show_steps=True,       # Show detailed step information
    tool_choice="auto",    # Tool selection mode
    planning_interval=2    # How often to run planning steps
)
```

## Memory Management

The framework includes built-in memory management treated as short-term memory (i.e. the message history).

```python
from limbic.memory import AgentMemory

# Memory is automatically managed by the agent
agent = Agent(
    tools=[...],
    model="gpt-4-turbo-preview"
)

# The agent will maintain context between steps
result = agent.run("First task")
result = agent.run("Follow-up task using previous context")
```

## Session Management

You can save and load agent sessions:

```python
# Save a session
agent.save_session("my_session.json")

# Load a session
loaded_agent = Agent.load_from_session("my_session.json")
```

## Error Handling

Tools should use the `ToolExecutionError` for proper error handling:

```python
from limbic.tools import tool, ToolExecutionError

@tool
def my_tool():
    try:
        # Your tool implementation
        pass
    except Exception as e:
        raise ToolExecutionError(
            message="User-friendly error message",
            developer_message=f"Detailed error: {str(e)}"
        )
```

## Example: Research Agent

Here's how to create a research agent using the framework:

```python
from limbic.core import Agent, AgentConfig
from limbic.research import get_research_tools

# Create a research agent
agent = Agent(
    tools=get_research_tools(),
    model="gpt-4o-mini",
    config=AgentConfig()
)

# Run a research task
result = agent.run("Research the latest developments in quantum computing")
```

## Contributing

## License
