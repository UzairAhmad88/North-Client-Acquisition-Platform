"""
Product Strategy & PRD Generation Agent for Phase 55.
Synthesizes validated concepts into product concepts, unit economics models, and draft PRDs.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )
except ImportError:
    from app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )

logger = logging.getLogger(__name__)


class ProductStrategyAgent(BaseAgent):
    """Generates structured product/service concepts and PRD drafts from validated experiments."""

    agent_id = "product_strategy_agent"
    name = "Product Strategy & PRD Agent"
    version = "1.0"
    description = "Drafts comprehensive Product Requirements Documents (PRDs) and models unit economics."
    permissions = {
        AgentPermission.READ_INNOVATION,
        AgentPermission.GENERATE_PRD,
    }

    def __init__(self, service: Optional[InnovationPlatformService] = None):
        super().__init__()
        self.service = service or global_innovation_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        name = context.metadata.get("name", "New Product Concept")
        persona = context.metadata.get("target_customer_persona", "Target Enterprise Operator")
        value_prop = context.metadata.get("value_proposition", "High-velocity AI workflow automation.")
        features = context.metadata.get("core_features", ["Feature A", "Feature B"])

        concept = self.service.concepts.create_product_concept(
            workspace_id=ws_id,
            name=name,
            target_customer_persona=persona,
            value_proposition=value_prop,
            core_features=features,
        )

        prd = self.service.concepts.generate_prd(
            concept_id=concept["id"],
            title=f"PRD: {name}",
            problem_summary=value_prop,
        )

        return {"status": "SUCCESS", "product_concept": concept, "prd_draft": prd}
