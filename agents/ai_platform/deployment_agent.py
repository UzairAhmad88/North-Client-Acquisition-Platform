"""Deployment & Canary Rollout Agent for Phase 63."""

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


class DeploymentAgent(BaseAgent):
    """Coordinates Canary and Champion/Challenger model deployments."""

    agent_id = "deployment_agent"
    name = "AI Model Deployment Agent"
    version = "1.0"
    description = "Orchestrates Canary, Blue/Green, and Shadow model deployments with traffic weighting."
    permissions = {
        AgentPermission.READ_AI_MODEL_FACTORY,
        AgentPermission.MANAGE_AI_DEPLOYMENTS,
    }

    def __init__(self, service: Optional[AiModelFactoryService] = None):
        super().__init__()
        self.service = service or AiModelFactoryService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        model_version_id = context.metadata.get("model_version_id", "aimv_default")

        depl = self.service.deployments_service.create_deployment(
            tenant_id=tenant_id,
            model_version_id=model_version_id,
            environment="PRODUCTION",
            traffic_weight_pct=10.0,
        )
        return {
            "status": "COMPLETED",
            "deployment_id": depl.id,
            "strategy": depl.strategy,
            "traffic_weight_pct": depl.traffic_weight_pct,
        }
