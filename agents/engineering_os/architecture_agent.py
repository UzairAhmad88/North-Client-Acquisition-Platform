"""Architecture & Service Catalog Agent for Phase 61."""

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


class ArchitectureAgent(BaseAgent):
    """Manages service catalog definitions, API contracts, and architectural dependency topologies."""

    agent_id = "architecture_agent"
    name = "Architecture & Service Catalog Agent"
    version = "1.0"
    description = "Registers microservices, validates SLO availability targets, and documents API schemas."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
        AgentPermission.MANAGE_ENGINEERING_REPOSITORIES,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        service_name = context.metadata.get("name", "analytics-stream-service")
        service_tier = context.metadata.get("service_tier", "TIER_1")

        srv = self.service.architecture_service.register_service(
            tenant_id=tenant_id,
            name=service_name,
            service_tier=service_tier,
            owner_team=context.metadata.get("owner_team", "Data Platform"),
            runtime="FASTAPI_PYTHON_311",
            target_slo_availability=99.95,
        )

        return {
            "status": "COMPLETED",
            "service_id": srv.service_id,
            "service_name": srv.name,
            "service_tier": srv.service_tier,
            "target_slo": srv.target_slo_availability,
        }
