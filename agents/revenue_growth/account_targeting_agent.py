"""Target Account Scoring & Prioritization Agent for Phase 58."""
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


class AccountTargetingAgent(BaseAgent):
    """Scores target accounts against ICP fit, digital gap, and revenue potential."""

    agent_id = "account_targeting_agent"
    name = "Target Account Scoring Agent"
    version = "1.0"
    description = "Calculates composite fit scores for target enterprise accounts based on firmographic and buying signals."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
        AgentPermission.SCORE_TARGET_ACCOUNTS,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        company_name = context.metadata.get("company_name", "Global Enterprise Corp")
        industry = context.metadata.get("industry", "FinTech")
        employee_count = context.metadata.get("employee_count", 600)
        annual_revenue = context.metadata.get("estimated_annual_revenue", 50000000.0)

        account = self.service.gtm.create_target_account(
            company_name=company_name,
            industry=industry,
            employee_count=employee_count,
            estimated_annual_revenue=annual_revenue,
        )

        score = self.service.gtm.score_target_account(
            account_id=account["id"],
            icp_fit=context.metadata.get("icp_fit", 0.90),
            business_need=context.metadata.get("business_need", 0.85),
            revenue_potential=context.metadata.get("revenue_potential", 0.90),
        )

        return {
            "status": "SUCCESS",
            "account_id": account["id"],
            "company_name": company_name,
            "composite_score": score["composite_score"],
            "score_details": score,
        }
