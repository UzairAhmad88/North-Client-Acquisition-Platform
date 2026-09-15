"""Product Opportunity & Solution Tree Scoring Agent for Phase 60."""

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


class OpportunityScoringAgent(BaseAgent):
    """Evaluates product opportunities, builds opportunity solution trees, and calculates multi-factor opportunity scores."""

    agent_id = "opportunity_scoring_agent"
    name = "Product Opportunity Scoring Agent"
    version = "1.0"
    description = "Calculates explainable opportunity scores from customer value, business value, confidence, and effort."
    permissions = {
        AgentPermission.READ_PRODUCT_OS,
        AgentPermission.SCORE_PRODUCT_OPPORTUNITIES,
    }

    def __init__(self, service: Optional[ProductOperatingSystemService] = None):
        super().__init__()
        self.service = service or ProductOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        product_id = context.metadata.get("product_id", "prod_default")
        title = context.metadata.get("title", "Real-time Autonomous Decision Validation")
        problem_id = context.metadata.get("problem_id", "prob_default")

        opp = self.service.problems_feedback_service.create_opportunity(
            tenant_id=tenant_id,
            product_id=product_id,
            title=title,
            problem_id=problem_id,
            customer_value_score=context.metadata.get("customer_value_score", 9.0),
            business_value_score=context.metadata.get("business_value_score", 8.5),
            confidence_score=context.metadata.get("confidence_score", 9.0),
            effort_score=context.metadata.get("effort_score", 4.0),
            strategic_fit_score=context.metadata.get("strategic_fit_score", 9.5),
            revenue_potential_usd=context.metadata.get("revenue_potential_usd", 500000.0),
        )

        return {
            "status": "COMPLETED",
            "opportunity_id": opp.opportunity_id,
            "title": opp.title,
            "composite_score": opp.score,
            "revenue_potential_usd": opp.revenue_potential_usd,
        }
