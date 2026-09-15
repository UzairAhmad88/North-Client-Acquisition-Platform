"""Content Strategy & Brief Generation Agent for Phase 59."""
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


class ContentStrategyAgent(BaseAgent):
    """Analyzes content gaps, creates structured briefs, and plans content assets."""

    agent_id = "content_strategy_agent"
    name = "Content Strategy & Brief Agent"
    version = "1.0"
    description = "Discovers content gaps and generates evidence-grounded content briefs."
    permissions = {
        AgentPermission.READ_MARKETING_INTELLIGENCE,
        AgentPermission.CREATE_CONTENT_DRAFT,
        AgentPermission.ANALYZE_CONTENT_GAPS,
    }

    def __init__(self, service: Optional[MarketingPlatformService] = None):
        super().__init__()
        self.service = service or MarketingPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        topic = context.metadata.get("topic", "Autonomous Multi-Agent Commercial Governance")
        stage = context.metadata.get("journey_stage", "CONSIDERATION")

        brief = self.service.content.create_content_brief(
            target_topic=topic,
            journey_stage=stage,
            search_intent="COMMERCIAL",
        )

        gaps = self.service.content.list_content_gaps()

        return {
            "status": "COMPLETED",
            "brief_id": brief.id,
            "target_topic": brief.target_topic,
            "total_gaps_identified": len(gaps),
        }
