"""Roadmap & Multi-Framework Prioritization Agent for Phase 60."""

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


class RoadmapPrioritizationAgent(BaseAgent):
    """Manages roadmaps, initiative sequencing, RICE/WSJF prioritization, and dependency health."""

    agent_id = "roadmap_agent"
    name = "Roadmap & Prioritization Agent"
    version = "1.0"
    description = "Sequences initiatives across Now/Next/Later horizons and detects dependency bottlenecks."
    permissions = {
        AgentPermission.READ_PRODUCT_OS,
        AgentPermission.MANAGE_PRODUCT_ROADMAPS,
    }

    def __init__(self, service: Optional[ProductOperatingSystemService] = None):
        super().__init__()
        self.service = service or ProductOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        product_id = context.metadata.get("product_id", "prod_default")
        title = context.metadata.get("title", "Enterprise Strategy Roadmap")

        roadmap = self.service.prioritization_roadmap_service.create_roadmap(
            tenant_id=tenant_id,
            product_id=product_id,
            title=title,
            horizon_type=context.metadata.get("horizon_type", "QUARTERLY"),
        )

        item = self.service.prioritization_roadmap_service.add_roadmap_item(
            tenant_id=tenant_id,
            roadmap_id=roadmap.roadmap_id,
            title=context.metadata.get("item_title", "Distributed Realtime Event Pipeline"),
            horizon="NOW",
            opportunity_id=context.metadata.get("opportunity_id", "opp_default"),
            target_quarter="2026-Q3",
            engineering_effort_weeks=4.0,
            dependencies=[],
        )

        score_res = self.service.prioritization_roadmap_service.score_prioritization(
            tenant_id=tenant_id,
            item_id=item.item_id,
            framework="RICE",
            reach=10000.0,
            impact=3.0,
            confidence=85.0,
            effort=4.0,
        )

        return {
            "status": "COMPLETED",
            "roadmap_id": roadmap.roadmap_id,
            "item_id": item.item_id,
            "calculated_score": score_res.score,
            "framework": score_res.framework,
        }
