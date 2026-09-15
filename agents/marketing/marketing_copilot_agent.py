"""Marketing Copilot Interactive Reasoning Agent for Phase 59."""
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


class MarketingCopilotAgent(BaseAgent):
    """Answers natural language marketing strategy, campaign, and attribution queries with evidence."""

    agent_id = "marketing_copilot_agent"
    name = "Marketing Copilot Agent"
    version = "1.0"
    description = "Provides evidence-grounded marketing decision support and conversational insights."
    permissions = {
        AgentPermission.READ_MARKETING_INTELLIGENCE,
    }

    def __init__(self, service: Optional[MarketingPlatformService] = None):
        super().__init__()
        self.service = service or MarketingPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        query = context.metadata.get("query", "What campaigns are performing best?")
        response = self.service.answer_copilot_query(query=query)

        return {
            "status": "COMPLETED",
            "query": query,
            "answer": response["answer"],
            "evidence": response["evidence"],
            "uncertainty": response["uncertainty"],
            "timestamp": response["timestamp"],
        }
