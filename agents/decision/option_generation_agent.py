"""
Option Generation Agent for Phase 53.
Synthesizes candidate alternatives, decision criteria, and multi-factor trade-offs.
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


class OptionGenerationAgent(BaseAgent):
    """Generates distinct candidate options, evaluates decision criteria, and builds trade-offs."""

    agent_id = "option_generation_agent"
    name = "Option Generation Agent"
    version = "1.0"
    description = "Formulates diverse candidate alternatives and calculates weighted decision matrices."
    permissions = {
        AgentPermission.READ_DECISION_ROOM,
        AgentPermission.GENERATE_DECISION_OPTIONS,
        AgentPermission.EVALUATE_DECISION_TRADEOFFS,
    }

    def __init__(self, service: Optional[DecisionRoomPlatformService] = None):
        super().__init__()
        self.service = service or global_decision_room_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        room_id = context.metadata.get("room_id")
        name = context.metadata.get("name", "Alternative Option")
        description = context.metadata.get("description", "Generated candidate option.")
        benefits = context.metadata.get("benefits", [])
        costs = float(context.metadata.get("costs", 0.0))

        option = self.service.assumptions_options.create_option(
            room_id=room_id,
            name=name,
            description=description,
            benefits=benefits,
            costs=costs,
        )
        return {"status": "SUCCESS", "option": option}
