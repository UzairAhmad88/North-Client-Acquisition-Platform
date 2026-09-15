"""
Strategic Budget & Resource Allocation Subsystem for Phase 51.
Optimizes capital deployment and human/AI capacity allocation with overload detection.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.strategy.base import StrategicInitiative
except ImportError:
    from app.services.strategy.base import StrategicInitiative

logger = logging.getLogger(__name__)


class BudgetManager:
    """Manages strategic budgets, capital allocation categories, and capacity load monitoring."""

    def evaluate_budget_and_resources(
        self,
        funded_initiatives: List[StrategicInitiative],
        total_budget_usd: float = 120000.0,
        total_capacity_fte: float = 8.0,
    ) -> Dict[str, Any]:
        """Calculates budget variance, ROI projections, and team capacity utilization."""
        allocated_cost = sum(i.estimated_cost_usd for i in funded_initiatives)
        allocated_fte = sum(i.required_fte_capacity for i in funded_initiatives)
        projected_value = sum(i.expected_value_usd for i in funded_initiatives)

        budget_variance = total_budget_usd - allocated_cost
        capacity_variance = total_capacity_fte - allocated_fte

        is_over_budget = allocated_cost > total_budget_usd
        is_over_capacity = allocated_fte > total_capacity_fte

        # Category breakdown
        category_breakdown: Dict[str, float] = {}
        for i in funded_initiatives:
            category_breakdown[i.category] = category_breakdown.get(i.category, 0.0) + i.estimated_cost_usd

        return {
            "total_budget_usd": total_budget_usd,
            "allocated_cost_usd": round(allocated_cost, 2),
            "remaining_budget_usd": round(budget_variance, 2),
            "budget_utilization_pct": round((allocated_cost / total_budget_usd * 100.0), 2) if total_budget_usd > 0 else 0.0,
            "is_over_budget": is_over_budget,
            "total_capacity_fte": total_capacity_fte,
            "allocated_capacity_fte": round(allocated_fte, 2),
            "remaining_capacity_fte": round(capacity_variance, 2),
            "capacity_utilization_pct": round((allocated_fte / total_capacity_fte * 100.0), 2) if total_capacity_fte > 0 else 0.0,
            "is_over_capacity": is_over_capacity,
            "total_projected_value_usd": round(projected_value, 2),
            "projected_roi_pct": round(((projected_value - allocated_cost) / max(1.0, allocated_cost) * 100.0), 2),
            "category_breakdown": category_breakdown,
        }
