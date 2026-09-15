"""Deal Risk & Commercial Vulnerability Agent for Phase 58."""
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


class DealRiskAgent(BaseAgent):
    """Monitors deal vulnerabilities across decision-maker access, timeline slippage, and scope expansion."""

    agent_id = "deal_risk_agent"
    name = "Deal Risk & Commercial Vulnerability Agent"
    version = "1.0"
    description = "Detects commercial, technical, and stakeholder risks across active sales opportunities."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
        AgentPermission.ASSESS_DEAL_RISK,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        opportunity_id = context.metadata.get("opportunity_id", "opp-demo-001")
        category = context.metadata.get("risk_category", "decision_maker")
        severity = context.metadata.get("severity", "medium")
        desc = context.metadata.get("description", "Evaluation timeline dependent on corporate legal review")

        risk = self.service.pricing.record_deal_risk(
            opportunity_id=opportunity_id,
            risk_category=category,
            severity=severity,
            description=desc,
        )

        return {
            "status": "SUCCESS",
            "risk_id": risk["id"],
            "opportunity_id": opportunity_id,
            "severity": risk["severity"],
            "risk_details": risk,
        }
