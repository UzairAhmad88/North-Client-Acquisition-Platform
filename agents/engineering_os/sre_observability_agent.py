"""SRE Reliability & Observability Agent for Phase 61."""

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


class SreObservabilityAgent(BaseAgent):
    """Monitors service availability, SLO error budgets, and distributed trace health."""

    agent_id = "sre_observability_agent"
    name = "SRE Reliability & Observability Agent"
    version = "1.0"
    description = "Calculates remaining error budgets, burn rates, and surfaces SLO degradation risks."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
        AgentPermission.MONITOR_OBSERVABILITY_RELIABILITY,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        service_name = context.metadata.get("service_name", "decision-fabric-service")

        budget = self.service.observability_service.calculate_slo_error_budget(
            tenant_id=tenant_id,
            service_name=service_name,
            slo_target_pct=context.metadata.get("slo_target_pct", 99.95),
            measured_uptime_pct=context.metadata.get("measured_uptime_pct", 99.98),
        )

        return {
            "status": "COMPLETED",
            "service_name": service_name,
            "remaining_budget_pct": budget.remaining_budget_pct,
            "burn_rate": budget.burn_rate,
            "health_status": budget.status,
        }
