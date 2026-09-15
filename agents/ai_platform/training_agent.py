"""Training Job & GPU Allocation Agent for Phase 63."""

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


class TrainingAgent(BaseAgent):
    """Manages distributed training jobs, fine-tuning, and GPU cluster allocation."""

    agent_id = "training_agent"
    name = "AI Training & Fine-Tuning Agent"
    version = "1.0"
    description = "Submits distributed training/fine-tuning jobs and monitors GPU hardware utilization."
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
        project_id = context.metadata.get("project_id", "aiproj_default")
        model_name = context.metadata.get("model_name", "FineTuned-LLM-7B")

        job = self.service.experiments_service.create_training_job(
            tenant_id=tenant_id,
            project_id=project_id,
            model_name=model_name,
        )
        return {
            "status": "COMPLETED",
            "training_job_id": job.id,
            "gpu_type": job.gpu_type,
            "progress_pct": job.progress_pct,
        }
