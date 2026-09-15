"""Ingestion & Pipeline Orchestration Agent for Phase 62."""

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


class IngestionPipelineAgent(BaseAgent):
    """Manages batch ingestion jobs, streaming connectors, and ETL/ELT pipeline DAGs."""

    agent_id = "ingestion_pipeline_agent"
    name = "Ingestion & Pipeline Agent"
    version = "1.0"
    description = "Schedules data pipelines, tracks ingestion watermarks, and monitors latency SLAs."
    permissions = {
        AgentPermission.READ_ENTERPRISE_DATA_OS,
        AgentPermission.MANAGE_DATA_PIPELINES,
    }

    def __init__(self, service: Optional[EnterpriseDataOperatingSystemService] = None):
        super().__init__()
        self.service = service or EnterpriseDataOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        pipeline_name = context.metadata.get("name", "silver_to_gold_daily_aggregation")

        pipe = self.service.pipelines_service.create_data_pipeline(
            tenant_id=tenant_id,
            name=pipeline_name,
            target_dataset="gold_daily_metrics_mart",
            owner_team="Data Platform",
        )
        return {
            "status": "COMPLETED",
            "pipeline_id": pipe.pipeline_id,
            "pipeline_name": pipe.name,
            "created_at": pipe.created_at,
        }
