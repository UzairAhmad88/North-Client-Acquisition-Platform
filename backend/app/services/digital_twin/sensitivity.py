"""
Sensitivity Analysis Engine for Phase 50: Unified Digital Twin.
Computes parameter elasticity, Tornado rankings, and multi-variable variance impact scores.
"""

import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.digital_twin.base import (
        Scenario,
        SensitivityLevel,
        SensitivityRanking,
        SimulationMethod,
        TwinState,
    )
    from backend.app.services.digital_twin.simulation import SimulationEngine
except ImportError:
    from app.services.digital_twin.base import (
        Scenario,
        SensitivityLevel,
        SensitivityRanking,
        SimulationMethod,
        TwinState,
    )
    from app.services.digital_twin.simulation import SimulationEngine

logger = logging.getLogger(__name__)


class SensitivityAnalyzer:
    """
    Performs one-at-a-time (OAT) parameter sweeps to rank variable impact on core business metrics.
    Produces Tornado chart rankings and sensitivity matrices.
    """

    KEY_PARAMETERS = [
        ("lead_conversion_rate", "Conversion Rate", 0.08, 0.50), # 50% relative sweep
        ("average_deal_value_usd", "Average Deal Size", 4500.0, 0.30),
        ("lead_volume_monthly", "Inbound Lead Volume", 120.0, 0.40),
        ("client_churn_rate_monthly", "Client Churn Rate", 0.03, 0.50),
        ("developer_capacity_fte", "Engineering Capacity (FTE)", 6.0, 0.33),
        ("monthly_operating_cost_usd", "Monthly Operating Cost", 18000.0, 0.20),
        ("ai_cost_per_client_usd", "AI Cost Per Client", 45.0, 0.50),
    ]

    def __init__(self, simulation_engine: Optional[SimulationEngine] = None):
        self.simulation_engine = simulation_engine or SimulationEngine()

    def run_sensitivity_analysis(
        self,
        base_scenario: Scenario,
        twin_state: Optional[TwinState] = None,
        target_metric: str = "cumulative_revenue_usd",
        sweep_percentage: float = 0.25,
    ) -> List[SensitivityRanking]:
        """
        Sweeps each key parameter by +/- sweep_percentage and evaluates target metric variance.
        Returns sorted list of sensitivity rankings (Tornado chart representation).
        """
        # Run baseline deterministic simulation
        baseline_sim = self.simulation_engine.run_simulation(
            scenario=base_scenario,
            twin_state=twin_state,
            iterations=1,
        )
        base_val = float(baseline_sim.metrics_summary.get(target_metric, 100000.0))
        if base_val == 0.0:
            base_val = 1.0

        rankings: List[SensitivityRanking] = []

        for param_code, param_name, default_base, rel_range in self.KEY_PARAMETERS:
            effective_base = float(base_scenario.parameter_overrides.get(param_code, default_base))
            
            # Low sweep (-sweep_percentage)
            low_val = effective_base * (1.0 - sweep_percentage)
            scenario_low = base_scenario.model_copy(deep=True) if hasattr(base_scenario, "model_copy") else base_scenario.copy(deep=True)
            scenario_low.parameter_overrides[param_code] = low_val
            scenario_low.simulation_method = SimulationMethod.DETERMINISTIC
            res_low = self.simulation_engine.run_simulation(scenario_low, twin_state=twin_state, iterations=1)
            metric_low = float(res_low.metrics_summary.get(target_metric, base_val))

            # High sweep (+sweep_percentage)
            high_val = effective_base * (1.0 + sweep_percentage)
            scenario_high = base_scenario.model_copy(deep=True) if hasattr(base_scenario, "model_copy") else base_scenario.copy(deep=True)
            scenario_high.parameter_overrides[param_code] = high_val
            scenario_high.simulation_method = SimulationMethod.DETERMINISTIC
            res_high = self.simulation_engine.run_simulation(scenario_high, twin_state=twin_state, iterations=1)
            metric_high = float(res_high.metrics_summary.get(target_metric, base_val))

            # Compute sensitivity score = absolute normalized spread
            spread = abs(metric_high - metric_low)
            sensitivity_score = round(spread / base_val, 4)

            # Assign Level
            if sensitivity_score >= 0.50:
                level = SensitivityLevel.CRITICAL
            elif sensitivity_score >= 0.25:
                level = SensitivityLevel.HIGH
            elif sensitivity_score >= 0.10:
                level = SensitivityLevel.MEDIUM
            elif sensitivity_score >= 0.03:
                level = SensitivityLevel.LOW
            else:
                level = SensitivityLevel.NEGLIGIBLE

            rankings.append(
                SensitivityRanking(
                    parameter_code=param_code,
                    parameter_name=param_name,
                    target_metric=target_metric,
                    sensitivity_score=sensitivity_score,
                    impact_level=level,
                    low_impact_value=round(metric_low, 2),
                    high_impact_value=round(metric_high, 2),
                )
            )

        # Sort by sensitivity score descending for Tornado order
        rankings.sort(key=lambda r: r.sensitivity_score, reverse=True)
        return rankings
