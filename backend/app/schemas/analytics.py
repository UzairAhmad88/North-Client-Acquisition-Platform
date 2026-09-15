"""Pydantic request & response schemas for Phase 31 Business Intelligence & Analytics API."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# =============================================================================
# 1. Metrics Registry Schemas
# =============================================================================

class MetricResponse(BaseModel):
    id: str
    tenant_id: str
    metric_key: str
    name: str
    description: str
    category: str
    formula: str
    source_tables: List[str]
    dimensions: List[str]
    time_window_default: str
    version: str
    owner: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MetricCreate(BaseModel):
    metric_key: str
    name: str
    description: str
    category: str = "OPERATIONS"
    formula: str
    source_tables: List[str] = []
    dimensions: List[str] = []
    time_window_default: str = "30d"
    owner: str = "system"


# =============================================================================
# 2. Domain Analytics Responses
# =============================================================================

class ExecutiveOverviewResponse(BaseModel):
    overview_timestamp: str
    pipeline_win_rate_pct: float
    active_projects_count: int
    estimation_variance_pct: float
    sla_compliance_pct: float
    realized_revenue_usd: float
    ai_cost_usd: float
    top_insights_count: int
    top_insights: List[Dict[str, Any]]


class SemanticQueryRequest(BaseModel):
    query: str = Field(..., description="User question (e.g., 'Why are project estimates inaccurate?')")
    context_filters: Dict[str, Any] = Field(default_factory=dict)


class SemanticQueryResponse(BaseModel):
    query_key: str
    intent: str
    parameters: Dict[str, Any]
    data: Any
    summary: str
    evidence_notes: List[str]


# =============================================================================
# 3. Insights & Recommendations Schemas
# =============================================================================

class InsightEvidenceResponse(BaseModel):
    id: str
    source_type: str
    sample_count: int
    baseline_value: Optional[float]
    observed_value: Optional[float]
    variance_pct: Optional[float]
    details: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    id: str
    insight_id: Optional[str]
    title: str
    recommendation: str
    reason: str
    expected_benefit: str
    potential_downside: str
    confidence: str
    affected_workflow: str
    status: str
    decision_reason: Optional[str]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class InsightResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: str
    category: str
    confidence: str
    sample_size: int
    time_window: str
    affected_entities: Dict[str, Any]
    recommended_action: Optional[str]
    status: str
    created_by: str
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime
    evidence_items: List[InsightEvidenceResponse] = []

    class Config:
        from_attributes = True


class InsightReviewRequest(BaseModel):
    action: str = Field(..., description="ACCEPT, REJECT, ARCHIVE, REVIEW")
    reviewed_by: str = Field(default="user")
    notes: Optional[str] = None


class RecommendationReviewRequest(BaseModel):
    action: str = Field(..., description="APPROVE, REJECT, IMPLEMENT")
    reviewer: str = Field(default="user")
    notes: Optional[str] = None
    policy_impact: Dict[str, Any] = Field(default_factory=dict)


# =============================================================================
# 4. Experiments & Hypotheses Schemas
# =============================================================================

class ExperimentCreateRequest(BaseModel):
    title: str
    hypothesis: str
    target_workflow: str
    target_metric: str
    baseline_value: float = 0.0
    target_value: float = 0.0
    sample_target: int = 10
    created_by: str = "user"


class ExperimentResultCreateRequest(BaseModel):
    entity_id: Optional[str] = None
    observed_value: float
    notes: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class ExperimentMetricResponse(BaseModel):
    id: str
    metric_name: str
    is_primary: bool
    baseline_value: float
    current_value: float
    unit: str

    class Config:
        from_attributes = True


class ExperimentResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    hypothesis: str
    target_workflow: str
    target_metric: str
    baseline_value: float
    target_value: float
    sample_target: int
    current_sample_count: int
    status: str
    created_by: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    conclusion: Optional[str]
    created_at: datetime
    metrics: List[ExperimentMetricResponse] = []

    class Config:
        from_attributes = True


# =============================================================================
# 5. Model Registry Schemas
# =============================================================================

class ModelRegistryResponse(BaseModel):
    id: str
    tenant_id: str
    model_key: str
    name: str
    purpose: str
    version: str
    model_type: str
    features: List[str]
    training_window: str
    evaluation_metrics: Dict[str, Any]
    status: str
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ModelApproveRequest(BaseModel):
    approved_by: str
