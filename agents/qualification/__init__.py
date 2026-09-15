"""Phase 17 Qualification Agent package initialization and auto-registration."""

from agents.core.registry import global_registry
from agents.qualification.agent import QualificationAgent

# Auto-register QualificationAgent in the global registry
global_registry.register(QualificationAgent())

__all__ = ["QualificationAgent"]
