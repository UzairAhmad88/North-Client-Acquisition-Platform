"""
Unit and Integration Tests for Phase 50:
Unified Digital Twin, Business Simulation, Scenario Intelligence & Strategic What-If Engine.
"""

import pytest
from datetime import datetime, timezone
import uuid

from backend.app.services.digital_twin.base import (
    EntityDomain,
    ScenarioStatus,
    ScenarioType,
    SensitivityLevel,
    SimulationMethod,
    TimeHorizon,
)
from backend.app.services.digital_twin.state import DigitalTwinStateManager
from backend.app.services.digital_twin.scenarios import ScenarioEngine
from backend.app.services.digital_twin.simulation import SimulationEngine
from backend.app.services.digital_twin.sensitivity import SensitivityAnalyzer
from backend.app.services.digital_twin.counterfactual import CounterfactualEngine
from backend.app.services.digital_twin.decisions import DecisionSupportManager
from backend.app.services.digital_twin.calibration import OutcomeLearningManager
from backend.app.services.digital_twin.service import DigitalTwinPlatformService

from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS
from agents.digital_twin.twin_builder import TwinBuilderAgent
from agents.digital_twin.scenario_simulation import ScenarioSimulationAgent
from agents.digital_twin.sensitivity_impact import SensitivityImpactAgent
from agents.digital_twin.decision_support import DecisionSupportAgent
from agents.digital_twin.outcome_learning import OutcomeLearningAgent

from workers.tasks.digital_twin import (
    task_capture_twin_state_snapshot,
    task_run_scenario_simulation,
    task_run_tornado_sensitivity,
    task_calibrate_twin_models,
)


class TestDigitalTwinStateManager:
    """Tests point-in-time state capture and cryptographic integrity hashing."""

    def test_state_snapshot_capture_and_integrity(self):
        manager = DigitalTwinStateManager()
        state = manager.generate_snapshot(tenant_id="tenant_alpha", title="Q3 Baseline Snapshot")

        assert state.snapshot_code.startswith("SNAP-")
        assert state.tenant_id == "tenant_alpha"
        assert state.composite_health_score > 0.0
        assert len(state.state_hash) == 64  # SHA-256 hex length
        assert manager.verify_snapshot_integrity(state) is True

    def test_state_tampering_fails_integrity(self):
        manager = DigitalTwinStateManager()
        state = manager.generate_snapshot(tenant_id="tenant_alpha")

        # Mutate payload without updating hash
        state.commercial_state["active_clients_count"] = 9999
        assert manager.verify_snapshot_integrity(state) is False


class TestScenarioEngine:
    """Tests scenario creation, parameter overrides, and assumption lineage."""

    def test_create_and_validate_scenario(self):
        engine = ScenarioEngine()
        scenario = engine.create_scenario(
            name="20% Price Increase",
            twin_model_id="twin_01",
            scenario_type=ScenarioType.PRICING,
            parameter_overrides={"average_deal_value_usd": 5400.0, "lead_conversion_rate": 0.10},
        )

        assert scenario.scenario_code.startswith("SCEN-")
        assert len(scenario.assumptions) == 2
        # Check explicit assumption deltas
        deal_asm = next(a for a in scenario.assumptions if a.parameter_code == "average_deal_value_usd")
        assert deal_asm.baseline_value == 4500.0
        assert deal_asm.assumed_value == 5400.0
        assert deal_asm.delta_percentage == 20.0

        val_res = engine.validate_scenario(scenario)
        assert val_res["is_valid"] is True
        assert scenario.status == ScenarioStatus.READY_FOR_SIMULATION


