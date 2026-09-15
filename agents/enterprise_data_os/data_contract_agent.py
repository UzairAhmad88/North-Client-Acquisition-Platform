"""Data Contract & Data Product Agent for Phase 62."""

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


class DataContractAgent(BaseAgent):
    """Manages formal producer-consumer data contracts and publishes curated Gold data products."""

    agent_id = "data_contract_agent"
    name = "Data Contract & Product Agent"
    version = "1.0"
    description = "Governs schema versions, SLA compliance, and publishes self-describing Data Products."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
        AgentPermission.MANAGE_DATA_CONTRACTS,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        product_name = context.metadata.get("name", "Engineering Health Data Product")

        prod = self.service.schemas_service.publish_data_product(
            tenant_id=tenant_id,
            domain_id="dom_002",
            name=product_name,
            purpose="Curated data product tracking DORA metrics, PR cycle times, and deployment frequencies.",
        )
        return {
            "status": "COMPLETED",
            "product_id": prod.product_id,
            "product_name": prod.name,
            "published_at": prod.published_at,
        }
