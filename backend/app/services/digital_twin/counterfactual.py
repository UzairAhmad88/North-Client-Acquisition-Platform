"""
Counterfactual Evaluation Engine for Phase 50: Unified Digital Twin.
Simulates alternative historical paths ("What if we had done X?") and computes divergence against actual outcomes.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.digital_twin.base import (
        CounterfactualResult,
        Scenario,
        ScenarioType,
        SimulationMethod,
        TimeHorizon,
        TwinState,
    )
    from backend.app.services.digital_twin.simulation import SimulationEngine
except ImportError:
    from app.services.digital_twin.base import (
        CounterfactualResult,
        Scenario,
        ScenarioType,
        SimulationMethod,
        TimeHorizon,
        TwinState,
    )
    from app.services.digital_twin.simulation import SimulationEngine

logger = logging.getLogger(__name__)


class CounterfactualEngine:
    """
    Evaluates past strategic decisions or conditions by reconstructing past state and running
    hypothetical alternative parameter configurations.
    """

    def __init__(self, simulation_engine: Optional[SimulationEngine] = None):
        self.simulation_engine = simulation_engine or SimulationEngine()

    def evaluate_counterfactual(
        self,
        historical_event_id: str,
        hypothetical_condition: str,
        historical_actual_metrics: Dict[str, Any],
        hypothetical_parameter_overrides: Dict[str, float],
        base_twin_state: Optional[TwinState] = None,
        tenant_id: str = "default_tenant",
    ) -> CounterfactualResult:
        """
        Executes counterfactual simulation comparing actual historical outcome to alternative branch.
        """
        scenario = Scenario(
            tenant_id=tenant_id,
            twin_model_id="historical_model",
            name=f"Counterfactual: {hypothetical_condition}",
            scenario_type=ScenarioType.GROWTH,
            time_horizon=TimeHorizon.MONTH_12,
            simulation_method=SimulationMethod.DETERMINISTIC,
            parameter_overrides=hypothetical_parameter_overrides,
        )

        sim_res = self.simulation_engine.run_simulation(scenario, twin_state=base_twin_state, iterations=1)
        simulated_metrics = sim_res.metrics_summary

        actual_rev = float(historical_actual_metrics.get("cumulative_revenue_usd", 150000.0))
        sim_rev = float(simulated_metrics.get("cumulative_revenue_usd", 180000.0))
        rev_delta = sim_rev - actual_rev
        rev_delta_pct = (rev_delta / actual_rev * 100.0) if actual_rev != 0 else 0.0

        actual_clients = float(historical_actual_metrics.get("ending_active_clients", 12.0))
        sim_clients = float(simulated_metrics.get("ending_active_clients", 16.0))
        client_delta = sim_clients - actual_clients

        divergence_summary = (
            f"Under the counterfactual assumption ('{hypothetical_condition}'), "
            f"simulated cumulative revenue would be ${sim_rev:,.2f} vs actual ${actual_rev:,.2f} "
            f"({rev_delta_pct:+.1f}%), with {sim_clients:.1f} clients vs actual {actual_clients:.1f} ({client_delta:+.1f})."
        )

        return CounterfactualResult(
            counterfactual_code=f"CF-{uuid.uuid4().hex[:8].upper()}",
            historical_event_id=historical_event_id,
            hypothetical_condition=hypothetical_condition,
            historical_actual=historical_actual_metrics,
            simulated_alternative=simulated_metrics,
            divergence_summary=divergence_summary,
            limitations="Counterfactual simulation assumes exogenous market demand and competitor actions remained invariant.",
        )
