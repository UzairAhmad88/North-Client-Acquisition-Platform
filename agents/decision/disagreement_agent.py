"""
Disagreement and Consensus Agent for Phase 53.
Identifies, categorizes, and surfaces explicit disagreements between human stakeholders and AI specialists.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.decision_rooms.service import DecisionRoomPlatformService, global_decision_room_service
    from backend.app.services.decision_rooms.base import DisagreementCategory
except ImportError:
    from app.services.decision_rooms.service import DecisionRoomPlatformService, global_decision_room_service
    from app.services.decision_rooms.base import DisagreementCategory

logger = logging.getLogger(__name__)


class DisagreementAgent(BaseAgent):
    """Detects and categorizes disagreements without forcing false consensus."""

    agent_id = "disagreement_agent"
    name = "Disagreement Agent"
    version = "1.0"
    description = "Surfaces and categorizes factual, strategic, and risk disagreements."
    permissions = {
        AgentPermission.READ_DECISION_ROOM,
        AgentPermission.ANALYZE_DECISION_CONTEXT,
    }

    def __init__(self, service: Optional[DecisionRoomPlatformService] = None):
        super().__init__()
        self.service = service or global_decision_room_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        room_id = context.metadata.get("room_id")
        topic = context.metadata.get("topic", "Divergent Forecasts")
        category = context.metadata.get("disagreement_category", DisagreementCategory.FACTUAL)
        party_a = context.metadata.get("party_a", "Finance Specialist")
        view_a = context.metadata.get("view_a", "Conservative margin assumptions")
        party_b = context.metadata.get("party_b", "Growth Specialist")
        view_b = context.metadata.get("view_b", "Aggressive adoption assumptions")

        disag = self.service.specialists.register_disagreement(
            room_id=room_id,
            topic=topic,
            disagreement_category=category,
            party_a=party_a,
            view_a=view_a,
            party_b=party_b,
            view_b=view_b,
        )
        return {"status": "SUCCESS", "disagreement": disag}
