"""Model Registry & Lineage Agent for Phase 63."""

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


class ModelRegistryAgent(BaseAgent):
    """Registers models, version manifests, and enforces artifact provenance."""

    agent_id = "model_registry_agent"
    name = "AI Model Registry Agent"
    version = "1.0"
    description = "Registers multi-framework model artifacts, manifests, and tracks lineage back to training data."
    permissions = {
        AgentPermission.READ_AI_MODEL_FACTORY,
        AgentPermission.MANAGE_MODEL_REGISTRY,
    }

    def __init__(self, service: Optional[AiModelFactoryService] = None):
        super().__init__()
        self.service = service or AiModelFactoryService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        project_id = context.metadata.get("project_id", "aiproj_default")
        model_name = context.metadata.get("name", "Predictive Scoring Model")
        owner = context.metadata.get("owner", "lead.ai@uzaii.internal")

        model = self.service.registry_service.register_model(
            tenant_id=tenant_id,
            project_id=project_id,
            name=model_name,
            owner=owner,
        )
        return {
            "status": "COMPLETED",
            "model_id": model.id,
            "current_stage": model.current_stage,
            "active_version": model.active_version,
        }
