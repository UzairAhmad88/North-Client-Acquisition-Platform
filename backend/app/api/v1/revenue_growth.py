"""FastAPI Router for Phase 58: Unified Revenue Growth, Go-to-Market Intelligence & Optimization Platform."""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.revenue_growth import (
    ActivityLogRequest,
    CapacityPlanCreateRequest,
    DealRiskRecordRequest,
    DiscountApprovalRequest,
    DiscountSubmitRequest,
    ForecastGenerateRequest,
    GtmStrategyCreateRequest,
    IcpCreateRequest,
    NextBestActionRequest,
    OpportunityCreateRequest,
    PricingTierSetRequest,
    RevenueCopilotQueryRequest,
    RevenueSimulationRequest,
    RevenueTargetCreateRequest,
    SegmentCreateRequest,
    StageAdvanceRequest,
    TargetAccountCreateRequest,
    TargetAccountScoreRequest,
)
from backend.app.services.revenue_growth.service import RevenueGrowthPlatformService

router = APIRouter(prefix="/revenue", tags=["Revenue Growth & Commercial Optimization"])

# Global singleton service for in-process state consistency
_service = RevenueGrowthPlatformService()


@router.get("/overview")
async def get_overview():
    """Retrieve top-level revenue operating metrics."""
    return _service.get_overview_metrics()


# --- GTM, Segments, ICP & Targeting ---
@router.post("/gtm", status_code=status.HTTP_201_CREATED)
async def create_gtm_strategy(req: GtmStrategyCreateRequest):
    """Create a new GTM strategy."""
    return _service.gtm.create_gtm_strategy(
        name=req.name,
        target_market=req.target_market,
        sales_motion=req.sales_motion,
        positioning=req.positioning,
        value_proposition=req.value_proposition,
        channels=req.channels,
        metrics_targets=req.metrics_targets,
    )


@router.get("/gtm")
async def list_gtm_strategies():
    """List active GTM strategies."""
    return _service.gtm.list_gtm_strategies()


@router.post("/segments", status_code=status.HTTP_201_CREATED)
async def create_segment(req: SegmentCreateRequest):
    """Create market segment."""
    return _service.gtm.create_segment(
        name=req.name,
        industry=req.industry,
        company_size_tier=req.company_size_tier,
        estimated_tam_usd=req.estimated_tam_usd,
        estimated_sam_usd=req.estimated_sam_usd,
        priority_tier=req.priority_tier,
        description=req.description,
        strategy_id=req.strategy_id,
    )


@router.get("/segments")
async def list_segments():
    """List market segments."""
    return _service.gtm.list_segments()


@router.post("/icp", status_code=status.HTTP_201_CREATED)
async def create_icp(req: IcpCreateRequest):
    """Define ICP criteria."""
    return _service.gtm.create_icp(
        name=req.name,
        target_industries=req.target_industries,
        min_employee_count=req.min_employee_count,
        max_employee_count=req.max_employee_count,
        min_arr_usd=req.min_arr_usd,
        required_tech_profile=req.required_tech_profile,
        pain_points=req.pain_points,
        buying_signals=req.buying_signals,
        exclusions=req.exclusions,
        segment_id=req.segment_id,
    )


@router.get("/icp")
async def list_icps():
    """List ICP criteria profiles."""
    return _service.gtm.list_icps()


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_target_account(req: TargetAccountCreateRequest):
    """Create target enterprise account."""
    return _service.gtm.create_target_account(
        company_name=req.company_name,
        domain=req.domain,
        industry=req.industry,
        employee_count=req.employee_count,
        estimated_annual_revenue=req.estimated_annual_revenue,
        country=req.country,
        priority_level=req.priority_level,
        assigned_rep=req.assigned_rep,
    )


@router.get("/accounts")
async def list_target_accounts():
    """List target accounts."""
    return _service.gtm.list_target_accounts()


@router.post("/targeting/score", status_code=status.HTTP_201_CREATED)
async def score_account(req: TargetAccountScoreRequest):
    """Score target account against ICP fit."""
    return _service.gtm.score_target_account(
        account_id=req.account_id,
        icp_fit=req.icp_fit,
        business_need=req.business_need,
        digital_gap=req.digital_gap,
        revenue_potential=req.revenue_potential,
        buying_signal=req.buying_signal,
    )


@router.get("/targeting")
async def list_targeting_scores(account_id: Optional[str] = Query(None)):
    """List target account scores."""
    return _service.gtm.list_account_scores(account_id)


@router.get("/coverage")
async def get_market_coverage():
    """Get market coverage telemetry."""
    return _service.gtm.get_market_coverage()


@router.get("/territories")
async def list_territories():
    """List territory definitions."""
    return _service.gtm.list_territories()


# --- Pipelines & Opportunities ---
@router.get("/pipelines")
async def list_pipelines():
    """List sales pipelines."""
    return _service.pipeline.list_pipelines()


