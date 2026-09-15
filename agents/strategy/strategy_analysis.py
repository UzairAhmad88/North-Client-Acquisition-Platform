"""
Strategy Analysis Agent (Phase 51).
Analyzes enterprise strategic health scorecards, objectives progress, and strategic gap assessments.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.service import StrategyPlatformService


class StrategyAnalysisAgent(BaseAgent):
    """
    Agent for evaluating organizational strategy health and strategic gap analysis.
    Cannot autonomously approve strategic plans or commit capital.
    """

    agent_id = "strategy_analysis_agent"
    name = "Strategy Analysis Agent"
    version = "1.0"
    description = "Evaluates strategic health scorecards and performs objective gap analysis."

    def __init__(self, service: Optional[StrategyPlatformService] = None):
        super().__init__()
        self.service = service or StrategyPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_STRATEGY,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        period = str(params.get("period") or "CURRENT_QUARTER")

        scorecard = self.service.get_scorecard(period=period)
        objectives = self.service.list_objectives()
        gaps = self.service.evaluate_gaps(objectives)

        return {
            "status": "SUCCESS",
            "scorecard": scorecard,
            "total_objectives_count": len(objectives),
            "gaps_evaluated": len(gaps),
            "strategic_gaps": gaps,
        }
