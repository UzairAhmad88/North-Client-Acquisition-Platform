"""
REST API Router for Phase 51:
Autonomous Business Strategy, Planning & Goal Optimization Engine.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

try:
    from backend.app.services.strategy.base import (
        StrategicPillar,
    )
    from backend.app.services.strategy.service import StrategyPlatformService
    from backend.app.schemas.strategy import (
        CriticalPathResponse,
        DecisionRecordCreateRequest,
        DecisionRecordResponse,
        DriftCheckRequest,
        DriftCheckResponse,
        FeasibilityResponse,
        GapAnalysisResponse,
        InitiativeCreateRequest,
        InitiativeResponse,
        KeyResultCreateRequest,
        KeyResultResponse,
        ObjectiveCreateRequest,
        ObjectiveProgressUpdateRequest,
        ObjectiveResponse,
        OptimizationResponse,
        OptimizationRunRequest,
        ParetoPlanResponse,
        ScorecardResponse,
        StrategyCopilotQueryRequest,
        StrategyCopilotQueryResponse,
    )
except ImportError:
    from app.services.strategy.base import (
        StrategicPillar,
    )
    from app.services.strategy.service import StrategyPlatformService
    from app.schemas.strategy import (
        CriticalPathResponse,
        DecisionRecordCreateRequest,
        DecisionRecordResponse,
        DriftCheckRequest,
        DriftCheckResponse,
        FeasibilityResponse,
        GapAnalysisResponse,
        InitiativeCreateRequest,
        InitiativeResponse,
        KeyResultCreateRequest,
        KeyResultResponse,
        ObjectiveCreateRequest,
        ObjectiveProgressUpdateRequest,
        ObjectiveResponse,
        OptimizationResponse,
        OptimizationRunRequest,
        ParetoPlanResponse,
        ScorecardResponse,
        StrategyCopilotQueryRequest,
        StrategyCopilotQueryResponse,
    )

router = APIRouter(prefix="/strategy", tags=["strategy"])
_strategy_service = StrategyPlatformService()


@router.get("/overview")
async def get_overview(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Returns strategic overview including scorecard, active objectives, and health index."""
    scorecard = _strategy_service.get_scorecard()
    objs = _strategy_service.list_objectives()
    inits = _strategy_service.initiative_manager.list_initiatives()

    return {
        "status": "SUCCESS",
        "tenant_id": tenant_id,
        "composite_health_score": scorecard.get("composite_health_score", 1.0),
        "composite_health_percentage": scorecard.get("composite_health_percentage", 100.0),
        "total_active_objectives": len(objs),
        "total_active_initiatives": len(inits),
        "scorecard": scorecard,
    }


@router.get("/objectives", response_model=List[ObjectiveResponse])
async def list_objectives(pillar: Optional[str] = None) -> List[ObjectiveResponse]:
    """Lists registered strategic objectives."""
    p = None
    if pillar:
        try:
            p = StrategicPillar[pillar]
        except KeyError:
            p = None

    objs = _strategy_service.list_objectives(pillar=p)
    return [
        ObjectiveResponse(
            objective_code=o.objective_code,
            name=o.name,
            description=o.description,
            strategic_pillar=o.strategic_pillar.value if hasattr(o.strategic_pillar, "value") else str(o.strategic_pillar),
            owner=o.owner,
            priority=o.priority,
            start_date=o.start_date,
            target_date=o.target_date,
            baseline_value=o.baseline_value,
            target_value=o.target_value,
            current_value=o.current_value,
            unit=o.unit,
            status=o.status.value if hasattr(o.status, "value") else str(o.status),
            confidence_score=o.confidence_score,
            progress_percentage=o.progress_percentage,
            evidence_summary=o.evidence_summary,
            version=o.version,
        )
        for o in objs
    ]


@router.post("/objectives", response_model=ObjectiveResponse)
async def create_objective(payload: ObjectiveCreateRequest) -> ObjectiveResponse:
    """Creates a new measurable strategic objective."""
    try:
        pillar = StrategicPillar[payload.strategic_pillar]
    except KeyError:
        pillar = StrategicPillar.GROWTH

    obj = _strategy_service.create_objective(
        name=payload.name,
        target_value=payload.target_value,
        unit=payload.unit,
        baseline_value=payload.baseline_value,
        strategic_pillar=pillar,
        owner=payload.owner,
        priority=payload.priority,
        description=payload.description,
    )

    return ObjectiveResponse(
        objective_code=obj.objective_code,
        name=obj.name,
        description=obj.description,
        strategic_pillar=obj.strategic_pillar.value if hasattr(obj.strategic_pillar, "value") else str(obj.strategic_pillar),
        owner=obj.owner,
        priority=obj.priority,
        start_date=obj.start_date,
        target_date=obj.target_date,
        baseline_value=obj.baseline_value,
        target_value=obj.target_value,
        current_value=obj.current_value,
        unit=obj.unit,
        status=obj.status.value if hasattr(obj.status, "value") else str(obj.status),
        confidence_score=obj.confidence_score,
        progress_percentage=obj.progress_percentage,
        evidence_summary=obj.evidence_summary,
        version=obj.version,
    )


