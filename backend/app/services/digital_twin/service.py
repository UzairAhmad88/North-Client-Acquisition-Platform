"""
Unified Digital Twin Platform Service Facade for Phase 50.
Coordinates state modeling, scenario management, sandboxed simulations, sensitivity analysis,
counterfactual reasoning, decision intelligence, and model calibration.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.digital_twin.base import (
        Assumption,
        CalibrationReport,
        CounterfactualResult,
        DecisionOption,
        DecisionRecord,
        EntityDomain,
        OutcomeRecord,
        Parameter,
        Scenario,
        ScenarioStatus,
        ScenarioType,
        SensitivityRanking,
        SimulationMethod,
        SimulationResult,
        TimeHorizon,
        TwinEntity,
        TwinRelationship,
        TwinState,
    )
    from backend.app.services.digital_twin.state import DigitalTwinStateManager
    from backend.app.services.digital_twin.scenarios import ScenarioEngine
    from backend.app.services.digital_twin.simulation import SimulationEngine
    from backend.app.services.digital_twin.sensitivity import SensitivityAnalyzer
    from backend.app.services.digital_twin.counterfactual import CounterfactualEngine
    from backend.app.services.digital_twin.decisions import DecisionSupportManager
    from backend.app.services.digital_twin.calibration import OutcomeLearningManager
except ImportError:
    from app.services.digital_twin.base import (
        Assumption,
        CalibrationReport,
        CounterfactualResult,
        DecisionOption,
        DecisionRecord,
        EntityDomain,
        OutcomeRecord,
        Parameter,
        Scenario,
        ScenarioStatus,
        ScenarioType,
        SensitivityRanking,
        SimulationMethod,
        SimulationResult,
        TimeHorizon,
        TwinEntity,
        TwinRelationship,
        TwinState,
    )
    from app.services.digital_twin.state import DigitalTwinStateManager
    from app.services.digital_twin.scenarios import ScenarioEngine
    from app.services.digital_twin.simulation import SimulationEngine
    from app.services.digital_twin.sensitivity import SensitivityAnalyzer
    from app.services.digital_twin.counterfactual import CounterfactualEngine
    from app.services.digital_twin.decisions import DecisionSupportManager
    from app.services.digital_twin.calibration import OutcomeLearningManager

logger = logging.getLogger(__name__)


class DigitalTwinPlatformService:
    """
    Master Service for Phase 50: Unified Digital Twin & Strategic Simulation Engine.
    """

    def __init__(self):
        self.state_manager = DigitalTwinStateManager()
        self.scenario_engine = ScenarioEngine(self.state_manager)
        self.simulation_engine = SimulationEngine(self.state_manager)
        self.sensitivity_analyzer = SensitivityAnalyzer(self.simulation_engine)
        self.counterfactual_engine = CounterfactualEngine(self.simulation_engine)
        self.decision_manager = DecisionSupportManager()
        self.calibration_manager = OutcomeLearningManager()

    # --- State Management ---

    def capture_enterprise_state(
        self,
        tenant_id: str = "default_tenant",
        title: str = "Enterprise Point-in-Time Snapshot",
    ) -> TwinState:
        """Captures cross-domain state snapshot and computes cryptographic integrity hash."""
        return self.state_manager.generate_snapshot(tenant_id=tenant_id, title=title)

    def verify_state_integrity(self, state: TwinState) -> bool:
        """Verifies cryptographic hash of digital twin state snapshot."""
        return self.state_manager.verify_snapshot_integrity(state)

    # --- Scenarios ---

    def create_scenario(
        self,
        name: str,
        twin_model_id: str = "primary_twin_model",
        scenario_type: ScenarioType = ScenarioType.GROWTH,
        time_horizon: TimeHorizon = TimeHorizon.MONTH_12,
        simulation_method: SimulationMethod = SimulationMethod.MONTE_CARLO,
        parameter_overrides: Optional[Dict[str, float]] = None,
        custom_assumptions: Optional[List[Dict[str, Any]]] = None,
        constraints: Optional[List[Dict[str, Any]]] = None,
        tenant_id: str = "default_tenant",
        created_by: str = "executive_user",
    ) -> Scenario:
        """Creates and configures a strategic what-if scenario."""
        scenario = self.scenario_engine.create_scenario(
            name=name,
            twin_model_id=twin_model_id,
            scenario_type=scenario_type,
            time_horizon=time_horizon,
            simulation_method=simulation_method,
            parameter_overrides=parameter_overrides,
            custom_assumptions=custom_assumptions,
            constraints=constraints,
            tenant_id=tenant_id,
            created_by=created_by,
        )
        self.scenario_engine.validate_scenario(scenario)
        return scenario

    # --- Simulation Execution ---

    def run_scenario_simulation(
        self,
        scenario: Scenario,
        twin_state: Optional[TwinState] = None,
        iterations: int = 1000,
        random_seed: Optional[int] = 42,
    ) -> SimulationResult:
        """Runs sandboxed simulation for a scenario."""
        return self.simulation_engine.run_simulation(
            scenario=scenario,
            twin_state=twin_state,
            iterations=iterations,
            random_seed=random_seed,
        )

    def compare_scenarios(
        self,
        baseline_scenario: Scenario,
        alternative_scenarios: List[Scenario],
        twin_state: Optional[TwinState] = None,
        iterations: int = 1000,
    ) -> Dict[str, Any]:
        """Runs simulations and computes delta comparisons across multiple scenarios against baseline."""
        state = twin_state or self.capture_enterprise_state(tenant_id=baseline_scenario.tenant_id)
        baseline_sim = self.simulation_engine.run_simulation(baseline_scenario, twin_state=state, iterations=iterations)
        
        base_rev = float(baseline_sim.metrics_summary.get("cumulative_revenue_usd", 1.0))
        base_profit = float(baseline_sim.metrics_summary.get("cumulative_net_profit_usd", 0.0))

        comparisons = []
        for alt in alternative_scenarios:
            alt_sim = self.simulation_engine.run_simulation(alt, twin_state=state, iterations=iterations)
            alt_rev = float(alt_sim.metrics_summary.get("cumulative_revenue_usd", 0.0))
            alt_profit = float(alt_sim.metrics_summary.get("cumulative_net_profit_usd", 0.0))

            rev_delta = alt_rev - base_rev
            rev_delta_pct = (rev_delta / base_rev * 100.0) if base_rev != 0 else 0.0
            profit_delta = alt_profit - base_profit

            comparisons.append({
                "scenario_name": alt.name,
                "scenario_code": alt.scenario_code,
                "method": alt.simulation_method.value,
                "cumulative_revenue_usd": alt_rev,
                "revenue_delta_usd": round(rev_delta, 2),
                "revenue_delta_percentage": round(rev_delta_pct, 2),
                "cumulative_net_profit_usd": alt_profit,
                "net_profit_delta_usd": round(profit_delta, 2),
                "capacity_utilization_percentage": alt_sim.metrics_summary.get("final_capacity_utilization_percentage", 0.0),
                "constraint_violations": alt_sim.constraint_violations,
                "simulation_result": alt_sim.model_dump() if hasattr(alt_sim, "model_dump") else alt_sim.dict(),
            })

        return {
            "baseline": {
                "scenario_name": baseline_scenario.name,
                "scenario_code": baseline_scenario.scenario_code,
                "cumulative_revenue_usd": base_rev,
                "cumulative_net_profit_usd": base_profit,
                "capacity_utilization_percentage": baseline_sim.metrics_summary.get("final_capacity_utilization_percentage", 0.0),
                "simulation_result": baseline_sim.model_dump() if hasattr(baseline_sim, "model_dump") else baseline_sim.dict(),
            },
            "alternatives": comparisons,
        }

    # --- Sensitivity Analysis ---

    def analyze_sensitivity(
        self,
        scenario: Scenario,
        target_metric: str = "cumulative_revenue_usd",
        twin_state: Optional[TwinState] = None,
    ) -> List[SensitivityRanking]:
        """Calculates parameter sensitivity and Tornado rankings."""
        return self.sensitivity_analyzer.run_sensitivity_analysis(
            base_scenario=scenario,
            twin_state=twin_state,
            target_metric=target_metric,
        )

    # --- Counterfactual Analysis ---

    def run_counterfactual(
        self,
        historical_event_id: str,
        hypothetical_condition: str,
        historical_actual_metrics: Dict[str, Any],
        hypothetical_parameter_overrides: Dict[str, float],
        base_twin_state: Optional[TwinState] = None,
    ) -> CounterfactualResult:
        """Executes counterfactual historical what-if comparison."""
        return self.counterfactual_engine.evaluate_counterfactual(
            historical_event_id=historical_event_id,
            hypothetical_condition=hypothetical_condition,
            historical_actual_metrics=historical_actual_metrics,
            hypothetical_parameter_overrides=hypothetical_parameter_overrides,
            base_twin_state=base_twin_state,
        )

    # --- Decision Intelligence ---

    def build_decision_options(
        self,
        simulations: List[SimulationResult],
    ) -> List[DecisionOption]:
        """Transforms simulation outputs into decision options."""
        return self.decision_manager.generate_options_from_simulations(simulations)

    def record_decision(
        self,
        question: str,
        rationale: str,
        decision_owner: str,
        selected_option_id: Optional[str] = None,
    ) -> DecisionRecord:
        """Records an approved human strategic decision."""
        return self.decision_manager.record_human_decision(
            question=question,
            rationale=rationale,
            decision_owner=decision_owner,
            selected_option_id=selected_option_id,
        )

    # --- Outcome Learning & Calibration ---

    def track_outcome(
        self,
        observed_period: str,
        predicted_metrics: Dict[str, Any],
        actual_metrics: Dict[str, Any],
        decision_id: Optional[str] = None,
        scenario_id: Optional[str] = None,
    ) -> OutcomeRecord:
        """Logs observed real-world performance against simulated predictions."""
        return self.calibration_manager.record_outcome(
            observed_period=observed_period,
            predicted_metrics=predicted_metrics,
            actual_metrics=actual_metrics,
            decision_id=decision_id,
            scenario_id=scenario_id,
        )

    def calibrate_twin_models(
        self,
        outcome_records: List[OutcomeRecord],
    ) -> CalibrationReport:
        """Computes calibration adjustments from historical outcome records."""
        return self.calibration_manager.generate_calibration_report(outcome_records)