@router.post("/opportunities", status_code=status.HTTP_201_CREATED)
async def create_opportunity(req: OpportunityCreateRequest):
    """Create deal opportunity."""
    return _service.pipeline.create_opportunity(
        account_id=req.account_id,
        title=req.title,
        estimated_arr_value=req.estimated_arr_value,
        stage=req.stage,
        win_probability=req.win_probability,
        owner_name=req.owner_name,
        sales_motion=req.sales_motion,
        primary_need=req.primary_need,
        pipeline_id=req.pipeline_id,
    )


@router.get("/opportunities")
async def list_opportunities(stage: Optional[str] = Query(None)):
    """List sales opportunities."""
    return _service.pipeline.list_opportunities(stage)


@router.get("/opportunities/{id}")
async def get_opportunity(id: str):
    """Get opportunity details."""
    opp = _service.pipeline.get_opportunity(id)
    if not opp:
        raise HTTPException(status_code=404, detail=f"Opportunity {id} not found")
    return opp


@router.post("/opportunities/{id}/advance")
async def advance_opportunity_stage(id: str, req: StageAdvanceRequest):
    """Advance opportunity to next pipeline stage."""
    opp = _service.pipeline.advance_stage(id, req.next_stage)
    if not opp:
        raise HTTPException(status_code=404, detail=f"Opportunity {id} not found")
    return opp


@router.get("/opportunities/{id}/health")
async def get_opportunity_health(id: str):
    """Get health indicators for opportunity."""
    h = _service.pipeline.get_opportunity_health(id)
    if not h:
        return _service.pipeline.evaluate_opportunity_health(id)
    return h


@router.get("/opportunities/{id}/risks")
async def list_opportunity_risks(id: str):
    """List deal risks for specific opportunity."""
    return _service.pricing.list_deal_risks(opportunity_id=id)


@router.post("/activities", status_code=status.HTTP_201_CREATED)
async def log_activity(req: ActivityLogRequest):
    """Log sales activity."""
    return _service.pipeline.log_activity(
        activity_type=req.activity_type,
        summary=req.summary,
        opportunity_id=req.opportunity_id,
        outcome=req.outcome,
        actor_name=req.actor_name,
    )


@router.get("/activities")
async def list_activities(opportunity_id: Optional[str] = Query(None)):
    """List sales activities."""
    return _service.pipeline.list_activities(opportunity_id)


# --- Forecasts, Targets & Capacity ---
@router.post("/forecasts", status_code=status.HTTP_201_CREATED)
async def generate_forecast(req: ForecastGenerateRequest):
    """Generate probabilistic revenue forecast."""
    return _service.forecasting.generate_forecast(
        forecast_period=req.forecast_period,
        scenario=req.scenario,
        pipeline_total_usd=req.pipeline_total_usd,
        weighted_pipeline_usd=req.weighted_pipeline_usd,
        assumptions=req.assumptions,
    )


@router.get("/forecasts")
async def list_forecasts():
    """List generated forecasts."""
    return _service.forecasting.list_forecasts()


@router.get("/forecasts/scenarios")
async def get_forecast_scenarios(period: str = Query("Q4-2026")):
    """Get multi-scenario forecast comparisons."""
    return _service.forecasting.get_forecast_scenarios(forecast_period=period)


@router.get("/forecasts/calibration")
async def get_forecast_calibration():
    """Get historical forecast calibration and bias telemetry."""
    return _service.forecasting.get_forecast_calibration()


@router.post("/targets", status_code=status.HTTP_201_CREATED)
async def create_revenue_target(req: RevenueTargetCreateRequest):
    """Create revenue target."""
    return _service.forecasting.create_revenue_target(
        period=req.period,
        target_amount_usd=req.target_amount_usd,
        actual_amount_usd=req.actual_amount_usd,
        target_type=req.target_type,
    )


@router.get("/targets")
async def list_revenue_targets():
    """List revenue targets."""
    return _service.forecasting.list_revenue_targets()


@router.post("/capacity", status_code=status.HTTP_201_CREATED)
async def create_capacity_plan(req: CapacityPlanCreateRequest):
    """Create sales capacity plan."""
    return _service.forecasting.create_capacity_plan(
        period=req.period,
        rep_count=req.rep_count,
        quota_per_rep_usd=req.quota_per_rep_usd,
        ramp_factor=req.ramp_factor,
    )


@router.get("/capacity")
async def list_capacity_plans():
    """List sales capacity plans."""
    return _service.forecasting.list_capacity_plans()


# --- Pricing, Discounts, Deal Risk & Next Best Action ---
@router.post("/pricing", status_code=status.HTTP_201_CREATED)
async def set_pricing_tier(req: PricingTierSetRequest):
    """Set pricing tier configuration."""
    return _service.pricing.set_pricing_tier(
        product_or_service=req.product_or_service,
        tier_name=req.tier_name,
        list_price_usd=req.list_price_usd,
        billing_frequency=req.billing_frequency,
        average_discount_pct=req.average_discount_pct,
        target_gross_margin_pct=req.target_gross_margin_pct,
        willingness_to_pay_evidence=req.willingness_to_pay_evidence,
    )


