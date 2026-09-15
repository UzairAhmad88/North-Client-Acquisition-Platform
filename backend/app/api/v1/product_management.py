"""
REST API Router for Phase 56 — Unified Product Lifecycle, Product Management & Continuous Delivery Intelligence Platform.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.product_management import (
    ProductCreateRequest,
    LifecycleTransitionRequest,
    VisionSetRequest,
    ObjectiveCreateRequest,
    MetricRegisterRequest,
    FeedbackIngestRequest,
    RequirementCreateRequest,
    EpicCreateRequest,
    FeatureCreateRequest,
    BacklogItemCreateRequest,
    PrioritizationScoreRequest,
    RoadmapCreateRequest,
    RoadmapItemAddRequest,
    SprintCreateRequest,
    ReleaseCreateRequest,
    ReleaseReadinessEvaluateRequest,
    FeatureFlagCreateRequest,
    LaunchChecklistUpdateRequest,
    ExperimentCreateRequest,
    HealthSnapshotRequest,
    SunsetPlanCreateRequest,
    ProductCopilotRequest,
)
from backend.app.services.product_management.service import global_product_management_service

router = APIRouter(prefix="/products", tags=["Product Management & Lifecycle Platform"])


@router.get("/portfolio", summary="Get Portfolio Overview")
async def get_portfolio() -> Dict[str, Any]:
    portfolio = global_product_management_service.get_portfolio_overview()
    return {"status": "SUCCESS", "data": portfolio}


@router.get("", summary="List All Products")
async def list_products(
    stage: Optional[str] = Query(None),
    product_type: Optional[str] = Query(None),
) -> Dict[str, Any]:
    products = global_product_management_service.products.list_products(stage=stage, product_type=product_type)
    return {"status": "SUCCESS", "count": len(products), "data": products}


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create New Product")
async def create_product(req: ProductCreateRequest) -> Dict[str, Any]:
    prod = global_product_management_service.products.create_product(
        name=req.name,
        type=req.type,
        description=req.description,
        target_market=req.target_market,
        owner=req.owner,
        team=req.team,
        workspace_id=req.workspace_id,
    )
    return {"status": "SUCCESS", "data": prod}


@router.get("/{id}", summary="Get Full Product Details & Subsystems")
async def get_product(id: str) -> Dict[str, Any]:
    try:
        data = global_product_management_service.get_product_dashboard(id)
        return {"status": "SUCCESS", "data": data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/lifecycle", summary="Transition Product Lifecycle Stage")
async def transition_lifecycle(id: str, req: LifecycleTransitionRequest) -> Dict[str, Any]:
    try:
        updated = global_product_management_service.products.transition_lifecycle_stage(
            product_id=id,
            new_stage=req.new_stage,
            actor=req.actor,
            rationale=req.rationale,
        )
        return {"status": "SUCCESS", "data": updated}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/vision", summary="Define Product Vision & Strategy")
async def set_vision(id: str, req: VisionSetRequest) -> Dict[str, Any]:
    vision = global_product_management_service.vision_strategy.set_product_vision(
        product_id=id,
        target_customer=req.target_customer,
        problem_statement=req.problem_statement,
        desired_future_state=req.desired_future_state,
        value_proposition=req.value_proposition,
        differentiation=req.differentiation,
        strategic_alignment=req.strategic_alignment,
        success_definition=req.success_definition,
    )
    return {"status": "SUCCESS", "data": vision}


@router.get("/{id}/objectives", summary="List Product Objectives & OKRs")
async def list_objectives(id: str) -> Dict[str, Any]:
    objs = global_product_management_service.vision_strategy.list_objectives(id)
    return {"status": "SUCCESS", "count": len(objs), "data": objs}


@router.post("/{id}/objectives", status_code=status.HTTP_201_CREATED, summary="Create Product Objective")
async def create_objective(id: str, req: ObjectiveCreateRequest) -> Dict[str, Any]:
    obj = global_product_management_service.vision_strategy.create_objective(
        product_id=id,
        name=req.name,
        metric=req.metric,
        baseline=req.baseline,
        target=req.target,
        time_window=req.time_window,
        owner=req.owner,
        confidence=req.confidence,
    )
    return {"status": "SUCCESS", "data": obj}


@router.get("/{id}/metrics", summary="List Product Metrics Registry")
async def list_metrics(id: str) -> Dict[str, Any]:
    metrics = global_product_management_service.vision_strategy.list_metrics(id)
    return {"status": "SUCCESS", "count": len(metrics), "data": metrics}


@router.post("/{id}/metrics", status_code=status.HTTP_201_CREATED, summary="Register Metric")
async def register_metric(id: str, req: MetricRegisterRequest) -> Dict[str, Any]:
    met = global_product_management_service.vision_strategy.register_metric(
        product_id=id,
        name=req.name,
        definition=req.definition,
        formula=req.formula,
        source=req.source,
        owner=req.owner,
        current_value=req.current_value,
        target_value=req.target_value,
        is_north_star=req.is_north_star,
    )
    return {"status": "SUCCESS", "data": met}


@router.get("/{id}/feedback", summary="List Customer Feedback & Clusters")
async def list_feedback(id: str) -> Dict[str, Any]:
    fb = global_product_management_service.feedback_intelligence.list_feedback(id)
    themes = global_product_management_service.feedback_intelligence.cluster_feedback_into_themes(id)
    return {"status": "SUCCESS", "feedback_count": len(fb), "themes_count": len(themes), "feedback": fb, "themes": themes}


@router.post("/{id}/feedback", status_code=status.HTTP_201_CREATED, summary="Ingest Customer Feedback")
async def ingest_feedback(id: str, req: FeedbackIngestRequest) -> Dict[str, Any]:
    fb = global_product_management_service.feedback_intelligence.ingest_feedback(
        product_id=id,
        source=req.source,
        feedback_type=req.feedback_type,
        customer_segment=req.customer_segment,
        content=req.content,
        sentiment_score=req.sentiment_score,
        revenue_impact_usd=req.revenue_impact_usd,
    )
    return {"status": "SUCCESS", "data": fb}


@router.get("/{id}/traceability", summary="Get Complete Traceability Matrix & Orphan Detection")
async def get_traceability(id: str) -> Dict[str, Any]:
    matrix = global_product_management_service.requirements_traceability.get_traceability_matrix(id)
    return {"status": "SUCCESS", "data": matrix}


@router.post("/{id}/requirements", status_code=status.HTTP_201_CREATED, summary="Create PRD Requirement")
async def create_requirement(id: str, req: RequirementCreateRequest) -> Dict[str, Any]:
    req_obj = global_product_management_service.requirements_traceability.create_requirement(
        product_id=id,
        title=req.title,
        description=req.description,
        category=req.category,
        priority=req.priority,
        acceptance_criteria=req.acceptance_criteria,
        source=req.source,
        problem_id=req.problem_id,
        objective_id=req.objective_id,
    )
    return {"status": "SUCCESS", "data": req_obj}


@router.get("/{id}/backlog", summary="List Product Backlog & Epics")
async def list_backlog(id: str) -> Dict[str, Any]:
    epics = global_product_management_service.backlog_prioritization.list_epics(id)
    features = global_product_management_service.backlog_prioritization.list_features(id)
    items = global_product_management_service.backlog_prioritization.list_backlog_items(id)
    return {"status": "SUCCESS", "epics": epics, "features": features, "items": items}


@router.post("/{id}/backlog/score/{item_id}", summary="Prioritize Backlog Item (RICE/WSJF)")
async def score_backlog_item(id: str, item_id: str, req: PrioritizationScoreRequest) -> Dict[str, Any]:
    score = global_product_management_service.backlog_prioritization.score_item(
        item_id=item_id,
        product_id=id,
        framework=req.framework,
        inputs=req.inputs,
    )
    return {"status": "SUCCESS", "data": score}


@router.get("/{id}/roadmap", summary="Get Roadmaps & Scenarios")
async def get_roadmaps(id: str) -> Dict[str, Any]:
    roadmaps = global_product_management_service.roadmaps_capacity.list_roadmaps(id)
    return {"status": "SUCCESS", "data": roadmaps}


@router.post("/{id}/roadmap", status_code=status.HTTP_201_CREATED, summary="Create Roadmap Scenario")
async def create_roadmap(id: str, req: RoadmapCreateRequest) -> Dict[str, Any]:
    rm = global_product_management_service.roadmaps_capacity.create_roadmap(
        product_id=id,
        title=req.title,
        scenario=req.scenario,
        description=req.description,
    )
    return {"status": "SUCCESS", "data": rm}


@router.get("/{id}/sprints-releases", summary="List Sprints and Releases")
async def list_sprints_releases(id: str) -> Dict[str, Any]:
    sprints = global_product_management_service.sprints_releases.list_sprints(id)
    releases = global_product_management_service.sprints_releases.list_releases(id)
    return {"status": "SUCCESS", "sprints": sprints, "releases": releases}


@router.post("/{id}/releases/{release_id}/readiness", summary="Evaluate Release Readiness Gate")
async def evaluate_readiness(id: str, release_id: str, req: ReleaseReadinessEvaluateRequest) -> Dict[str, Any]:
    gate = global_product_management_service.sprints_releases.evaluate_release_readiness(
        release_id=release_id,
        product_id=id,
        qa_passed=req.qa_passed,
        critical_defects=req.critical_defects,
        security_reviewed=req.security_reviewed,
        performance_benchmarked=req.performance_benchmarked,
        rollback_tested=req.rollback_tested,
    )
    return {"status": "SUCCESS", "data": gate}


@router.get("/{id}/deployments-launches", summary="Get Deployments, Feature Flags & Launch Checklists")
async def get_deployments_launches(id: str) -> Dict[str, Any]:
    flags = global_product_management_service.deployments_launches.list_flags(id)
    launches = global_product_management_service.deployments_launches.list_launches(id)
    return {"status": "SUCCESS", "feature_flags": flags, "launches": launches}


@router.get("/{id}/analytics-experiments", summary="Get Adoption Analytics and A/B Experiments")
async def get_analytics_experiments(id: str) -> Dict[str, Any]:
    adoption = global_product_management_service.analytics_experimentation.get_adoption_overview(id)
    experiments = global_product_management_service.analytics_experimentation.list_experiments(id)
    return {"status": "SUCCESS", "adoption": adoption, "experiments": experiments}


@router.get("/{id}/health", summary="Get Composite Product Health & Risk Factors")
async def get_product_health(id: str) -> Dict[str, Any]:
    health = global_product_management_service.health_sunset.get_latest_health(id)
    history = global_product_management_service.health_sunset.list_health_history(id)
    return {"status": "SUCCESS", "current_health": health, "history": history}


@router.post("/{id}/copilot", summary="Query Product Copilot")
async def query_copilot(id: str, req: ProductCopilotRequest) -> Dict[str, Any]:
    try:
        res = global_product_management_service.query_product_copilot(product_id=id, query=req.query)
        return {"status": "SUCCESS", "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
