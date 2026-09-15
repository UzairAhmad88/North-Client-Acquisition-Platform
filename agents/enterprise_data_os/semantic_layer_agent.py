"""Semantic Layer & Business Glossary Agent for Phase 62."""

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


class SemanticLayerAgent(BaseAgent):
    """Manages authoritative metrics definitions, business terms, and dimension mappings."""

    agent_id = "semantic_layer_agent"
    name = "Semantic Layer & Glossary Agent"
    version = "1.0"
    description = "Defines authoritative business metrics, terms, and SQL semantic layer logic."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
        AgentPermission.MANAGE_SEMANTIC_LAYER,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        metric_name = context.metadata.get("name", "Gross Margin Percentage")

        met = self.service.catalog_service.define_semantic_metric(
            tenant_id=tenant_id,
            name=metric_name,
            definition="Total gross revenue minus cost of goods sold divided by gross revenue.",
            formula_sql="(gross_revenue - cogs) / nullif(gross_revenue, 0) * 100",
            source_table="gold_financial_summary_mart",
            owner_team="Finance Operations",
        )
        return {
            "status": "COMPLETED",
            "metric_id": met.metric_id,
            "metric_name": met.name,
            "formula_sql": met.formula_sql,
            "created_at": met.created_at,
        }
