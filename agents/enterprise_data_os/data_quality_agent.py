"""Data Quality & Schema Drift Agent for Phase 62."""

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


class DataQualityAgent(BaseAgent):
    """Monitors 6-dimensional data quality, detects schema drift, and flags invalid records."""

    __test__ = False
    agent_id = "data_quality_agent"
    name = "Data Quality & Observability Agent"
    version = "1.0"
    description = "Enforces completeness, accuracy, consistency, validity, uniqueness, and timeliness rules."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
        AgentPermission.MANAGE_DATA_QUALITY,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        dataset_id = context.metadata.get("dataset_id", "silver_customer_profiles")

        scorecard = self.service.quality_service.evaluate_quality_scorecard(
            tenant_id=tenant_id,
            dataset_id=dataset_id,
        )
        return {
            "status": "COMPLETED",
            "scorecard_id": scorecard.qc_id,
            "composite_score": scorecard.composite_score,
            "quality_status": scorecard.status,
            "evaluated_at": scorecard.evaluated_at,
        }
