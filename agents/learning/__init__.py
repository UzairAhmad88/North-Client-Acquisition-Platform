"""Business Intelligence & Organizational Learning AI Agent Package."""

from agents.learning.agent import BusinessIntelligenceAgent
from agents.core.registry import global_registry

# Register BusinessIntelligenceAgent in global registry
global_registry.register(BusinessIntelligenceAgent())

__all__ = ["BusinessIntelligenceAgent"]
