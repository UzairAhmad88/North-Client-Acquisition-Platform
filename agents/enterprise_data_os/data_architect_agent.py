"""Data Architect & Domain Taxonomy Agent for Phase 62."""

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


class DataArchitectAgent(BaseAgent):
    """Manages data domains, source registrations, and Lakehouse architectural layout."""

    agent_id = "data_architect_agent"
    name = "Data Architect Agent"
    version = "1.0"
    description = "Defines enterprise data domains, catalog sources, and Bronze/Silver/Gold tier boundaries."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
        AgentPermission.MANAGE_DATA_SOURCES,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        domain_name = context.metadata.get("name", "Product Telemetry")
        slug = context.metadata.get("slug", "product-telemetry")

        dom = self.service.sources_service.create_data_domain(
            tenant_id=tenant_id,
            name=domain_name,
            slug=slug,
            owner_team="Product Engineering",
            lead_steward_email="steward-prod@uzaii.com",
            description="Domain managing feature adoption, usage events, and telemetry.",
        )
        return {
            "status": "COMPLETED",
            "domain_id": dom.domain_id,
            "name": dom.name,
            "created_at": dom.created_at,
        }
