"""Revenue Intelligence Copilot Agent for Phase 58."""
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


class RevenueCopilotAgent(BaseAgent):
    """Answers strategic revenue, pipeline, forecast, and commercial questions backed by verified evidence."""

    agent_id = "revenue_copilot_agent"
    name = "Revenue Intelligence Copilot Agent"
    version = "1.0"
    description = "Provides evidence-grounded answers to natural language revenue and commercial inquiries."
    permissions = {
        AgentPermission.READ_REVENUE_GROWTH,
    }

    def __init__(self, service: Optional[RevenueGrowthPlatformService] = None):
        super().__init__()
        self.service = service or RevenueGrowthPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        query = context.metadata.get("query", "What is our expected revenue?")

        res = self.service.answer_copilot_query(query=query)

        return {
            "status": "SUCCESS",
            "query": query,
            "answer": res["answer"],
            "supporting_evidence": res["supporting_evidence_sources"],
            "details": res,
        }
