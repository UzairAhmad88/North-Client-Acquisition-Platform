"""Customer Experience Copilot Agent for Phase 57."""
from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.customer_experience.service import CustomerExperiencePlatformService
except ImportError:
    from app.services.customer_experience.service import CustomerExperiencePlatformService

logger = logging.getLogger(__name__)


class CustomerExperienceCopilot(BaseAgent):
    """Answers complex customer journey, friction, health, and VoC inquiries with evidence provenance."""

    agent_id = "customer_experience_copilot"
    name = "Customer Experience Copilot"
    version = "1.0"
    description = "Evidence-grounded conversational agent for customer journey queries and experience analytics."
    permissions = {
        AgentPermission.READ_CUSTOMER_EXPERIENCE,
    }

    def __init__(self, service: Optional[CustomerExperiencePlatformService] = None):
        super().__init__()
        self.service = service or CustomerExperiencePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        query = context.metadata.get("query", "Show me this customer's complete journey")
        customer_id = context.metadata.get("customer_id", "cust-demo-001")

        result = self.service.answer_copilot_query(query=query, customer_id=customer_id)

        return {
            "status": "SUCCESS",
            "query": query,
            "customer_id": customer_id,
            "answer": result["answer"],
            "supporting_evidence": result["supporting_evidence_sources"],
            "details": result,
        }
