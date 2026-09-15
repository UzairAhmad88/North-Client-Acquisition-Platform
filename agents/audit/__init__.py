"""Phase 16 Audit Agent package initialization and auto-registration."""

from agents.audit.agent import AuditAgent
from agents.core.registry import global_registry

# Auto-register AuditAgent in the global registry
global_registry.register(AuditAgent())

__all__ = ["AuditAgent"]
