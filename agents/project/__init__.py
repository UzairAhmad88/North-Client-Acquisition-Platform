"""Project Execution AI Agent Package."""

from agents.core.registry import global_registry
from agents.project.agent import ProjectAgent

# Register ProjectAgent in global registry
global_registry.register(ProjectAgent())

__all__ = ["ProjectAgent"]
