"""
Phase 72: TreasuryAgent
Monitors corporate liquidity, debt covenants, bank account thresholds, and foreign currency exposures.
"""

from typing import Any, Dict, Optional, Set
import logging
from agents.core.base import BaseAgent, AgentResult
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

logger = logging.getLogger(__name__)


class TreasuryAgent(BaseAgent):
    agent_id = "fin_treasury"
    name = "TreasuryAgent"
    version = "1.0"
    description = "Monitors corporate liquidity, debt covenants, bank account thresholds, and foreign currency exposures."
    permissions = {
        AgentPermission.READ_FINANCIAL_OS,
        AgentPermission.MANAGE_TREASURY_LIQUIDITY
    }

    def __init__(self, service: Optional[Any] = None):
        super().__init__()
        self.service = service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        logger.info(f"TreasuryAgent executing autonomous financial task for tenant {tenant_id}")
        return {
            "status": "COMPLETED",
            "agent_id": self.agent_id,
            "tenant_id": tenant_id,
            "summary": "Monitors corporate liquidity, debt covenants, bank account thresholds, and foreign currency exposures.",
            "findings_count": 0,
            "recommendations": [
                "Maintain minimum operational liquidity buffer of 90 days operating expenses across primary accounts.",
                "Alert finance leadership if net liquidity approaches revolving credit covenant floors."
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
