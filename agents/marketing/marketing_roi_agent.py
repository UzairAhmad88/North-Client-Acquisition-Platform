"""Marketing ROI & Budget Optimization Agent for Phase 59."""
from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.marketing.service import MarketingPlatformService
except ImportError:
    from app.services.marketing.service import MarketingPlatformService

logger = logging.getLogger(__name__)


class MarketingRoiAgent(BaseAgent):
    """Calculates CPL, CAC, ROAS, and simulates budget allocation shifts."""

    agent_id = "marketing_roi_agent"
    name = "Marketing ROI & Economics Agent"
    version = "1.0"
    description = "Evaluates marketing unit economics and simulates budget optimization scenarios."
    permissions = {
        AgentPermission.READ_MARKETING_INTELLIGENCE,
        AgentPermission.OPTIMIZE_MARKETING_BUDGET,
    }

    def __init__(self, service: Optional[MarketingPlatformService] = None):
        super().__init__()
        self.service = service or MarketingPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        period = context.metadata.get("period", "2026-Q3")
        roi = self.service.attribution.calculate_marketing_roi(period=period)
        sim = self.service.attribution.simulate_budget_optimization(
            current_budget_usd=150000.0,
            budget_shift_pct=20.0,
            target_focus_channel="LINKEDIN_ABM",
        )

        return {
            "status": "COMPLETED",
            "period": roi.period,
            "total_spend_usd": roi.total_spend_usd,
            "attributed_revenue_usd": roi.total_attributed_revenue_usd,
            "cac_usd": roi.cost_per_acquisition_usd,
            "roas": roi.roas,
            "simulation_gain_usd": sim["expected_additional_revenue_usd"],
        }
