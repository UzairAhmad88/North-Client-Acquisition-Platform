"""Contract Agent package exports and auto-registration."""

from agents.contracts.agent import ContractAgent, contract_agent
from agents.contracts.models import ContractGenerationResult
from agents.core.registry import global_registry

try:
    global_registry.register(contract_agent)
except Exception:
    pass

__all__ = [
    "ContractAgent",
    "contract_agent",
    "ContractGenerationResult",
]
