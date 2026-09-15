"""
Context Assembly Agent (Section 31-36, 63).
Assembles permission-bounded, budget-constrained context bundles for downstream AI agents
with strict prompt-injection defense tags (<UNTRUSTED_RETRIEVED_KNOWLEDGE>) and uncertainty disclosure.
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


class ContextAssemblyAgent(BaseAgent):
    """
    Context assembly agent providing grounded, authorized knowledge context to AI assistants.
    Enforces Rule 7 & 8: Untrusted content boundary encapsulation.
    Enforces Rule 17: Explicit disclosure when evidence is insufficient.
    """

    agent_id = "context_assembly_agent"
    name = "Context Assembly Agent"
    version = "1.0"
    description = "Prepares bounded, permission-filtered knowledge context for AI agents with injection defense boundaries."

    def __init__(self, service: Optional[KnowledgePlatformService] = None):
        super().__init__()
        self.service = service or KnowledgePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_KNOWLEDGE,
            AgentPermission.REQUEST_CONTEXT,
            AgentPermission.SEARCH_KNOWLEDGE,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_intent = str(params.get("task_intent") or "General Inquiry")
        target_agent_id = str(params.get("agent_id") or "assistant_agent")
        budget_tokens = int(params.get("budget_tokens") or 4000)
        domain_str = params.get("domain")
        domain = KnowledgeDomain(domain_str) if domain_str else None
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")
        user_role = str(params.get("user_role") or "INTERNAL_USER")

        bundle = self.service.assemble_ai_context(
            task_intent=task_intent,
            agent_id=target_agent_id,
            budget_tokens=budget_tokens,
            domain=domain,
            tenant_id=tenant_id,
            user_role=user_role,
        )

        return {
            "status": "SUCCESS",
            "request_code": bundle.request_code,
            "target_agent_id": target_agent_id,
            "budget_tokens": bundle.budget_tokens,
            "consumed_tokens": bundle.consumed_tokens,
            "items_count": len(bundle.items),
            "citations": bundle.citations,
            "encapsulated_context": bundle.encapsulated_context,
            "uncertainty_disclosures": bundle.uncertainty_disclosures,
            "assembled_at": bundle.assembled_at.isoformat(),
        }
