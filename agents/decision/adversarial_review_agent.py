"""
Adversarial Review Agent for Phase 53.
Challenges proposal assumptions, surfaces hidden costs, and identifies second-order unintended consequences.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.decision_rooms.service import DecisionRoomPlatformService, global_decision_room_service
except ImportError:
    from app.services.decision_rooms.service import DecisionRoomPlatformService, global_decision_room_service

logger = logging.getLogger(__name__)


class AdversarialReviewAgent(BaseAgent):
    """Adversarial challenger examining weak assumptions, data gaps, and hidden risks."""

    agent_id = "adversarial_review_agent"
    name = "Adversarial Review Agent"
    version = "1.0"
    description = "Conducts adversarial stress-testing, weak assumption detection, and risk critique."
    permissions = {
        AgentPermission.READ_DECISION_ROOM,
        AgentPermission.RUN_ADVERSARIAL_REVIEW,
    }

    def __init__(self, service: Optional[DecisionRoomPlatformService] = None):
        super().__init__()
        self.service = service or global_decision_room_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        room_id = context.metadata.get("room_id")
        critique = context.metadata.get("critique_summary", "Critical analysis of proposal risks and assumptions.")
        weak_assumptions = context.metadata.get("weak_assumptions", [])
        hidden_costs = context.metadata.get("hidden_costs", [])

        review = self.service.specialists.submit_adversarial_review(
            room_id=room_id,
            critique_summary=critique,
            weak_assumptions=weak_assumptions,
            hidden_costs=hidden_costs,
        )
        return {"status": "SUCCESS", "adversarial_review": review}
