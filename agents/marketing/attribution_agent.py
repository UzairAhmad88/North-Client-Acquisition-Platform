"""Marketing Multi-Touch Attribution Agent for Phase 59."""
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


class AttributionAgent(BaseAgent):
    """Calculates multi-touch marketing attribution across campaigns and channels."""

    agent_id = "attribution_agent"
    name = "Marketing Attribution Agent"
    version = "1.0"
    description = "Assigns revenue and pipeline influence credits across multi-touch customer journeys."
    permissions = {
        AgentPermission.READ_MARKETING_INTELLIGENCE,
        AgentPermission.CALCULATE_MARKETING_ATTRIBUTION,
    }

    def __init__(self, service: Optional[MarketingPlatformService] = None):
        super().__init__()
        self.service = service or MarketingPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        opp_id = context.metadata.get("opportunity_id", "opp_demo_101")
        deal_value = context.metadata.get("deal_value_usd", 150000.0)

        touches = context.metadata.get("touches", [
            {"touch_num": 1, "channel": "ORGANIC_SEARCH", "campaign_name": "SEO Content"},
            {"touch_num": 2, "channel": "EMAIL", "campaign_name": "Q3 Modernization"},
            {"touch_num": 3, "channel": "LINKEDIN", "campaign_name": "Executive Case Study"},
        ])

        record = self.service.attribution.calculate_attribution(
            opportunity_id=opp_id,
            deal_value_usd=deal_value,
            touches=touches,
        )

        return {
            "status": "COMPLETED",
            "attribution_id": record.id,
            "attribution_model": record.attribution_model,
            "campaign_credits": record.campaign_credits,
            "channel_credits": record.channel_credits,
        }
