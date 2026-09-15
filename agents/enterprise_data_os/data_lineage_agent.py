"""Data Lineage & Impact Analysis Agent for Phase 62."""

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


class DataLineageAgent(BaseAgent):
    """Tracks end-to-end data lineage and computes blast radius impact analysis."""

    agent_id = "data_lineage_agent"
    name = "Data Lineage & Impact Agent"
    version = "1.0"
    description = "Traces source-to-dashboard lineage graphs and evaluates downstream change risks."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
        AgentPermission.MANAGE_DATA_CATALOG,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        dataset_id = context.metadata.get("dataset_id", "silver_customer_profiles")

        impact = self.service.governance_service.analyze_change_impact(
            tenant_id=tenant_id,
            dataset_id=dataset_id,
            proposed_change="Rename column 'mrr' to 'monthly_recurring_revenue'",
        )
        return {
            "status": "COMPLETED",
            "impact_id": impact.impact_id,
            "blast_radius_score": impact.blast_radius_score,
            "risk_level": impact.risk_level,
            "analyzed_at": impact.analyzed_at,
        }