@router.get("/pricing")
async def list_pricing_tiers():
    """List pricing tiers."""
    return _service.pricing.list_pricing_tiers()


@router.post("/discounts", status_code=status.HTTP_201_CREATED)
async def request_discount(req: DiscountSubmitRequest):
    """Submit discount approval request."""
    return _service.pricing.request_discount(
        opportunity_id=req.opportunity_id,
        requested_discount_pct=req.requested_discount_pct,
        original_price_usd=req.original_price_usd,
        justification=req.justification,
    )


@router.post("/discounts/{id}/approve")
async def approve_discount(id: str, req: DiscountApprovalRequest):
    """Approve discount request with human authorization."""
    d = _service.pricing.approve_discount(id, req.approver_name, req.approval_notes)
    if not d:
        raise HTTPException(status_code=404, detail=f"Discount request {id} not found")
    return d


@router.get("/discounts")
async def list_discounts(opportunity_id: Optional[str] = Query(None)):
    """List discount requests."""
    return _service.pricing.list_discount_requests(opportunity_id)


@router.get("/negotiation")
async def get_negotiation_insights(opportunity_id: str = Query("opp-demo-001")):
    """Get negotiation intelligence and trade-off recommendations."""
    return _service.pricing.get_negotiation_insights(opportunity_id=opportunity_id)


@router.post("/next-best-action", status_code=status.HTTP_201_CREATED)
async def recommend_next_best_action(req: NextBestActionRequest):
    """Recommend next best sales action."""
    return _service.pricing.recommend_next_best_action(
        opportunity_id=req.opportunity_id,
        recommended_action=req.recommended_action,
        action_type=req.action_type,
        rationale=req.rationale,
        confidence=req.confidence,
    )


@router.get("/next-best-action")
async def list_next_best_actions(opportunity_id: Optional[str] = Query(None)):
    """List recommended next actions."""
    return _service.pricing.list_next_best_actions(opportunity_id)


@router.get("/routing")
async def list_lead_routing_rules():
    """List lead routing rules."""
    return _service.pricing.list_routing_rules()


# --- Channels, Attribution, Economics & Waterfall ---
@router.get("/channels")
async def list_channels():
    """List acquisition channels and conversion rates."""
    return _service.economics.list_channels()


@router.get("/attribution")
async def list_attributions(opportunity_id: Optional[str] = Query(None)):
    """List touchpoint attribution records."""
    return _service.economics.list_attributions(opportunity_id)


@router.get("/economics")
async def get_unit_economics(period: str = Query("Q3-2026")):
    """Get CAC, LTV, and payback economics."""
    return _service.economics.get_unit_economics(period=period)


@router.get("/waterfall")
async def list_revenue_waterfalls():
    """Get ARR waterfalls and net retention."""
    return _service.economics.list_waterfalls()


@router.get("/pipeline-quality")
async def get_pipeline_quality():
    """Get sales pipeline hygiene audit metrics."""
    return _service.economics.evaluate_pipeline_hygiene()


# --- Risk, Growth Opportunities, Partners & Simulations ---
@router.get("/concentration")
async def get_concentration_risk():
    """Get customer and industry revenue concentration analysis."""
    return _service.risk_growth.evaluate_concentration_risk()


@router.get("/risks")
async def list_revenue_risks():
    """List active revenue risks."""
    return _service.risk_growth.list_revenue_risks()


@router.get("/growth-opportunities")
async def list_growth_opportunities():
    """List high-leverage revenue growth opportunities."""
    return _service.risk_growth.list_growth_opportunities()


@router.get("/partners")
async def list_partners():
    """List partner profiles and performance."""
    return _service.risk_growth.list_partners()


@router.get("/decisions")
async def list_commercial_decisions():
    """List Decision Room commercial links."""
    return _service.risk_growth.list_commercial_decisions()


@router.post("/simulations")
async def simulate_revenue_outcomes(req: RevenueSimulationRequest):
    """Simulate revenue outcomes under adjusted conversion and volume levers."""
    return _service.risk_growth.simulate_revenue(
        conversion_rate_delta_pct=req.conversion_rate_delta_pct,
        lead_volume_delta_pct=req.lead_volume_delta_pct,
        average_deal_size_delta_pct=req.average_deal_size_delta_pct,
    )


@router.get("/metrics")
async def get_gtm_metrics():
    """Get comprehensive GTM and sales velocity metrics."""
    return {
        "velocity": _service.pipeline.get_sales_velocity(),
        "hygiene": _service.economics.evaluate_pipeline_hygiene(),
        "economics": _service.economics.get_unit_economics(),
    }


# --- Revenue Copilot ---
@router.post("/copilot")
async def ask_revenue_copilot(req: RevenueCopilotQueryRequest):
    """Query Revenue Intelligence Copilot with natural language."""
    return _service.answer_copilot_query(query=req.query)
