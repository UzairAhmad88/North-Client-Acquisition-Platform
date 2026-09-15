"""Scenario Generator creating scope and pricing comparison scenarios."""

from typing import List
from agents.estimation.models import EstimateScenarioSchema, EstimateWorkItemSchema
from agents.estimation.costing import CostEngine
from agents.estimation.pricing import PricingRecommendationEngine


class ScenarioGenerator:
    """Builds Lean, Standard, and Expanded project scenarios for human evaluation."""

    @classmethod
    def generate_scenarios(
        cls, work_items: List[EstimateWorkItemSchema], external_cost: float
    ) -> List[EstimateScenarioSchema]:
        scenarios: List[EstimateScenarioSchema] = []

        # 1. Lean Scenario (Essential / Required items only)
        lean_items = [w for w in work_items if w.complexity in ("LOW", "TRIVIAL") or "WEBSITE" in w.category.upper()]
        if not lean_items:
            lean_items = work_items[:1]

        lean_hours = round(sum(w.expected_hours for w in lean_items), 1)
        lean_int_cost = CostEngine.calculate_internal_labor_cost(lean_hours)
        _, lean_min, lean_max = PricingRecommendationEngine.calculate_commercial_range(
            lean_int_cost, external_cost, risk_buffer_percent=15.0
        )

        scenarios.append(
            EstimateScenarioSchema(
                name="LEAN",
                description="Core essential scope focus without non-critical add-ons.",
                scope=f"Includes {len(lean_items)} essential module(s): " + ", ".join([w.name for w in lean_items]),
                estimated_hours=lean_hours,
                internal_cost=lean_int_cost,
                external_cost=external_cost,
                recommended_min=lean_min,
                recommended_max=lean_max,
                risk_level="LOW",
            )
        )

        # 2. Standard Scenario (Recommended scope)
        std_hours = round(sum(w.expected_hours for w in work_items), 1)
        std_int_cost = CostEngine.calculate_internal_labor_cost(std_hours)
        _, std_min, std_max = PricingRecommendationEngine.calculate_commercial_range(
            std_int_cost, external_cost, risk_buffer_percent=20.0
        )

        scenarios.append(
            EstimateScenarioSchema(
                name="STANDARD",
                description="Recommended full scope addressing all confirmed client requirements.",
                scope=f"Includes all {len(work_items)} core and recommended module(s).",
                estimated_hours=std_hours,
                internal_cost=std_int_cost,
                external_cost=external_cost,
                recommended_min=std_min,
                recommended_max=std_max,
                risk_level="MEDIUM",
            )
        )

        # 3. Expanded Scenario (Recommended + Advanced AI / Automation add-ons)
        exp_hours = round(std_hours * 1.35, 1)
        exp_int_cost = CostEngine.calculate_internal_labor_cost(exp_hours)
        _, exp_min, exp_max = PricingRecommendationEngine.calculate_commercial_range(
            exp_int_cost, external_cost + 50.0, risk_buffer_percent=25.0
        )

        scenarios.append(
            EstimateScenarioSchema(
                name="EXPANDED",
                description="Full scope plus enhanced automation, advanced analytics, and custom AI integrations.",
                scope=f"Includes all {len(work_items)} modules plus advanced AI automation layer.",
                estimated_hours=exp_hours,
                internal_cost=exp_int_cost,
                external_cost=external_cost + 50.0,
                recommended_min=exp_min,
                recommended_max=exp_max,
                risk_level="HIGH",
            )
        )

        return scenarios
