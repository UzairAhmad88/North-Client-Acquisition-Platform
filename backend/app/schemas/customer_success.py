"""Pydantic schemas for Unified Client Relationship Intelligence & Customer Success Platform."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Client Profile ---

class ClientProfileCreate(BaseModel):
    client_id: str
    company_name: str
    industry: Optional[str] = None
    company_size: Optional[str] = None
    lifecycle_stage: str = "ONBOARDING"
    relationship_manager_id: Optional[str] = None
    executive_sponsor: Optional[str] = None
    communication_cadence: str = "BI_WEEKLY"
    client_timezone: str = "UTC"
    strategic_tier: str = "STANDARD"
    tags: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class ClientProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    lifecycle_stage: Optional[str] = None
    relationship_manager_id: Optional[str] = None
    executive_sponsor: Optional[str] = None
    communication_cadence: Optional[str] = None
    client_timezone: Optional[str] = None
    strategic_tier: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None


class ClientProfileResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    company_name: str
    industry: Optional[str] = None
    company_size: Optional[str] = None
    lifecycle_stage: str
    relationship_manager_id: Optional[str] = None
    executive_sponsor: Optional[str] = None
    client_since: datetime
    communication_cadence: str
    client_timezone: str
    strategic_tier: str
    tags: List[str]
    custom_fields: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Client Relationship ---

class ClientRelationshipCreate(BaseModel):
    client_id: str
    contact_name: str
    contact_email: str
    contact_role: Optional[str] = None
    decision_role: str = "STAKEHOLDER"
    influence_level: str = "MEDIUM"
    relationship_strength: str = "ESTABLISHED"
    last_interaction_date: Optional[datetime] = None
    notes: Optional[str] = None
    is_primary_contact: bool = False


class ClientRelationshipResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    contact_name: str
    contact_email: str
    contact_role: Optional[str] = None
    decision_role: str
    influence_level: str
    relationship_strength: str
    last_interaction_date: Optional[datetime] = None
    notes: Optional[str] = None
    is_primary_contact: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Timeline Event ---

class ClientTimelineEventCreate(BaseModel):
    client_id: str
    event_category: str
    event_type: str
    title: str
    summary: Optional[str] = None
    actor_id: Optional[str] = None
    actor_name: Optional[str] = None
    visibility: str = "INTERNAL_ONLY"
    metadata_payload: Dict[str, Any] = Field(default_factory=dict)


class ClientTimelineEventResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    event_category: str
    event_type: str
    title: str
    summary: Optional[str] = None
    occurred_at: datetime
    actor_id: Optional[str] = None
    actor_name: Optional[str] = None
    visibility: str
    metadata_payload: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# --- Client Goal ---

class ClientGoalCreate(BaseModel):
    client_id: str
    title: str
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    status: str = "NOT_STARTED"
    progress_percentage: Decimal = Decimal("0.00")
    metric_target: Optional[str] = None
    metric_current: Optional[str] = None


class ClientGoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    status: Optional[str] = None
    progress_percentage: Optional[Decimal] = None
    metric_target: Optional[str] = None
    metric_current: Optional[str] = None


class ClientGoalResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    title: str
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    status: str
    progress_percentage: Decimal
    metric_target: Optional[str] = None
    metric_current: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Success Plan & Task ---

class ClientSuccessPlanCreate(BaseModel):
    client_id: str
    title: str
    owner_id: Optional[str] = None
    start_date: Optional[datetime] = None
    target_completion_date: Optional[datetime] = None
    strategic_objectives: List[Dict[str, Any]] = Field(default_factory=list)


class ClientSuccessPlanUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    owner_id: Optional[str] = None
    start_date: Optional[datetime] = None
    target_completion_date: Optional[datetime] = None
    strategic_objectives: Optional[List[Dict[str, Any]]] = None


class ClientSuccessPlanResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    title: str
    status: str
    owner_id: Optional[str] = None
    start_date: Optional[datetime] = None
    target_completion_date: Optional[datetime] = None
    strategic_objectives: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClientSuccessTaskCreate(BaseModel):
    plan_id: str
    title: str
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None


class ClientSuccessTaskResponse(BaseModel):
    id: str
    plan_id: str
    title: str
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Health Score & History ---

class ClientHealthScoreResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    composite_score: Decimal
    health_band: str
    engagement_score: Optional[Decimal] = None
    project_health_score: Optional[Decimal] = None
    support_satisfaction_score: Optional[Decimal] = None
    financial_health_score: Optional[Decimal] = None
    relationship_health_score: Optional[Decimal] = None
    goal_progress_score: Optional[Decimal] = None
    confidence_score: Decimal
    trend: str
    explanation_summary: Optional[str] = None
    calculation_breakdown: Dict[str, Any]
    calculated_at: datetime

    class Config:
        from_attributes = True


class ClientHealthHistoryResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    score: Decimal
    health_band: str
    recorded_at: datetime
    breakdown_snapshot: Dict[str, Any]

    class Config:
        from_attributes = True


# --- Survey & Response ---

class ClientSurveyCreate(BaseModel):
    client_id: str
    survey_type: str
    trigger_event: Optional[str] = None
    title: str
    questions: List[Dict[str, Any]]


class ClientSurveyResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    survey_type: str
    trigger_event: Optional[str] = None
    title: str
    questions: List[Dict[str, Any]]
    status: str
    sent_at: datetime

    class Config:
        from_attributes = True


class ClientSurveyAnswerCreate(BaseModel):
    survey_id: str
    respondent_id: Optional[str] = None
    respondent_name: Optional[str] = None
    score: Decimal
    answers: Dict[str, Any]
    feedback_text: Optional[str] = None


class ClientSurveyAnswerResponse(BaseModel):
    id: str
    survey_id: str
    respondent_id: Optional[str] = None
    respondent_name: Optional[str] = None
    score: Decimal
    answers: Dict[str, Any]
    feedback_text: Optional[str] = None
    submitted_at: datetime

    class Config:
        from_attributes = True


# --- Sentiment Analysis ---

class ClientSentimentAnalysisCreate(BaseModel):
    client_id: str
    source_type: str
    source_id: Optional[str] = None
    sentiment_score: Decimal
    sentiment_label: str
    key_phrases: List[str] = Field(default_factory=list)
    summary: Optional[str] = None


class ClientSentimentAnalysisResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    source_type: str
    source_id: Optional[str] = None
    sentiment_score: Decimal
    sentiment_label: str
    key_phrases: List[str]
    summary: Optional[str] = None
    analyzed_at: datetime

    class Config:
        from_attributes = True


# --- Risk ---

class ClientRiskCreate(BaseModel):
    client_id: str
    category: str
    title: str
    description: Optional[str] = None
    severity: str = "MEDIUM"
    impact_summary: Optional[str] = None
    mitigation_plan: Optional[str] = None
    owner_id: Optional[str] = None


class ClientRiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    impact_summary: Optional[str] = None
    mitigation_plan: Optional[str] = None
    owner_id: Optional[str] = None
    status: Optional[str] = None


class ClientRiskResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    category: str
    title: str
    description: Optional[str] = None
    severity: str
    impact_summary: Optional[str] = None
    mitigation_plan: Optional[str] = None
    owner_id: Optional[str] = None
    status: str
    detected_by: str
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Opportunity ---

class ClientOpportunityCreate(BaseModel):
    client_id: str
    opportunity_type: str
    title: str
    description: Optional[str] = None
    estimated_value: Decimal = Decimal("0.00")
    confidence_score: Decimal = Decimal("0.50")
    target_service_id: Optional[str] = None


class ClientOpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    estimated_value: Optional[Decimal] = None
    confidence_score: Optional[Decimal] = None
    status: Optional[str] = None
    linked_lead_id: Optional[str] = None
    linked_opportunity_id: Optional[str] = None


class ClientOpportunityResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    opportunity_type: str
    title: str
    description: Optional[str] = None
    estimated_value: Decimal
    confidence_score: Decimal
    status: str
    target_service_id: Optional[str] = None
    linked_lead_id: Optional[str] = None
    linked_opportunity_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Renewal ---

class ClientRenewalCreate(BaseModel):
    client_id: str
    contract_id: Optional[str] = None
    subscription_id: Optional[str] = None
    current_period_end: datetime
    renewal_date: datetime
    estimated_renewal_value: Decimal = Decimal("0.00")
    renewal_probability: Decimal = Decimal("0.50")
    assigned_owner_id: Optional[str] = None
    notes: Optional[str] = None


class ClientRenewalUpdate(BaseModel):
    current_period_end: Optional[datetime] = None
    renewal_date: Optional[datetime] = None
    status: Optional[str] = None
    estimated_renewal_value: Optional[Decimal] = None
    renewal_probability: Optional[Decimal] = None
    assigned_owner_id: Optional[str] = None
    notes: Optional[str] = None


class ClientRenewalResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    contract_id: Optional[str] = None
    subscription_id: Optional[str] = None
    current_period_end: datetime
    renewal_date: datetime
    status: str
    estimated_renewal_value: Decimal
    renewal_probability: Decimal
    assigned_owner_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Referral ---

class ClientReferralCreate(BaseModel):
    client_id: str
    referred_company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None


class ClientReferralResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    referred_company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    status: str
    reward_status: str
    converted_lead_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Segment ---

class ClientSegmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    criteria: Dict[str, Any] = Field(default_factory=dict)
    matching_client_ids: List[str] = Field(default_factory=list)


class ClientSegmentResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    description: Optional[str] = None
    criteria: Dict[str, Any]
    matching_client_ids: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Account Plan ---

class ClientAccountPlanCreate(BaseModel):
    client_id: str
    fiscal_year: str
    account_strategy: Optional[str] = None
    revenue_target: Decimal = Decimal("0.00")
    expansion_initiatives: List[Dict[str, Any]] = Field(default_factory=list)


class ClientAccountPlanResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    fiscal_year: str
    account_strategy: Optional[str] = None
    revenue_target: Decimal
    expansion_initiatives: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Review (QBR) ---

class ClientReviewCreate(BaseModel):
    client_id: str
    review_type: str = "QBR"
    scheduled_date: datetime
    attendees: List[str] = Field(default_factory=list)
    presentation_deck_url: Optional[str] = None
    meeting_notes: Optional[str] = None
    action_items: List[Dict[str, Any]] = Field(default_factory=list)


class ClientReviewResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    review_type: str
    scheduled_date: datetime
    conducted_date: Optional[datetime] = None
    attendees: List[str]
    presentation_deck_url: Optional[str] = None
    meeting_notes: Optional[str] = None
    action_items: List[Dict[str, Any]]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Computation & 360 Schemas ---

class HealthCalculationRequest(BaseModel):
    engagement_score: Optional[Decimal] = None
    project_health_score: Optional[Decimal] = None
    support_satisfaction_score: Optional[Decimal] = None
    financial_health_score: Optional[Decimal] = None
    relationship_health_score: Optional[Decimal] = None
    goal_progress_score: Optional[Decimal] = None


class HealthCalculationResponse(BaseModel):
    composite_score: Decimal
    health_band: str
    confidence_score: Decimal
    trend: str
    explanation_summary: str
    calculation_breakdown: Dict[str, Any]


class Client360Response(BaseModel):
    profile: Optional[Dict[str, Any]] = None
    relationships: List[Dict[str, Any]] = Field(default_factory=list)
    latest_health: Optional[Dict[str, Any]] = None
    goals: List[Dict[str, Any]] = Field(default_factory=list)
    active_risks: List[Dict[str, Any]] = Field(default_factory=list)
    opportunities: List[Dict[str, Any]] = Field(default_factory=list)
    upcoming_renewals: List[Dict[str, Any]] = Field(default_factory=list)
    recent_timeline: List[Dict[str, Any]] = Field(default_factory=list)
    account_plans: List[Dict[str, Any]] = Field(default_factory=list)
    reviews: List[Dict[str, Any]] = Field(default_factory=list)
