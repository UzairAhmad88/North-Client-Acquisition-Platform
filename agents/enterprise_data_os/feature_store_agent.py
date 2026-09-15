"""Feature Store & ML Data Layer Agent for Phase 62."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.enterprise_data_os.service import EnterpriseDataOperatingSystemService
except ImportError:
    from app.services.enterprise_data_os.service import EnterpriseDataOperatingSystemService

logger = logging.getLogger(__name__)


class FeatureStoreAgent(BaseAgent):
    """Manages online/offline feature store transformations, training dataset splits, and point-in-time correctness."""

    agent_id = "feature_store_agent"
    name = "Feature Store & ML Data Agent"
    version = "1.0"
    description = "Registers curated features, point-in-time joins, and ML dataset splits for AI models."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
        AgentPermission.MANAGE_FEATURE_STORE,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        feature_name = context.metadata.get("name", "customer_nps_rolling_avg")

        feat = self.service.features_service.register_feature(
            tenant_id=tenant_id,
            name=feature_name,
            entity_name="CUSTOMER",
            data_type="FLOAT",
            source_dataset_id="silver_feedback_events",
            transformation_logic="AVG(score_value) OVER (PARTITION BY customer_id ORDER BY event_time ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)",
        )
        return {
            "status": "COMPLETED",
            "feature_id": feat.feature_id,
            "feature_name": feat.name,
            "created_at": feat.created_at,
        }
