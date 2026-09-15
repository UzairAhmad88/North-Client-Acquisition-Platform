"""Incident Response & Root Cause Analysis Agent for Phase 61."""

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


class IncidentResponseAgent(BaseAgent):
    """Assists in SEV0-SEV4 incident detection, timeline reconstruction, 5-Whys root cause analysis, and postmortems."""

    agent_id = "incident_response_agent"
    name = "Incident Response & RCA Agent"
    version = "1.0"
    description = "Facilitates blameless postmortems and structures 5-Whys causal chains. Human responders retain decision authority."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
        AgentPermission.MANAGE_INCIDENTS_POSTMORTEMS,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        incident_id = context.metadata.get("incident_id", "inc_001")
        root_cause = context.metadata.get("root_cause", "Unbounded async worker memory allocation during burst.")

        pm = self.service.observability_service.create_postmortem(
            tenant_id=tenant_id,
            incident_id=incident_id,
            root_cause_summary=root_cause,
            five_whys=context.metadata.get("five_whys", ["High memory", "Queue buffer full", "Worker unthrottled", "Rate limiter missing", "Test missed load spike"]),
            corrective_actions=context.metadata.get("corrective_actions", [{"action": "Add token bucket rate limiter", "status": "COMPLETED"}]),
        )

        return {
            "status": "COMPLETED",
            "postmortem_id": pm.pm_id,
            "incident_id": incident_id,
            "root_cause_summary": pm.root_cause_summary,
            "corrective_actions_count": len(pm.corrective_actions),
        }
