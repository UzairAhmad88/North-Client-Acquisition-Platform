"""PERT Three-Point Effort Estimation Engine."""

from typing import List
from agents.estimation.models import EstimateWorkItemSchema


class PERTEstimator:
    """Calculates PERT Three-Point expected hours and total effort ranges."""

    @classmethod
    def calculate_expected_hours(
        cls, optimistic: float, most_likely: float, pessimistic: float
    ) -> float:
        """Standard PERT formula: (O + 4M + P) / 6."""
        expected = (optimistic + (4.0 * most_likely) + pessimistic) / 6.0
        return round(expected, 1)

    @classmethod
    def calculate_totals(
        cls, work_items: List[EstimateWorkItemSchema]
    ) -> tuple[float, float, float]:
        """Calculates total minimum (optimistic), expected, and maximum (pessimistic) hours."""
        total_opt = sum(w.optimistic_hours for w in work_items)
        total_exp = sum(
            w.expected_hours or cls.calculate_expected_hours(w.optimistic_hours, w.most_likely_hours, w.pessimistic_hours)
            for w in work_items
        )
        total_pess = sum(w.pessimistic_hours for w in work_items)

        return round(total_opt, 1), round(total_exp, 1), round(total_pess, 1)
