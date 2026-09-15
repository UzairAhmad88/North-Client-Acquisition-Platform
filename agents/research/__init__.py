"""Research Agent Package."""

from agents.core.registry import global_registry
from agents.research.agent import ResearchAgent

# Automatic registration of ResearchAgent into AgentRegistry
_research_agent = ResearchAgent()
try:
    global_registry.register(_research_agent)
except ValueError:
    pass  # Already registered

__all__ = ["ResearchAgent"]
