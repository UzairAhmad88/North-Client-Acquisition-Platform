"""GTM Strategy & Market Segmentation Agent for Phase 58."""
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


class GtmStrategyAgent(BaseAgent):
    """Analyzes market segments, defines ICP profiles, and evaluates GTM motions."""

    agent_id = "gtm_strategy_agent"
    name = "GTM Strategy & Segmentation Agent"
    version = "1.0"
    description = "Defines GTM positioning, creates target segments, and maps TAM/SAM feasibility."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
        AgentPermission.ANALYZE_GTM_STRATEGY,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        strategy_name = context.metadata.get("strategy_name", "Enterprise GTM Expansion")
        target_market = context.metadata.get("target_market", "Tier-1 FinTech")
        sales_motion = context.metadata.get("sales_motion", "consultative")

        strategy = self.service.gtm.create_gtm_strategy(
            name=strategy_name,
            target_market=target_market,
            sales_motion=sales_motion,
        )

        segments = self.service.gtm.list_segments()

        return {
            "status": "SUCCESS",
            "strategy": strategy,
            "segments_count": len(segments),
        }
