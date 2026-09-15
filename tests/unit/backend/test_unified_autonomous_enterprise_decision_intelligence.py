"""
Phase 75 Test Suite: Unified Autonomous Enterprise Simulation, Digital Twin, Predictive Intelligence,
Scenario Planning & Strategic Decision Intelligence.
Validating 14-Stage Decision Cycle, Digital Twin Graph, Probabilistic Forecasting,
Monte Carlo & Pareto Optimization, Causal Driver Trees, 12 Decision Agents, and Safety Guardrails.
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.services.decision.service import EnterpriseDecisionIntelligenceService
from app.api.v1.decision_os import router as decision_os_router
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS
)
from agents.decision import (
    ForecastingAgent,
    ScenarioAgent,
    SimulationAgent,
    CausalAnalysisAgent,
    OptimizationAgent,
    SensitivityAgent,
    StrategicRiskAgent,
    RiskAgent,
    StrategicIntelligenceAgent,
    EarlyWarningAgent,
    DecisionBriefAgent,
    CrisisAgent,
    DecisionOrchestratorAgent
)
from agents.core.base import AgentContext


@pytest.fixture
def decision_service():
    return EnterpriseDecisionIntelligenceService()


@pytest.fixture
def test_client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(decision_os_router)
    return TestClient(app)


# ----------------------------------------------------------------------
# 1. 14-Stage Closed-Loop Decision Intelligence Cycle Tests
# ----------------------------------------------------------------------
def test_14_stage_decision_cycle(decision_service):
    """Verify end-to-end execution of the 14-stage closed-loop decision intelligence cycle."""
    res = decision_service.run_decision_cycle(
        question="Should we enter the EU Enterprise Market in Q1 2027?",
        tenant_id="tenant-corp-1",
        dry_run=True
    )
    assert res["status"] == "COMPLETED_SIMULATION"
    assert len(res["stages"]) == 14

    stage_names = [s["stage"] for s in res["stages"]]
    expected_stages = [
        "QUESTION", "DATA", "CONTEXT", "FORECAST", "SCENARIOS",
        "SIMULATION", "OPTIMIZATION", "RISK", "SENSITIVITY",
        "RECOMMENDATION", "HUMAN_DECISION", "EXECUTION", "OUTCOME", "LEARNING"
    ]
    assert stage_names == expected_stages
    assert res["metrics"]["decision_intelligence_score"] >= 90.0
    assert res["metrics"]["actions_requiring_human_approval"] >= 1


def test_control_center_summary_metrics(decision_service):
    """Verify synthesis of strategic enterprise health and control center KPIs."""
    summary = decision_service.get_control_center_summary("tenant-corp-1")
    assert summary["decision_intelligence_score"] >= 90.0
    assert summary["active_digital_twin_entities_count"] > 0
    assert summary["active_strategic_scenarios_count"] > 0
    assert summary["running_simulations_count"] > 0
    assert summary["pareto_optimal_options_count"] > 0
    assert summary["open_strategic_decisions_count"] >= 0
    assert summary["early_warning_signals_count"] >= 0
    assert summary["active_war_rooms_count"] >= 0


# ----------------------------------------------------------------------
# 2. Monte Carlo Simulation Engine & Distribution Metrics
# ----------------------------------------------------------------------
def test_monte_carlo_simulation_execution(decision_service):
    """Verify Monte Carlo simulation runs distributions and calculates VaR / Expected Shortfall."""
    sim_res = decision_service.run_monte_carlo_simulation(
        scenario_code="SCEN-BASE-2026",
        iterations=10000
    )
    assert sim_res["iterations_count"] == 10000
    assert sim_res["mean_outcome"] > 0.0
    assert sim_res["var_95_percentile"] > 0.0
    assert sim_res["cvar_expected_shortfall"] > 0.0
    assert "confidence_interval_90" in sim_res
    assert sim_res["status"] == "COMPLETED"


# ----------------------------------------------------------------------
# 3. Multi-Objective Decision Optimization & Pareto Frontier
# ----------------------------------------------------------------------
def test_multi_objective_pareto_optimization(decision_service):
    """Verify multi-objective optimization reveals non-dominated Pareto alternatives."""
    pareto_res = decision_service.calculate_pareto_frontier(
        objectives=["maximize_profit", "minimize_risk", "maximize_customer_experience"]
    )
    assert pareto_res["optimization_code"] == "OPT-STRAT-2026"
    assert "pareto_frontier" in pareto_res
    assert len(pareto_res["pareto_frontier"]) >= 3

    options = [opt["option_name"] for opt in pareto_res["pareto_frontier"]]
    assert any("Aggressive" in opt for opt in options)
    assert any("Balanced" in opt for opt in options)
    assert any("Conservative" in opt for opt in options)
    assert pareto_res["recommended_option"] is not None


# ----------------------------------------------------------------------
# 4. Causal Driver Tree & Elasticity Analysis
# ----------------------------------------------------------------------
def test_causal_driver_tree_evaluation(decision_service):
    """Verify business driver tree computes elasticity and impact weights."""
    driver_res = decision_service.get_revenue_driver_tree()
    assert driver_res["target_metric"] == "Enterprise Revenue"
    assert driver_res["current_value"] > 0.0
    assert len(driver_res["primary_drivers"]) >= 3

    # Check that elasticities are defined
    assert "elasticity_weights" in driver_res
    assert "price_increase_1pct" in driver_res["elasticity_weights"]
    assert "churn_reduction_1pct" in driver_res["elasticity_weights"]


# ----------------------------------------------------------------------
# 5. Security Permissions & Non-Negotiable Safety Prohibitions
# ----------------------------------------------------------------------
def test_strategic_decision_permissions_and_prohibitions():
    """Verify that Phase 75 permissions exist and non-negotiable prohibitions are enforced."""
    # Permissions verification
    assert AgentPermission.READ_DECISION_OS.value == "READ_DECISION_OS"
    assert AgentPermission.OPERATE_ENTERPRISE_DIGITAL_TWIN.value == "OPERATE_ENTERPRISE_DIGITAL_TWIN"
    assert AgentPermission.RUN_STRATEGIC_SIMULATION.value == "RUN_STRATEGIC_SIMULATION"
    assert AgentPermission.EXECUTE_DECISION_OPTIMIZATION.value == "EXECUTE_DECISION_OPTIMIZATION"
    assert AgentPermission.MANAGE_STRATEGIC_MODELS.value == "MANAGE_STRATEGIC_MODELS"
    assert AgentPermission.GOVERN_CAPITAL_ALLOCATION.value == "GOVERN_CAPITAL_ALLOCATION"
    assert AgentPermission.TRIGGER_CRISIS_WAR_ROOM.value == "TRIGGER_CRISIS_WAR_ROOM"

    # Non-negotiable strategic prohibitions verification
    expected_prohibitions = [
        "AUTONOMOUS_EXECUTE_STRATEGIC_DECISION_UNREVIEWED",
        "AUTONOMOUS_COMMIT_CAPITAL_ALLOCATION_UNREVIEWED",
        "AUTONOMOUS_MUTATE_ORGANIZATIONAL_STRUCTURE",
        "AUTONOMOUS_TRIGGER_CRISIS_CONTAINMENT_UNREVIEWED",
        "EXPOSE_BOARD_STRATEGIC_SCENARIOS_PLAINTEXT",
        "AUTONOMOUS_MODIFY_EXECUTIVE_COMPENSATION"
    ]
    for p in expected_prohibitions:
        assert p in PROHIBITED_PERMISSIONS



# ----------------------------------------------------------------------
# 6. 12 Autonomous Decision AI Agents Verification
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_all_12_autonomous_decision_agents():
    """Verify all 12 autonomous decision agents instantiate and execute safely."""
    agents = [
        ForecastingAgent(),
        ScenarioAgent(),
        SimulationAgent(),
        CausalAnalysisAgent(),
        OptimizationAgent(),
        SensitivityAgent(),
        StrategicRiskAgent(),
        StrategicIntelligenceAgent(),
        EarlyWarningAgent(),
        DecisionBriefAgent(),
        CrisisAgent(),
        DecisionOrchestratorAgent()
    ]
    assert len(agents) == 12

    context = AgentContext(
        workflow_id="wf-decision-test",
        task_id="t-decision-test-1",
        agent_run_id="run-decision-test-1",
        metadata={"tenant_id": "tenant-corp-1", "strategic_context": "GTM Planning"}
    )
    for agent in agents:
        res = await agent.run(context)
        assert res.status == "COMPLETED"
        assert res.confidence == "HIGH"
        assert "summary" in res.result
        assert len(res.result["recommendations"]) >= 1


# ----------------------------------------------------------------------
# 7. FastAPI REST Endpoints Integration
# ----------------------------------------------------------------------
def test_api_control_center_summary(test_client):
    """Test GET /decision-os/control-center/summary endpoint."""
    resp = test_client.get("/decision-os/control-center/summary?tenant_id=tenant-corp-1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["decision_intelligence_score"] >= 90.0
    assert data["active_digital_twin_entities_count"] > 0


def test_api_run_operating_cycle(test_client):
    """Test POST /decision-os/operating-cycle/run endpoint."""
    resp = test_client.post(
        "/decision-os/operating-cycle/run?question=Optimize+Capex&tenant_id=tenant-corp-1&dry_run=true"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_status"] == "COMPLETED_SIMULATION"
    assert len(data["stages_executed"]) == 14


def test_api_digital_twin_entities(test_client):
    """Test GET & POST /decision-os/twin/entities endpoints."""
    resp = test_client.get("/decision-os/twin/entities?tenant_id=tenant-corp-1")
    assert resp.status_code == 200
    ents = resp.json()
    assert len(ents) >= 2

    post_resp = test_client.post(
        "/decision-os/twin/entities",
        json={
            "entity_code": "TWIN-FACILITY-APAC",
            "entity_type": "FACILITY",
            "name": "Singapore High-Tech Hub",
            "current_state": {"utilization_pct": 87.5},
            "owner": "Director of APAC Operations",
            "source_system": "IOT_PLATFORM"
        }
    )
    assert post_resp.status_code == 200
    assert post_resp.json()["entity_code"] == "TWIN-FACILITY-APAC"


def test_api_forecasts_and_drivers(test_client):
    """Test POST /decision-os/forecasts/probabilistic and GET /drivers/tree."""
    resp_fc = test_client.post(
        "/decision-os/forecasts/probabilistic",
        json={
            "metric_name": "quarterly_ebitda",
            "forecast_horizon_days": 90
        }
    )
    assert resp_fc.status_code == 200
    fc_data = resp_fc.json()
    assert fc_data["metric_name"] == "quarterly_ebitda"
    assert fc_data["prediction_interval_p10"] < fc_data["prediction_interval_p50"] < fc_data["prediction_interval_p90"]

    resp_dr = test_client.get("/decision-os/drivers/tree")
    assert resp_dr.status_code == 200
    dr_data = resp_dr.json()
    assert dr_data["target_metric"] == "Enterprise Revenue"
    assert len(dr_data["primary_drivers"]) >= 3


def test_api_scenarios_and_simulations(test_client):
    """Test GET /decision-os/scenarios and POST /simulations/monte-carlo."""
    resp_scen = test_client.get("/decision-os/scenarios?tenant_id=tenant-corp-1")
    assert resp_scen.status_code == 200
    scens = resp_scen.json()
    assert len(scens) >= 2

    resp_mc = test_client.post(
        "/decision-os/simulations/monte-carlo",
        json={
            "scenario_code": "SCEN-BASE-2026",
            "iterations_count": 1000
        }
    )
    assert resp_mc.status_code == 200
    mc_data = resp_mc.json()
    assert mc_data["iterations_count"] == 1000
    assert mc_data["status"] == "COMPLETED"


def test_api_optimization_and_brief(test_client):
    """Test POST /decision-os/optimization/pareto and GET /decisions/brief."""
    resp_opt = test_client.post(
        "/decision-os/optimization/pareto",
        json={
            "decision_code": "DEC-2026-CAPEX-EU",
            "objectives": ["profit", "risk", "resilience"]
        }
    )
    assert resp_opt.status_code == 200
    opt_data = resp_opt.json()
    assert len(opt_data["pareto_frontier"]) >= 3
    assert opt_data["recommended_option"] is not None

    resp_brief = test_client.get("/decision-os/decisions/brief?decision_code=DEC-2026-CAPEX-EU")
    assert resp_brief.status_code == 200
    brief_data = resp_brief.json()
    assert brief_data["decision_code"] == "DEC-2026-CAPEX-EU"
    assert len(brief_data["options_evaluated"]) >= 3
    assert brief_data["governance_approval_required"] is not None


def test_api_okrs_warnings_war_room(test_client):
    """Test GET /decision-os/okrs, /early-warnings, and /crisis/war-room."""
    resp_okr = test_client.get("/decision-os/okrs")
    assert resp_okr.status_code == 200
    assert len(resp_okr.json()) >= 1

    resp_ew = test_client.get("/decision-os/early-warnings")
    assert resp_ew.status_code == 200
    assert len(resp_ew.json()) >= 1

    resp_wr = test_client.get("/decision-os/crisis/war-room")
    assert resp_wr.status_code == 200
    wr_data = resp_wr.json()
    assert wr_data["containment_status"] == "ACTIVE_CONTAINMENT"
    assert wr_data["war_room_lead"] == "Chief Operating Officer"
