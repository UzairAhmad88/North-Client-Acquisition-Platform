"""AgentState structure and transition rules."""

from typing import Any, Dict, List, Set, TypedDict, Optional
from agents.core.errors import AgentStateInvalidError


# Allowed workflow run status states
VALID_STATES: Set[str] = {
    "CREATED",
    "RUNNING",
    "WAITING_FOR_APPROVAL",
    "PAUSED",
    "COMPLETED",
    "FAILED",
    "CANCELLED",
}

# Allowed transition graph
VALID_TRANSITIONS: Dict[str, Set[str]] = {
    "CREATED": {"RUNNING", "CANCELLED"},
    "RUNNING": {"WAITING_FOR_APPROVAL", "PAUSED", "COMPLETED", "FAILED", "CANCELLED"},
    "WAITING_FOR_APPROVAL": {"RUNNING", "COMPLETED", "FAILED", "CANCELLED"},
    "PAUSED": {"RUNNING", "CANCELLED"},
    "COMPLETED": set(),
    "FAILED": set(),
    "CANCELLED": set(),
}


def validate_state_transition(current_state: str, new_state: str) -> None:
    """Validate that state transition follows allowed graph transitions."""
    curr = current_state.upper()
    nxt = new_state.upper()

    if curr not in VALID_STATES:
        raise AgentStateInvalidError(f"Invalid current state '{curr}'.")
    if nxt not in VALID_STATES:
        raise AgentStateInvalidError(f"Invalid target state '{nxt}'.")

    if nxt not in VALID_TRANSITIONS.get(curr, set()):
        raise AgentStateInvalidError(
            f"Invalid state transition: Cannot transition from '{curr}' to '{nxt}'."
        )


class AgentState(TypedDict, total=False):
    workflow_id: str
    lead_id: Optional[str]
    business_id: Optional[str]
    business_profile: Dict[str, Any]
    research_data: Dict[str, Any]
    audit_data: Dict[str, Any]
    score_data: Dict[str, Any]
    recommended_services: List[Dict[str, Any]]
    outreach_draft: Dict[str, Any]
    approval_status: str
    conversation_context: List[Dict[str, Any]]
    response_analysis: Dict[str, Any]
    next_action: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    confidence: str
