"""
Objective & OKR Agent (Phase 51).
Assists leadership in drafting measurable strategic objectives and quantitative Key Results.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.strategy.base import StrategicPillar
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.base import StrategicPillar
    from app.services.strategy.service import StrategyPlatformService


class ObjectiveOKRAgent(BaseAgent):
    """
    Agent for drafting strategic objectives and decomposing targets into measurable Key Results.
    Cannot unilaterally commit organizational strategy or modify binding baselines.
    """

    agent_id = "objective_okr_agent"
    name = "Objective & OKR Agent"
    version = "1.0"
    description = "Drafts strategic objectives and configures OKR key results."

    def __init__(self, service: Optional[StrategyPlatformService] = None):
        super().__init__()
        self.service = service or StrategyPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_STRATEGY,
            AgentPermission.CREATE_OBJECTIVE_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        name = str(params.get("name") or "Expand High-Margin AI Client Accounts")
        target_val = float(params.get("target_value") or 250000.0)
        unit = str(params.get("unit") or "USD")
        raw_pillar = str(params.get("strategic_pillar") or "GROWTH")
        owner = str(params.get("owner") or "VP Commercial")

        try:
            pillar = StrategicPillar[raw_pillar]
        except KeyError:
            pillar = StrategicPillar.GROWTH

        obj = self.service.create_objective(
            name=name,
            target_value=target_val,
            unit=unit,
            strategic_pillar=pillar,
            owner=owner,
        )

        kr = self.service.create_key_result(
            objective_id=obj.objective_code,
            name=f"Reach ${target_val:,.0f} in recurring revenue",
            target_value=100.0,
            unit="PERCENT",
            owner=owner,
        )

        return {
            "status": "SUCCESS",
            "objective_code": obj.objective_code,
            "objective_name": obj.name,
            "strategic_pillar": obj.strategic_pillar.value if hasattr(obj.strategic_pillar, "value") else str(obj.strategic_pillar),
            "key_result_code": kr.kr_code,
            "key_result_name": kr.name,
        }
