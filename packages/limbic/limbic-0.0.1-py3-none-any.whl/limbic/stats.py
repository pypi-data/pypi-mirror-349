"""
Statistics for agent execution.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from time import time

@dataclass
class StepStats:
    """Statistics for a single step of agent execution"""
    step: int
    latency: float  # Time taken for this step in seconds
    prompt_tokens: int
    completion_tokens: int
    tool_calls: int
    timestamp: float = field(default_factory=time)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

@dataclass
class AgentStats:
    """Tracks statistics for an agent's execution"""
    steps: List[StepStats] = field(default_factory=list)
    start_time: float = field(default_factory=time)
    end_time: float = None

    def add_step(self, stats: StepStats):
        self.steps.append(stats)

    def complete(self):
        self.end_time = time()

    @property
    def total_duration(self) -> float:
        if not self.end_time:
            return time() - self.start_time
        return self.end_time - self.start_time

    @property
    def total_tokens(self) -> int:
        return sum(step.total_tokens for step in self.steps)

    @property
    def total_tool_calls(self) -> int:
        return sum(step.tool_calls for step in self.steps)

    @property
    def avg_latency_per_step(self) -> float:
        if not self.steps:
            return 0
        return sum(step.latency for step in self.steps) / len(self.steps)

    def summary(self) -> Dict[str, float]:
        return {
            "total_steps": len(self.steps),
            "total_duration": self.total_duration,
            "total_tokens": self.total_tokens,
            "total_tool_calls": self.total_tool_calls,
            "avg_latency_per_step": self.avg_latency_per_step,
        } 