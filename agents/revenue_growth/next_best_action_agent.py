"""Sales Next-Best-Action & Negotiation Assistant Agent for Phase 58."""
from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.revenue_growth.service import RevenueGrowthPlatformService
except ImportError:
    from app.services.revenue_growth.service import RevenueGrowthPlatformService

logger = logging.getLogger(__name__)


class NextBestActionAgent(BaseAgent):
    """Generates evidence-backed next-best sales actions without taking autonomous external actions."""

    agent_id = "next_best_action_agent"
    name = "Sales Next-Best-Action Agent"
    version = "1.0"
    description = "Recommends high-leverage next actions for sales reps based on deal signals and customer requirements."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
        AgentPermission.MANAGE_SALES_PIPELINE,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        opportunity_id = context.metadata.get("opportunity_id", "opp-demo-001")
        action = context.metadata.get("recommended_action", "Provide customized ROI analysis and case studies")
        action_type = context.metadata.get("action_type", "deliver_roi_case_study")

        nba = self.service.pricing.recommend_next_best_action(
            opportunity_id=opportunity_id,
            recommended_action=action,
            action_type=action_type,
        )

        return {
            "status": "SUCCESS",
            "opportunity_id": opportunity_id,
            "recommended_action": nba["recommended_action"],
            "confidence": nba["confidence"],
            "action_details": nba,
        }
