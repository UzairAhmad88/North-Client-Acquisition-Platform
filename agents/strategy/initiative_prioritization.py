"""
Initiative Prioritization Agent (Phase 51).
Scores proposed initiatives across ROI, feasibility, strategic alignment, and risk.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.service import StrategyPlatformService


class InitiativePrioritizationAgent(BaseAgent):
    """
    Agent for evaluating and ranking proposed initiatives.
    Prohibited from committing budgets or authorizing hiring.
    """

    agent_id = "initiative_prioritization_agent"
    name = "Initiative Prioritization Agent"
    version = "1.0"
    description = "Evaluates initiatives and calculates multi-factor priority scores."

    def __init__(self, service: Optional[StrategyPlatformService] = None):
        super().__init__()
        self.service = service or StrategyPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_STRATEGY,
            AgentPermission.CREATE_INITIATIVE_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        title = str(params.get("title") or "Automate Client Onboarding Pipeline")
        owner = str(params.get("owner") or "Product Lead")
        expected_val = float(params.get("expected_value_usd") or 60000.0)
        est_cost = float(params.get("estimated_cost_usd") or 12000.0)
        fte = float(params.get("required_fte_capacity") or 1.0)
        duration_weeks = float(params.get("estimated_duration_weeks") or 4.0)

        init = self.service.create_initiative(
            title=title,
            owner=owner,
            expected_value_usd=expected_val,
            estimated_cost_usd=est_cost,
            required_fte_capacity=fte,
            estimated_duration_weeks=duration_weeks,
        )

        ranked = self.service.score_initiatives([init])

        return {
            "status": "SUCCESS",
            "initiative_code": init.initiative_code,
            "title": init.title,
            "priority_evaluation": ranked[0] if ranked else {},
        }
