"""Client Collaboration AI Agent Package."""

from agents.client_collaboration.agent import ClientCollaborationAgent
from agents.core.registry import global_registry

# Register ClientCollaborationAgent in global registry
global_registry.register(ClientCollaborationAgent())

__all__ = ["ClientCollaborationAgent"]
