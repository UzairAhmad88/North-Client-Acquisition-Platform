"""Marketing Campaign Management Agent for Phase 59."""
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


class CampaignAgent(BaseAgent):
    """Designs marketing campaigns, manages channel orchestration, and checks governance gates."""

    agent_id = "campaign_agent"
    name = "Campaign Management Agent"
    version = "1.0"
    description = "Prepares campaign drafts, configures multi-channel schedules, and checks governance rules."
    permissions = {
        AgentPermission.READ_MARKETING_INTELLIGENCE,
        AgentPermission.MANAGE_CAMPAIGNS,
    }

    def __init__(self, service: Optional[MarketingPlatformService] = None):
        super().__init__()
        self.service = service or MarketingPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        campaign_name = context.metadata.get("campaign_name", "Q4 Multi-Agent Thought Leadership")
        budget = context.metadata.get("allocated_budget_usd", 35000.0)

        campaign = self.service.campaigns.create_campaign(
            name=campaign_name,
            campaign_type="DEMAND_GENERATION",
            allocated_budget_usd=budget,
            channels=["EMAIL", "LINKEDIN", "ORGANIC_SEARCH"],
        )

        return {
            "status": "COMPLETED",
            "campaign_id": campaign.id,
            "campaign_name": campaign.name,
            "campaign_status": campaign.status,
            "is_governance_approved": campaign.is_governance_approved,
        }