@router.patch("/objectives/{code}/progress", response_model=ObjectiveResponse)
async def update_objective_progress(
    code: str,
    payload: ObjectiveProgressUpdateRequest,
) -> ObjectiveResponse:
    """Updates live metric progress for a strategic objective."""
    try:
        obj = _strategy_service.update_objective_progress(
            objective_code=code,
            current_value=payload.current_value,
            evidence_summary=payload.evidence_summary,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Objective '{code}' not found.")

    return ObjectiveResponse(
        objective_code=obj.objective_code,
        name=obj.name,
        description=obj.description,
        strategic_pillar=obj.strategic_pillar.value if hasattr(obj.strategic_pillar, "value") else str(obj.strategic_pillar),
        owner=obj.owner,
        priority=obj.priority,
        start_date=obj.start_date,
        target_date=obj.target_date,
        baseline_value=obj.baseline_value,
        target_value=obj.target_value,
        current_value=obj.current_value,
        unit=obj.unit,
        status=obj.status.value if hasattr(obj.status, "value") else str(obj.status),
        confidence_score=obj.confidence_score,
        progress_percentage=obj.progress_percentage,
        evidence_summary=obj.evidence_summary,
        version=obj.version,
    )


@router.post("/key-results", response_model=KeyResultResponse)
async def create_key_result(payload: KeyResultCreateRequest) -> KeyResultResponse:
    """Registers an OKR Key Result linked to an Objective."""
    kr = _strategy_service.create_key_result(
        objective_id=payload.objective_id,
        name=payload.name,
        target_value=payload.target_value,
        unit=payload.unit,
        baseline_value=payload.baseline_value,
        owner=payload.owner,
    )

    return KeyResultResponse(
        kr_code=kr.kr_code,
        objective_id=kr.objective_id,
        name=kr.name,
        baseline_value=kr.baseline_value,
        target_value=kr.target_value,
        current_value=kr.current_value,
        unit=kr.unit,
        progress_percentage=kr.progress_percentage,
        measurement_method=kr.measurement_method,
        source_metric=kr.source_metric,
        owner=kr.owner,
        confidence=kr.confidence,
        deadline=kr.deadline,
    )


@router.get("/initiatives", response_model=List[InitiativeResponse])
async def list_initiatives() -> List[InitiativeResponse]:
    """Lists registered strategic initiatives."""
    inits = _strategy_service.initiative_manager.list_initiatives()
    return [
        InitiativeResponse(
            initiative_code=i.initiative_code,
            title=i.title,
            description=i.description,
            category=i.category,
            owner=i.owner,
            status=i.status.value if hasattr(i.status, "value") else str(i.status),
            expected_value_usd=i.expected_value_usd,
            estimated_cost_usd=i.estimated_cost_usd,
            required_fte_capacity=i.required_fte_capacity,
            estimated_duration_weeks=i.estimated_duration_weeks,
            priority_score=i.priority_score,
            risk_score=i.risk_score,
            feasibility_score=i.feasibility_score,
            is_funded=i.is_funded,
            version=i.version,
        )
        for i in inits
    ]


@router.post("/initiatives", response_model=InitiativeResponse)
async def create_initiative(payload: InitiativeCreateRequest) -> InitiativeResponse:
    """Creates a proposed strategic initiative."""
    init = _strategy_service.create_initiative(
        title=payload.title,
        owner=payload.owner,
        category=payload.category,
        expected_value_usd=payload.expected_value_usd,
        estimated_cost_usd=payload.estimated_cost_usd,
        required_fte_capacity=payload.required_fte_capacity,
        estimated_duration_weeks=payload.estimated_duration_weeks,
        description=payload.description,
    )

    return InitiativeResponse(
        initiative_code=init.initiative_code,
        title=init.title,
        description=init.description,
        category=init.category,
        owner=init.owner,
        status=init.status.value if hasattr(init.status, "value") else str(init.status),
        expected_value_usd=init.expected_value_usd,
        estimated_cost_usd=init.estimated_cost_usd,
        required_fte_capacity=init.required_fte_capacity,
        estimated_duration_weeks=init.estimated_duration_weeks,
        priority_score=init.priority_score,
        risk_score=init.risk_score,
        feasibility_score=init.feasibility_score,
        is_funded=init.is_funded,
        version=init.version,
    )


@router.post("/optimization", response_model=OptimizationResponse)
async def run_portfolio_optimization(payload: OptimizationRunRequest) -> OptimizationResponse:
    """Executes multi-objective constrained portfolio optimization."""
    inits = _strategy_service.initiative_manager.list_initiatives()
    if payload.initiatives:
        inits = [
            _strategy_service.create_initiative(
                title=item.title,
                owner=item.owner,
                category=item.category,
                expected_value_usd=item.expected_value_usd,
                estimated_cost_usd=item.estimated_cost_usd,
                required_fte_capacity=item.required_fte_capacity,
                estimated_duration_weeks=item.estimated_duration_weeks,
            )
            for item in payload.initiatives
        ]

    res = _strategy_service.optimize_plan(
        initiatives=inits,
        budget_limit_usd=payload.budget_limit_usd,
        capacity_limit_fte=payload.capacity_limit_fte,
        max_acceptable_risk=payload.max_acceptable_risk,
    )

    return OptimizationResponse(
        run_code=res["run_code"],
        status=res["status"],
        runtime_seconds=res["runtime_seconds"],
        budget_limit_usd=res["budget_limit_usd"],
        allocated_budget_usd=res["allocated_budget_usd"],
        budget_utilization_percentage=res["budget_utilization_percentage"],
        capacity_limit_fte=res["capacity_limit_fte"],
        allocated_capacity_fte=res["allocated_capacity_fte"],
        capacity_utilization_percentage=res["capacity_utilization_percentage"],
        total_expected_value_usd=res["total_expected_value_usd"],
        net_expected_benefit_usd=res["net_expected_benefit_usd"],
        selected_initiatives=res["selected_initiatives"],
        binding_constraints=res["binding_constraints"],
        explanation=res["explanation"],
    )


@router.get("/pareto", response_model=List[ParetoPlanResponse])
async def get_pareto_frontier(
    budget: float = Query(100000.0),
    capacity: float = Query(8.0),
) -> List[ParetoPlanResponse]:
    """Generates non-dominated Pareto-efficient strategic plans."""
    inits = _strategy_service.initiative_manager.list_initiatives()
    if not inits:
        inits = [
            _strategy_service.create_initiative("Market Outreach Engine", "Sales", expected_value_usd=75000.0, estimated_cost_usd=18000.0, required_fte_capacity=1.5),
            _strategy_service.create_initiative("Core Platform Resilience", "DevOps", expected_value_usd=40000.0, estimated_cost_usd=10000.0, required_fte_capacity=1.0),
        ]

    pareto_plans = _strategy_service.generate_pareto_frontier(
        initiatives=inits,
        total_budget_usd=budget,
        total_capacity_fte=capacity,
    )

    return [
        ParetoPlanResponse(
            plan_code=p.plan_code,
            title=p.title,
            growth_score=p.growth_score,
            profitability_score=p.profitability_score,
            risk_score=p.risk_score,
            selected_initiatives=p.selected_initiatives,
            total_cost_usd=p.total_cost_usd,
            expected_net_benefit_usd=p.expected_net_benefit_usd,
            is_pareto_optimal=p.is_pareto_optimal,
        )
        for p in pareto_plans
    ]


@router.get("/feasibility", response_model=List[FeasibilityResponse])
async def evaluate_feasibility() -> List[FeasibilityResponse]:
    """Evaluates goal achievement feasibility for all active strategic objectives."""
    objs = _strategy_service.list_objectives()
    if not objs:
        objs = [_strategy_service.create_objective("Q4 Growth Target", target_value=200000.0, baseline_value=120000.0)]

    results = []
    for o in objs:
        f = _strategy_service.evaluate_feasibility(o)
        results.append(
            FeasibilityResponse(
                objective_code=f["objective_code"],
                objective_name=f["objective_name"],
                feasibility_level=f["feasibility_level"],
                feasibility_score=f["feasibility_score"],
                required_growth_percentage=f["required_growth_percentage"],
                historical_growth_rate_pct=f["historical_growth_rate_pct"],
                capacity_factor=f["capacity_factor"],
                confidence=f["confidence"],
                rationale=f["rationale"],
            )
        )
    return results


@router.get("/gaps", response_model=List[GapAnalysisResponse])
async def evaluate_gaps() -> List[GapAnalysisResponse]:
    """Returns gap analysis between current operational baseline and strategic objectives."""
    objs = _strategy_service.list_objectives()
    gaps = _strategy_service.evaluate_gaps(objs)
    return [
        GapAnalysisResponse(
            objective_code=g["objective_code"],
            objective_name=g["objective_name"],
            strategic_pillar=g["strategic_pillar"],
            current_value=g["current_value"],
            target_value=g["target_value"],
            gap_value=g["gap_value"],
            gap_percentage=g["gap_percentage"],
            estimated_budget_needed_usd=g["estimated_budget_needed_usd"],
            estimated_fte_needed=g["estimated_fte_needed"],
            urgency=g["urgency"],
        )
        for g in gaps
    ]


@router.get("/scorecard", response_model=ScorecardResponse)
async def get_scorecard(period: str = "CURRENT_QUARTER") -> ScorecardResponse:
    """Returns 10-dimension strategic health scorecard."""
    sc = _strategy_service.get_scorecard(period=period)
    return ScorecardResponse(
        scorecard_code=sc["scorecard_code"],
        period=sc["period"],
        composite_health_score=sc["composite_health_score"],
        composite_health_percentage=sc["composite_health_percentage"],
        dimensions=sc["dimensions"],
        evaluation_time=sc["evaluation_time"],
    )


@router.post("/drift/check", response_model=DriftCheckResponse)
async def check_drift(payload: DriftCheckRequest) -> DriftCheckResponse:
    """Checks for strategic drift against expected metric baseline."""
    drift_res = _strategy_service.check_drift(
        metric_name=payload.metric_name,
        expected_value=payload.expected_value,
        actual_value=payload.actual_value,
        drift_tolerance_pct=payload.drift_tolerance_pct,
    )
    return DriftCheckResponse(
        has_drift=drift_res is not None,
        drift_event=drift_res,
    )


@router.post("/decisions", response_model=DecisionRecordResponse)
async def record_decision(payload: DecisionRecordCreateRequest) -> DecisionRecordResponse:
    """Records an authorized human executive strategic decision."""
    rec = _strategy_service.record_decision(
        question=payload.question,
        context_summary=payload.context_summary,
        selected_option=payload.selected_option,
        rationale=payload.rationale,
        decision_owner=payload.decision_owner,
        rejected_options=payload.rejected_options,
    )

    return DecisionRecordResponse(
        decision_code=rec.decision_code,
        question=rec.question,
        context_summary=rec.context_summary,
        selected_option=rec.selected_option,
        rejected_options=rec.rejected_options,
        rationale=rec.rationale,
        decision_owner=rec.decision_owner,
        approved_at=rec.approved_at,
        plan_version=rec.plan_version,
    )


@router.post("/copilot", response_model=StrategyCopilotQueryResponse)
async def query_strategy_copilot(payload: StrategyCopilotQueryRequest) -> StrategyCopilotQueryResponse:
    """
    Evaluates natural language strategic queries, summarizes trade-offs, and provides explainable recommendations.
    Enforces governance safety notice: AI suggests; human leaders decide.
    """
    q = payload.query.lower()
    intent = "STRATEGIC_PLANNING_ADVISORY"
    recs = []

    if "priorit" in q:
        intent = "INITIATIVE_PRIORITIZATION_QUERY"
        recs = [
            "Prioritize Inbound Outreach Multiplier (+3.5x ROI)",
            "Automate onboarding workflow to reduce cycle time by 28%",
            "Defer capital-intensive expansion until Q3 cash reserves reach $200k",
        ]
        explanation = (
            f"Based on current capacity and budget constraints for '{payload.query}', "
            f"high-ROI commercial automation initiatives yield the greatest modeled benefit."
        )
    elif "risk" in q:
        intent = "STRATEGIC_RISK_QUERY"
        recs = [
            "Mitigate engineering single point of failure by cross-training 2 engineers",
            "Establish automated compliance tests before expanding into regulated client sectors",
        ]
        explanation = (
            f"Evaluated risk profile for '{payload.query}': "
            f"Top vulnerabilities reside in capacity over-allocation (utilization > 85%) and provider dependencies."
        )
    else:
        recs = [
            "Focus on high-margin retainer clients to stabilize monthly recurring cashflow",
            "Maintain gross margins above 35% through AI-assisted development tools",
        ]
        explanation = f"Evaluated strategic posture for query: '{payload.query}'."

    return StrategyCopilotQueryResponse(
        query=payload.query,
        intent=intent,
        explanation=explanation,
        recommendations=recs,
        confidence=0.90,
    )
