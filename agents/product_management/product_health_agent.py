"""
Product Health & Risk Monitoring Agent for Phase 56.
Computes multi-factor composite health index and surfaces strategic, delivery, and reliability risks.
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


class ProductHealthAgent(BaseAgent):
    """Monitors 6-factor composite health score, detects risk factors, and recommends corrective action."""

    agent_id = "product_health_agent"
    name = "Product Health & Risk Agent"
    version = "1.0"
    description = "Calculates multi-dimensional product health (adoption, satisfaction, reliability, velocity, revenue, security)."
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

        if not product_id:
            return {"status": "FAILED", "error": "product_id is required"}

        factors = context.metadata.get("factors")
        health = self.service.health_sunset.record_health_snapshot(
            product_id=product_id,
            factors=factors,
        )

        return {
            "status": "SUCCESS",
            "product_id": product_id,
            "composite_score": health.get("composite_score"),
            "health_status": health.get("status"),
            "health_details": health,
        }
