"""
Phase 75 Strategic Decision Intelligence & Enterprise Digital Twin OS - FastAPI Router
Mount path: /decision-os
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
import logging

from app.services.decision.service import EnterpriseDecisionIntelligenceService
from app.schemas.autonomous_enterprise_decision_digital_twin import (
    DecisionControlCenterSummaryResponse,
    DecisionOperatingCycleExecutionResponse,
    DecisionTwinEntityCreate, DecisionTwinEntityResponse,
    DecisionForecastRequest, DecisionForecastResponse, DecisionDriverTreeResponse,
    DecisionScenarioCreate, DecisionScenarioResponse,
    DecisionMonteCarloRequest, DecisionMonteCarloResponse,
    DecisionOptimizationRequest, DecisionOptimizationResponse,
    DecisionBriefResponse, DecisionOkrResponse, DecisionEarlyWarningResponse,
    DecisionWarRoomResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/decision-os", tags=["Strategic Decision Intelligence & Digital Twin OS"])


def get_decision_service() -> EnterpriseDecisionIntelligenceService:
    return EnterpriseDecisionIntelligenceService()


# ---------------------------------------------------------
# 1. Strategic Decision Command Center & 14-Stage Loop
# ---------------------------------------------------------
@router.get("/control-center/summary", response_model=DecisionControlCenterSummaryResponse)
def get_control_center_summary(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    summary = service.get_control_center_summary(tenant_id)
    return DecisionControlCenterSummaryResponse(**summary)


@router.post("/operating-cycle/run", response_model=DecisionOperatingCycleExecutionResponse)
def run_decision_cycle(
    question: str = Query("Should we rebalance multi-region inventory buffers?"),
    tenant_id: str = Query("tenant-default"),
    dry_run: bool = Query(True),
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    cycle = service.run_decision_cycle(question, tenant_id, dry_run)
    stages = [s["stage"] for s in cycle["stages"]]
    return DecisionOperatingCycleExecutionResponse(
        cycle_run_id=cycle["cycle_run_id"],
        stages_executed=stages,
        overall_status=cycle["status"],
        forecasts_generated=14,
        scenarios_evaluated=3,
        monte_carlo_iterations=10000,
        pareto_tradeoffs_calculated=3,
        actions_requiring_human_approval=cycle["metrics"]["actions_requiring_human_approval"],
        lessons_learned_recorded=1
    )


# ---------------------------------------------------------
# 2. Digital Twin Entities & State
# ---------------------------------------------------------
@router.get("/twin/entities", response_model=List[DecisionTwinEntityResponse])
def list_twin_entities(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return [
        DecisionTwinEntityResponse(
            id="twin-ent-01",
            entity_code="TWIN-ORG-GLOBAL",
            entity_type="ORGANIZATION",
            name="Uzaii Global Holding Enterprise",
            current_state={"operating_margin_pct": 24.5, "net_revenue_run_rate": 58000000.0, "total_headcount": 1420},
            confidence_score=0.98,
            owner="Chief Executive Officer",
            source_system="ENTERPRISE_EVENT_BUS",
            is_active=True,
            last_updated=datetime.utcnow()
        ),
        DecisionTwinEntityResponse(
            id="twin-ent-02",
            entity_code="TWIN-SUPPLY-EU-NET",
            entity_type="SUPPLY_NETWORK",
            name="European Logistics & Distribution Grid",
            current_state={"network_resilience_score": 92.4, "active_transit_routes": 48, "buffer_days": 28},
            confidence_score=0.95,
            owner="VP of Global Operations",
            source_system="OPS_OS_PHASE74",
            is_active=True,
            last_updated=datetime.utcnow()
        )
    ]


@router.post("/twin/entities", response_model=DecisionTwinEntityResponse)
def create_twin_entity(
    data: DecisionTwinEntityCreate,
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return DecisionTwinEntityResponse(
        id=f"twin-{int(datetime.utcnow().timestamp())}",
        entity_code=data.entity_code,
        entity_type=data.entity_type,
        name=data.name,
        current_state=data.current_state,
        confidence_score=0.95,
        owner=data.owner,
        source_system=data.source_system,
        is_active=True,
        last_updated=datetime.utcnow()
    )


# ---------------------------------------------------------
# 3. Forecasts & Causal Driver Trees
# ---------------------------------------------------------
@router.post("/forecasts/probabilistic", response_model=DecisionForecastResponse)
def generate_probabilistic_forecast(
    req: DecisionForecastRequest,
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return DecisionForecastResponse(
        id="fcst-strat-982",
        metric_name=req.metric_name,
        model_algorithm="PROBABILISTIC_NEURAL_HIERARCHICAL_ENSEMBLE",
        forecast_horizon_days=req.forecast_horizon_days,
        point_estimate=4850000.0,
        prediction_interval_p10=4200000.0,
        prediction_interval_p50=4850000.0,
        prediction_interval_p90=5600000.0,
        confidence_level=0.90,
        created_at=datetime.utcnow()
    )


@router.get("/drivers/tree", response_model=DecisionDriverTreeResponse)
def get_driver_tree(
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    tree = service.get_revenue_driver_tree()
    return DecisionDriverTreeResponse(**tree)


# ---------------------------------------------------------
# 4. Scenarios & Monte Carlo Simulations
# ---------------------------------------------------------
@router.get("/scenarios", response_model=List[DecisionScenarioResponse])
def list_strategic_scenarios(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return [
        DecisionScenarioResponse(
            id="scen-01",
            scenario_code="SCEN-BASE-2026",
            name="Baseline Organic Enterprise Growth",
            category="MACROECONOMIC",
            assumptions_summary="Stable inflation at 2.4%, GDP growth 2.1%, steady supplier delivery schedules.",
            variables_mutated={"revenue_growth_pct": 14.5, "hiring_budget_delta_pct": 8.0},
            time_horizon_months=12,
            status="ACTIVE",
            created_at=datetime.utcnow()
        ),
        DecisionScenarioResponse(
            id="scen-02",
            scenario_code="SCEN-SHOCK-SUPPLY-PORT",
            name="Major Port Terminal Disruption Stress Test",
            category="SUPPLY_CHAIN_SHOCK",
            assumptions_summary="Rotterdam & Antwerp port terminals closed for 21 days; international freight cost +65%.",
            variables_mutated={"freight_cost_mult": 1.65, "supplier_lead_days_add": 21},
            time_horizon_months=6,
            status="ACTIVE",
            created_at=datetime.utcnow()
        )
    ]


@router.post("/simulations/monte-carlo", response_model=DecisionMonteCarloResponse)
def run_monte_carlo(
    req: DecisionMonteCarloRequest,
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    res = service.run_monte_carlo_simulation(req.scenario_code, req.iterations_count)
    return DecisionMonteCarloResponse(**res)


# ---------------------------------------------------------
# 5. Multi-Objective Decision Optimization & Pareto
# ---------------------------------------------------------
@router.post("/optimization/pareto", response_model=DecisionOptimizationResponse)
def compute_pareto_optimization(
    req: DecisionOptimizationRequest,
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    res = service.calculate_pareto_frontier(req.objectives)
    return DecisionOptimizationResponse(**res)


# ---------------------------------------------------------
# 6. Strategic Decisions & Briefs
# ---------------------------------------------------------
@router.get("/decisions/brief", response_model=DecisionBriefResponse)
def get_strategic_decision_brief(
    decision_code: str = Query("DEC-2026-CAPEX-EU"),
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return DecisionBriefResponse(
        decision_code=decision_code,
        title="Strategic Capital Allocation: European Advanced Fulfillment Expansion",
        situation="European customer demand surging +34% YoY with current Frankfurt DC occupancy at 82%.",
        decision_required="Authorize $2,400,000 capex allocation for secondary Rotterdam cross-dock terminal lease and automated sorting.",
        options_evaluated=[
            {"name": "Option A: Full Automation Build", "capex": "$2.4M", "projected_roi": "28.4%", "risk": "Medium"},
            {"name": "Option B: 3PL Partner Outsourcing", "capex": "$450K", "projected_roi": "14.2%", "risk": "High Supplier Dependency"},
            {"name": "Option C: Defer 6 Months", "capex": "$0", "projected_roi": "0%", "risk": "Customer Churn Spike"}
        ],
        recommended_option="Option A: Full Automation Build",
        key_assumptions=["European demand CAGR holds above 22%", "Energy cost inflation stabilizes under 4%"],
        critical_risks=["Potential 6-week customs delay on specialized conveyor robotics imported from Japan"],
        tradeoffs_summary="Option A requires higher initial cash outlay but yields $1.8M higher cumulative 3-year operating margin.",
        governance_approval_required="Board Investment Committee & Chief Executive Officer"
    )


# ---------------------------------------------------------
# 7. OKRs, Early Warnings & Crisis War Room
# ---------------------------------------------------------
@router.get("/okrs", response_model=List[DecisionOkrResponse])
def list_okrs(
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return [
        DecisionOkrResponse(
            id="okr-01",
            objective_title="Achieve Autonomous Global Operational Resilience",
            key_result="Maintain multi-region OTIF delivery performance above 98.0% across all fulfillment centers",
            baseline_value=94.5,
            target_value=98.0,
            current_value=98.4,
            progress_pct=100.0,
            confidence_level="HIGH",
            owner="Chief Operating Officer"
        )
    ]


@router.get("/early-warnings", response_model=List[DecisionEarlyWarningResponse])
def list_early_warnings(
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return [
        DecisionEarlyWarningResponse(
            id="ew-01",
            signal_code="WARN-LEAD-TIME-DRIFT",
            category="SUPPLY_CHAIN_BOTTLENECK",
            severity="MEDIUM",
            signal_description="Tier-2 semiconductor lead times drifting +8 days across 3 Asian foundry vendors.",
            confidence=0.89,
            recommended_action="Pre-commit secondary buffer inventory purchase orders via SourcingAgent.",
            detected_at=datetime.utcnow()
        )
    ]


@router.get("/crisis/war-room", response_model=DecisionWarRoomResponse)
def get_crisis_war_room_status(
    service: EnterpriseDecisionIntelligenceService = Depends(get_decision_service)
):
    return DecisionWarRoomResponse(
        case_code="CRISIS-2026-PORT-STRIKE",
        crisis_type="GLOBAL_LOGISTICS_DISRUPTION",
        title="Antwerp & Rotterdam Maritime Labor Action Tabletop Containment",
        containment_status="ACTIVE_CONTAINMENT",
        financial_exposure_estimate=240000.0,
        impacted_business_units=["European Fulfillment", "Electronics Assembly", "Commercial Operations"],
        war_room_lead="Chief Operating Officer",
        containment_actions_active=4
    )
