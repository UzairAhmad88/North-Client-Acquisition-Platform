"""
Roadmap & Capacity Planning Agent for Phase 56.
Generates multi-horizon roadmaps, evaluates scenario plans, and performs capacity bottleneck analysis.
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


class RoadmapAgent(BaseAgent):
    """Analyzes roadmap timeline horizons, scenario trade-offs, and team capacity constraints."""

    agent_id = "roadmap_agent"
    name = "Product Roadmap & Capacity Agent"
    version = "1.0"
    description = "Synthesizes Now/Next/Later horizons, models scenarios, and checks FTE capacity limits."
    permissions = {
        AgentPermission.READ_PRODUCT,
        AgentPermission.PRIORITIZE_BACKLOG,
    }

    def __init__(self, service: Optional[ProductManagementPlatformService] = None):
        super().__init__()
        self.service = service or global_product_management_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        product_id = context.metadata.get("product_id")
        action = context.metadata.get("action", "analyze_capacity")

        if not product_id:
            return {"status": "FAILED", "error": "product_id is required"}

        if action == "add_roadmap_item":
            roadmap_id = context.metadata.get("roadmap_id")
            title = context.metadata.get("title", "Roadmap Initiative")
            horizon = context.metadata.get("horizon", "now")
            confidence = float(context.metadata.get("confidence", 0.85))
            item = self.service.roadmaps_capacity.add_roadmap_item(
                roadmap_id=roadmap_id,
                title=title,
                horizon=horizon,
                confidence=confidence,
                objective_link=context.metadata.get("objective_link"),
            )
            return {"status": "SUCCESS", "action": "add_roadmap_item", "item": item}

        roadmaps = self.service.roadmaps_capacity.list_roadmaps(product_id=product_id)
        capacity_plans = self.service.roadmaps_capacity.list_capacity_plans(product_id=product_id)
        
        return {
            "status": "SUCCESS",
            "action": "analyze_capacity",
            "roadmaps_count": len(roadmaps),
            "roadmaps": roadmaps,
            "capacity_plans": capacity_plans,
        }
