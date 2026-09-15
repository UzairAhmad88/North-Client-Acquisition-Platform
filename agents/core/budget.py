"""Agent Run Budget Tracking and Controls."""

import time
from dataclasses import dataclass
from typing import Optional

from agents.core.errors import AgentBudgetExceededError


@dataclass
class AgentBudget:
    """Tracking and bounds for agent step, tool call, runtime, and token limits."""

    max_steps: int = 10
    steps_used: int = 0
    max_tool_calls: int = 8
    tool_calls_used: int = 0
    max_runtime_seconds: int = 60
    started_at: Optional[float] = None
    max_tokens: int = 8000
    tokens_used: int = 0
    estimated_cost: float = 0.0

    def start(self) -> None:
        """Mark start timestamp."""
        if self.started_at is None:
            self.started_at = time.time()

    def increment_step(self) -> None:
        """Increment step count and check budget."""
        self.steps_used += 1
        if self.steps_used > self.max_steps:
            raise AgentBudgetExceededError(
                f"Step budget exceeded: {self.steps_used} > max {self.max_steps} steps."
            )
        self.check_runtime()

    def increment_tool_call(self) -> None:
        """Increment tool call count and check budget."""
        self.tool_calls_used += 1
        if self.tool_calls_used > self.max_tool_calls:
            raise AgentBudgetExceededError(
                f"Tool call budget exceeded: {self.tool_calls_used} > max {self.max_tool_calls} calls."
            )
        self.check_runtime()

    def add_tokens(self, tokens: int, cost: float = 0.0) -> None:
        """Add token usage and estimated cost."""
        self.tokens_used += tokens
        self.estimated_cost += cost
        if self.tokens_used > self.max_tokens:
            raise AgentBudgetExceededError(
                f"Token budget exceeded: {self.tokens_used} > max {self.max_tokens} tokens."
            )

    def check_runtime(self) -> None:
        """Check runtime elapsed seconds."""
        if self.started_at is not None:
            elapsed = time.time() - self.started_at
            if elapsed > self.max_runtime_seconds:
                raise AgentBudgetExceededError(
                    f"Runtime limit exceeded: {elapsed:.1f}s > max {self.max_runtime_seconds}s."
                )
