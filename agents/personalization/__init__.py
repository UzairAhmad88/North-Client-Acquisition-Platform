"""Personalization Agent Package."""

from agents.core.registry import global_registry
from agents.personalization.agent import PersonalizationAgent

# Register Personalization Agent into global registry
personalization_agent = PersonalizationAgent()
global_registry.register(personalization_agent)

__all__ = ["PersonalizationAgent", "personalization_agent"]
