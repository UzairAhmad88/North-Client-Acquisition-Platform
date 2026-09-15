"""
Background Tasks for Phase 50:
Unified Digital Twin, Business Simulation, Scenario Intelligence & Strategic What-If Engine.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.digital_twin.service import DigitalTwinPlatformService
    from backend.app.services.digital_twin.base import ScenarioType, SimulationMethod, TimeHorizon
except ImportError:
    from app.services.digital_twin.service import DigitalTwinPlatformService
    from app.services.digital_twin.base import ScenarioType, SimulationMethod, TimeHorizon

logger = logging.getLogger(__name__)
_twin_service = DigitalTwinPlatformService()


def task_capture_twin_state_snapshot(
    tenant_id: str = "default_tenant",
    title: str = "Scheduled Enterprise State Snapshot",
) -> Dict[str, Any]:
    """Captures and hashes a point-in-time enterprise digital twin snapshot."""
    state = _twin_service.capture_enterprise_state(tenant_id=tenant_id, title=title)
    is_valid = _twin_service.verify_state_integrity(state)
    return {
        "task": "capture_twin_state_snapshot",
        "status": "SUCCESS",
        "snapshot_code": state.snapshot_code,
        "state_hash": state.state_hash,
        "is_valid": is_valid,
        "composite_health_score": state.composite_health_score,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_run_scenario_simulation(
    scenario_name: str,
    parameter_overrides: Optional[Dict[str, float]] = None,
    simulation_method: str = "MONTE_CARLO",
    iterations: int = 1000,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Executes background sandboxed simulation for a scenario."""
    try:
        method = SimulationMethod[simulation_method]
    except KeyError:
        method = SimulationMethod.MONTE_CARLO

    scenario = _twin_service.create_scenario(
        name=scenario_name,
        simulation_method=method,
        parameter_overrides=parameter_overrides or {},
        tenant_id=tenant_id,
    )
    sim_res = _twin_service.run_scenario_simulation(scenario=scenario, iterations=iterations)

    return {
        "task": "run_scenario_simulation",
        "status": "SUCCESS",
        "scenario_code": scenario.scenario_code,
        "simulation_code": sim_res.simulation_code,
        "method": sim_res.method.value,
        "iterations": sim_res.iterations,
        "runtime_seconds": sim_res.runtime_seconds,
        "metrics_summary": sim_res.metrics_summary,
        "violations_count": len(sim_res.constraint_violations),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_run_tornado_sensitivity(
    target_metric: str = "cumulative_revenue_usd",
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Executes parameter elasticity sweeps to compute Tornado chart rankings."""
    scenario = _twin_service.create_scenario(
        name="Scheduled Sensitivity Analysis",
        simulation_method=SimulationMethod.DETERMINISTIC,
        tenant_id=tenant_id,
    )
    rankings = _twin_service.analyze_sensitivity(scenario, target_metric=target_metric)

    return {
        "task": "run_tornado_sensitivity",
        "status": "SUCCESS",
        "target_metric": target_metric,
        "parameters_ranked": len(rankings),
        "top_impact_parameter": rankings[0].parameter_name if rankings else None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_calibrate_twin_models(
    outcome_records_data: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Evaluates prediction errors across recorded outcomes and generates model calibration updates."""
    records = []
    for rec in outcome_records_data:
        records.append(
            _twin_service.track_outcome(
                observed_period=rec.get("observed_period", "PERIOD"),
                predicted_metrics=rec.get("predicted_metrics", {}),
                actual_metrics=rec.get("actual_metrics", {}),
                decision_id=rec.get("decision_id"),
                scenario_id=rec.get("scenario_id"),
            )
        )

    report = _twin_service.calibrate_twin_models(records)

    return {
        "task": "calibrate_twin_models",
        "status": "SUCCESS",
        "calibrations_count": report.calibrations_count,
        "average_prediction_error": report.average_prediction_error,
        "proposed_updates_count": len(report.parameter_updates),
        "summary": report.summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
