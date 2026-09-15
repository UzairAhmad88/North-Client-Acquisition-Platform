"""
Evidence Agent for Phase 53.
Ingests, categorizes (Fact vs Inference), and validates provenance of evidence items in Decision Rooms.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.decision_rooms.service import DecisionRoomPlatformService, global_decision_room_service
    from backend.app.services.decision_rooms.base import EvidenceType, StatementCategory
except ImportError:
    from app.services.decision_rooms.service import DecisionRoomPlatformService, global_decision_room_service
    from app.services.decision_rooms.base import EvidenceType, StatementCategory

logger = logging.getLogger(__name__)


class EvidenceAgent(BaseAgent):
    """Categorizes and links evidence items with fact vs inference classification."""

    agent_id = "evidence_agent"
    name = "Evidence Agent"
    version = "1.0"
    description = "Extracts and categorizes evidence into FACT, INFERENCE, HYPOTHESIS, and UNKNOWN."
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
        claim = context.metadata.get("claim", "")
        source = context.metadata.get("source", "System Analysis")
        ev_type = context.metadata.get("evidence_type", EvidenceType.DATABASE)

        category = self.service.context_evidence.classify_statement(claim, str(ev_type))
        item = self.service.context_evidence.add_evidence(
            room_id=room_id,
            evidence_type=ev_type,
            source=source,
            claim=claim,
            statement_category=category,
        )
        return {"status": "SUCCESS", "evidence_item": item}
