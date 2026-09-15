"""
REST API Router for Phase 54 — Unified Autonomous Research, Intelligence & Continuous Discovery Engine.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.research_intelligence import (
    ResearchWorkspaceCreateRequest,
    DecomposeQuestionRequest,
    RegisterSourceRequest,
    ExtractFactRequest,
    VerifyClaimRequest,
    SurfaceConflictRequest,
    UpsertCompetitorRequest,
    CreateMonitoringRuleRequest,
    GenerateSynthesisRequest,
    GenerateReportRequest,
    CopilotQueryRequest,
)
from backend.app.services.research_intelligence.service import global_research_intelligence_service
from backend.app.services.research_intelligence.base import (
    ResearchType,
    SourceTrustLevel,
    SignificanceLevel,
)

router = APIRouter(prefix="/research-intelligence", tags=["Research Intelligence & Continuous Discovery"])


@router.get("/workspaces", summary="List Research Workspaces")
async def list_workspaces(
    status: Optional[str] = Query(None),
    research_type: Optional[str] = Query(None),
) -> Dict[str, Any]:
    workspaces = global_research_intelligence_service.workspaces.list_workspaces(status, research_type)
    return {"status": "SUCCESS", "count": len(workspaces), "data": workspaces}


@router.post("/workspaces", status_code=status.HTTP_201_CREATED, summary="Create Research Workspace")
async def create_workspace(req: ResearchWorkspaceCreateRequest) -> Dict[str, Any]:
    rtype = ResearchType(req.research_type) if req.research_type in ResearchType.__members__ else ResearchType.MARKET
    ws = global_research_intelligence_service.workspaces.create_workspace(
        title=req.title,
        research_question=req.research_question,
        owner_id=req.owner_id,
        research_type=rtype,
        objective=req.objective,
        scope=req.scope,
    )
    return {"status": "SUCCESS", "data": ws}


@router.get("/workspaces/{id}", summary="Get Full Research Workspace Overview")
async def get_workspace_overview(id: str) -> Dict[str, Any]:
    try:
        data = global_research_intelligence_service.get_workspace_overview(id)
        return {"status": "SUCCESS", "data": data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/workspaces/{id}/decompose", summary="Decompose Research Question into Subtasks")
async def decompose_question(id: str, req: DecomposeQuestionRequest) -> Dict[str, Any]:
    try:
        tasks = global_research_intelligence_service.workspaces.decompose_question(id, req.subquestions)
        return {"status": "SUCCESS", "count": len(tasks), "data": tasks}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/workspaces/{id}/sources", summary="Register and Validate Research Source")
async def register_source(id: str, req: RegisterSourceRequest) -> Dict[str, Any]:
    try:
        stype = SourceTrustLevel(req.source_type) if req.source_type in SourceTrustLevel.__members__ else SourceTrustLevel.SECONDARY
        source = global_research_intelligence_service.sources.register_source(
            workspace_id=id,
            url_or_reference=req.url_or_reference,
            source_type=stype,
            publisher=req.publisher,
            author=req.author,
            authority_score=req.authority_score,
            freshness=req.freshness,
        )
        return {"status": "SUCCESS", "data": source}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/workspaces/{id}/facts", summary="Extract Atomic Fact")
async def extract_fact(id: str, req: ExtractFactRequest) -> Dict[str, Any]:
    fact = global_research_intelligence_service.extraction.extract_fact(
        workspace_id=id,
        claim=req.claim,
        source_id=req.source_id,
        value_extracted=req.value_extracted,
        confidence=req.confidence,
        provenance=req.provenance,
    )
    return {"status": "SUCCESS", "data": fact}


@router.post("/workspaces/{id}/claims/verify", summary="Verify Claim with Corroboration Engine")
async def verify_claim(id: str, req: VerifyClaimRequest) -> Dict[str, Any]:
    claim = global_research_intelligence_service.extraction.verify_claim(
        workspace_id=id,
        claim_text=req.claim_text,
        supporting_sources=req.supporting_sources,
        contradicting_sources=req.contradicting_sources,
    )
    return {"status": "SUCCESS", "data": claim}


@router.post("/workspaces/{id}/conflicts", summary="Surface Detected Contradiction")
async def surface_conflict(id: str, req: SurfaceConflictRequest) -> Dict[str, Any]:
    conf = global_research_intelligence_service.extraction.surface_conflict(
        workspace_id=id,
        topic=req.topic,
        source_a_id=req.source_a_id,
        claim_a=req.claim_a,
        source_b_id=req.source_b_id,
        claim_b=req.claim_b,
        possible_explanation=req.possible_explanation,
    )
    return {"status": "SUCCESS", "data": conf}


@router.get("/competitive/profiles", summary="List Competitive Intelligence Profiles")
async def list_competitors() -> Dict[str, Any]:
    comps = global_research_intelligence_service.domains.list_competitors()
    return {"status": "SUCCESS", "count": len(comps), "data": comps}


@router.post("/competitive/profiles", summary="Upsert Competitive Profile")
async def upsert_competitor(req: UpsertCompetitorRequest) -> Dict[str, Any]:
    comp = global_research_intelligence_service.domains.upsert_competitor_profile(
        company_name=req.company_name,
        market_position=req.market_position,
        products_offered=req.products_offered,
        pricing_signals=req.pricing_signals,
        strengths=req.strengths,
        weaknesses=req.weaknesses,
        recent_changes=req.recent_changes,
    )
    return {"status": "SUCCESS", "data": comp}


@router.post("/workspaces/{id}/monitoring-rules", summary="Create Continuous Monitoring Rule")
async def create_monitoring_rule(id: str, req: CreateMonitoringRuleRequest) -> Dict[str, Any]:
    sig = SignificanceLevel(req.alert_significance_threshold) if req.alert_significance_threshold in SignificanceLevel.__members__ else SignificanceLevel.MEDIUM
    rule = global_research_intelligence_service.monitoring.create_monitoring_rule(
        workspace_id=id,
        target_entity=req.target_entity,
        watch_frequency=req.watch_frequency,
        topics_monitored=req.topics_monitored,
        alert_significance_threshold=sig,
    )
    return {"status": "SUCCESS", "data": rule}


@router.get("/monitoring/events", summary="List Intelligence Events")
async def list_intelligence_events(
    significance: Optional[str] = Query(None),
    target_entity: Optional[str] = Query(None),
) -> Dict[str, Any]:
    events = global_research_intelligence_service.monitoring.list_events(significance, target_entity)
    return {"status": "SUCCESS", "count": len(events), "data": events}


@router.post("/workspaces/{id}/syntheses", summary="Generate Intelligence Synthesis")
async def generate_synthesis(id: str, req: GenerateSynthesisRequest) -> Dict[str, Any]:
    synth = global_research_intelligence_service.synthesis.generate_synthesis(
        workspace_id=id,
        executive_summary=req.executive_summary,
        key_findings=req.key_findings,
        strategic_implications=req.strategic_implications,
        recommended_actions=req.recommended_actions,
        uncertainties_and_limitations=req.uncertainties_and_limitations,
    )
    return {"status": "SUCCESS", "data": synth}


@router.post("/workspaces/{id}/reports", summary="Generate Structured Research Report")
async def generate_report(id: str, req: GenerateReportRequest) -> Dict[str, Any]:
    rep = global_research_intelligence_service.synthesis.generate_report(
        workspace_id=id,
        title=req.title,
        report_markdown=req.report_markdown,
        citations=req.citations,
        confidence_rating=req.confidence_rating,
    )
    return {"status": "SUCCESS", "data": rep}


@router.post("/copilot/query", summary="Query Research Copilot")
async def query_research_copilot(req: CopilotQueryRequest) -> Dict[str, Any]:
    try:
        res = global_research_intelligence_service.ask_copilot(req.workspace_id, req.query)
        return {"status": "SUCCESS", "data": res}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
