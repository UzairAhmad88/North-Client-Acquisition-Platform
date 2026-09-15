"""Unified Model Evaluation & LLM-as-a-Judge Agent for Phase 63."""

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


class EvaluationAgent(BaseAgent):
    """Executes deterministic benchmark evaluations and LLM-as-a-Judge evaluations."""

    __test__ = False

    agent_id = "evaluation_agent"
    name = "AI Model Evaluation Agent"
    version = "1.0"
    description = "Evaluates models against golden benchmarks, LLM-as-a-judge scorecards, and safety thresholds."
    permissions = {
        AgentPermission.READ_AI_MODEL_FACTORY,
        AgentPermission.EXECUTE_MODEL_EVALUATION,
    }

    def __init__(self, service: Optional[AiModelFactoryService] = None):
        super().__init__()
        self.service = service or AiModelFactoryService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        model_version_id = context.metadata.get("model_version_id", "aimv_default")

        suites = self.service.evaluation_service.list_suites(tenant_id)
        suite_id = suites[0].id if suites else "aisup_default"

        res = self.service.evaluation_service.run_evaluation(
            tenant_id=tenant_id,
            suite_id=suite_id,
            model_version_id=model_version_id,
        )
        return {
            "status": "COMPLETED",
            "evaluation_id": res.id,
            "passed": res.passed,
            "score": res.score,
        }
