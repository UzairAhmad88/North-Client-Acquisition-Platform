"""
Phase 59: FastAPI Router for Unified Marketing Platform
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from backend.app.services.marketing.service import MarketingPlatformService
from backend.app.schemas.marketing import (
    AudienceCreateRequest,
    PositioningCreateRequest,
    ContentAssetCreateRequest,
    ClaimRecordRequest,
    CampaignCreateRequest,
    LeadCaptureRequest,
    LeadScoreCalculateRequest,
    AttributionCalculateRequest,
    BudgetSimulationRequest,
    CopilotQueryRequest,
)

router = APIRouter(prefix="/marketing", tags=["Marketing Platform"])
service = MarketingPlatformService()


@router.get("/overview")
def get_overview():
    """Returns high-level marketing metrics summary."""
    return service.get_overview_metrics()


# Audiences & Positioning
@router.get("/audiences")
def list_audiences():
    return service.audiences.list_audiences()


@router.post("/audiences")
def create_audience(req: AudienceCreateRequest):
    return service.audiences.create_audience(
        name=req.name,
        description=req.description,
        target_icp=req.target_icp,
        industry=req.industry,
        company_size_tier=req.company_size_tier,
        buying_context=req.buying_context,
        primary_pain_points=req.primary_pain_points,
        channel_preferences=req.channel_preferences,
        total_market_size=req.total_market_size,
        reachable_market_size=req.reachable_market_size,
    )


@router.get("/positioning")
def list_positionings(audience_id: Optional[str] = Query(None)):
    return service.audiences.list_positionings(audience_id=audience_id)


@router.post("/positioning")
def create_positioning(req: PositioningCreateRequest):
    return service.audiences.create_positioning(
        audience_id=req.audience_id,
        target_customer=req.target_customer,
        problem_statement=req.problem_statement,
        alternative_solution=req.alternative_solution,
        our_solution=req.our_solution,
        key_differentiators=req.key_differentiators,
        value_statement=req.value_statement,
        proof_points=req.proof_points,
    )


@router.post("/positioning/{id}/approve")
def approve_positioning(id: str, approver: str = Query("Chief Marketing Officer")):
    try:
        return service.audiences.approve_positioning(positioning_id=id, approver=approver)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Content & Claims
@router.get("/content")
def list_content(stage: Optional[str] = Query(None)):
    return service.content.list_content_assets(journey_stage=stage)


@router.post("/content")
def create_content(req: ContentAssetCreateRequest):
    return service.content.create_content_asset(
        title=req.title,
        content_type=req.content_type,
        journey_stage=req.journey_stage,
        target_audience_id=req.target_audience_id,
        body_markdown=req.body_markdown,
        primary_cta=req.primary_cta,
    )


@router.get("/content/gaps")
def list_content_gaps():
    return service.content.list_content_gaps()


@router.get("/content/briefs")
def list_content_briefs():
    return service.content.list_content_briefs()


@router.post("/content/claims")
def record_claim(req: ClaimRecordRequest):
    return service.content.record_claim(
        asset_id=req.asset_id,
        claim_text=req.claim_text,
        source_reference=req.source_reference,
        source_date=req.source_date,
        confidence_pct=req.confidence_pct,
        verification_status=req.verification_status,
        reviewer_notes=req.reviewer_notes,
    )


# Campaigns & Channels
@router.get("/campaigns")
def list_campaigns(status: Optional[str] = Query(None)):
    return service.campaigns.list_campaigns(status=status)


@router.post("/campaigns")
def create_campaign(req: CampaignCreateRequest):
    return service.campaigns.create_campaign(
        name=req.name,
        campaign_type=req.campaign_type,
        target_audience_id=req.target_audience_id,
        allocated_budget_usd=req.allocated_budget_usd,
        channels=req.channels,
        owner=req.owner,
    )


@router.post("/campaigns/{id}/advance")
def advance_campaign_status(id: str, target_status: str = Query(...), approved_by: Optional[str] = Query(None)):
    try:
        return service.campaigns.advance_campaign_status(campaign_id=id, target_status=target_status, approved_by=approved_by)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/channels")
def list_channels():
    return service.campaigns.list_channels()


# Leads & Funnel
@router.get("/leads")
def list_leads(stage: Optional[str] = Query(None)):
    return service.leads.list_leads(qualification_stage=stage)


@router.post("/leads")
def capture_lead(req: LeadCaptureRequest):
    return service.leads.capture_lead(
        email=req.email,
        first_name=req.first_name,
        last_name=req.last_name,
        company_name=req.company_name,
        source_channel=req.source_channel,
        first_touch_campaign=req.first_touch_campaign,
    )


@router.post("/lead-scoring/calculate")
def calculate_lead_score(req: LeadScoreCalculateRequest):
    try:
        return service.leads.calculate_lead_score(
            lead_id=req.lead_id,
            company_size_tier=req.company_size_tier,
            industry_match=req.industry_match,
            budget_signal=req.budget_signal,
            page_views=req.page_views,
            content_downloads=req.content_downloads,
            webinar_attended=req.webinar_attended,
            pricing_page_visits=req.pricing_page_visits,
            demo_requested=req.demo_requested,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/funnel")
def get_funnel(period: str = Query("2026-Q3")):
    return service.leads.get_funnel_metrics(period=period)


# Attribution, ROI & Budgets
@router.post("/attribution")
def calculate_attribution(req: AttributionCalculateRequest):
    try:
        return service.attribution.calculate_attribution(
            opportunity_id=req.opportunity_id,
            deal_value_usd=req.deal_value_usd,
            touches=req.touches,
            attribution_model=req.attribution_model,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/roi")
def get_roi(period: str = Query("2026-Q3")):
    return service.attribution.get_marketing_roi(period=period)


@router.get("/budgets")
def get_budget(period: str = Query("2026-Q3")):
    return service.attribution.get_budget(period=period)


@router.post("/simulations")
def simulate_budget_optimization(req: BudgetSimulationRequest):
    return service.attribution.simulate_budget_optimization(
        current_budget_usd=req.current_budget_usd,
        budget_shift_pct=req.budget_shift_pct,
        target_focus_channel=req.target_focus_channel,
    )


# Forecasts, Risks & Fatigue
@router.get("/forecasts")
def list_forecasts():
    return service.forecast_risks.list_forecasts()


@router.get("/risks")
def list_risks():
    return service.forecast_risks.list_risks()


@router.get("/fatigue")
def list_fatigue():
    return service.forecast_risks.list_fatigue_records()


# Copilot
@router.post("/copilot")
def query_copilot(req: CopilotQueryRequest):
    return service.answer_copilot_query(query=req.query)
