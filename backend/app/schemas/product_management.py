"""
Pydantic Schemas for Phase 56 — Unified Product Lifecycle, Product Management & Continuous Delivery Intelligence Platform.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    name: str = Field(..., description="Product name")
    type: str = Field(default="software", description="product | service | platform | internal | ai | automation")
    description: Optional[str] = None
    target_market: Optional[str] = None
    owner: str = Field(default="Product Lead")
    team: Optional[str] = "Core Platform Team"
    workspace_id: Optional[str] = None


class LifecycleTransitionRequest(BaseModel):
    new_stage: str = Field(..., description="Target lifecycle stage: discovery, concept, strategy, planning, validation, development, testing, release, launch, adoption, optimization, maturity, sunset, paused, deprecated")
    actor: str = Field(default="system")
    rationale: Optional[str] = None


class VisionSetRequest(BaseModel):
    target_customer: str = Field(...)
    problem_statement: str = Field(...)
    desired_future_state: str = Field(...)
    value_proposition: str = Field(...)
    differentiation: Optional[str] = None
    strategic_alignment: Optional[str] = None
    success_definition: Optional[str] = None


class ObjectiveCreateRequest(BaseModel):
    name: str = Field(..., description="Objective title / OKR")
    metric: str = Field(..., description="Target metric name")
    baseline: float = Field(default=0.0)
    target: float = Field(...)
    time_window: str = Field(default="Q3-2026")
    owner: str = Field(default="Product Lead")
    confidence: float = Field(default=0.85)


class MetricRegisterRequest(BaseModel):
    name: str = Field(..., description="Metric name")
    definition: str = Field(...)
    formula: Optional[str] = None
    source: str = Field(default="Telemetry")
    owner: str = Field(default="Data Team")
    current_value: float = Field(default=0.0)
    target_value: Optional[float] = None
    is_north_star: bool = Field(default=False)


class FeedbackIngestRequest(BaseModel):
    source: str = Field(default="client", description="client, customer_support, sales, reviews, analytics, ai_agent")
    feedback_type: str = Field(default="feature_request", description="bug, feature_request, usability, performance, praise, complaint")
    customer_segment: str = Field(default="enterprise")
    content: str = Field(...)
    sentiment_score: Optional[float] = None
    revenue_impact_usd: Optional[float] = None


class RequirementCreateRequest(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    category: str = Field(default="functional", description="functional, non_functional, security, performance, reliability, compliance, ai")
    priority: str = Field(default="high", description="critical, high, medium, low")
    acceptance_criteria: Optional[List[str]] = None
    source: str = Field(default="User Need")
    problem_id: Optional[str] = None
    objective_id: Optional[str] = None


class EpicCreateRequest(BaseModel):
    title: str = Field(...)
    objective: str = Field(...)
    problem_statement: Optional[str] = None


class FeatureCreateRequest(BaseModel):
    title: str = Field(...)
    epic_id: Optional[str] = None
    requirement_id: Optional[str] = None
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None


class BacklogItemCreateRequest(BaseModel):
    title: str = Field(...)
    type: str = Field(default="user_story", description="user_story, bug, technical_debt, spike, task")
    description: Optional[str] = None
    epic_id: Optional[str] = None
    feature_id: Optional[str] = None
    requirement_id: Optional[str] = None
    story_points: int = Field(default=3)


class PrioritizationScoreRequest(BaseModel):
    framework: str = Field(default="RICE", description="RICE | WSJF | VALUE_VS_EFFORT | MOSCOW")
    inputs: Dict[str, float] = Field(...)


class RoadmapCreateRequest(BaseModel):
    title: str = Field(...)
    scenario: str = Field(default="base_plan", description="base_plan, accelerated, constrained, risk_reduced")
    description: Optional[str] = None


class RoadmapItemAddRequest(BaseModel):
    title: str = Field(...)
    horizon: str = Field(default="now", description="now, next, later, q1, q2, q3, q4")
    feature_id: Optional[str] = None
    objective_link: Optional[str] = None
    confidence: float = Field(default=0.85)


class SprintCreateRequest(BaseModel):
    name: str = Field(...)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    capacity_points: int = Field(default=40)


class ReleaseCreateRequest(BaseModel):
    version: str = Field(..., description="Semantic version string, e.g. v2.4.0")
    target_date: Optional[str] = None
    scope_description: Optional[str] = None
    features: Optional[List[str]] = None


class ReleaseReadinessEvaluateRequest(BaseModel):
    qa_passed: bool = Field(default=True)
    critical_defects: int = Field(default=0)
    security_reviewed: bool = Field(default=True)
    performance_benchmarked: bool = Field(default=True)
    rollback_tested: bool = Field(default=True)


class FeatureFlagCreateRequest(BaseModel):
    key: str = Field(..., description="Unique flag key")
    description: Optional[str] = None
    state: str = Field(default="OFF", description="OFF, SHADOW, INTERNAL, CANARY, PERCENTAGE, SEGMENT, FULL")
    rollout_percentage: int = Field(default=0)


class LaunchChecklistUpdateRequest(BaseModel):
    item_key: str = Field(...)
    completed: bool = Field(default=True)


class ExperimentCreateRequest(BaseModel):
    name: str = Field(...)
    hypothesis: str = Field(...)
    primary_metric: str = Field(...)
    guardrail_metrics: Optional[List[str]] = None
    control_variant: str = Field(default="Control Baseline")
    treatment_variants: Optional[List[str]] = None


class HealthSnapshotRequest(BaseModel):
    factors: Optional[Dict[str, float]] = None


class SunsetPlanCreateRequest(BaseModel):
    rationale: str = Field(...)
    target_date: Optional[str] = None
    customer_impact_review: Optional[str] = None
    migration_path: Optional[str] = None


class ProductCopilotRequest(BaseModel):
    query: str = Field(..., description="Product management co-pilot inquiry")