class TestSimulationEngine:
    """Tests Deterministic and Monte Carlo simulation with P10-P90 uncertainty envelopes."""

    def test_deterministic_simulation(self):
        sim_engine = SimulationEngine()
        scenario_engine = ScenarioEngine()

        scenario = scenario_engine.create_scenario(
            name="Deterministic Baseline",
            twin_model_id="twin_01",
            simulation_method=SimulationMethod.DETERMINISTIC,
            time_horizon=TimeHorizon.MONTH_12,
        )

        result = sim_engine.run_simulation(scenario)
        assert result.method == SimulationMethod.DETERMINISTIC
        assert result.iterations == 1
        assert result.is_sandboxed is True
        assert result.metrics_summary["cumulative_revenue_usd"] > 0
        assert result.metrics_summary["cumulative_net_profit_usd"] > 0
        assert result.metrics_summary["average_gross_margin_percentage"] > 0

    def test_monte_carlo_simulation_with_uncertainty(self):
        sim_engine = SimulationEngine()
        scenario_engine = ScenarioEngine()

        scenario = scenario_engine.create_scenario(
            name="Monte Carlo Growth",
            twin_model_id="twin_01",
            simulation_method=SimulationMethod.MONTE_CARLO,
            time_horizon=TimeHorizon.MONTH_12,
            parameter_overrides={"lead_volume_monthly": 180.0},
        )

        result = sim_engine.run_simulation(scenario, iterations=500, random_seed=123)
        assert result.method == SimulationMethod.MONTE_CARLO
        assert result.iterations == 500
        
        # Verify P10 - P90 uncertainty distribution
        dist = result.uncertainty_distribution["cumulative_revenue_usd"]
        assert dist["p10"] <= dist["p50"] <= dist["p90"]
        assert dist["min"] <= dist["max"]

    def test_constraint_violation_detection(self):
        sim_engine = SimulationEngine()
        scenario_engine = ScenarioEngine()

        # Overload leads with tiny capacity to force capacity constraint breach
        scenario = scenario_engine.create_scenario(
            name="Overloaded Capacity Scenario",
            twin_model_id="twin_01",
            simulation_method=SimulationMethod.DETERMINISTIC,
            parameter_overrides={"lead_volume_monthly": 1000.0, "developer_capacity_fte": 2.0},
            constraints=[{"name": "Team Capacity Limit", "metric": "final_capacity_utilization_percentage", "max_threshold": 100.0}],
        )

        result = sim_engine.run_simulation(scenario)
        assert len(result.constraint_violations) > 0
        assert "Constraint 'Team Capacity Limit' breached" in result.constraint_violations[0]


class TestSensitivityAndCounterfactual:
    """Tests parameter elasticity ranking and historical counterfactual evaluations."""

    def test_tornado_sensitivity_ranking(self):
        analyzer = SensitivityAnalyzer()
        scenario_engine = ScenarioEngine()
        scenario = scenario_engine.create_scenario(name="Base", twin_model_id="twin_01")

        rankings = analyzer.run_sensitivity_analysis(scenario, target_metric="cumulative_revenue_usd")
        assert len(rankings) > 0
        # Sorted descending by sensitivity score
        for i in range(len(rankings) - 1):
            assert rankings[i].sensitivity_score >= rankings[i + 1].sensitivity_score

    def test_counterfactual_evaluation(self):
        cf_engine = CounterfactualEngine()
        actuals = {"cumulative_revenue_usd": 150000.0, "ending_active_clients": 14.0}
        overrides = {"lead_conversion_rate": 0.12}

        res = cf_engine.evaluate_counterfactual(
            historical_event_id="EVT-2025-Q2",
            hypothetical_condition="Lead conversion was 12% instead of 8%",
            historical_actual_metrics=actuals,
            hypothetical_parameter_overrides=overrides,
        )

        assert res.counterfactual_code.startswith("CF-")
        assert res.historical_actual == actuals
        assert "simulated cumulative revenue" in res.divergence_summary
        assert len(res.limitations) > 0


class TestDecisionAndOutcomeGovernance:
    """Tests human-in-the-loop decision recording and model calibration learning."""

    def test_decision_support_and_human_signoff(self):
        service = DigitalTwinPlatformService()
        base_sc = service.create_scenario(name="Base", simulation_method=SimulationMethod.DETERMINISTIC)
        alt_sc = service.create_scenario(name="Hire 2 FTE", simulation_method=SimulationMethod.DETERMINISTIC, parameter_overrides={"developer_capacity_fte": 8.0})

        sim_base = service.run_scenario_simulation(base_sc, iterations=1)
        sim_alt = service.run_scenario_simulation(alt_sc, iterations=1)

        options = service.build_decision_options([sim_base, sim_alt])
        assert len(options) == 2

        # Human executive records decision
        record = service.record_decision(
            question="Should we hire 2 developers?",
            rationale="Simulation confirms capacity utilization drops to safe 68% with +$30k profit.",
            decision_owner="Chief Operating Officer",
            selected_option_id=options[1].option_code,
        )

        assert record.decision_code.startswith("DEC-")
        assert record.decision_owner == "Chief Operating Officer"

    def test_outcome_tracking_and_calibration(self):
        service = DigitalTwinPlatformService()
        rec = service.track_outcome(
            observed_period="2026-Q1",
            predicted_metrics={"cumulative_revenue_usd": 150000.0},
            actual_metrics={"cumulative_revenue_usd": 165000.0},
        )

        assert rec.variance_percentage == 10.0
        assert rec.model_error == 0.10

        cal_report = service.calibrate_twin_models([rec])
        assert cal_report.calibrations_count == 1
        assert len(cal_report.parameter_updates) > 0
        assert "INCREASE baseline estimate" in cal_report.parameter_updates[0]["recommended_action"]


