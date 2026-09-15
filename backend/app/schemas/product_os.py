"""Phase 60: Pydantic Schemas for Unified Product Operating System API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    name: str = Field(..., example="Uzaii Cognitive Decision Fabric")
    product_line: str = Field("Enterprise Intelligence", example="Enterprise Intelligence")
    code: Optional[str] = Field(None, example="UZAII-DECISION-01")
    lifecycle_state: str = Field("DISCOVERY", example="DISCOVERY")
    target_icp: str = Field("Global 2000 Chief AI Officers", example="Global 2000 Chief AI Officers")
    owner_email: str = Field("chief-product@uzaii.com", example="chief-product@uzaii.com")
    description: str = Field("", example="Unified sensory, analytical, and governance operating layer.")


class VisionCreateRequest(BaseModel):
    product_id: str
    target_users: str
    core_problem: str
    value_proposition: str
    differentiation: str
    strategic_fit: str = ""
    market_opportunity: str = ""


class StrategyCreateRequest(BaseModel):
    product_id: str
    positioning: str
    growth_strategy: str
    product_bets: List[str] = Field(default_factory=list)
    core_metrics: Dict[str, Any] = Field(default_factory=dict)
    icp_definition: Optional[Dict[str, Any]] = None


class ProblemCreateRequest(BaseModel):
    product_id: str
    title: str
    reported_by_count: int = 1
    severity: str = "MEDIUM"
    validation_status: str = "HYPOTHESIS"
    context: str = ""
    cost_of_inaction_usd: float = 0.0
    evidence_sources: List[str] = Field(default_factory=list)


class FeedbackItemCreateRequest(BaseModel):
    product_id: str
    source_type: str
    raw_content: str
    sentiment_score: float = 0.0
    feedback_category: str = "PROBLEM"
    customer_account_id: Optional[str] = None
    urgency_level: str = "NORMAL"


class OpportunityCreateRequest(BaseModel):
    product_id: str
    title: str
    problem_id: Optional[str] = None
    customer_value_score: float = 8.0
    business_value_score: float = 8.0
    confidence_score: float = 8.0
    effort_score: float = 4.0
    strategic_fit_score: float = 8.5
    revenue_potential_usd: float = 250000.0


class PrioritizationScoreRequest(BaseModel):
    item_id: str
    framework: str = "RICE"
    reach: float = 1000.0
    impact: float = 3.0
    confidence: float = 80.0
    effort: float = 4.0
    user_business_value: float = 8.0
    time_criticality: float = 7.0
    risk_reduction: float = 6.0


class RoadmapCreateRequest(BaseModel):
    product_id: str
    title: str
    horizon_type: str = "QUARTERLY"


class RoadmapItemCreateRequest(BaseModel):
    roadmap_id: str
    title: str
    horizon: str = "NOW"
    opportunity_id: Optional[str] = None
    target_quarter: Optional[str] = "2026-Q3"
    engineering_effort_weeks: float = 4.0
    dependencies: List[str] = Field(default_factory=list)
    confidence: float = 85.0


class RequirementCreateRequest(BaseModel):
    opportunity_id: str
    title: str
    requirement_type: str = "FUNCTIONAL"
    priority: str = "HIGH"
    description: str = ""
    acceptance_criteria: List[str] = Field(default_factory=list)
    linked_initiative_id: Optional[str] = None


class UserStoryCreateRequest(BaseModel):
    requirement_id: str
    role: str
    capability: str
    benefit: str
    given_when_then: Optional[List[Dict[str, str]]] = None
    story_points: int = 3
    technical_notes: str = ""


class FeatureAdoptionTrackRequest(BaseModel):
    product_id: str
    feature_key: str
    feature_name: str
    eligible_users: int
    activated_users: int
    weekly_active_users: int
    retention_rate_30d: float
    customer_satisfaction_score: float
    efficiency_gain_pct: float
    revenue_influenced_usd: float = 0.0


class ProductHealthScoreRequest(BaseModel):
    product_id: str
    product_name: str
    adoption_score: float = 85.0
    retention_score: float = 80.0
    reliability_score: float = 98.0
    feedback_sentiment_score: float = 80.0
    support_efficiency_score: float = 75.0
    quality_defect_score: float = 85.0
    gross_margin_score: float = 80.0


class LaunchPlanCreateRequest(BaseModel):
    product_id: str
    release_name: str
    target_release_date: str
    strategy: str = "PHASED_ROLLOUT"
    audience_segment: str = "Enterprise Early Access"
    checklists: Optional[Dict[str, bool]] = None
    rollback_plan: str = "Canary auto-revert upon error rate > 1.5%"


class FeatureFlagCreateRequest(BaseModel):
    flag_key: str
    name: str
    environment: str = "production"
    is_enabled: bool = False
    rollout_percentage: int = 10
    targeting_rules: Optional[Dict[str, Any]] = None
    owner_email: str = "product-ops@uzaii.com"


class SunsetPlanCreateRequest(BaseModel):
    product_id: str
    product_name: str
    reason: str
    active_customer_count: int
    revenue_impact_usd: float
    alternative_product_id: str
    target_sunset_date: str
    governance_approver: str


class UnitEconomicsCalculateRequest(BaseModel):
    product_id: str
    active_customers: int
    mrr_usd: float
    infrastructure_cost_usd: float
    support_cost_usd: float
    r_and_d_allocated_usd: float
    cac_usd: float
    churn_rate_monthly: float


class ForecastGenerateRequest(BaseModel):
    product_id: str
    metric_name: str
    time_horizon_months: int = 12
    baseline_value: float = 100000.0
    growth_rate_base: float = 0.08


class TwinSimulationRequest(BaseModel):
    product_id: str
    scenario_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ProductRiskCreateRequest(BaseModel):
    product_id: str
    category: str
    title: str
    probability: float
    impact_score: float
    severity: str = "HIGH"
    mitigation_strategy: str = ""
    owner: str = "product-lead@uzaii.com"


class ProductCopilotQueryRequest(BaseModel):
    query: str
    tenant_id: Optional[str] = "default_tenant"
