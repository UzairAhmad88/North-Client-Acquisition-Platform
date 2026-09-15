"""Decision Intelligence AI Agent Package."""

from agents.decision_intelligence.agent import DecisionIntelligenceAgent
from agents.core.registry import global_registry

# Register DecisionIntelligenceAgent in global registry
global_registry.register(DecisionIntelligenceAgent())

__all__ = ["DecisionIntelligenceAgent"]
