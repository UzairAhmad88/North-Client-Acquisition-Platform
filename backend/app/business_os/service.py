"""Consolidated Business OS & Executive Platform Service."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.business_os.assistant import ExecutiveCopilotResponse, ExecutiveCopilotService
from app.business_os.base import (
    BriefingFrequency,
    BusinessHealthReport,
    DecisionPriority,
    DecisionStatus,
    KPICategory,
    KPISnapshot,
    RiskCategory,
    RiskSeverity,
    ScenarioSimulationResult,
    ScenarioType,
)
from app.business_os.briefings import BusinessCalendarEvent, ExecutiveBriefingEngine, ExecutiveBriefingReport
from app.business_os.decisions import DecisionIntelligenceEngine, DecisionRecord
from app.business_os.health import BusinessHealthEngine
from app.business_os.kpi import KPIRegistry
from app.business_os.portfolio import CapacityPlanningSummary, PortfolioCapacityManager, PortfolioSummary
from app.business_os.risks import OrganizationalRiskRegister, RiskRecord
from app.business_os.portfolio import CapacityPlanningSummary, PortfolioCapacityManager, PortfolioSummary
from app.business_os.risks import OrganizationalRiskRegister
from app.business_os.scenarios import ScenarioPlanningEngine
from app.business_os.scorecards import DepartmentScorecard, ScorecardEngine
from app.business_os.strategy import StrategicObjective, StrategyManager


class BusinessOSPlatformService:
    """
    Central orchestration service for the Executive Business Operating System.
    Harmonizes operational data from all 41 preceding domains into strategic decision intelligence.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.kpi_registry = KPIRegistry()
        self.strategy_mgr = StrategyManager()
        self.scorecard_engine = ScorecardEngine(self.kpi_registry)
        self.portfolio_mgr = PortfolioCapacityManager()
        self.risk_register = OrganizationalRiskRegister()
        self.decision_engine = DecisionIntelligenceEngine()
        self.scenario_engine = ScenarioPlanningEngine()
        self.health_engine = BusinessHealthEngine()
        self.briefing_engine = ExecutiveBriefingEngine()
        self.copilot_service = ExecutiveCopilotService()

    # --- Executive 360 & Health ---

    def get_executive_360_overview(self) -> Dict[str, Any]:
        """Provides the unified top-level executive command center payload."""
        health = self.get_business_health()
        portfolio = self.portfolio_mgr.evaluate_portfolio()
        capacity = self.portfolio_mgr.evaluate_capacity()
        top_risks = self.risk_register.list_risks(min_severity=RiskSeverity.HIGH)
        pending_decisions = self.decision_engine.list_decisions(status=DecisionStatus.DECISION_REQUIRED)
        upcoming_events = self.briefing_engine.get_upcoming_calendar_events()

        # Key baseline metric snapshots
        kpis = [
            self.kpi_registry.calculate_snapshot("monthly_recurring_revenue", Decimal("3800000.00"), previous_value=Decimal("3450000.00")),
            self.kpi_registry.calculate_snapshot("gross_profit_margin", Decimal("65.40"), previous_value=Decimal("64.80")),
            self.kpi_registry.calculate_snapshot("pipeline_weighted_value", Decimal("12400000.00"), previous_value=Decimal("10800000.00")),
            self.kpi_registry.calculate_snapshot("active_client_retention_rate", Decimal("94.50"), previous_value=Decimal("93.00")),
            self.kpi_registry.calculate_snapshot("on_time_milestone_delivery_rate", Decimal("88.00"), previous_value=Decimal("90.00")),
            self.kpi_registry.calculate_snapshot("platform_availability_uptime", Decimal("99.95"), previous_value=Decimal("99.90")),
        ]

        return {
            "organization_name": "Uzaii Develop By North's",
            "business_health": health,
            "core_kpis": kpis,
            "portfolio_summary": portfolio,
            "capacity_summary": capacity,
            "critical_risks_count": len(top_risks),
            "top_risks": top_risks[:3],
            "pending_decisions_count": len(pending_decisions),
            "pending_decisions": pending_decisions,
            "upcoming_events": upcoming_events[:4],
        }

    def get_business_health(self) -> BusinessHealthReport:
        return self.health_engine.evaluate_organization_health()

    # --- KPIs & Scorecards ---

    def list_kpis(self, category: Optional[KPICategory] = None) -> List[KPISnapshot]:
        definitions = self.kpi_registry.list_definitions(category=category)
        snapshots = []
        for d in definitions:
            val = d.target_value if d.target_value else Decimal("100.00")
            snap = self.kpi_registry.calculate_snapshot(d.kpi_id, val)
            snapshots.append(snap)
        return snapshots

    def get_scorecards(self) -> List[DepartmentScorecard]:
        sample_metrics = {
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
        return self.scorecard_engine.generate_all_scorecards(sample_metrics)

    def reconcile_metrics(
        self,
        finance_revenue: Decimal,
        crm_revenue: Decimal,
        active_contracts: int,
        active_billing_profiles: int,
    ) -> List[Dict[str, Any]]:
        return self.kpi_registry.reconcile_cross_domain_metrics(
            finance_revenue, crm_revenue, active_contracts, active_billing_profiles
        )

    # --- Strategy & OKRs ---

    def list_strategic_objectives(self) -> List[StrategicObjective]:
        return self.strategy_mgr.list_objectives()

    def get_strategic_objective(self, objective_id: str) -> Optional[StrategicObjective]:
        return self.strategy_mgr.get_objective(objective_id)

    # --- Risk Register ---

    def list_risks(
        self,
        category: Optional[RiskCategory] = None,
        min_severity: Optional[RiskSeverity] = None,
    ) -> List[RiskRecord]:
        return self.risk_register.list_risks(category=category, min_severity=min_severity)

    def create_risk(
        self,
        title: str,
        description: str,
        category: RiskCategory,
        probability: Any,
        impact: Any,
        owner: str,
        evidence_signals: Optional[List[str]] = None,
        mitigation_strategy: str = "",
        contingency_plan: str = "",
    ) -> RiskRecord:
        return self.risk_register.register_risk(
            title=title,
            description=description,
            category=category,
            probability=probability,
            impact=impact,
            owner=owner,
            evidence_signals=evidence_signals,
            mitigation_strategy=mitigation_strategy,
            contingency_plan=contingency_plan,
        )

    # --- Decision Intelligence ---

    def list_decisions(self, status: Optional[DecisionStatus] = None) -> List[DecisionRecord]:
        return self.decision_engine.list_decisions(status=status)

    def record_decision(
        self,
        decision_id: str,
        chosen_option_id: str,
        decision_rationale: str,
        decided_by: str,
    ) -> Optional[DecisionRecord]:
        return self.decision_engine.record_human_decision(
            decision_id=decision_id,
            chosen_option_id=chosen_option_id,
            decision_rationale=decision_rationale,
            decided_by=decided_by,
        )

    def record_decision_outcome(
        self,
        decision_id: str,
        actual_outcome: str,
        outcome_variance_analysis: str,
        lessons_learned: List[str],
    ) -> Optional[DecisionRecord]:
        return self.decision_engine.record_decision_outcome(
            decision_id=decision_id,
            actual_outcome=actual_outcome,
            outcome_variance_analysis=outcome_variance_analysis,
            lessons_learned=lessons_learned,
        )

    # --- Scenario Planning ---

    def run_scenario(
        self,
        scenario_name: str,
        scenario_type: ScenarioType = ScenarioType.CUSTOM,
        base_revenue: Decimal = Decimal("4000000.00"),
        base_cost: Decimal = Decimal("1400000.00"),
        price_change_pct: Decimal = Decimal("0.0"),
        conversion_change_pct: Decimal = Decimal("0.0"),
        client_churn_revenue: Decimal = Decimal("0.0"),
        new_hires_count: int = 0,
        additional_project_hours: Decimal = Decimal("0.0"),
    ) -> ScenarioSimulationResult:
        return self.scenario_engine.run_simulation(
            scenario_name=scenario_name,
            scenario_type=scenario_type,
            base_revenue=base_revenue,
            base_cost=base_cost,
            price_change_pct=price_change_pct,
            conversion_change_pct=conversion_change_pct,
            client_churn_revenue=client_churn_revenue,
            new_hires_count=new_hires_count,
            additional_project_hours=additional_project_hours,
        )

    # --- Briefings & Calendar ---

    def get_briefing(self, frequency: BriefingFrequency = BriefingFrequency.DAILY) -> ExecutiveBriefingReport:
        return self.briefing_engine.generate_briefing(frequency=frequency)

    def get_calendar_events(self) -> List[BusinessCalendarEvent]:
        return self.briefing_engine.get_upcoming_calendar_events()

    # --- Executive AI Copilot ---

    def query_copilot(self, query: str, user_role: str = "EXECUTIVE") -> ExecutiveCopilotResponse:
        return self.copilot_service.answer_query(query=query, user_role=user_role)
