"""API Endpoints for Scenario Planning, What-If Simulations, and Sensitivity Analysis."""

from typing import Any, List
from fastapi import APIRouter, Depends, status

from app.business_os.service import BusinessOSPlatformService
from app.schemas.business_os import ScenarioResponse, ScenarioRunRequest

router = APIRouter(prefix="/scenarios", tags=["scenario-planning"])

_service_instance = BusinessOSPlatformService()


def get_business_os_service() -> BusinessOSPlatformService:
    return _service_instance


@router.post("/run", response_model=ScenarioResponse, status_code=status.HTTP_200_OK)
async def run_scenario_simulation(
    payload: ScenarioRunRequest,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Execute an isolated What-If scenario simulation without mutating production state."""
    result = service.run_scenario(
        scenario_name=payload.scenario_name,
        scenario_type=payload.scenario_type,
        base_revenue=payload.base_revenue,
        base_cost=payload.base_cost,
        price_change_pct=payload.price_change_pct,
        conversion_change_pct=payload.conversion_change_pct,
        client_churn_revenue=payload.client_churn_revenue,
        new_hires_count=payload.new_hires_count,
        additional_project_hours=payload.additional_project_hours,
    )
    return ScenarioResponse(
        scenario_id=result.scenario_id,
        scenario_name=result.scenario_name,
        scenario_type=result.scenario_type,
        simulated_revenue=result.simulated_revenue,
        simulated_profit=result.simulated_profit,
        simulated_margin_pct=result.simulated_margin_pct,
        capacity_utilization_pct=result.capacity_utilization_pct,
        cash_requirement=result.cash_requirement,
        risk_level=result.risk_level,
        assumptions_applied=result.assumptions_applied,
        sensitivity_rankings=result.sensitivity_rankings,
        generated_at=result.generated_at,
        is_production_isolated=result.is_production_isolated,
    )
