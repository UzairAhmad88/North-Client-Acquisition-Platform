"""
Goal Feasibility Engine for Phase 51.
Evaluates realistic goal achievement likelihood based on historical performance, capacity, and constraints.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.strategy.base import FeasibilityLevel, StrategicObjective
except ImportError:
    from app.services.strategy.base import FeasibilityLevel, StrategicObjective

logger = logging.getLogger(__name__)


class FeasibilityAnalyzer:
    """
    Evaluates whether strategic goals can realistically be achieved under current resource limits and historical run rates.
    """

    def evaluate_objective_feasibility(
        self,
        objective: StrategicObjective,
        available_fte_capacity: float = 6.0,
        historical_growth_rate_pct: float = 15.0,
    ) -> Dict[str, Any]:
        """Calculates probabilistic feasibility rating for an objective."""
        gap = objective.target_value - objective.current_value
        if gap <= 0:
            return {
                "objective_code": objective.objective_code,
                "feasibility_level": FeasibilityLevel.ACHIEVED.value if hasattr(FeasibilityLevel, "ACHIEVED") else "FEASIBLE",
                "feasibility_score": 1.0,
                "gap_remaining": 0.0,
                "confidence": 1.0,
                "rationale": "Target value already achieved or exceeded.",
            }

        required_growth_pct = (gap / max(1.0, objective.baseline_value)) * 100.0
        growth_ratio = required_growth_pct / max(1.0, historical_growth_rate_pct)

        # Capacity penalty
        capacity_factor = min(1.0, available_fte_capacity / 5.0)

        # Base feasibility calculation
        if growth_ratio <= 1.2 and capacity_factor >= 0.8:
            level = FeasibilityLevel.FEASIBLE
            score = 0.90
            rationale = "Target aligns well with historical growth momentum and available team capacity."
        elif growth_ratio <= 2.0 and capacity_factor >= 0.6:
            level = FeasibilityLevel.LIKELY
            score = 0.75
            rationale = "Achievable with focused resource allocation and operational discipline."
        elif growth_ratio <= 3.5:
            level = FeasibilityLevel.CHALLENGING
            score = 0.50
            rationale = "Requires significant acceleration above historical growth trajectory."
        elif growth_ratio <= 5.0:
            level = FeasibilityLevel.UNLIKELY
            score = 0.30
            rationale = "High probability of falling short without structural capacity expansion or acquisitions."
        else:
            level = FeasibilityLevel.INFEASIBLE
            score = 0.10
            rationale = "Target demands unrealistic multiplier under current operational constraints."

        return {
            "objective_code": objective.objective_code,
            "objective_name": objective.name,
            "feasibility_level": level.value,
            "feasibility_score": score,
            "required_growth_percentage": round(required_growth_pct, 1),
            "historical_growth_rate_pct": historical_growth_rate_pct,
            "capacity_factor": round(capacity_factor, 2),
            "confidence": 0.85,
            "rationale": rationale,
        }
