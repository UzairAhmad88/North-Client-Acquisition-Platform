"""Support Intelligence AI Agent Package."""

from agents.support.agent import SupportAgent
from agents.core.registry import global_registry

# Register SupportAgent in global registry
global_registry.register(SupportAgent())

__all__ = ["SupportAgent"]
