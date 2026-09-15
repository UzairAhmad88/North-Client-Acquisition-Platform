"""Solution Agent package exports and auto-registration."""

from agents.core.registry import global_registry
from agents.solution.agent import SolutionAgent, solution_agent
from agents.solution.models import SolutionDesignResult

try:
    global_registry.register(solution_agent)
except Exception:
    pass

__all__ = [
    "SolutionAgent",
    "solution_agent",
    "SolutionDesignResult",
]
