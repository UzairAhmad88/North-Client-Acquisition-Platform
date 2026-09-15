"""Product Copilot Agent for Phase 60."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.product_os.service import ProductOperatingSystemService
except ImportError:
    from app.services.product_os.service import ProductOperatingSystemService

logger = logging.getLogger(__name__)


class ProductCopilotAgent(BaseAgent):
    """Answers product leadership questions with evidence citations, assumptions, and confidence bounds."""

    agent_id = "product_copilot_agent"
    name = "Product Operating System Copilot Agent"
    version = "1.0"
    description = "Provides strategic, discovery, roadmap, and health answers grounded in verifiable evidence."
    permissions = {
        AgentPermission.READ_PRODUCT_OS,
    }

    def __init__(self, service: Optional[ProductOperatingSystemService] = None):
        super().__init__()
        self.service = service or ProductOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        query = context.metadata.get("query", "What should we build next?")

        result = self.service.query_product_copilot(tenant_id=tenant_id, query=query)

        return {
            "status": "COMPLETED",
            "query": query,
            "response": result.get("response"),
            "evidence_sources": result.get("evidence_sources"),
            "confidence": result.get("confidence"),
            "governance_notice": result.get("governance_notice"),
        }
