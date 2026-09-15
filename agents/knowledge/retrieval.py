"""
Knowledge Retrieval Agent (Section 15, 36, 63).
Performs authorization-aware multi-factor enterprise search across governed knowledge stores.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.knowledge.base import KnowledgeDomain
    from backend.app.knowledge.service import KnowledgePlatformService
except ImportError:
    from app.knowledge.base import KnowledgeDomain
    from app.knowledge.service import KnowledgePlatformService


class KnowledgeRetrievalAgent(BaseAgent):
    """
    Retrieval agent executing permission-aware hybrid search across internal knowledge.
    Enforces Rule 4-6: Access scopes and tenant boundaries are strictly respected.
    """

    agent_id = "knowledge_retrieval_agent"
    name = "Knowledge Retrieval Agent"
    version = "1.0"
    description = "Searches the organizational memory across keyword, semantic, and graph dimensions with strict tenant isolation."

    def __init__(self, service: Optional[KnowledgePlatformService] = None):
        super().__init__()
        self.service = service or KnowledgePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_KNOWLEDGE,
            AgentPermission.SEARCH_KNOWLEDGE,
            AgentPermission.SEARCH_DOCUMENTS,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        query = str(params.get("query") or "")
        domain_str = params.get("domain")
        domain = KnowledgeDomain(domain_str) if domain_str else None
        strategy = str(params.get("strategy") or "HYBRID")
        top_k = int(params.get("top_k") or 10)
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")
        user_role = str(params.get("user_role") or "INTERNAL_USER")

        if not query:
            return {
                "status": "ERROR",
                "message": "Search query is required.",
                "results": [],
            }

        results = self.service.search_knowledge(
            query=query,
            domain=domain,
            strategy=strategy,
            top_k=top_k,
            tenant_id=tenant_id,
            user_role=user_role,
        )

        return {
            "status": "SUCCESS",
            "query": query,
            "strategy": strategy,
            "results_count": len(results),
            "results": [r.model_dump() for r in results],
        }
