"""
Session manager for agent execution.
Handles saving and loading agent sessions as JSON files.
"""

import json
import os

from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Tuple, Type

from rich.console import Console
from rich.panel import Panel

from limbic.tools.inventory import inventory as tools

console = Console()

# load the tools into globals
for tool in tools:
    globals()[tool.__tool_name__] = tool

class SessionManager:
    """
    Handles saving and loading agent sessions.
    """
    def __init__(self, session_dir: str = "sessions"):
        self.session_dir = session_dir
        self.current_session_path = None  # Track the current session file path
        Path(session_dir).mkdir(parents=True, exist_ok=True)
    
    def save_session(self, agent: 'Agent', task: str) -> str:
        """
        Save the current agent session to a JSON file.
        If continuing from a loaded session, updates the existing file.
        Returns the path to the saved session file.
        """
        session_data = {
            'name': agent.name,
            'task': task,
            'model': agent.model,
            'config': asdict(agent.config),
            'tools': [t.__tool_name__ for t in agent.tools.values()],
            'memory': agent.memory.to_dict(),
            'action_step': agent.action_step,
            'planning_step': agent.planning_step,
            'stats': {
                'steps': [asdict(step) for step in agent.stats.steps],
                'start_time': agent.stats.start_time,
                'end_time': agent.stats.end_time
            }
        }

        # If we're continuing from a loaded session, update the existing file
        if self.current_session_path:
            filepath = self.current_session_path
            # Preserve the original timestamp
            with open(filepath, 'r') as f:
                original_data = json.load(f)
                session_data['timestamp'] = original_data['timestamp']
        else:
            # Create new session file with new timestamp
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            session_data['timestamp'] = timestamp
            filename = f"session_{timestamp}.json"
            filepath = os.path.join(self.session_dir, filename)
            self.current_session_path = filepath
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
            
        if agent.config.show_steps:
            console.print(Panel(
                f"Session saved to: {filepath}",
                border_style="green",
                title="Session Saved",
                expand=False
            ))
            
        return filepath

    @staticmethod
    def load_session(session_path: str, agent_cls: Type['Agent']) -> Tuple['Agent', str]:
        """
        Load an agent session from a JSON file.

        Returns a tuple of (agent, task)
        """
        with open(session_path, 'r') as f:
            session_data = json.load(f)
            
        from limbic.core import AgentConfig  # Import here to avoid circular imports
        config = AgentConfig(**session_data['config'])
        tools = [globals()[tool_name] for tool_name in session_data['tools']]
        
        agent = agent_cls(
            tools=tools,
            model=session_data['model'],
            config=config
        )
        
        agent.memory = agent.memory.from_dict(session_data['memory'])
        agent.action_step = session_data['action_step']
        agent.planning_step = session_data['planning_step']
        
        # Set the current session path so we know to update this file
        agent.session_manager.current_session_path = session_path
        
        return agent, session_data['task']
