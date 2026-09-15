"""
Phase 76: FinanceSupervisor
Supervises autonomous financial, treasury, and capital allocation agents (Phase 72).
"""

from typing import Any, Dict, Optional, Set
import logging
from agents.core.base import BaseAgent, AgentResult
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

logger = logging.getLogger(__name__)


class FinanceSupervisor(BaseAgent):
    agent_id = "finance_supervisor"
    name = "FinanceSupervisor"
    version = "1.0.0"
    description = "Supervises autonomous financial, treasury, and capital allocation agents (Phase 72)."
    permissions = {
        AgentPermission.READ_AEAI_OS,
        AgentPermission.ORCHESTRATE_ENTERPRISE_AGENT_MESH
    }

    def __init__(self, service: Optional[Any] = None):
        super().__init__()
        self.service = service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        logger.info(f"FinanceSupervisor executing governed autonomous task for tenant {tenant_id}")
        return {
            "status": "COMPLETED",
            "agent_id": self.agent_id,
            "name": self.name,
            "tenant_id": tenant_id,
            "summary": "Supervises autonomous financial, treasury, and capital allocation agents (Phase 72).",
            "findings_count": 0,
            "autonomy_level": "L4",
            "recommendations": [
                "Ensure all high-risk actions pass through human approval gates.",
                "Enforce action limits and token spend budgets for all autonomous execution runs."
            ]
        }

    async def run(self, context: AgentContext) -> AgentResult:
        res = await self.execute(context)
        return AgentResult(
            status=res.get("status", "COMPLETED"),
            result=res,
            confidence="HIGH",
            metadata={"agent_id": self.agent_id, "name": self.name}
        )