class TestMultiScenarioComparison:
    """Tests side-by-side delta comparisons across baseline and strategic alternatives."""

    def test_scenario_comparison(self):
        service = DigitalTwinPlatformService()
        base = service.create_scenario(name="Current Path", simulation_method=SimulationMethod.DETERMINISTIC)
        alt1 = service.create_scenario(name="Price Bump +15%", simulation_method=SimulationMethod.DETERMINISTIC, parameter_overrides={"average_deal_value_usd": 5175.0})
        alt2 = service.create_scenario(name="Marketing Push", simulation_method=SimulationMethod.DETERMINISTIC, parameter_overrides={"lead_volume_monthly": 180.0})

        comp = service.compare_scenarios(base, [alt1, alt2], iterations=1)
        assert comp["baseline"]["scenario_name"] == "Current Path"
        assert len(comp["alternatives"]) == 2
        assert comp["alternatives"][0]["revenue_delta_usd"] > 0


@pytest.mark.asyncio
class TestDigitalTwinAgents:
    """Tests execution of Phase 50 AI Agents under strict safety permissions."""

    async def test_twin_builder_agent(self):
        agent = TwinBuilderAgent()
        context = AgentContext(
            workflow_id="wf_twin_builder",
            task_id="task_twin_builder",
            agent_run_id="run_twin_builder",
            metadata={"tenant_id": "tenant_01", "parameters": {"title": "Agent Automated Snapshot"}},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["is_cryptographically_verified"] is True

    async def test_scenario_simulation_agent(self):
        agent = ScenarioSimulationAgent()
        context = AgentContext(
            workflow_id="wf_scenario_sim",
            task_id="task_scenario_sim",
            agent_run_id="run_scenario_sim",
            metadata={"tenant_id": "tenant_01", "parameters": {"name": "AI Formulated Growth", "parameter_overrides": {"lead_conversion_rate": 0.11}, "iterations": 100}},
        )
        res = await agent.execute(context)
        assert res["status"] == "SUCCESS"
        assert res["scenario_name"] == "AI Formulated Growth"
        assert res["iterations"] == 100

    async def test_prohibited_safety_permissions(self):
        assert "AUTONOMOUS_STRATEGIC_DECISION" in PROHIBITED_PERMISSIONS
        assert "MUTATE_PRODUCTION_STATE" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_PRICE_CHANGE" in PROHIBITED_PERMISSIONS


class TestDigitalTwinBackgroundWorkers:
    """Tests background worker tasks for twin snapshots, simulations, and calibrations."""

    def test_task_capture_snapshot(self):
        res = task_capture_twin_state_snapshot(tenant_id="tenant_worker")
        assert res["status"] == "SUCCESS"
        assert res["is_valid"] is True

    def test_task_run_simulation(self):
        res = task_run_scenario_simulation(
            scenario_name="Worker Task Scenario",
            parameter_overrides={"lead_conversion_rate": 0.09},
            iterations=100,
        )
        assert res["status"] == "SUCCESS"
        assert res["metrics_summary"]["cumulative_revenue_usd"] > 0

    def test_task_run_sensitivity(self):
        res = task_run_tornado_sensitivity()
        assert res["status"] == "SUCCESS"
        assert res["parameters_ranked"] > 0

    def test_task_calibrate_models(self):
        res = task_calibrate_twin_models([{
            "observed_period": "2026-Q1",
            "predicted_metrics": {"cumulative_revenue_usd": 100000.0},
            "actual_metrics": {"cumulative_revenue_usd": 112000.0},
        }])
        assert res["status"] == "SUCCESS"
        assert res["calibrations_count"] == 1
