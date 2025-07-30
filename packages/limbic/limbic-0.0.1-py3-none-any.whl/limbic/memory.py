from dataclasses import dataclass, asdict
from time import time
from typing import List, Dict, Any, Optional

################
#### MEMORY ####
################
@dataclass
class Memory:
    """
    Represents a single step of agent execution, recording the action taken and its results.
    """
    step: int
    timestamp: float
    messages: List[Dict[str, str]]
    action: str
    observation: Optional[str] = None
    error: Optional[str] = None
    tool_calls: List[Dict[str, Any]] = None

    def is_final_answer(self) -> bool:
        """
        Check if this memory represents a final answer.

        Returns:
        --------
        bool
            True if the memory represents a final answer, False otherwise.
        """
        check = (
            isinstance(self.observation, str) and "final_answer" in self.observation.lower()
        )
        return check

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memory':
        return cls(**data)


@dataclass
class PlanningMemory:
    """
    A memory entry for a planning step.
    """
    step: int
    timestamp: float
    facts: str
    plan: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlanningMemory':
        return cls(**data)


class AgentMemory:
    """
    Manages the agent's memory and message history.
    """
    def __init__(self):
        self.task: Optional[str] = None
        self.system_prompt: Optional[str] = None

        self.memories: List[Memory] = []
        self.planning_memories: List[PlanningMemory] = []
        self.message_history: List[Dict[str, str]] = []


    def add_memory(self, memory: Memory):
        """Add a memory entry with current message context."""
        if memory.messages:
            self.message_history.extend(memory.messages)

        self.memories.append(memory)

    def add_planning_memory(self, memory: PlanningMemory):
        """Add a planning memory to the agent's memory."""
        self.planning_memories.append(memory)
    
    def get_memory_messages(self) -> List[Dict[str, str]]:
        """Convert memories into LLM context format with enhanced structure."""
        messages = []
        
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})

        messages.extend(self.message_history)

        return messages

    def _generate_memory_summary(self) -> str:
        """Generate a structured summary of all memories."""
        summary = []
        
        # Add key interactions
        summary.append("Previous Interactions:")
        for mem in self.memories[:-5]:  # Exclude most recent ones as they'll be in full context
            if mem.messages:
                for msg in mem.messages:
                    if msg['role'] == 'assistant' and 'tool_calls' in msg:
                        summary.append(f"Step {mem.step}: Used tool {msg['tool_calls'][0]['function']['name']}")
                    elif msg['role'] == 'tool':
                        summary.append(f"Step {mem.step}: Tool returned: {msg['content'][:100]}...")
        
        # Add planning history
        if self.planning_memories:
            summary.append("\nPlanning History:")
            for plan_mem in self.planning_memories:
                summary.append(f"Step {plan_mem.step}:")
                summary.append(f"Facts: {plan_mem.facts}")
                summary.append(f"Plan: {plan_mem.plan}")

        return "\n".join(summary)

    def summary(self) -> str:
        """
        Get a human-readable summary of the agent's memory.
        """
        summary = []
        for mem in self.memories:
            summary.append(f"Step {mem.step} (Time: {mem.timestamp}):")
            summary.append(f"Action:\n{mem.action}")

            if mem.error:
                summary.append(f"Error: {mem.error}")
            else:
                summary.append(f"Observation: {mem.observation}")

            summary.append("-" * 40)

        return "\n".join(summary)

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary format."""
        return {
            'memories': [m.to_dict() for m in self.memories],
            'planning_memories': [m.to_dict() for m in self.planning_memories],
            'system_prompt': self.system_prompt,
            'message_history': self.message_history,
            'task': self.task
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMemory':
        """Create memory from dictionary format."""
        memory = cls()
        memory.memories = [Memory.from_dict(m) for m in data['memories']]
        memory.planning_memories = [PlanningMemory.from_dict(m) for m in data['planning_memories']]
        memory.system_prompt = data['system_prompt']
        memory.message_history = data.get('message_history', [])
        memory.task = data.get('task')
        return memory

    def get_relevant_memories(self, query: str) -> str:
        """
        Retrieve memories relevant to the current query/task.

        Returns a formatted string of relevant memories.
        """
        # For now, return a simple chronological summary of previous actions and observations
        relevant_memories = []
        for mem in self.memories:
            memory_entry = f"Step {mem.step}:\n"
            memory_entry += f"Action: {mem.action}\n"

            if mem.observation:
                memory_entry += f"Observation: {mem.observation}\n"
            if mem.error:
                memory_entry += f"Error: {mem.error}\n"

            relevant_memories.append(memory_entry)
        
        if not relevant_memories:
            return ""
        
        return "\n".join(relevant_memories)