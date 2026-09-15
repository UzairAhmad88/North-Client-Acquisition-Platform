"""Pydantic Schemas for Phase 57 — Unified Customer Experience, Journey Intelligence & Optimization Platform."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class JourneyCreateRequest(BaseModel):
    customer_id: str = Field(..., description="Target customer identifier")
    customer_name: Optional[str] = Field(None, description="Customer organizational name")
    journey_type: str = Field(default="sales", description="sales | onboarding | product | service | support | renewal | expansion")
    initial_stage: str = Field(default="discovery", description="Starting journey stage")
    metadata_json: Optional[Dict[str, Any]] = None


class StageAdvanceRequest(BaseModel):
    next_stage: str = Field(..., description="Target next stage to transition to")
    notes: Optional[str] = Field(None, description="Context or transition notes")


class EventRecordRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    event_type: str = Field(..., description="Canonical event name (e.g. CONTRACT_SIGNED, FEATURE_USED)")
    stage: str = Field(..., description="Stage where event occurred")
    channel: str = Field(default="web", description="Channel name")
    actor_type: str = Field(default="customer", description="customer | internal | agent")
    actor_id: Optional[str] = None
    provenance_source: Optional[str] = "event_bus"
    properties: Optional[Dict[str, Any]] = None


class TouchpointRecordRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    channel: str = Field(..., description="Touchpoint channel (e.g. portal, email, meeting)")
    touchpoint_type: str = Field(..., description="Type of touchpoint")
    purpose: Optional[str] = None
    outcome: str = Field(default="completed", description="Touchpoint outcome")
    sentiment: str = Field(default="neutral", description="Observed sentiment")
    friction_detected: bool = Field(default=False)
    duration_seconds: float = Field(default=0.0)
    interaction_metadata: Optional[Dict[str, Any]] = None


class FrictionRecordRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    stage: str = Field(..., description="Journey stage where friction occurred")
    friction_type: str = Field(..., description="Type of friction")
    severity: str = Field(default="medium", description="low | medium | high | critical")
    description: str = Field(..., description="Description of the friction point")
    evidence: Optional[Dict[str, Any]] = None
    customer_impact: Optional[str] = None
    business_impact: Optional[str] = None
    confidence: float = Field(default=0.88)
    journey_id: Optional[str] = None


class EffortCalculateRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    stage: str = Field(..., description="Journey stage")
    step_count: int = Field(default=1)
    form_count: int = Field(default=0)
    repeated_info_instances: int = Field(default=0)
    waiting_time_minutes: float = Field(default=0.0)
    support_contacts_count: int = Field(default=0)
    journey_id: Optional[str] = None


class SentimentRecordRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    source_channel: str = Field(..., description="Source channel of statement")
    sentiment: str = Field(default="neutral", description="positive | neutral | negative | mixed")
    confidence: float = Field(default=0.85)
    model_version: str = Field(default="cx-sentiment-v2")
    detected_emotions: Optional[List[str]] = None
    excerpt: Optional[str] = None
    is_customer_stated: bool = Field(default=False)


class GoalCreateRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    title: str = Field(..., description="Goal title")
    goal_type: str = Field(default="business_goal", description="business_goal | product_goal | project_goal | operational_goal")
    description: Optional[str] = None
    baseline_value: Optional[str] = "0"
    target_value: Optional[str] = "100"
    current_value: Optional[str] = "0"
    progress_pct: float = Field(default=0.0)
    evidence: Optional[Dict[str, Any]] = None


class HealthEvaluateRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    engagement_score: float = Field(default=85.0)
    adoption_score: float = Field(default=88.0)
    support_score: float = Field(default=92.0)
    effort_score: float = Field(default=80.0)
    sentiment_score: float = Field(default=85.0)


class ChurnPredictRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    churn_probability: float = Field(default=0.10)
    risk_level: str = Field(default="low")
    primary_drivers: Optional[List[str]] = None
    recommended_interventions: Optional[List[str]] = None
    confidence: float = Field(default=0.88)


class RetentionCreateRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    title: str = Field(..., description="Retention opportunity title")
    trigger_reason: str = Field(...)
    proposed_action: str = Field(...)
    impact_estimate: str = Field(default="high")
    effort_required: str = Field(default="medium")


class ExpansionCreateRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    title: str = Field(..., description="Expansion opportunity title")
    expansion_type: str = Field(default="additional_capacity")
    description: Optional[str] = None
    estimated_arr_value: float = Field(default=25000.0)
    evidence_signals: Optional[List[str]] = None
    confidence: float = Field(default=0.85)


class AdvocacyCreateRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    title: str = Field(..., description="Advocacy title / headline")
    content: str = Field(..., description="Testimonial or case study excerpt")
    advocacy_type: str = Field(default="testimonial")
    permission_granted: bool = Field(default=False)


class ReferralCreateRequest(BaseModel):
    referrer_customer_id: str = Field(..., description="Referring customer identifier")
    referred_company_name: str = Field(..., description="Referred business entity")
    referred_contact_email: Optional[str] = None
    relationship_context: Optional[str] = None
    conversion_value: float = Field(default=0.0)


class VoiceRecordRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    source_channel: str = Field(..., description="Feedback channel")
    quote_text: str = Field(..., description="Customer statement or verbatim quote")
    feedback_category: str = Field(default="need", description="need | problem | request | objection | complaint | praise")
    extracted_topics: Optional[List[str]] = None
    sentiment: str = Field(default="neutral")


class ExpectationGapRecordRequest(BaseModel):
    customer_id: str = Field(..., description="Customer identifier")
    area: str = Field(..., description="Capability area")
    promised_capability: str = Field(..., description="Authoritative commitment from contract/SOW")
    customer_expected: str = Field(..., description="Customer understanding")
    delivered_reality: str = Field(..., description="Actual observed telemetry or output")
    gap_severity: str = Field(default="moderate")
    evidence_source: Optional[str] = None
    remediation_action: Optional[str] = None


class ExperimentCreateRequest(BaseModel):
    name: str = Field(..., description="Experiment title")
    hypothesis: str = Field(..., description="Scientific hypothesis")
    control_variant: Dict[str, Any] = Field(...)
    treatment_variant: Dict[str, Any] = Field(...)
    target_stage: str = Field(default="onboarding")
    primary_metric: str = Field(default="conversion_rate")
    experiment_type: str = Field(default="onboarding_flow")


class OpportunityCreateRequest(BaseModel):
    problem: str = Field(...)
    stage: str = Field(...)
    proposed_improvement: str = Field(...)
    business_impact: str = Field(...)
    customer_impact: str = Field(...)
    effort: str = Field(default="medium")
    confidence: float = Field(default=0.87)


class AlertCreateRequest(BaseModel):
    customer_id: str = Field(...)
    alert_type: str = Field(default="health_decline")
    severity: str = Field(default="warning")
    title: str = Field(...)
    message: str = Field(default="")
    evidence_signals: Optional[List[str]] = None
    recommended_action: Optional[str] = None


class CopilotQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language question for CX Copilot")
    customer_id: Optional[str] = Field(default=None, description="Optional customer context filter")
