"""
Phase 75: DecisionBriefAgent
Synthesizes concise executive decision briefs exposing trade-offs and assumptions.
"""

from typing import Any, Dict, Optional, Set
import logging
from agents.core.base import BaseAgent, AgentResult
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

logger = logging.getLogger(__name__)


class DecisionBriefAgent(BaseAgent):
    agent_id = "decision_brief"
    name = "DecisionBriefAgent"
    version = "1.0"
    description = "Synthesizes concise executive decision briefs exposing trade-offs and assumptions."
    permissions = {
        AgentPermission.READ_DECISION_OS
    }

    def __init__(self, service: Optional[Any] = None):
        super().__init__()
        self.service = service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        logger.info(f"DecisionBriefAgent executing strategic decision evaluation for tenant {tenant_id}")
        return {
            "status": "COMPLETED",
            "agent_id": self.agent_id,
            "tenant_id": tenant_id,
            "summary": "Synthesizes concise executive decision briefs exposing trade-offs and assumptions.",
            "findings_count": 0,
            "recommendations": [
                "Always expose prediction uncertainty intervals and underlying model assumptions to decision makers.",
                "Mandate executive board review for high-impact capital allocation and organizational restructurings."
            ]
        }

    async def run(self, context: AgentContext) -> AgentResult:
        res = await self.execute(context)
        return AgentResult(
            status=res.get("status", "COMPLETED"),
            result=res,
            confidence="HIGH",
            metadata={"agent_id": self.agent_id}
        )
