"""AI Model Factory Grounded Copilot Agent for Phase 63."""

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


class AiCopilotAgent(BaseAgent):
    """Evidence-grounded conversational AI Copilot strictly separating Facts, Inferences, Hypotheses, and Recommendations."""

    agent_id = "ai_copilot_agent"
    name = "AI Model Factory Copilot Agent"
    version = "1.0"
    description = "Provides grounded answers on model registry, evaluations, drift, GPU utilization, and FinOps."
    permissions = {
        AgentPermission.READ_AI_MODEL_FACTORY,
    }

    def __init__(self, service: Optional[AiModelFactoryService] = None):
        super().__init__()
        self.service = service or AiModelFactoryService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        query = context.metadata.get("query", "What is the accuracy and stage of Customer Churn Classifier?")

        copilot_resp = self.service.copilot_service.query_ai_copilot(
            tenant_id=tenant_id,
            query=query,
        )
        facts = copilot_resp.get("facts", [])
        inferences = copilot_resp.get("inferences", [])
        hypotheses = copilot_resp.get("hypotheses", [])
        recommendations = copilot_resp.get("recommendations", [])
        response_summary = "\n".join(facts + inferences + hypotheses + recommendations)

        return {
            "status": "COMPLETED",
            "query": copilot_resp["query"],
            "response": response_summary,
            "facts": facts,
            "inferences": inferences,
            "hypotheses": hypotheses,
            "recommendations": recommendations,
            "confidence_score": copilot_resp["confidence_score"],
            "facts_count": len(facts),
            "governance_notice": copilot_resp.get("governance_notice", ""),
            "timestamp": copilot_resp["timestamp"],
        }
