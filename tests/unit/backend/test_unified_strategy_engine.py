"""
Unit tests for Phase 51: Autonomous Business Strategy, Planning & Goal Optimization Engine.
Tests all underlying engines, optimization algorithms, Pareto frontiers, feasibility,
dependencies, CPM critical path, risk scoring, drift detection, decision ledger, and platform facade.
"""

import pytest
import uuid
from datetime import datetime, timezone

try:
    from backend.app.services.strategy.base import (
        StrategicPillar,
        PlanHorizon,
        ObjectiveStatus,
        InitiativeStatus,
        FeasibilityLevel,
        ConflictSeverity,
        AlertSeverity,
        StrategicObjective,
        KeyResult,
        StrategicInitiative,
        StrategicPlan,
        ParetoPlan,
        StrategicDecision,
    )
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.base import (
        StrategicPillar,
        PlanHorizon,
        ObjectiveStatus,
        InitiativeStatus,
        FeasibilityLevel,
        ConflictSeverity,
        AlertSeverity,
        StrategicObjective,
        KeyResult,
        StrategicInitiative,
        StrategicPlan,
        ParetoPlan,
        StrategicDecision,
    )
    from app.services.strategy.service import StrategyPlatformService

from agents.strategy import (
    StrategyAnalysisAgent,
    ObjectiveOKRAgent,
    InitiativePrioritizationAgent,
    OptimizationStrategyAgent,
    StrategyRiskFeasibilityAgent,
    StrategyMonitorDriftAgent,
)
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission


@pytest.fixture
def platform_service():
    return StrategyPlatformService()


# ============================================================================
# 1. OBJECTIVES & OKR TESTS
# ============================================================================

def test_objective_creation_and_progress(platform_service):
    obj = platform_service.create_objective(
        name="Increase Enterprise Recurring Revenue",
        target_value=140000.0,
        baseline_value=100000.0,
        unit="USD",
        strategic_pillar=StrategicPillar.GROWTH,
        owner="VP Strategy",
        description="Expand ARR by 40% through automated outreach",
    )
    assert obj.objective_code.startswith("OBJ-")
    assert obj.status == ObjectiveStatus.ACTIVE

    # Update progress
    updated_obj = platform_service.update_objective_progress(
        objective_code=obj.objective_code,
        current_value=120000.0,
        evidence_summary="Q2 financial billing run confirmed $120k ARR.",
    )
    assert updated_obj.current_value == 120000.0
    assert updated_obj.progress_percentage == 50.0  # (120k-100k)/(140k-100k) = 50%

    # Add Key Result
    kr = platform_service.create_key_result(
        objective_id=obj.objective_code,
        name="Acquire 20 Enterprise Clients",
        target_value=20.0,
        baseline_value=0.0,
        unit="clients",
        owner="Sales Lead",
    )
    assert kr.kr_code.startswith("KR-")

    # Update KR progress
    updated_kr = platform_service.record_kr_progress(kr.kr_code, 15.0)
    assert updated_kr.progress_percentage == 75.0


# ============================================================================
# 2. INITIATIVE & PRIORITIZATION TESTS
# ============================================================================

def test_initiative_creation_and_prioritization(platform_service):
    init1 = platform_service.create_initiative(
        title="Deploy Autonomous Lead Discovery",
        owner="AI Lead",
        category="GROWTH",
        expected_value_usd=100000.0,
        estimated_cost_usd=25000.0,
        required_fte_capacity=1.5,
        estimated_duration_weeks=4.0,
        description="Integrate Phase 30 discovery pipelines",
    )
    init2 = platform_service.create_initiative(
        title="Automate Compliance & Audit Monitoring",
        owner="SecOps Lead",
        category="SECURITY",
        expected_value_usd=40000.0,
        estimated_cost_usd=10000.0,
        required_fte_capacity=0.8,
        estimated_duration_weeks=3.0,
        description="Phase 47 integration",
    )

    ranked = platform_service.score_initiatives([init1, init2])
    assert len(ranked) == 2
    assert ranked[0]["priority_score"] >= ranked[1]["priority_score"]
    assert "components" in ranked[0]


