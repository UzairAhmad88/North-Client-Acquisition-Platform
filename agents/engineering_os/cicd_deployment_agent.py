"""CI/CD & Deployment Strategy Agent for Phase 61."""

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


class CicdDeploymentAgent(BaseAgent):
    """Monitors CI/CD pipelines, container builds, and enforces 10-point release readiness gates."""

    agent_id = "cicd_deployment_agent"
    name = "CI/CD & Deployment Agent"
    version = "1.0"
    description = "Evaluates release readiness checklists and manages deployment strategies."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
        AgentPermission.MANAGE_CICD_PIPELINES,
        AgentPermission.MANAGE_ENGINEERING_DEPLOYMENTS,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        version_tag = context.metadata.get("version_tag", "v2.4.0")
        service_name = context.metadata.get("service_name", "decision-fabric-service")

        gate = self.service.deployments_service.evaluate_release_readiness_gate(
            tenant_id=tenant_id,
            version_tag=version_tag,
            service_name=service_name,
        )

        return {
            "status": "COMPLETED",
            "version_tag": version_tag,
            "readiness_pct": gate.readiness_pct,
            "is_approved_for_release": gate.is_approved_for_release,
            "decision": gate.decision,
        }
