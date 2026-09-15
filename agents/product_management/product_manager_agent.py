"""
Product Manager Agent for Phase 56.
Acts as the central Product Management Co-Pilot & Lifecycle Orchestrator.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.product_management.service import (
        ProductManagementPlatformService,
        global_product_management_service,
    )
except ImportError:
    from app.services.product_management.service import (
        ProductManagementPlatformService,
        global_product_management_service,
    )

logger = logging.getLogger(__name__)


class ProductManagerAgent(BaseAgent):
    """Orchestrates product portfolio lifecycle, strategic alignment, and copilot reasoning."""

    agent_id = "product_manager_agent"
    name = "Product Manager Agent"
    version = "1.0"
    description = "Governed AI Product Manager providing portfolio lifecycle synthesis and evidence-backed copilot guidance."
    permissions = {
        AgentPermission.READ_PRODUCT,
        AgentPermission.EVALUATE_PRODUCT_HEALTH,
    }

    def __init__(self, service: Optional[ProductManagementPlatformService] = None):
        super().__init__()
        self.service = service or global_product_management_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        product_id = context.metadata.get("product_id")
        query = context.metadata.get("query", "Summarize current product lifecycle state and health.")
        
        if not product_id:
            return {"status": "FAILED", "error": "product_id is required"}

        copilot_response = self.service.query_product_copilot(product_id=product_id, query=query)
        health = self.service.health_sunset.get_latest_health(product_id=product_id)
        
        return {
            "status": "SUCCESS",
            "product_id": product_id,
            "query": query,
            "copilot_response": copilot_response,
            "health_summary": health,
        }
