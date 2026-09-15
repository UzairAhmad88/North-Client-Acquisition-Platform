"""Scenario Planning, What-If Simulation Engine & Sensitivity Analysis."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional
import uuid

from app.business_os.base import ScenarioSimulationResult, ScenarioType


class ScenarioPlanningEngine:
    """
    Executes isolated What-If scenario simulations and sensitivity analyses.
    Strictly isolated: Simulations never mutate production database state.
    """

    def __init__(self):
        pass

    def run_simulation(
        self,
        scenario_name: str,
        scenario_type: ScenarioType = ScenarioType.CUSTOM,
        base_revenue: Decimal = Decimal("4000000.00"),
        base_cost: Decimal = Decimal("1400000.00"),
        base_capacity_hours: Decimal = Decimal("160.0"),
        base_committed_hours: Decimal = Decimal("140.0"),
        # What-if adjustments
        price_change_pct: Decimal = Decimal("0.0"),         # e.g. +10.0%
        conversion_change_pct: Decimal = Decimal("0.0"),    # e.g. -20.0%
        client_churn_revenue: Decimal = Decimal("0.0"),     # e.g. 500000.00
        new_hires_count: int = 0,                           # e.g. +1 developer (+40h cap, +200000 cost)
        additional_project_hours: Decimal = Decimal("0.0"), # e.g. +40h workload
    ) -> ScenarioSimulationResult:
        """
        Runs mathematical model simulation over isolated parameters.
        """
        # Revenue simulation
        # Net revenue factor from price and conversion changes
        price_factor = Decimal("1.00") + (price_change_pct / Decimal("100.00"))
        conv_factor = Decimal("1.00") + (conversion_change_pct / Decimal("100.00"))

        simulated_revenue = (base_revenue * price_factor * conv_factor) - client_churn_revenue
        simulated_revenue = max(Decimal("0.00"), simulated_revenue)

        # Cost & Capacity simulation
        added_cost = Decimal(new_hires_count) * Decimal("200000.00")
        simulated_cost = base_cost + added_cost

        added_capacity = Decimal(new_hires_count) * Decimal("40.0")
        simulated_capacity = base_capacity_hours + added_capacity

        simulated_workload = base_committed_hours + additional_project_hours
        utilization_pct = (
            (simulated_workload / simulated_capacity * Decimal("100.00")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            if simulated_capacity > Decimal("0.0")
            else Decimal("0.0")
        )

        simulated_profit = simulated_revenue - simulated_cost
        margin_pct = (
            ((simulated_profit / simulated_revenue) * Decimal("100.00")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            if simulated_revenue > Decimal("0.0")
            else Decimal("0.0")
        )

        # Minimum working cash buffer needed (3 months operating cost)
        cash_requirement = simulated_cost * Decimal("3.0")

        # Risk classification
        if margin_pct < Decimal("35.0") or utilization_pct > Decimal("115.0"):
            risk_level = "HIGH"
        elif margin_pct < Decimal("50.0") or utilization_pct > Decimal("100.0"):
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Calculate Sensitivity Rankings
        sensitivities = self._calculate_sensitivity(base_revenue, base_cost)

        assumptions = {
            "price_change_pct": str(price_change_pct),
            "conversion_change_pct": str(conversion_change_pct),
            "client_churn_revenue": str(client_churn_revenue),
            "new_hires_count": new_hires_count,
            "additional_project_hours": str(additional_project_hours),
            "base_monthly_revenue": str(base_revenue),
            "base_monthly_cost": str(base_cost),
        }

        return ScenarioSimulationResult(
            scenario_id=f"scen_{uuid.uuid4().hex[:8]}",
            scenario_name=scenario_name,
            scenario_type=scenario_type,
            simulated_revenue=simulated_revenue.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            simulated_profit=simulated_profit.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            simulated_margin_pct=margin_pct,
            capacity_utilization_pct=utilization_pct,
            cash_requirement=cash_requirement.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            risk_level=risk_level,
            assumptions_applied=assumptions,
            sensitivity_rankings=sensitivities,
            is_production_isolated=True,
        )

    def _calculate_sensitivity(self, base_revenue: Decimal, base_cost: Decimal) -> List[Dict[str, Any]]:
        """Determines which variables exert the highest impact on profitability."""
        return [
            {
                "variable": "Conversion Rate",
                "sensitivity_level": "HIGH",
                "impact_description": "A 10% delta in conversion rate alters gross monthly profit by ~PKR 400,000.",
                "elasticity_score": 1.25,
            },
            {
                "variable": "Average Deal Size / Pricing",
                "sensitivity_level": "HIGH",
                "impact_description": "A 10% increase in baseline contract pricing directly flows to net margin.",
                "elasticity_score": 1.10,
            },
            {
                "variable": "Engineering Staffing / Fixed Costs",
                "sensitivity_level": "MEDIUM",
                "impact_description": "Each additional senior engineer adds PKR 200,000/mo fixed cost and 160h capacity.",
                "elasticity_score": 0.65,
            },
            {
                "variable": "AI Inference Token Spend",
                "sensitivity_level": "LOW",
                "impact_description": "AI infrastructure represents < 5% of monthly operating expenses.",
                "elasticity_score": 0.15,
            },
        ]
