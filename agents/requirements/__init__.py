"""Requirements Agent package exports and auto-registration."""

from agents.core.registry import global_registry
from agents.requirements.agent import RequirementsAgent, requirements_agent
from agents.requirements.models import RequirementsAnalysisResult

try:
    global_registry.register(requirements_agent)
except Exception:
    pass

__all__ = [
    "RequirementsAgent",
    "requirements_agent",
    "RequirementsAnalysisResult",
]
