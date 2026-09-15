"""
Post-Decision Learning Agent for Phase 53.
Conducts retrospective outcome variance analysis and feeds lessons into Organizational Memory (Phase 48).
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


class PostDecisionLearningAgent(BaseAgent):
    """Evaluates decision quality, categorizes retrospective errors, and extracts institutional lessons."""

    agent_id = "post_decision_learning_agent"
    name = "Post-Decision Learning Agent"
    version = "1.0"
    description = "Conducts post-decision retrospective analysis and captures organizational memory lessons."
    permissions = {
        AgentPermission.READ_DECISION_ROOM,
        AgentPermission.RECORD_DECISION_POST_REVIEW,
    }

    def __init__(self, service: Optional[DecisionRoomPlatformService] = None):
        super().__init__()
        self.service = service or global_decision_room_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        room_id = context.metadata.get("room_id")
        reviewed_by = context.metadata.get("reviewed_by", "system_auditor")
        outcome_rating = context.metadata.get("outcome_rating", "SUCCESSFUL")
        lessons = context.metadata.get("lessons", ["Documented assumptions improve post-decision error attribution."])

        review = self.service.outcomes_journal.submit_post_review(
            room_id=room_id,
            reviewed_by=reviewed_by,
            outcome_rating=outcome_rating,
            lessons_learned=lessons,
        )
        return {"status": "SUCCESS", "post_review": review}
