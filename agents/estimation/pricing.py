"""Pricing Recommendation Engine computing internal commercial ranges."""

import os
from typing import Tuple


class PricingRecommendationEngine:
    """Computes internal commercial range recommendations from costs, risk buffers, and configured margins."""

    DEFAULT_MIN_MARGIN = float(os.getenv("PRICING_MIN_MARGIN", "0.30"))  # 30% min margin
    DEFAULT_TARGET_MARGIN = float(os.getenv("PRICING_TARGET_MARGIN", "0.50"))  # 50% target margin

    @classmethod
    def calculate_commercial_range(
        cls,
        internal_cost: float,
        external_cost: float,
        risk_buffer_percent: float = 20.0,
        min_margin: float = DEFAULT_MIN_MARGIN,
        target_margin: float = DEFAULT_TARGET_MARGIN,
    ) -> Tuple[float, float, float]:
        base_cost = internal_cost + external_cost
        risk_buffer_amount = base_cost * (risk_buffer_percent / 100.0)
        total_cost_basis = base_cost + risk_buffer_amount

        recommended_min = round(total_cost_basis * (1.0 + min_margin), 2)
        recommended_max = round(total_cost_basis * (1.0 + target_margin), 2)

        return round(risk_buffer_amount, 2), recommended_min, recommended_max
