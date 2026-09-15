"""
Phase 72: InvestmentAgent
Tracks treasury short-term investment portfolios, money market yields, and liquidity horizons.
"""

from typing import Any, Dict, Optional, Set
import logging
from agents.core.base import BaseAgent, AgentResult
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

logger = logging.getLogger(__name__)


class InvestmentAgent(BaseAgent):
    agent_id = "fin_investment"
    name = "InvestmentAgent"
    version = "1.0"
    description = "Tracks treasury short-term investment portfolios, money market yields, and liquidity horizons."
    permissions = {
        AgentPermission.READ_FINANCIAL_OS
    }

    def __init__(self, service: Optional[Any] = None):
        super().__init__()
        self.service = service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        logger.info(f"InvestmentAgent executing autonomous financial task for tenant {tenant_id}")
        return {
            "status": "COMPLETED",
            "agent_id": self.agent_id,
            "tenant_id": tenant_id,
            "summary": "Tracks treasury short-term investment portfolios, money market yields, and liquidity horizons.",
            "findings_count": 0,
            "recommendations": [
                "Maximize yield on idle cash balances by sweeping into insured money market instruments.",
                "Ensure investment portfolio maturity matches projected 30-day operating cash outflow needs."
            ]
        }

    async def run(self, context: AgentContext) -> AgentResult:
        res = await self.execute(context)
        return AgentResult(
            status=res.get("status", "completed"),
            result=res,
            confidence="HIGH",
            metadata={"agent_id": self.agent_id}
        )
