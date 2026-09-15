"""Revenue Economics, Attribution & Waterfall Agent for Phase 58."""
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


class EconomicsAgent(BaseAgent):
    """Calculates unit acquisition economics (CAC/LTV), attribution breakdowns, and ARR waterfalls."""

    agent_id = "economics_agent"
    name = "Revenue Economics & Attribution Agent"
    version = "1.0"
    description = "Evaluates blended CAC, LTV ratios, multi-touch attribution, and authoritative ARR waterfall metrics."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
        AgentPermission.CALCULATE_REVENUE_ECONOMICS,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        period = context.metadata.get("period", "Q3-2026")
        
        econ = self.service.economics.get_unit_economics(period=period)
        waterfall = self.service.economics.record_revenue_waterfall(period=period)

        return {
            "status": "SUCCESS",
            "period": period,
            "blended_cac_usd": econ["blended_cac_usd"],
            "ltv_to_cac_ratio": econ["ltv_to_cac_ratio"],
            "ending_arr_usd": waterfall["ending_arr_usd"],
            "net_retention_pct": waterfall["net_retention_pct"],
        }
