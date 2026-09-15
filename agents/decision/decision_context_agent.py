"""
Decision Context Agent for Phase 53.
Assembles background context, organizational memory links, and relevant constraints for Decision Rooms.
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


class DecisionContextAgent(BaseAgent):
    """Assembles context, relevant policies, and background data for a Decision Room."""

    agent_id = "decision_context_agent"
    name = "Decision Context Agent"
    version = "1.0"
    description = "Assembles background context, memory references, and organizational constraints."
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
        if not room_id:
            return {"status": "FAILED", "error": "room_id required in context metadata"}

        background = context.metadata.get("background", "Context assembly requested by user.")
        constraints = context.metadata.get("constraints", [])
        entities = context.metadata.get("entities", [])

        ctx = self.service.context_evidence.set_context(
            room_id=room_id,
            background=background,
            constraints=constraints,
            entities_involved=entities,
        )
        return {"status": "SUCCESS", "context": ctx}
