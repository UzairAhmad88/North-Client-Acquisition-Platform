"""Proposal Agent package exports and auto-registration."""

from agents.core.registry import global_registry
from agents.proposal.agent import ProposalAgent, proposal_agent
from agents.proposal.models import ProposalGenerationResult

try:
    global_registry.register(proposal_agent)
except Exception:
    pass

__all__ = [
    "ProposalAgent",
    "proposal_agent",
    "ProposalGenerationResult",
]
