"""Sales Pipeline & Opportunity Intelligence Agent for Phase 58."""
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


class PipelineAgent(BaseAgent):
    """Manages opportunity health, tracks deal velocity, and monitors stage progression."""

    agent_id = "pipeline_agent"
    name = "Sales Pipeline Agent"
    version = "1.0"
    description = "Evaluates opportunity health across engagement, decision access, and budget evidence."
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
        opportunity_id = context.metadata.get("opportunity_id")
        
        if not opportunity_id:
            opps = self.service.pipeline.list_opportunities()
            if not opps:
                return {"status": "FAILED", "error": "No opportunities found in pipeline"}
            opportunity_id = opps[0]["id"]

        health = self.service.pipeline.evaluate_opportunity_health(
            opportunity_id=opportunity_id,
            engagement_score=context.metadata.get("engagement_score", 85.0),
            decision_access_score=context.metadata.get("decision_access_score", 80.0),
            budget_evidence_score=context.metadata.get("budget_evidence_score", 90.0),
        )

        return {
            "status": "SUCCESS",
            "opportunity_id": opportunity_id,
            "overall_health_score": health["overall_health_score"],
            "health_state": health["health_state"],
        }
