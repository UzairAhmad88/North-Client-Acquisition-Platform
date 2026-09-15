"""DORA Metrics, Tech Debt & Cloud FinOps Agent for Phase 61."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.engineering_os.service import EngineeringOperatingSystemService
except ImportError:
    from app.services.engineering_os.service import EngineeringOperatingSystemService

logger = logging.getLogger(__name__)


class DoraFinopsAgent(BaseAgent):
    """Calculates DORA performance tiers, tracks technical debt registries, and monitors cloud cost FinOps."""

    agent_id = "dora_finops_agent"
    name = "DORA Metrics & FinOps Agent"
    version = "1.0"
    description = "Calculates Deployment Frequency, Lead Time, MTTR, Change Failure Rate, and cloud waste reduction."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
        AgentPermission.MANAGE_TECHNICAL_DEBT,
        AgentPermission.OPTIMIZE_FINOPS_CLOUD_COST,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")

        dora = self.service.dora_finops_service.calculate_dora_metrics(
            tenant_id=tenant_id,
            deployment_frequency_per_day=context.metadata.get("deployment_frequency", 4.2),
            lead_time_for_changes_hours=context.metadata.get("lead_time_hours", 2.0),
            change_failure_rate_pct=context.metadata.get("failure_rate_pct", 1.5),
            time_to_restore_service_minutes=context.metadata.get("mttr_minutes", 20.0),
        )

        debt = self.service.dora_finops_service.log_technical_debt_item(
            tenant_id=tenant_id,
            title=context.metadata.get("debt_title", "Optimize database indexing on telemetry timestamps"),
            area="DATABASE",
            effort_person_days=3.0,
        )

        return {
            "status": "COMPLETED",
            "dora_tier": dora.dora_performance_tier,
            "deployment_frequency": dora.deployment_frequency_per_day,
            "change_failure_rate": dora.change_failure_rate_pct,
            "mttr_minutes": dora.time_to_restore_service_minutes,
            "debt_id": debt.debt_id,
        }
