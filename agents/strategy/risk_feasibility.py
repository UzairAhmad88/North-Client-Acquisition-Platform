"""
Strategic Risk & Feasibility Agent (Phase 51).
Assesses initiative risks across 10 categories and calculates objective achievement feasibility.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.service import StrategyPlatformService


class StrategyRiskFeasibilityAgent(BaseAgent):
    """
    Agent for evaluating strategic vulnerabilities, goal feasibility, and dependency conflicts.
    """

    agent_id = "strategy_risk_feasibility_agent"
    name = "Strategy Risk & Feasibility Agent"
    version = "1.0"
    description = "Evaluates strategic risks and calculates goal feasibility ratings."

    def __init__(self, service: Optional[StrategyPlatformService] = None):
        super().__init__()
        self.service = service or StrategyPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_STRATEGY,
            AgentPermission.EVALUATE_FEASIBILITY,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        mode = str(params.get("mode") or "FEASIBILITY").upper()

        if mode == "RISK":
            title = str(params.get("title") or "Key Dependency Technology Failure")
            cat = str(params.get("category") or "TECHNOLOGY")
            risk_eval = self.service.evaluate_strategic_risk(title=title, category=cat)
            return {
                "status": "SUCCESS",
                "mode": "RISK",
                "risk_evaluation": risk_eval,
            }
        else:
            objs = self.service.list_objectives()
            if not objs:
                sample_obj = self.service.create_objective("Q4 MRR Acceleration", target_value=300000.0, baseline_value=180000.0)
                objs = [sample_obj]

            feasibility_res = self.service.evaluate_feasibility(objs[0])
            return {
                "status": "SUCCESS",
                "mode": "FEASIBILITY",
                "feasibility_evaluation": feasibility_res,
            }
