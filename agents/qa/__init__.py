"""Quality Assurance, UAT & Handover AI Agent Package."""

from agents.qa.agent import QAAgent
from agents.core.registry import global_registry

# Register QAAgent in global registry
global_registry.register(QAAgent())

__all__ = ["QAAgent"]
