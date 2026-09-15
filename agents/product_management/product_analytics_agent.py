"""
Product Analytics & Experimentation Agent for Phase 56.
Analyzes cohort retention, feature adoption, and A/B test statistical significance with guardrails.
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


class ProductAnalyticsAgent(BaseAgent):
    """Evaluates product adoption metrics, cohort behavior, feature usage, and experiment conclusions."""

    agent_id = "product_analytics_agent"
    name = "Product Analytics & Experimentation Agent"
    version = "1.0"
    description = "Provides rigorous behavioral cohort analysis, feature adoption rankings, and guardrail-protected A/B evaluation."
    permissions = {
        AgentPermission.READ_PRODUCT,
    }

    def __init__(self, service: Optional[ProductManagementPlatformService] = None):
        super().__init__()
        self.service = service or global_product_management_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        product_id = context.metadata.get("product_id")
        action = context.metadata.get("action", "adoption_overview")

        if not product_id:
            return {"status": "FAILED", "error": "product_id is required"}

        if action == "evaluate_experiment":
            exp_id = context.metadata.get("experiment_id")
            if not exp_id:
                return {"status": "FAILED", "error": "experiment_id is required"}
            res = self.service.analytics_experimentation.evaluate_experiment(
                experiment_id=exp_id,
                control_metrics=context.metadata.get("control_metrics", {}),
                variant_metrics=context.metadata.get("variant_metrics", {}),
            )
            return {"status": "SUCCESS", "action": "evaluate_experiment", "result": res}

        adoption = self.service.analytics_experimentation.get_adoption_overview(product_id=product_id)
        experiments = self.service.analytics_experimentation.list_experiments(product_id=product_id)

        return {
            "status": "SUCCESS",
            "action": "adoption_overview",
            "product_id": product_id,
            "adoption": adoption,
            "experiments_count": len(experiments),
        }