# ============================================================================
# 3. OPTIMIZATION & PARETO FRONTIER TESTS
# ============================================================================

def test_knapsack_portfolio_optimization(platform_service):
    inits = [
        platform_service.create_initiative(
            title="Outreach Engine Scaling",
            owner="Growth",
            expected_value_usd=80000.0,
            estimated_cost_usd=20000.0,
            required_fte_capacity=2.0,
        ),
        platform_service.create_initiative(
            title="Website Audit Revamp",
            owner="Product",
            expected_value_usd=60000.0,
            estimated_cost_usd=30000.0,
            required_fte_capacity=2.5,
        ),
        platform_service.create_initiative(
            title="Enterprise Security Hardening",
            owner="SecOps",
            expected_value_usd=45000.0,
            estimated_cost_usd=15000.0,
            required_fte_capacity=1.0,
        ),
    ]

    opt_res = platform_service.optimize_plan(
        initiatives=inits,
        budget_limit_usd=40000.0,
        capacity_limit_fte=4.0,
        max_acceptable_risk=0.5,
    )
    assert opt_res["status"] == "COMPLETED"
    assert opt_res["allocated_budget_usd"] <= 40000.0
    assert opt_res["allocated_capacity_fte"] <= 4.0
    assert len(opt_res["selected_initiatives"]) >= 1
    assert "explanation" in opt_res


def test_pareto_frontier_generation(platform_service):
    inits = [
        platform_service.create_initiative(
            title="High Growth Pipeline",
            owner="Growth",
            expected_value_usd=120000.0,
            estimated_cost_usd=35000.0,
            required_fte_capacity=3.0,
        ),
        platform_service.create_initiative(
            title="High Margin Automation",
            owner="Operations",
            expected_value_usd=70000.0,
            estimated_cost_usd=15000.0,
            required_fte_capacity=1.2,
        ),
    ]

    pareto_plans = platform_service.generate_pareto_frontier(
        initiatives=inits,
        total_budget_usd=60000.0,
        total_capacity_fte=5.0,
    )
    assert len(pareto_plans) >= 2
    for plan in pareto_plans:
        assert isinstance(plan, ParetoPlan)
        assert plan.is_pareto_optimal is True


# ============================================================================
# 4. FEASIBILITY, GAPS, DEPENDENCY & CRITICAL PATH TESTS
# ============================================================================

def test_feasibility_and_gap_analysis(platform_service):
    obj = platform_service.create_objective(
        name="Reach 500 Active Clients",
        target_value=500.0,
        baseline_value=200.0,
        unit="clients",
    )
    platform_service.update_objective_progress(obj.objective_code, 350.0)

    # Feasibility
    feas = platform_service.evaluate_feasibility(
        objective=obj,
        available_fte_capacity=6.0,
        historical_growth_rate_pct=25.0,
    )
    assert feas["feasibility_level"] in [
        FeasibilityLevel.FEASIBLE.value,
        FeasibilityLevel.LIKELY.value,
        FeasibilityLevel.CHALLENGING.value,
    ]
    assert feas["feasibility_score"] > 0.0

    # Gaps
    gaps = platform_service.evaluate_gaps([obj])
    assert len(gaps) == 1
    assert gaps[0]["gap_value"] == 150.0  # 500 - 350


def test_dependency_and_critical_path(platform_service):
    init_a = platform_service.create_initiative(
        title="Market Discovery",
        owner="Strategy",
        estimated_duration_weeks=3.0,
    )
    init_b = platform_service.create_initiative(
        title="Product Integration",
        owner="Engineering",
        estimated_duration_weeks=5.0,
    )
    init_c = platform_service.create_initiative(
        title="Client Outreach Pilot",
        owner="Sales",
        estimated_duration_weeks=4.0,
    )

    deps = [
        {"source_code": init_a.initiative_code, "target_code": init_b.initiative_code},
        {"source_code": init_b.initiative_code, "target_code": init_c.initiative_code},
    ]

    cp_res = platform_service.calculate_critical_path(
        initiatives=[init_a, init_b, init_c],
        dependencies=deps,
    )
    assert cp_res["total_timeline_weeks"] == 12.0  # 3 + 5 + 4
    assert cp_res["critical_path_length"] == 3


