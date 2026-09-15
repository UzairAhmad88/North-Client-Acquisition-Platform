"""Inference Gateway & Policy Routing Agent for Phase 63."""

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


class InferenceAgent(BaseAgent):
    """Manages policy-routed inference gateways, rate limits, and fallback chains."""

    agent_id = "inference_agent"
    name = "AI Inference Gateway Agent"
    version = "1.0"
    description = "Configures SLA-driven inference endpoints, fallback models, and rate limits."
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
        route_name = context.metadata.get("route_name", "inference-route-01")
        primary_deployment_id = context.metadata.get("primary_deployment_id", "aidepl_default")

        ep = self.service.deployments_service.create_inference_endpoint(
            tenant_id=tenant_id,
            route_name=route_name,
            primary_deployment_id=primary_deployment_id,
        )
        return {
            "status": "COMPLETED",
            "endpoint_id": ep.id,
            "route_name": ep.route_name,
            "routing_policy": ep.routing_policy,
        }
