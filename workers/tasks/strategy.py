"""
Background Tasks for Phase 51:
Autonomous Business Strategy, Planning & Goal Optimization Engine.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.strategy.service import StrategyPlatformService
except ImportError:
    from app.services.strategy.service import StrategyPlatformService

logger = logging.getLogger(__name__)
_strategy_service = StrategyPlatformService()


def task_monitor_strategic_objectives(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Evaluates progress and health scorecards across registered strategic objectives."""
    scorecard = _strategy_service.get_scorecard()
    objectives = _strategy_service.list_objectives()
    gaps = _strategy_service.evaluate_gaps(objectives)

    return {
        "task": "monitor_strategic_objectives",
        "status": "SUCCESS",
        "composite_health_score": scorecard.get("composite_health_score"),
        "objectives_monitored": len(objectives),
        "gaps_identified": len(gaps),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_optimize_strategic_portfolio(
    budget_limit_usd: float = 100000.0,
    capacity_limit_fte: float = 8.0,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Executes scheduled portfolio optimization and generates Pareto-efficient packages."""
    inits = _strategy_service.initiative_manager.list_initiatives()
    if not inits:
        inits = [
            _strategy_service.create_initiative("Inbound SEO Multiplier", "Marketing", expected_value_usd=50000.0, estimated_cost_usd=10000.0, required_fte_capacity=1.0),
            _strategy_service.create_initiative("AI Workflow Auto-Remediation", "Engineering", expected_value_usd=85000.0, estimated_cost_usd=22000.0, required_fte_capacity=1.5),
        ]

    opt_res = _strategy_service.optimize_plan(inits, budget_limit_usd=budget_limit_usd, capacity_limit_fte=capacity_limit_fte)
    pareto_plans = _strategy_service.generate_pareto_frontier(inits, total_budget_usd=budget_limit_usd, total_capacity_fte=capacity_limit_fte)

    return {
        "task": "optimize_strategic_portfolio",
        "status": "SUCCESS",
        "run_code": opt_res.get("run_code"),
        "net_expected_benefit_usd": opt_res.get("net_expected_benefit_usd"),
        "pareto_plans_count": len(pareto_plans),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_detect_strategic_drift(
    metric_name: str = "monthly_recurring_revenue_usd",
    expected_value: float = 180000.0,
    actual_value: float = 150000.0,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Sweeps core metrics against plan baselines to identify strategic drift."""
    drift_res = _strategy_service.check_drift(metric_name=metric_name, expected_value=expected_value, actual_value=actual_value)

    return {
        "task": "detect_strategic_drift",
        "status": "SUCCESS",
        "metric_name": metric_name,
        "has_drift": drift_res is not None,
        "drift_event": drift_res,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_record_strategic_outcome_learning(
    observed_period: str = "2026-Q1",
    planned_metrics: Optional[Dict[str, Any]] = None,
    actual_metrics: Optional[Dict[str, Any]] = None,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Calculates strategic variance and prepares organizational learning entries."""
    plans = planned_metrics or {"expected_revenue_usd": 200000.0}
    actuals = actual_metrics or {"actual_revenue_usd": 215000.0}

    outcome_rec = _strategy_service.record_outcome(
        observed_period=observed_period,
        planned_metrics=plans,
        actual_metrics=actuals,
    )

    return {
        "task": "record_strategic_outcome_learning",
        "status": "SUCCESS",
        "outcome_code": outcome_rec.get("outcome_code"),
        "variance_percentage": outcome_rec.get("variance_percentage"),
        "model_prediction_error": outcome_rec.get("model_prediction_error"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
