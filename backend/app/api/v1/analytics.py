"""API router for Phase 31 Business Intelligence & Analytics."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.repositories.analytics import AnalyticsRepository
from app.services.analytics import AnalyticsService
from app.schemas.analytics import (
    ExecutiveOverviewResponse,
    MetricResponse,
    MetricCreate,
    SemanticQueryRequest,
    SemanticQueryResponse,
)
from app.models.analytics import AnalyticsMetric, InsightCategory

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_analytics_service(session: AsyncSession = Depends(get_db)) -> AnalyticsService:
    repo = AnalyticsRepository(session)
    return AnalyticsService(repo)


@router.get("/overview", response_model=ExecutiveOverviewResponse)
async def get_executive_overview(
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Get high-level executive health summary answering: How is the business performing?"""
    await service.ensure_default_metrics_seeded(tenant_id)
    return await service.get_executive_overview(tenant_id)


@router.get("/sales")
async def get_sales_intelligence(
    tenant_id: str = "default_tenant",
    time_window: str = "30d",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Get sales funnel conversions, qualification rates, and lead score calibration."""
    return await service.get_sales_intelligence(tenant_id, time_window)


@router.get("/delivery")
async def get_delivery_intelligence(
    tenant_id: str = "default_tenant",
    time_window: str = "30d",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Get project effort variance (PERT actual vs estimate), scope change causes, and defect leakage."""
    return await service.get_delivery_intelligence(tenant_id, time_window)


@router.get("/support")
async def get_support_intelligence(
    tenant_id: str = "default_tenant",
    time_window: str = "30d",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Get support ticket volumes, category distributions, and SLA adherence."""
    return await service.get_support_intelligence(tenant_id, time_window)


@router.get("/ai")
async def get_ai_operations_intelligence(
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Get AI operational token consumptions, latency stats, and dollar costs."""
    return await service.get_ai_operations_intelligence(tenant_id)


@router.get("/financial")
async def get_financial_intelligence(
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Get authoritative financial numbers strictly segregated by ACTUAL vs FORECAST vs ESTIMATE."""
    return await service.get_financial_intelligence(tenant_id)


@router.get("/metrics", response_model=List[MetricResponse])
async def list_registered_metrics(
    tenant_id: str = "default_tenant",
    category: Optional[str] = None,
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """List registered centralized metrics from the metric registry."""
    await service.ensure_default_metrics_seeded(tenant_id)
    return await service.repo.list_metrics(tenant_id, category=category)


@router.post("/metrics", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
async def create_metric_definition(
    req: MetricCreate,
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Create a new centralized metric definition."""
    cat = InsightCategory(req.category) if req.category in InsightCategory.__members__ else InsightCategory.OPERATIONS
    metric = AnalyticsMetric(
        tenant_id=tenant_id,
        metric_key=req.metric_key,
        name=req.name,
        description=req.description,
        category=cat,
        formula=req.formula,
        source_tables=req.source_tables,
        dimensions=req.dimensions,
        time_window_default=req.time_window_default,
        owner=req.owner,
    )
    return await service.repo.create_metric(metric)


@router.post("/query", response_model=SemanticQueryResponse)
async def execute_natural_language_query(
    req: SemanticQueryRequest,
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Execute a natural language analytical query via the approved Semantic Layer (raw SQL is strictly prohibited)."""
    return await service.execute_semantic_query(tenant_id, req.query)


@router.post("/learning-cycle")
async def run_learning_cycle(
    tenant_id: str = "default_tenant",
    service: AnalyticsService = Depends(get_analytics_service),
) -> Any:
    """Trigger the organizational learning engine to analyze operational data and synthesize insights."""
    return await service.run_learning_cycle(tenant_id)
