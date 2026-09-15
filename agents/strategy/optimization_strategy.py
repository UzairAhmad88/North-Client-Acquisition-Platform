"""
Optimization Strategy Agent (Phase 51).
Runs multi-objective portfolio optimizations and computes Pareto-optimal strategic packages.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.service import StrategyPlatformService


class OptimizationStrategyAgent(BaseAgent):
    """
    Agent for executing constrained mathematical optimization across strategic initiative portfolios.
    Prohibited from making binding decisions or modifying financial allocations directly.
    """

    agent_id = "optimization_strategy_agent"
    name = "Optimization Strategy Agent"
    version = "1.0"
    description = "Executes portfolio optimization and generates Pareto-efficient strategic plans."

    def __init__(self, service: Optional[StrategyPlatformService] = None):
        super().__init__()
        self.service = service or StrategyPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_STRATEGY,
            AgentPermission.RUN_STRATEGY_OPTIMIZATION,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        budget = float(params.get("budget_limit_usd") or 80000.0)
        capacity = float(params.get("capacity_limit_fte") or 6.0)

        # Create sample candidate portfolio if empty
        inits = self.service.initiative_manager.list_initiatives()
        if not inits:
            inits = [
                self.service.create_initiative("Expand Outbound Outreach Engine", "Sales Lead", expected_value_usd=80000.0, estimated_cost_usd=20000.0, required_fte_capacity=1.5),
                self.service.create_initiative("Develop Real-time Webhook Hub", "Tech Lead", expected_value_usd=45000.0, estimated_cost_usd=12000.0, required_fte_capacity=1.0),
                self.service.create_initiative("AI Support Agent Scaler", "AI Lead", expected_value_usd=90000.0, estimated_cost_usd=25000.0, required_fte_capacity=2.0),
            ]

        opt_res = self.service.optimize_plan(inits, budget_limit_usd=budget, capacity_limit_fte=capacity)
        pareto_plans = self.service.generate_pareto_frontier(inits, total_budget_usd=budget, total_capacity_fte=capacity)

        return {
            "status": "SUCCESS",
            "optimization_result": opt_res,
            "pareto_frontier": [
                p.model_dump() if hasattr(p, "model_dump") else p.dict()
                for p in pareto_plans
            ],
            "governance_notice": "Optimization produces mathematical candidate models. Human executive authorization required.",
        }