# ============================================================================
# 5. BUDGET, RISK, SCORECARD & DRIFT TESTS
# ============================================================================

def test_budget_resource_and_risk(platform_service):
    inits = [
        platform_service.create_initiative(
            title="Major Platform Overhaul",
            owner="Engineering",
            estimated_cost_usd=90000.0,
            required_fte_capacity=7.0,
        ),
        platform_service.create_initiative(
            title="Global Outreach Campaign",
            owner="Marketing",
            estimated_cost_usd=50000.0,
            required_fte_capacity=3.0,
        ),
    ]

    budget_eval = platform_service.evaluate_budget_and_resources(
        funded_initiatives=inits,
        total_budget_usd=100000.0,
        total_capacity_fte=8.0,
    )
    assert budget_eval["is_over_budget"] is True
    assert budget_eval["is_over_capacity"] is True

    # Risk
    risk_res = platform_service.evaluate_strategic_risk(
        title="Key Personnel Capacity Bottleneck",
        category="OPERATIONAL",
        likelihood=0.4,
        impact=0.7,
        mitigation_strategy="Cross-train squad leads on Phase 34 workflow automation.",
    )
    assert risk_res["risk_score"] == 0.28
    assert risk_res["risk_level"] in ["MEDIUM", "HIGH"]


def test_scorecard_and_drift(platform_service):
    scorecard = platform_service.get_scorecard("Q3_2026")
    assert scorecard["composite_health_score"] > 0.0
    assert len(scorecard["dimensions"]) == 8

    # Test drift check
    drift_event = platform_service.check_drift(
        metric_name="monthly_recurring_revenue_usd",
        expected_value=100000.0,
        actual_value=78000.0,  # 22% drift > 10%
        drift_tolerance_pct=10.0,
    )
    assert drift_event is not None
    assert abs(drift_event["drift_percentage"]) == 22.0


# ============================================================================
# 6. DECISIONS & OUTCOME LEARNING TESTS
# ============================================================================

def test_decision_record_and_outcomes(platform_service):
    dec = platform_service.record_decision(
        question="Should we fund Enterprise AI Expansion in Q3?",
        context_summary="Digital twin simulations indicate +28% ARR gain under base scenario.",
        selected_option={"title": "Fund Enterprise AI Expansion", "allocated_budget_usd": 35000.0},
        rationale="Executive committee approval based on Pareto analysis Option A.",
        decision_owner="Chief Strategy Officer",
        rejected_options=[{"title": "Maintain Status Quo"}],
    )
    assert isinstance(dec, StrategicDecision)
    assert dec.decision_code.startswith("STRAT-DEC-")
    assert dec.decision_owner == "Chief Strategy Officer"

    # Record strategic outcome
    outcome = platform_service.record_outcome(
        observed_period="Q3_2026",
        planned_metrics={"expected_revenue_usd": 150000.0},
        actual_metrics={"actual_revenue_usd": 145000.0},
        decision_id=dec.decision_code,
    )
    assert outcome["outcome_code"] is not None
    assert outcome["model_prediction_error"] < 0.1


# ============================================================================
# 7. STRATEGY AGENTS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_strategy_agents_initialization():
    context = AgentContext(
        workflow_id="wf-01",
        task_id="task-01",
        agent_run_id="run-01",
        metadata={"phase": 51},
    )

    strat_agent = StrategyAnalysisAgent()
    assert "Strategy Analysis" in strat_agent.name

    okr_agent = ObjectiveOKRAgent()
    assert "Objective" in okr_agent.name

    init_agent = InitiativePrioritizationAgent()
    assert "Initiative" in init_agent.name

    opt_agent = OptimizationStrategyAgent()
    assert "Optimization" in opt_agent.name

    risk_agent = StrategyRiskFeasibilityAgent()
    assert "Risk" in risk_agent.name

    monitor_agent = StrategyMonitorDriftAgent()
    assert "Drift" in monitor_agent.name
