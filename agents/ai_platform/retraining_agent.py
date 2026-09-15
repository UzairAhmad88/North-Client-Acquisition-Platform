"""Automated Retraining & Active Learning Agent for Phase 63."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.ai_model_factory.service import AiModelFactoryService
except ImportError:
    from app.services.ai_model_factory.service import AiModelFactoryService

logger = logging.getLogger(__name__)


class RetrainingAgent(BaseAgent):
    """Triggers and orchestrates continuous retraining workflows upon drift or feedback volume thresholds."""

    agent_id = "retraining_agent"
    name = "AI Retraining & Continuous Learning Agent"
    version = "1.0"
    description = "Assembles retraining datasets from verified feedback and submits retraining jobs."
    permissions = {
        AgentPermission.READ_AI_MODEL_FACTORY,
        AgentPermission.MANAGE_AI_PROJECTS,
        AgentPermission.RUN_AI_EXPERIMENTS,
    }

    def __init__(self, service: Optional[AiModelFactoryService] = None):
        super().__init__()
        self.service = service or AiModelFactoryService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        model_id = context.metadata.get("model_id", "aimodel_default")

        job = self.service.monitoring_service.trigger_retraining_workflow(
            tenant_id=tenant_id,
            model_id=model_id,
            reason="SCHEDULED_CYCLE",
        )
        return {
            "status": "COMPLETED",
            "retraining_job_id": job.id,
            "trigger_reason": job.trigger_reason,
            "generated_dataset_id": job.generated_dataset_id,
        }
