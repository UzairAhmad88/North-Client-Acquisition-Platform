"""Base Agent Specification Interface."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from agents.core.context import AgentContext
from agents.core.permissions import validate_agent_permissions


@dataclass
class AgentResult:
    """Standard structured output returned by all agent executions."""

    status: str = "completed"
    result: Dict[str, Any] = field(default_factory=dict)
    confidence: str = "MEDIUM"
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    next_action: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent:
    """Base interface for all North's Agent implementations."""

    name: str = "base_agent"
    version: str = "1.0"
    description: str = "Base agent interface"
    enabled: bool = True
    permissions: Set[str] = set()
    max_steps: int = 10
    max_tool_calls: int = 8
    max_runtime_seconds: int = 60

    def __init__(self) -> None:
        # Validate permissions at instantiation time
        validate_agent_permissions(self.permissions)

    async def run(self, context: AgentContext) -> AgentResult:
        """Execute agent task asynchronously and return structured AgentResult."""
        raise NotImplementedError("Subclasses must implement run(context)")
