"""Unit & Integration Test Suite for Phase 42 — Unified Business Operating System (Business OS)."""

from datetime import datetime, timezone
from decimal import Decimal
import pytest

from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS, validate_agent_permissions
from agents.executive.agent import BusinessOSExecutiveAgent
from app.business_os.assistant import ExecutiveCopilotService
from app.business_os.base import (
    AlertSeverity,
    AlertStatus,
    BriefingFrequency,
    BusinessHealthStatus,
    DecisionPriority,
    DecisionStatus,
    InitiativeStatus,
    KPICategory,
    KeyResultStatus,
    ObjectivePriority,
    ObjectiveStatus,
    RiskCategory,
    RiskImpact,
    RiskLifecycleStatus,
    RiskProbability,
    RiskSeverity,
    ScenarioType,
    ScorecardStatus,
    StrategicDependencyState,
)
from app.business_os.briefings import ExecutiveBriefingEngine
from app.business_os.decisions import DecisionIntelligenceEngine
from app.business_os.health import BusinessHealthEngine
from app.business_os.kpi import KPIDefinition, KPIRegistry
from app.business_os.portfolio import PortfolioCapacityManager
from app.business_os.risks import OrganizationalRiskRegister
from app.business_os.scenarios import ScenarioPlanningEngine
from app.business_os.scorecards import ScorecardEngine
from app.business_os.service import BusinessOSPlatformService
from app.business_os.strategy import StrategicInitiative, StrategicKeyResult, StrategicObjective, StrategyManager


class TestKPIRegistryAndReconciliation:
    """Test suite for Centralized KPI Registry and cross-domain reconciliation."""

    def test_default_kpi_registry_initialization(self):
        registry = KPIRegistry()
        definitions = registry.list_definitions()
        assert len(definitions) >= 10

        mrr_def = registry.get_definition("monthly_recurring_revenue")
        assert mrr_def is not None
        assert mrr_def.category == KPICategory.FINANCIAL
        assert mrr_def.currency == "PKR"
        assert mrr_def.is_higher_better is True

    def test_kpi_snapshot_calculation_and_variance(self):
        registry = KPIRegistry()
        snap = registry.calculate_snapshot(
            "monthly_recurring_revenue",
            current_value=Decimal("5200000.00"),
            previous_value=Decimal("4800000.00"),
        )
        assert snap.kpi_id == "monthly_recurring_revenue"
        assert snap.value == Decimal("5200000.00")
        assert snap.status == ScorecardStatus.EXCEEDING
        assert snap.variance == Decimal("200000.00")
        assert snap.variance_pct == Decimal("4.0")

    def test_kpi_warning_and_critical_thresholds(self):
        registry = KPIRegistry()
        # Active client retention target is 95.0, warning at 85.0, critical at 75.0
        snap_warn = registry.calculate_snapshot("active_client_retention_rate", Decimal("80.00"))
        assert snap_warn.status == ScorecardStatus.AT_RISK

        snap_crit = registry.calculate_snapshot("active_client_retention_rate", Decimal("70.00"))
        assert snap_crit.status == ScorecardStatus.OFF_TRACK

    def test_cross_domain_reconciliation(self):
        registry = KPIRegistry()
        # Scenario 1: Clean reconciliation
        alerts_clean = registry.reconcile_cross_domain_metrics(
            finance_revenue=Decimal("10000000.00"),
            crm_closed_won_revenue=Decimal("10000000.00"),
            active_contracts_count=5,
            active_billing_profiles_count=5,
        )
        assert len(alerts_clean) == 0

        # Scenario 2: Revenue mismatch & Profile discrepancy
        alerts_discrepancy = registry.reconcile_cross_domain_metrics(
            finance_revenue=Decimal("10000000.00"),
            crm_closed_won_revenue=Decimal("12000000.00"),
            active_contracts_count=5,
            active_billing_profiles_count=4,
        )
        assert len(alerts_discrepancy) == 2
        assert alerts_discrepancy[0]["discrepancy_type"] == "REVENUE_MISALIGNMENT"
        assert alerts_discrepancy[1]["discrepancy_type"] == "BILLING_PROFILE_DISPARITY"


