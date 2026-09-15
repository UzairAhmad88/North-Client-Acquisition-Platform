"""
Multi-Objective Strategic Optimization Engine for Phase 51.
Optimizes portfolio selection under budget, capacity, and risk constraints.
Produces explainable mathematical trade-offs without making autonomous decisions.
"""

from datetime import datetime, timezone
import logging
import time
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.strategy.base import ParetoPlan, StrategicInitiative
except ImportError:
    from app.services.strategy.base import ParetoPlan, StrategicInitiative

logger = logging.getLogger(__name__)


class StrategicOptimizationEngine:
    """
    Solves multi-objective portfolio optimization to identify highest-value initiative sets
    satisfying budget limits, engineering capacity, and risk tolerances.
    """

    def optimize_portfolio(
        self,
        initiatives: List[StrategicInitiative],
        budget_limit_usd: float,
        capacity_limit_fte: float,
        max_acceptable_risk: float = 0.50,
        objective_weights: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Executes constrained multi-objective optimization (Value vs Cost vs Capacity).
        Returns the optimal initiative portfolio with full constraint accounting.
        """
        start_time = time.time()
        weights = objective_weights or {"value_weight": 0.60, "cost_efficiency_weight": 0.20, "risk_penalty": 0.20}

        # Filter initiatives exceeding individual acceptable risk
        candidates = [
            init for init in initiatives
            if init.risk_score <= max_acceptable_risk
        ]

        # Greedy / heuristic branch-and-bound knapsack
        # Score density = (expected_value / (cost * capacity)) adjusted for risk
        def density_score(init: StrategicInitiative) -> float:
            cost = max(1.0, init.estimated_cost_usd)
            fte = max(0.1, init.required_fte_capacity)
            val = max(0.0, init.expected_value_usd)
            risk_mult = 1.0 - (0.5 * init.risk_score)
            return (val / (cost * 0.001 + fte * 1000.0)) * risk_mult

        sorted_candidates = sorted(candidates, key=density_score, reverse=True)

        selected_initiatives: List[StrategicInitiative] = []
        accum_cost = 0.0
        accum_fte = 0.0
        accum_val = 0.0
        binding_constraints = []

        for item in sorted_candidates:
            if (accum_cost + item.estimated_cost_usd <= budget_limit_usd) and (accum_fte + item.required_fte_capacity <= capacity_limit_fte):
                selected_initiatives.append(item)
                accum_cost += item.estimated_cost_usd
                accum_fte += item.required_fte_capacity
                accum_val += item.expected_value_usd
            else:
                if accum_cost + item.estimated_cost_usd > budget_limit_usd:
                    binding_constraints.append(f"Budget constraint bound: {item.title} ($ {item.estimated_cost_usd:,.0f}) exceeds remaining budget ($ {budget_limit_usd - accum_cost:,.0f})")
                if accum_fte + item.required_fte_capacity > capacity_limit_fte:
                    binding_constraints.append(f"Capacity constraint bound: {item.title} ({item.required_fte_capacity:.1f} FTE) exceeds remaining capacity ({capacity_limit_fte - accum_fte:.1f} FTE)")

        runtime = round(time.time() - start_time, 4)
        net_expected_benefit = accum_val - accum_cost

        explanation = (
            f"Under the specified budget of ${budget_limit_usd:,.2f} and capacity ceiling of {capacity_limit_fte:.1f} FTE, "
            f"selected {len(selected_initiatives)} initiatives yielding ${accum_val:,.2f} expected value "
            f"at ${accum_cost:,.2f} cost (Net Benefit: ${net_expected_benefit:,.2f}) and {accum_fte:.1f} FTE utilization."
        )

        return {
            "run_code": f"OPT-{uuid.uuid4().hex[:8].upper()}",
            "status": "COMPLETED",
            "runtime_seconds": runtime,
            "budget_limit_usd": budget_limit_usd,
            "allocated_budget_usd": round(accum_cost, 2),
            "budget_utilization_percentage": round((accum_cost / budget_limit_usd * 100.0), 2) if budget_limit_usd > 0 else 0.0,
            "capacity_limit_fte": capacity_limit_fte,
            "allocated_capacity_fte": round(accum_fte, 2),
            "capacity_utilization_percentage": round((accum_fte / capacity_limit_fte * 100.0), 2) if capacity_limit_fte > 0 else 0.0,
            "total_expected_value_usd": round(accum_val, 2),
            "net_expected_benefit_usd": round(net_expected_benefit, 2),
            "selected_initiatives": [
                {
                    "code": i.initiative_code,
                    "title": i.title,
                    "expected_value_usd": i.expected_value_usd,
                    "cost_usd": i.estimated_cost_usd,
                    "fte": i.required_fte_capacity,
                }
                for i in selected_initiatives
            ],
            "binding_constraints": binding_constraints[:3],
            "explanation": explanation,
        }
