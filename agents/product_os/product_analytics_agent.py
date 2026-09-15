"""Product Analytics & Feature Value Realization Agent for Phase 60."""

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


class ProductAnalyticsAgent(BaseAgent):
    """Measures adoption curves, funnel conversions, and true feature value realization."""

    agent_id = "product_analytics_agent"
    name = "Product Analytics & Feature Value Agent"
    version = "1.0"
    description = "Tracks activation rates, 30d retention, and enforces the principle: Feature Shipped != Value."
    permissions = {
        AgentPermission.READ_PRODUCT_OS,
        AgentPermission.EVALUATE_FEATURE_VALUE,
    }

    def __init__(self, service: Optional[ProductOperatingSystemService] = None):
        super().__init__()
        self.service = service or ProductOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        product_id = context.metadata.get("product_id", "prod_default")
        feature_key = context.metadata.get("feature_key", "stream_dashboard")
        feature_name = context.metadata.get("feature_name", "Live Streaming Dashboard")

        adoption = self.service.analytics_service.track_feature_adoption(
            tenant_id=tenant_id,
            product_id=product_id,
            feature_key=feature_key,
            feature_name=feature_name,
            eligible_users=context.metadata.get("eligible_users", 5000),
            activated_users=context.metadata.get("activated_users", 3500),
            weekly_active_users=context.metadata.get("weekly_active_users", 2800),
            retention_rate_30d=context.metadata.get("retention_rate_30d", 82.0),
            customer_satisfaction_score=context.metadata.get("csat", 4.7),
            efficiency_gain_pct=context.metadata.get("efficiency_gain_pct", 30.0),
            revenue_influenced_usd=context.metadata.get("revenue_influenced_usd", 850000.0),
        )

        return {
            "status": "COMPLETED",
            "adoption_id": adoption.adoption_id,
            "feature_key": adoption.feature_key,
            "adoption_rate": adoption.adoption_rate,
            "value_realization_score": adoption.value_realization_score,
            "is_high_value": adoption.is_high_value,
        }
