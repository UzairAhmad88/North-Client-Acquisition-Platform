"""Prompt Registry & RAGOps Evaluation Agent for Phase 63."""

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


class PromptRagopsAgent(BaseAgent):
    """Manages versioned Prompt templates and evaluates RAG retrieval/generation groundedness."""

    agent_id = "prompt_ragops_agent"
    name = "AI Prompt & RAGOps Agent"
    version = "1.0"
    description = "Registers prompt templates and measures RAG context precision, groundedness, and token cost."
    permissions = {
        AgentPermission.READ_AI_MODEL_FACTORY,
        AgentPermission.MANAGE_AI_PROMPTS,
    }

    def __init__(self, service: Optional[AiModelFactoryService] = None):
        super().__init__()
        self.service = service or AiModelFactoryService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        query = context.metadata.get("query", "Summarize Q3 financial revenue")

        rag_eval = self.service.prompts_service.evaluate_rag_pipeline(
            tenant_id=tenant_id,
            query=query,
            retrieved_contexts=["doc_chunk_revenue_01", "doc_chunk_revenue_02"],
            generated_answer="Q3 Revenue was $1.4M with 18% QoQ growth.",
        )
        return {
            "status": "COMPLETED",
            "rag_eval_id": rag_eval.id,
            "is_grounded": rag_eval.is_grounded,
            "groundedness_score": rag_eval.metrics.get("context_groundedness"),
        }