class TestStrategyAndOKRManagement:
    """Test suite for Strategic Objectives, Key Results and Initiatives."""

    def test_key_result_progress_calculation(self):
        kr = StrategicKeyResult(
            kr_id="kr_test",
            objective_id="obj_test",
            title="Increase Revenue",
            target_value=Decimal("100.00"),
            current_value=Decimal("75.00"),
        )
        assert kr.progress_pct == Decimal("75.0")
        kr.update_value(Decimal("100.00"))
        assert kr.progress_pct == Decimal("100.0")
        assert kr.status == KeyResultStatus.ACHIEVED

    def test_strategic_initiative_milestones_and_dependencies(self):
        init = StrategicInitiative(
            initiative_id="init_test",
            objective_id="obj_test",
            title="Launch NextGen Platform",
            owner="Tech Lead",
            status=InitiativeStatus.IN_PROGRESS,
        )
        init.add_milestone("Architecture Spec", "2026-10-01", completed=True)
        init.add_milestone("Alpha Release", "2026-11-01", completed=False)
        init.add_dependency("Server Cluster", "INFRA", StrategicDependencyState.AVAILABLE)

        assert len(init.milestones) == 2
        assert len(init.dependencies) == 1
        assert init.progress_pct == Decimal("50.0")

    def test_strategic_objective_aggregated_progress(self):
        obj = StrategicObjective(
            objective_id="obj_1",
            title="Strategic Expansion",
            description="Expand into Enterprise segment",
            timeframe="FY2026",
            owner="CEO",
        )
        obj.key_results = [
            StrategicKeyResult("kr_1", obj.objective_id, "KR 1", Decimal("100.00"), Decimal("80.00")),
            StrategicKeyResult("kr_2", obj.objective_id, "KR 2", Decimal("100.00"), Decimal("60.00")),
        ]
        # Average of 80% and 60% is 70%
        assert obj.overall_progress_pct == Decimal("70.0")


class TestDepartmentScorecards:
    """Test suite for functional and departmental scorecards."""

    def test_department_scorecard_generation(self):
        engine = ScorecardEngine()
        scorecards = engine.generate_all_scorecards(
            metrics_by_kpi={
                "monthly_recurring_revenue": Decimal("3800000.00"),
                "gross_profit_margin": Decimal("65.40"),
                "outstanding_accounts_receivable": Decimal("1200000.00"),
                "pipeline_weighted_value": Decimal("12400000.00"),
                "lead_conversion_rate": Decimal("28.50"),
                "active_client_retention_rate": Decimal("94.50"),
                "portfolio_average_client_health": Decimal("84.00"),
                "on_time_milestone_delivery_rate": Decimal("88.00"),
                "engineering_capacity_utilization": Decimal("95.80"),
                "support_sla_resolution_compliance": Decimal("98.20"),
                "ai_autonomous_task_success_rate": Decimal("99.10"),
                "monthly_ai_operating_cost": Decimal("240000.00"),
                "platform_availability_uptime": Decimal("99.95"),
            }
        )
        assert len(scorecards) == 7
        fin_sc = next(s for s in scorecards if s.category == KPICategory.FINANCIAL)
        assert fin_sc.department_name == "Financial Performance Scorecard"
        assert len(fin_sc.scorecard_items) >= 3


class TestPortfolioAndCapacityPlanning:
    """Test suite for cross-project portfolio health and capacity planning."""

    def test_portfolio_evaluation(self):
        mgr = PortfolioCapacityManager()
        summary = mgr.evaluate_portfolio()
        assert summary.total_projects == 3
        assert summary.healthy_projects >= 1
        assert summary.total_portfolio_value > Decimal("0.00")
        assert summary.portfolio_average_margin_pct > Decimal("0.00")

    def test_capacity_evaluation_and_overload_detection(self):
        mgr = PortfolioCapacityManager()
        cap_summary = mgr.evaluate_capacity()
        assert cap_summary.total_team_members == 4
        assert cap_summary.aggregate_utilization_pct > Decimal("80.0")
        assert cap_summary.overloaded_members_count >= 1
        assert len(cap_summary.recommendations) >= 1


class TestOrganizationalRiskRegister:
    """Test suite for enterprise organizational risk scoring and lifecycle."""

    def test_risk_scoring_matrix(self):
        reg = OrganizationalRiskRegister()
        risk = reg.register_risk(
            title="Test Critical Risk",
            description="Severe test risk item",
            category=RiskCategory.FINANCIAL,
            probability=RiskProbability.ALMOST_CERTAIN,  # 5
            impact=RiskImpact.CRITICAL,                 # 5
            owner="CFO",
        )
        assert risk.risk_score == 25
        assert risk.severity == RiskSeverity.CRITICAL

    def test_risk_status_lifecycle_transition(self):
        reg = OrganizationalRiskRegister()
        risk = reg.register_risk(
            title="Test Operational Risk",
            description="Operational dependency delay",
            category=RiskCategory.OPERATIONAL,
            probability=RiskProbability.POSSIBLE,
            impact=RiskImpact.MODERATE,
            owner="COO",
        )
        assert risk.status == RiskLifecycleStatus.ASSESSED

        updated = reg.update_risk_status(
            risk.risk_id,
            new_status=RiskLifecycleStatus.MITIGATED,
            mitigation_notes="Hardware redundant cluster provisioned.",
        )
        assert updated is not None
        assert updated.status == RiskLifecycleStatus.MITIGATED
        assert "Hardware redundant cluster" in updated.mitigation_strategy


