"""
REST API Router for Phase 55 — Unified Product & Innovation Intelligence, Idea Discovery, Validation & R&D Platform.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.innovation import (
    InnovationWorkspaceCreateRequest,
    RecordProblemRequest,
    CreateOpportunityRequest,
    CreateIdeaRequest,
    FormHypothesisRequest,
    MapAssumptionRequest,
    DesignExperimentRequest,
    RecordExperimentResultRequest,
    CreateProductConceptRequest,
    CreateBusinessCaseRequest,
    ConductGateReviewRequest,
    InnovationCopilotRequest,
)
from backend.app.services.innovation.service import global_innovation_service
from backend.app.services.innovation.base import (
    InnovationStage,
    HorizonLevel,
    GateStage,
    GateDecision,
)

router = APIRouter(prefix="/innovation", tags=["Product & Innovation Intelligence"])


@router.get("/overview", summary="Get Innovation Platform Overview")
async def get_overview() -> Dict[str, Any]:
    data = global_innovation_service.get_overview()
    return {"status": "SUCCESS", "data": data}


@router.get("/workspaces", summary="List Innovation Workspaces")
async def list_workspaces(
    status: Optional[str] = Query(None),
    horizon: Optional[str] = Query(None),
) -> Dict[str, Any]:
    workspaces = global_innovation_service.workspaces.list_workspaces(status, horizon)
    return {"status": "SUCCESS", "count": len(workspaces), "data": workspaces}


@router.post("/workspaces", status_code=status.HTTP_201_CREATED, summary="Create Innovation Workspace")
async def create_workspace(req: InnovationWorkspaceCreateRequest) -> Dict[str, Any]:
    h = HorizonLevel(req.horizon) if req.horizon in HorizonLevel.__members__ else HorizonLevel.H1
    ws = global_innovation_service.workspaces.create_workspace(
        title=req.title,
        owner_id=req.owner_id,
        theme=req.theme,
        objective=req.objective,
        target_market=req.target_market,
        horizon=h,
    )
    return {"status": "SUCCESS", "data": ws}


@router.get("/workspaces/{id}", summary="Get Full Innovation Workspace Graph")
async def get_workspace(id: str) -> Dict[str, Any]:
    try:
        data = global_innovation_service.get_workspace_overview(id)
        return {"status": "SUCCESS", "data": data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/workspaces/{id}/problems", summary="Record Customer Problem")
async def record_problem(id: str, req: RecordProblemRequest) -> Dict[str, Any]:
    prob = global_innovation_service.problems_opportunities.record_problem(
        workspace_id=id,
        statement=req.statement,
        affected_users=req.affected_users,
        frequency=req.frequency,
        severity=req.severity,
        existing_solutions=req.existing_solutions,
        willingness_to_pay_signal=req.willingness_to_pay_signal,
        evidence_sources=req.evidence_sources,
    )
    return {"status": "SUCCESS", "data": prob}


@router.post("/workspaces/{id}/opportunities", summary="Create Opportunity from Problem")
async def create_opportunity(id: str, req: CreateOpportunityRequest) -> Dict[str, Any]:
    opp = global_innovation_service.problems_opportunities.create_opportunity_from_problem(
        workspace_id=id,
        title=req.title,
        description=req.description,
        market_potential=req.market_potential,
        revenue_potential_usd=req.revenue_potential_usd,
        competitive_intensity=req.competitive_intensity,
        technical_feasibility=req.technical_feasibility,
    )
    return {"status": "SUCCESS", "data": opp}


@router.post("/workspaces/{id}/ideas", summary="Create Innovation Idea")
async def create_idea(id: str, req: CreateIdeaRequest) -> Dict[str, Any]:
    idea = global_innovation_service.ideas.create_idea(
        workspace_id=id,
        title=req.title,
        description=req.description,
        origin_source=req.origin_source,
        problem_id=req.problem_id,
        opportunity_id=req.opportunity_id,
        target_users=req.target_users,
        proposed_value=req.proposed_value,
        scoring_factors=req.scoring_factors,
    )
    return {"status": "SUCCESS", "data": idea}


@router.post("/workspaces/{id}/hypotheses", summary="Form Innovation Hypothesis")
async def form_hypothesis(id: str, req: FormHypothesisRequest) -> Dict[str, Any]:
    hyp = global_innovation_service.hypotheses_assumptions.form_hypothesis(
        workspace_id=id,
        idea_id=req.idea_id,
        statement=req.statement,
        prediction=req.prediction,
        metric_name=req.metric_name,
        baseline_value=req.baseline_value,
        target_value=req.target_value,
        confidence=req.confidence,
    )
    return {"status": "SUCCESS", "data": hyp}


@router.post("/hypotheses/{id}/assumptions", summary="Map Assumption to Priority Grid")
async def map_assumption(id: str, req: MapAssumptionRequest) -> Dict[str, Any]:
    asm = global_innovation_service.hypotheses_assumptions.map_assumption(
        hypothesis_id=id,
        assumption_text=req.assumption_text,
        category=req.category,
        impact_level=req.impact_level,
        uncertainty_level=req.uncertainty_level,
    )
    return {"status": "SUCCESS", "data": asm}


@router.post("/workspaces/{id}/experiments", summary="Design Experiment")
async def design_experiment(id: str, req: DesignExperimentRequest) -> Dict[str, Any]:
    exp = global_innovation_service.experiments.design_experiment(
        workspace_id=id,
        hypothesis_id=req.hypothesis_id,
        title=req.title,
        sample_size=req.sample_size,
        duration_days=req.duration_days,
    )
    return {"status": "SUCCESS", "data": exp}


@router.post("/experiments/{id}/results", summary="Record Experiment Results and Statistical Test")
async def record_experiment_result(id: str, req: RecordExperimentResultRequest) -> Dict[str, Any]:
    res = global_innovation_service.experiments.record_experiment_result(
        experiment_id=id,
        control_values=req.control_values,
        treatment_values=req.treatment_values,
        limitations=req.limitations,
    )
    return {"status": "SUCCESS", "data": res}


@router.post("/workspaces/{id}/products", summary="Create Product Concept")
async def create_product_concept(id: str, req: CreateProductConceptRequest) -> Dict[str, Any]:
    pcon = global_innovation_service.concepts.create_product_concept(
        workspace_id=id,
        name=req.name,
        target_customer_persona=req.target_customer_persona,
        value_proposition=req.value_proposition,
        core_features=req.core_features,
        differentiators=req.differentiators,
        idea_id=req.idea_id,
    )
    return {"status": "SUCCESS", "data": pcon}


@router.post("/workspaces/{id}/business-cases", summary="Create Business Case")
async def create_business_case(id: str, req: CreateBusinessCaseRequest) -> Dict[str, Any]:
    bcase = global_innovation_service.concepts.create_business_case(
        workspace_id=id,
        concept_id=req.concept_id,
        target_tam_usd=req.target_tam_usd,
        projected_year1_revenue_usd=req.projected_year1_revenue_usd,
        estimated_development_cost_usd=req.estimated_development_cost_usd,
        estimated_cac_usd=req.estimated_cac_usd,
        estimated_ltv_usd=req.estimated_ltv_usd,
    )
    return {"status": "SUCCESS", "data": bcase}


@router.post("/workspaces/{id}/gates", summary="Conduct Stage-Gate Review")
async def conduct_gate_review(id: str, req: ConductGateReviewRequest) -> Dict[str, Any]:
    g = GateStage(req.gate_stage) if req.gate_stage in GateStage.__members__ else GateStage.GATE_1_PROBLEM
    d = GateDecision(req.decision) if req.decision in GateDecision.__members__ else GateDecision.PROCEED
    review = global_innovation_service.portfolios_gates.conduct_gate_review(
        workspace_id=id,
        gate_stage=g,
        reviewer_id=req.reviewer_id,
        evidence_completeness_score=req.evidence_completeness_score,
        decision=d,
        review_notes=req.review_notes,
    )
    return {"status": "SUCCESS", "data": review}


@router.post("/copilot", summary="Query Innovation Copilot")
async def query_copilot(req: InnovationCopilotRequest) -> Dict[str, Any]:
    try:
        data = global_innovation_service.ask_copilot(req.workspace_id, req.query)
        return {"status": "SUCCESS", "data": data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
