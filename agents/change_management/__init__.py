"""Change Management AI Agent Package."""

from agents.change_management.agent import ChangeAgent
from agents.core.registry import global_registry

# Register ChangeAgent in global registry
global_registry.register(ChangeAgent())

__all__ = ["ChangeAgent"]