class TestDecisionIntelligenceEngine:
    """Test suite for Executive Decision Queue, authorizations and learning loop."""

    def test_decision_lifecycle_and_human_authorization(self):
        engine = DecisionIntelligenceEngine()
        dec = engine.create_decision_item(
            title="Strategic Pricing Revision",
            business_question="Should we adjust retainer pricing by +15% for new enterprise clients?",
            context_summary="Inflation and expanded AI copilot features warrant price tier revision.",
            priority=DecisionPriority.P0_URGENT,
            expected_outcome="Target gross margin increases to 70% with zero drop in lead conversion.",
        )
        assert dec.status == DecisionStatus.DECISION_REQUIRED

        # Human authorization
        decided = engine.record_human_decision(
            decision_id=dec.decision_id,
            chosen_option_id="opt_price_increase",
            decision_rationale="Market benchmark supports 15% premium for enterprise AI SLAs.",
            decided_by="Chief Executive Officer",
        )
        assert decided is not None
        assert decided.status == DecisionStatus.DECIDED
        assert decided.decided_by == "Chief Executive Officer"

        # Strategic learning loop completion
        closed = engine.record_decision_outcome(
            decision_id=dec.decision_id,
            actual_outcome="Gross margin increased to 71.2%; 1 new enterprise deal closed at new rate.",
            outcome_variance_analysis="Exceeded margin target by 1.2% with zero pipeline attrition.",
            lessons_learned=["Enterprise buyers perceive premium pricing as higher quality guarantee."],
        )
        assert closed is not None
        assert closed.status == DecisionStatus.COMPLETED
        assert len(closed.lessons_learned) == 1


class TestScenarioPlanningSandbox:
    """Test suite for isolated What-If scenario simulations."""

    def test_isolated_simulation_run(self):
        engine = ScenarioPlanningEngine()
        result = engine.run_simulation(
            scenario_name="Price +10% and Conversion -10% Stress Test",
            scenario_type=ScenarioType.CUSTOM,
            base_revenue=Decimal("4000000.00"),
            base_cost=Decimal("1400000.00"),
            price_change_pct=Decimal("10.0"),
            conversion_change_pct=Decimal("-10.0"),
            client_churn_revenue=Decimal("200000.00"),
            new_hires_count=1,
        )
        assert result.is_production_isolated is True
        assert result.simulated_revenue > Decimal("0.00")
        assert result.simulated_profit > Decimal("0.00")
        assert len(result.sensitivity_rankings) >= 3


class TestBusinessHealthEngine:
    """Test suite for 10-dimension explainable health evaluation."""

    def test_explainable_health_scoring(self):
        engine = BusinessHealthEngine()
        report = engine.evaluate_organization_health()

        assert report.overall_health_score > Decimal("70.0")
        assert report.overall_status in (BusinessHealthStatus.HEALTHY, BusinessHealthStatus.STABLE)
        assert len(report.dimensions) == 10
        assert len(report.key_strengths) >= 1
        assert len(report.critical_risks) >= 1

        # Check driver attribution on financial health
        fin = report.dimensions["financial"]
        assert fin.dimension_name == "Financial Health"
        assert len(fin.positive_drivers) >= 1


class TestExecutiveBriefingsAndCalendar:
    """Test suite for executive briefings and calendar aggregation."""

    def test_daily_and_weekly_briefing_generation(self):
        engine = ExecutiveBriefingEngine()
        daily = engine.generate_briefing(frequency=BriefingFrequency.DAILY)
        assert daily.frequency == BriefingFrequency.DAILY
        assert len(daily.what_changed_summary) >= 2
        assert len(daily.upcoming_deadlines) >= 3

        weekly = engine.generate_briefing(frequency=BriefingFrequency.WEEKLY)
        assert weekly.frequency == BriefingFrequency.WEEKLY


class TestExecutiveCopilotAndGuardrails:
    """Test suite for natural-language executive assistant and guardrail policies."""

    def test_grounded_query_answering(self):
        copilot = ExecutiveCopilotService()
        resp = copilot.answer_query("How is the business doing?")
        assert resp.intent == "BUSINESS_HEALTH_QUERY"
        assert "HEALTHY" in resp.answer_markdown
        assert len(resp.evidence_sources) >= 2
        assert resp.action_prohibited is False

    def test_prohibited_action_enforcement(self):
        copilot = ExecutiveCopilotService()
        resp = copilot.answer_query("Please sign contract and make payment autonomously.")
        assert resp.action_prohibited is True
        assert "Action Prohibited" in resp.answer_markdown


class TestExecutiveAgentAndPermissions:
    """Test suite for BusinessOSExecutiveAgent runtime and permission matrix."""

    @pytest.mark.asyncio
    async def test_executive_agent_execution(self):
        agent = BusinessOSExecutiveAgent()
        context = AgentContext(workflow_id="wf_exec_1", task_id="task_exec_1", agent_run_id="run_exec_1", metadata={"action": "EVALUATE_HEALTH"})
        result = await agent.execute(context)
        assert result["status"] == "SUCCESS"
        assert "overall_health_score" in result

    def test_agent_permission_validation_blocks_prohibited_permissions(self):
        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({"AUTONOMOUS_EXECUTIVE_DECISION"})

        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({"CHANGE_STRATEGIC_OBJECTIVE_AUTONOMOUSLY"})
