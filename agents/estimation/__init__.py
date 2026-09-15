"""Estimation Agent package exports and auto-registration."""

from agents.core.registry import global_registry
from agents.estimation.agent import EstimationAgent, estimation_agent
from agents.estimation.models import EstimationResult

try:
    global_registry.register(estimation_agent)
except Exception:
    pass

__all__ = [
    "EstimationAgent",
    "estimation_agent",
    "EstimationResult",
]
