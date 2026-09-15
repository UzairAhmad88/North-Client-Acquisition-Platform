"""Product Health & Quality Intelligence Agent for Phase 60."""

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


class ProductHealthAgent(BaseAgent):
    """Calculates 7-factor composite health scorecards across reliability, adoption, sentiment, and margins."""

    agent_id = "product_health_agent"
    name = "Product Health & Scorecard Agent"
    version = "1.0"
    description = "Evaluates composite health: HEALTHY, WATCH, AT_RISK, or CRITICAL with actionable risk factors."
    permissions = {
        AgentPermission.READ_PRODUCT_OS,
        AgentPermission.EVALUATE_PRODUCT_HEALTH_SCORE,
    }

    def __init__(self, service: Optional[ProductOperatingSystemService] = None):
        super().__init__()
        self.service = service or ProductOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        product_id = context.metadata.get("product_id", "prod_default")
        product_name = context.metadata.get("product_name", "Uzaii Decision Fabric")

        scorecard = self.service.analytics_service.calculate_product_health(
            tenant_id=tenant_id,
            product_id=product_id,
            product_name=product_name,
            adoption_score=context.metadata.get("adoption_score", 85.0),
            retention_score=context.metadata.get("retention_score", 82.0),
            reliability_score=context.metadata.get("reliability_score", 98.5),
            feedback_sentiment_score=context.metadata.get("feedback_sentiment_score", 80.0),
            support_efficiency_score=context.metadata.get("support_efficiency_score", 78.0),
            quality_defect_score=context.metadata.get("quality_defect_score", 88.0),
            gross_margin_score=context.metadata.get("gross_margin_score", 85.0),
        )

        return {
            "status": "COMPLETED",
            "scorecard_id": scorecard.scorecard_id,
            "product_name": scorecard.product_name,
            "composite_score": scorecard.composite_score,
            "health_state": scorecard.health_state,
            "risk_factors_count": len(scorecard.risk_factors),
        }
