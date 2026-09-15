"""Phase 60: FastAPI Router for Unified Product Management & Product Intelligence OS."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

try:
    from backend.app.services.product_os.service import ProductOperatingSystemService
except ImportError:
    from app.services.product_os.service import ProductOperatingSystemService

from backend.app.schemas.product_os import (
    ProductCreateRequest,
    VisionCreateRequest,
    StrategyCreateRequest,
    ProblemCreateRequest,
    FeedbackItemCreateRequest,
    OpportunityCreateRequest,
    PrioritizationScoreRequest,
    RoadmapCreateRequest,
    RoadmapItemCreateRequest,
    RequirementCreateRequest,
    UserStoryCreateRequest,
    FeatureAdoptionTrackRequest,
    ProductHealthScoreRequest,
    LaunchPlanCreateRequest,
    FeatureFlagCreateRequest,
    SunsetPlanCreateRequest,
    UnitEconomicsCalculateRequest,
    ForecastGenerateRequest,
    TwinSimulationRequest,
    ProductRiskCreateRequest,
    ProductCopilotQueryRequest,
)

router = APIRouter(prefix="/product-os", tags=["Product Operating System"])
service = ProductOperatingSystemService()


@router.get("/overview")
def get_overview(tenant_id: str = Query("default_tenant")):
    """Returns executive overview metrics for the product operating system."""
    return service.get_overview_metrics(tenant_id)


# Portfolio & Strategy
@router.get("/portfolio")
def list_products(tenant_id: str = Query("default_tenant")):
    return [p for p in service.portfolio_service._products.values() if p.get("tenant_id") == tenant_id]


@router.post("/portfolio")
def create_product(req: ProductCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_service.create_product(
        tenant_id=tenant_id,
        name=req.name,
        product_line=req.product_line,
        code=req.code,
        lifecycle_state=req.lifecycle_state,
        target_icp=req.target_icp,
        owner_email=req.owner_email,
        description=req.description,
    )


@router.post("/vision")
def create_vision(req: VisionCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_service.create_product_vision(
        tenant_id=tenant_id,
        product_id=req.product_id,
        target_users=req.target_users,
        core_problem=req.core_problem,
        value_proposition=req.value_proposition,
        differentiation=req.differentiation,
        strategic_fit=req.strategic_fit,
        market_opportunity=req.market_opportunity,
    )


@router.post("/strategy")
def create_strategy(req: StrategyCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.portfolio_service.create_product_strategy(
        tenant_id=tenant_id,
        product_id=req.product_id,
        positioning=req.positioning,
        growth_strategy=req.growth_strategy,
        product_bets=req.product_bets,
        core_metrics=req.core_metrics,
        icp_definition=req.icp_definition,
    )


# Problems & Opportunities
@router.get("/problems")
def list_problems(tenant_id: str = Query("default_tenant")):
    return [p for p in service.problems_feedback_service._problems.values() if p.get("tenant_id") == tenant_id]


@router.post("/problems")
def create_problem(req: ProblemCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.problems_feedback_service.record_problem(
        tenant_id=tenant_id,
        product_id=req.product_id,
        title=req.title,
        reported_by_count=req.reported_by_count,
        severity=req.severity,
        validation_status=req.validation_status,
        context=req.context,
        cost_of_inaction_usd=req.cost_of_inaction_usd,
        evidence_sources=req.evidence_sources,
    )


@router.get("/opportunities")
def list_opportunities(tenant_id: str = Query("default_tenant")):
    return [o for o in service.problems_feedback_service._opportunities.values() if o.get("tenant_id") == tenant_id]


@router.post("/opportunities")
def create_opportunity(req: OpportunityCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.problems_feedback_service.create_opportunity(
        tenant_id=tenant_id,
        product_id=req.product_id,
        title=req.title,
        problem_id=req.problem_id,
        customer_value_score=req.customer_value_score,
        business_value_score=req.business_value_score,
        confidence_score=req.confidence_score,
        effort_score=req.effort_score,
        strategic_fit_score=req.strategic_fit_score,
        revenue_potential_usd=req.revenue_potential_usd,
    )


# Roadmaps & Prioritization
@router.get("/roadmaps")
def list_roadmaps(tenant_id: str = Query("default_tenant")):
    return service.prioritization_roadmap_service.get_roadmap_board(tenant_id)


@router.post("/roadmaps")
def create_roadmap(req: RoadmapCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.prioritization_roadmap_service.create_roadmap(
        tenant_id=tenant_id,
        product_id=req.product_id,
        title=req.title,
        horizon_type=req.horizon_type,
    )


@router.post("/roadmaps/items")
def add_roadmap_item(req: RoadmapItemCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.prioritization_roadmap_service.add_roadmap_item(
        tenant_id=tenant_id,
        roadmap_id=req.roadmap_id,
        title=req.title,
        horizon=req.horizon,
        opportunity_id=req.opportunity_id,
        target_quarter=req.target_quarter,
        engineering_effort_weeks=req.engineering_effort_weeks,
        dependencies=req.dependencies,
        confidence=req.confidence,
    )


@router.post("/prioritization/score")
def score_prioritization(req: PrioritizationScoreRequest, tenant_id: str = Query("default_tenant")):
    return service.prioritization_roadmap_service.score_prioritization(
        tenant_id=tenant_id,
        item_id=req.item_id,
        framework=req.framework,
        reach=req.reach,
        impact=req.impact,
        confidence=req.confidence,
        effort=req.effort,
        user_business_value=req.user_business_value,
        time_criticality=req.time_criticality,
        risk_reduction=req.risk_reduction,
    )


# Requirements & Traceability
@router.get("/requirements/traceability")
def get_traceability_matrix(tenant_id: str = Query("default_tenant")):
    return service.requirements_service.build_traceability_matrix(
        tenant_id=tenant_id,
        opportunity_service=service.problems_feedback_service,
        problem_service=service.problems_feedback_service,
        roadmap_service=service.prioritization_roadmap_service,
    )


@router.post("/requirements")
def create_requirement(req: RequirementCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.requirements_service.create_requirement(
        tenant_id=tenant_id,
        opportunity_id=req.opportunity_id,
        title=req.title,
        requirement_type=req.requirement_type,
        priority=req.priority,
        description=req.description,
        acceptance_criteria=req.acceptance_criteria,
        linked_initiative_id=req.linked_initiative_id,
    )


@router.post("/requirements/stories")
def add_user_story(req: UserStoryCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.requirements_service.add_user_story(
        tenant_id=tenant_id,
        requirement_id=req.requirement_id,
        role=req.role,
        capability=req.capability,
        benefit=req.benefit,
        given_when_then=req.given_when_then,
        story_points=req.story_points,
        technical_notes=req.technical_notes,
    )


# Analytics & Health
@router.post("/analytics/adoption")
def track_feature_adoption(req: FeatureAdoptionTrackRequest, tenant_id: str = Query("default_tenant")):
    return service.analytics_service.track_feature_adoption(
        tenant_id=tenant_id,
        product_id=req.product_id,
        feature_key=req.feature_key,
        feature_name=req.feature_name,
        eligible_users=req.eligible_users,
        activated_users=req.activated_users,
        weekly_active_users=req.weekly_active_users,
        retention_rate_30d=req.retention_rate_30d,
        customer_satisfaction_score=req.customer_satisfaction_score,
        efficiency_gain_pct=req.efficiency_gain_pct,
        revenue_influenced_usd=req.revenue_influenced_usd,
    )


@router.get("/health")
def list_health_scorecards(tenant_id: str = Query("default_tenant")):
    return [h for h in service.analytics_service._health_scorecards.values() if h.get("tenant_id") == tenant_id]


@router.post("/health/calculate")
def calculate_product_health(req: ProductHealthScoreRequest, tenant_id: str = Query("default_tenant")):
    return service.analytics_service.calculate_product_health(
        tenant_id=tenant_id,
        product_id=req.product_id,
        product_name=req.product_name,
        adoption_score=req.adoption_score,
        retention_score=req.retention_score,
        reliability_score=req.reliability_score,
        feedback_sentiment_score=req.feedback_sentiment_score,
        support_efficiency_score=req.support_efficiency_score,
        quality_defect_score=req.quality_defect_score,
        gross_margin_score=req.gross_margin_score,
    )


# Launches & Feature Flags
@router.post("/launches")
def create_launch_plan(req: LaunchPlanCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.launches_service.create_launch_plan(
        tenant_id=tenant_id,
        product_id=req.product_id,
        release_name=req.release_name,
        target_release_date=req.target_release_date,
        strategy=req.strategy,
        audience_segment=req.audience_segment,
        checklists=req.checklists,
        rollback_plan=req.rollback_plan,
    )


@router.post("/feature-flags")
def register_feature_flag(req: FeatureFlagCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.launches_service.register_feature_flag(
        tenant_id=tenant_id,
        flag_key=req.flag_key,
        name=req.name,
        environment=req.environment,
        is_enabled=req.is_enabled,
        rollout_percentage=req.rollout_percentage,
        targeting_rules=req.targeting_rules,
        owner_email=req.owner_email,
    )


@router.post("/sunset")
def initiate_sunset(req: SunsetPlanCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.launches_service.initiate_sunset_workflow(
        tenant_id=tenant_id,
        product_id=req.product_id,
        product_name=req.product_name,
        reason=req.reason,
        active_customer_count=req.active_customer_count,
        revenue_impact_usd=req.revenue_impact_usd,
        alternative_product_id=req.alternative_product_id,
        target_sunset_date=req.target_sunset_date,
        governance_approver=req.governance_approver,
    )


# Economics, Forecast & Simulations
@router.post("/economics/unit")
def calculate_unit_economics(req: UnitEconomicsCalculateRequest, tenant_id: str = Query("default_tenant")):
    return service.economics_service.calculate_unit_economics(
        tenant_id=tenant_id,
        product_id=req.product_id,
        active_customers=req.active_customers,
        mrr_usd=req.mrr_usd,
        infrastructure_cost_usd=req.infrastructure_cost_usd,
        support_cost_usd=req.support_cost_usd,
        r_and_d_allocated_usd=req.r_and_d_allocated_usd,
        cac_usd=req.cac_usd,
        churn_rate_monthly=req.churn_rate_monthly,
    )


@router.post("/forecasts/probabilistic")
def generate_forecast(req: ForecastGenerateRequest, tenant_id: str = Query("default_tenant")):
    return service.economics_service.generate_probabilistic_forecast(
        tenant_id=tenant_id,
        product_id=req.product_id,
        metric_name=req.metric_name,
        time_horizon_months=req.time_horizon_months,
        baseline_value=req.baseline_value,
        growth_rate_base=req.growth_rate_base,
    )


@router.post("/simulations/twin")
def run_twin_simulation(req: TwinSimulationRequest, tenant_id: str = Query("default_tenant")):
    return service.economics_service.run_twin_scenario_simulation(
        tenant_id=tenant_id,
        product_id=req.product_id,
        scenario_type=req.scenario_type,
        parameters=req.parameters,
    )


@router.post("/risks")
def log_product_risk(req: ProductRiskCreateRequest, tenant_id: str = Query("default_tenant")):
    return service.economics_service.log_product_risk(
        tenant_id=tenant_id,
        product_id=req.product_id,
        category=req.category,
        title=req.title,
        probability=req.probability,
        impact_score=req.impact_score,
        severity=req.severity,
        mitigation_strategy=req.mitigation_strategy,
        owner=req.owner,
    )


# Copilot
@router.post("/copilot/query")
def query_copilot(req: ProductCopilotQueryRequest):
    return service.query_product_copilot(tenant_id=req.tenant_id or "default_tenant", query=req.query)
