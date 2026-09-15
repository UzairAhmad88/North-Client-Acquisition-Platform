"""
Unified Strategy Platform Service Facade for Phase 51.
Coordinates strategic planning, OKR management, multi-objective optimization,
Pareto analysis, feasibility, risk, budgeting, drift detection, decision governance, and outcome learning.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.strategy.base import (
        KeyResult,
        ObjectiveStatus,
        ParetoPlan,
        PlanHorizon,
        StrategicDecision,
        StrategicInitiative,
        StrategicObjective,
        StrategicPillar,
        StrategicPlan,
    )
    from backend.app.services.strategy.objectives import ObjectiveManager
    from backend.app.services.strategy.okrs import OKRManager
    from backend.app.services.strategy.initiatives import InitiativeManager
    from backend.app.services.strategy.prioritization import PrioritizationEngine
    from backend.app.services.strategy.optimization import StrategicOptimizationEngine
    from backend.app.services.strategy.pareto import ParetoAnalyzer
    from backend.app.services.strategy.feasibility import FeasibilityAnalyzer
    from backend.app.services.strategy.gap_analysis import GapAnalyzer
    from backend.app.services.strategy.dependencies import DependencyEngine
    from backend.app.services.strategy.critical_path import CriticalPathEngine
    from backend.app.services.strategy.budget import BudgetManager
    from backend.app.services.strategy.risk import StrategicRiskEngine
    from backend.app.services.strategy.scorecards import StrategicScorecardEngine
    from backend.app.services.strategy.drift import DriftDetectionEngine
    from backend.app.services.strategy.decisions import StrategicDecisionManager
    from backend.app.services.strategy.outcomes import OutcomeLearningEngine
except ImportError:
    from app.services.strategy.base import (
        KeyResult,
        ObjectiveStatus,
        ParetoPlan,
        PlanHorizon,
        StrategicDecision,
        StrategicInitiative,
        StrategicObjective,
        StrategicPillar,
        StrategicPlan,
    )
    from app.services.strategy.objectives import ObjectiveManager
    from app.services.strategy.okrs import OKRManager
    from app.services.strategy.initiatives import InitiativeManager
    from app.services.strategy.prioritization import PrioritizationEngine
    from app.services.strategy.optimization import StrategicOptimizationEngine
    from app.services.strategy.pareto import ParetoAnalyzer
    from app.services.strategy.feasibility import FeasibilityAnalyzer
    from app.services.strategy.gap_analysis import GapAnalyzer
    from app.services.strategy.dependencies import DependencyEngine
    from app.services.strategy.critical_path import CriticalPathEngine
    from app.services.strategy.budget import BudgetManager
    from app.services.strategy.risk import StrategicRiskEngine
    from app.services.strategy.scorecards import StrategicScorecardEngine
    from app.services.strategy.drift import DriftDetectionEngine
    from app.services.strategy.decisions import StrategicDecisionManager
    from app.services.strategy.outcomes import OutcomeLearningEngine

logger = logging.getLogger(__name__)


class StrategyPlatformService:
    """
    Master Service for Phase 51: Autonomous Business Strategy, Planning & Goal Optimization Engine.
    """

    def __init__(self):
        self.objective_manager = ObjectiveManager()
        self.okr_manager = OKRManager()
        self.initiative_manager = InitiativeManager()
        self.prioritization_engine = PrioritizationEngine()
        self.optimization_engine = StrategicOptimizationEngine()
        self.pareto_analyzer = ParetoAnalyzer()
        self.feasibility_analyzer = FeasibilityAnalyzer()
        self.gap_analyzer = GapAnalyzer()
        self.dependency_engine = DependencyEngine()
        self.critical_path_engine = CriticalPathEngine()
        self.budget_manager = BudgetManager()
        self.risk_engine = StrategicRiskEngine()
        self.scorecard_engine = StrategicScorecardEngine()
        self.drift_engine = DriftDetectionEngine()
        self.decision_manager = StrategicDecisionManager()
        self.outcome_engine = OutcomeLearningEngine()

    # --- Objectives & Pillars ---

    def create_objective(
        self,
        name: str,
        target_value: float,
        unit: str = "USD",
        baseline_value: float = 0.0,
        strategic_pillar: StrategicPillar = StrategicPillar.GROWTH,
        owner: str = "executive_team",
        priority: str = "HIGH",
        description: Optional[str] = None,
    ) -> StrategicObjective:
        return self.objective_manager.create_objective(
            name=name,
            target_value=target_value,
            unit=unit,
            baseline_value=baseline_value,
            strategic_pillar=strategic_pillar,
            owner=owner,
            priority=priority,
            description=description,
        )

    def update_objective_progress(
        self,
        objective_code: str,
        current_value: float,
        evidence_summary: Optional[str] = None,
    ) -> StrategicObjective:
        return self.objective_manager.update_progress(
            objective_code=objective_code,
            current_value=current_value,
            evidence_summary=evidence_summary,
        )

    def list_objectives(self, pillar: Optional[StrategicPillar] = None) -> List[StrategicObjective]:
        return self.objective_manager.list_objectives(pillar=pillar)

    # --- OKRs ---

    def create_key_result(
        self,
        objective_id: str,
        name: str,
        target_value: float,
        unit: str = "PERCENT",
        baseline_value: float = 0.0,
        owner: str = "team_lead",
    ) -> KeyResult:
        return self.okr_manager.create_key_result(
            objective_id=objective_id,
            name=name,
            target_value=target_value,
            unit=unit,
            baseline_value=baseline_value,
            owner=owner,
        )

    def record_kr_progress(self, kr_code: str, current_value: float) -> KeyResult:
        return self.okr_manager.record_kr_progress(kr_code=kr_code, current_value=current_value)

    # --- Initiatives & Prioritization ---

    def create_initiative(
        self,
        title: str,
        owner: str,
        category: str = "GROWTH",
        expected_value_usd: float = 50000.0,
        estimated_cost_usd: float = 15000.0,
        required_fte_capacity: float = 1.5,
        estimated_duration_weeks: float = 6.0,
        description: Optional[str] = None,
    ) -> StrategicInitiative:
        return self.initiative_manager.create_initiative(
            title=title,
            owner=owner,
            category=category,
            expected_value_usd=expected_value_usd,
            estimated_cost_usd=estimated_cost_usd,
            required_fte_capacity=required_fte_capacity,
            estimated_duration_weeks=estimated_duration_weeks,
            description=description,
        )

    def score_initiatives(self, initiatives: List[StrategicInitiative]) -> List[Dict[str, Any]]:
        return self.prioritization_engine.rank_initiatives(initiatives)

    # --- Optimization & Pareto Analysis ---

    def optimize_plan(
        self,
        initiatives: List[StrategicInitiative],
        budget_limit_usd: float,
        capacity_limit_fte: float,
        max_acceptable_risk: float = 0.50,
    ) -> Dict[str, Any]:
        return self.optimization_engine.optimize_portfolio(
            initiatives=initiatives,
            budget_limit_usd=budget_limit_usd,
            capacity_limit_fte=capacity_limit_fte,
            max_acceptable_risk=max_acceptable_risk,
        )

    def generate_pareto_frontier(
        self,
        initiatives: List[StrategicInitiative],
        total_budget_usd: float = 100000.0,
        total_capacity_fte: float = 8.0,
    ) -> List[ParetoPlan]:
        return self.pareto_analyzer.compute_pareto_frontier(
            initiatives=initiatives,
            total_budget_usd=total_budget_usd,
            total_capacity_fte=total_capacity_fte,
        )

    # --- Feasibility, Gap Analysis & Critical Path ---

    def evaluate_feasibility(
        self,
        objective: StrategicObjective,
        available_fte_capacity: float = 6.0,
        historical_growth_rate_pct: float = 15.0,
    ) -> Dict[str, Any]:
        return self.feasibility_analyzer.evaluate_objective_feasibility(
            objective=objective,
            available_fte_capacity=available_fte_capacity,
            historical_growth_rate_pct=historical_growth_rate_pct,
        )

    def evaluate_gaps(self, objectives: List[StrategicObjective]) -> List[Dict[str, Any]]:
        return self.gap_analyzer.perform_gap_analysis(objectives=objectives)

    def calculate_critical_path(
        self,
        initiatives: List[StrategicInitiative],
        dependencies: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        return self.critical_path_engine.calculate_critical_path(
            initiatives=initiatives,
            dependencies=dependencies,
        )

    # --- Budget, Risk & Scorecard ---

    def evaluate_budget_and_resources(
        self,
        funded_initiatives: List[StrategicInitiative],
        total_budget_usd: float = 120000.0,
        total_capacity_fte: float = 8.0,
    ) -> Dict[str, Any]:
        return self.budget_manager.evaluate_budget_and_resources(
            funded_initiatives=funded_initiatives,
            total_budget_usd=total_budget_usd,
            total_capacity_fte=total_capacity_fte,
        )

    def evaluate_strategic_risk(
        self,
        title: str,
        category: str = "OPERATIONAL",
        likelihood: float = 0.3,
        impact: float = 0.6,
        mitigation_strategy: str = "Implement weekly milestone reviews.",
        owner: str = "risk_lead",
    ) -> Dict[str, Any]:
        return self.risk_engine.evaluate_risk(
            title=title,
            category=category,
            likelihood=likelihood,
            impact=impact,
            mitigation_strategy=mitigation_strategy,
            owner=owner,
        )

    def get_scorecard(self, period: str = "CURRENT_QUARTER") -> Dict[str, Any]:
        return self.scorecard_engine.generate_scorecard(period=period)

    # --- Drift, Decision & Outcomes ---

    def check_drift(
        self,
        metric_name: str,
        expected_value: float,
        actual_value: float,
        drift_tolerance_pct: float = 10.0,
    ) -> Optional[Dict[str, Any]]:
        return self.drift_engine.check_metric_drift(
            metric_name=metric_name,
            expected_value=expected_value,
            actual_value=actual_value,
            drift_tolerance_pct=drift_tolerance_pct,
        )

    def record_decision(
        self,
        question: str,
        context_summary: str,
        selected_option: Dict[str, Any],
        rationale: str,
        decision_owner: str,
        rejected_options: Optional[List[Dict[str, Any]]] = None,
    ) -> StrategicDecision:
        return self.decision_manager.record_decision(
            question=question,
            context_summary=context_summary,
            selected_option=selected_option,
            rationale=rationale,
            decision_owner=decision_owner,
            rejected_options=rejected_options,
        )

    def record_outcome(
        self,
        observed_period: str,
        planned_metrics: Dict[str, Any],
        actual_metrics: Dict[str, Any],
        decision_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.outcome_engine.record_strategic_outcome(
            observed_period=observed_period,
            planned_metrics=planned_metrics,
            actual_metrics=actual_metrics,
            decision_id=decision_id,
        )
