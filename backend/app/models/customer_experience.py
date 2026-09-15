"""
SQLAlchemy ORM models for Phase 57 — Unified Customer Experience, Journey Intelligence & Experience Optimization Platform.
"""

from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class CustomerJourneyModel(BaseModel):
    """Canonical customer journey instance across the full enterprise lifecycle."""
    __tablename__ = "customer_journeys"

    customer_id = Column(String(36), nullable=False, index=True)
    journey_type = Column(String(64), nullable=False, default="SALES")  # SALES, ONBOARDING, PRODUCT, SERVICE, SUPPORT, RENEWAL, EXPANSION
    title = Column(String(255), nullable=False)
    current_stage = Column(String(64), nullable=False, default="AWARENESS")  # AWARENESS, DISCOVERY, CONSIDERATION, EVALUATION, PURCHASE, ONBOARDING, ACTIVATION, ADOPTION, VALUE, SUPPORT, RENEWAL, EXPANSION, ADVOCACY
    status = Column(String(32), nullable=False, default="ACTIVE")  # ACTIVE, COMPLETED, PAUSED, DROPPED, AT_RISK, CHURNED, LOST
    health_state = Column(String(32), nullable=False, default="HEALTHY")  # EXCELLENT, HEALTHY, STABLE, WATCH, AT_RISK, CRITICAL
    health_score = Column(Float, nullable=False, default=0.88)
    effort_level = Column(String(32), nullable=False, default="LOW_EFFORT")  # LOW_EFFORT, MODERATE_EFFORT, HIGH_EFFORT, CRITICAL_FRICTION
    friction_score = Column(Float, nullable=False, default=0.15)
    conversion_probability = Column(Float, nullable=False, default=0.75)
    version = Column(Integer, nullable=False, default=1)
    meta_info = Column(JSON, nullable=True, default=dict)

    # Relationships
    stages = relationship("CustomerJourneyStageModel", back_populates="journey", cascade="all, delete-orphan")
    events = relationship("CustomerJourneyEventModel", back_populates="journey", cascade="all, delete-orphan")
    touchpoints = relationship("CustomerTouchpointModel", back_populates="journey", cascade="all, delete-orphan")
    frictions = relationship("CustomerFrictionPointModel", back_populates="journey", cascade="all, delete-orphan")
    goals = relationship("CustomerGoalModel", back_populates="journey", cascade="all, delete-orphan")


class CustomerJourneyStageModel(BaseModel):
    """Discrete progression stage within a customer journey."""
    __tablename__ = "customer_journey_stages"

    journey_id = Column(String(36), ForeignKey("customer_journeys.id", ondelete="CASCADE"), nullable=False)
    stage_name = Column(String(64), nullable=False)  # DISCOVER, ENGAGE, QUALIFY, CONSIDER, DECIDE, ONBOARD, ADOPT, USE, RECEIVE_VALUE, SUPPORT, RENEW, EXPAND, REFER
    status = Column(String(32), nullable=False, default="IN_PROGRESS")  # PENDING, IN_PROGRESS, COMPLETED, SKIPPED, DROPPED
    entered_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True, default=0)
    drop_off_risk = Column(Float, nullable=False, default=0.10)
    satisfaction_score = Column(Float, nullable=True)

    journey = relationship("CustomerJourneyModel", back_populates="stages")


class CustomerJourneyEventModel(BaseModel):
    """Canonical journey event capturing user and system interactions."""
    __tablename__ = "customer_journey_events"

    journey_id = Column(String(36), ForeignKey("customer_journeys.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(String(36), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)  # PAGE_VIEWED, FORM_COMPLETED, MESSAGE_SENT, MEETING_SCHEDULED, PROPOSAL_VIEWED, CONTRACT_SIGNED, SUPPORT_REQUESTED, PAYMENT_COMPLETED, FEATURE_USED
    stage = Column(String(64), nullable=False, default="AWARENESS")
    channel = Column(String(64), nullable=False, default="PORTAL")  # WEBSITE, EMAIL, MEETING, PHONE, PORTAL, INVOICE, SURVEY, PRODUCT
    actor_type = Column(String(32), nullable=False, default="CUSTOMER")  # CUSTOMER, OPERATOR, AI_AGENT, SYSTEM
    actor_id = Column(String(128), nullable=True)
    payload = Column(JSON, nullable=True, default=dict)
    provenance = Column(String(255), nullable=True)

    journey = relationship("CustomerJourneyModel", back_populates="events")


class CustomerTouchpointModel(BaseModel):
    """Direct or indirect interaction touchpoint between customer and company."""
    __tablename__ = "customer_touchpoints"

    journey_id = Column(String(36), ForeignKey("customer_journeys.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String(64), nullable=False)  # WEBSITE, EMAIL, MEETING, PROPOSAL, CONTRACT, PORTAL, PRODUCT, SUPPORT, INVOICE
    touchpoint_name = Column(String(128), nullable=False)
    purpose = Column(String(255), nullable=True)
    sentiment_label = Column(String(32), nullable=False, default="POSITIVE")  # POSITIVE, NEUTRAL, NEGATIVE, MIXED
    sentiment_score = Column(Float, nullable=False, default=0.8)
    friction_detected = Column(Boolean, nullable=False, default=False)
    customer_feedback = Column(Text, nullable=True)

    journey = relationship("CustomerJourneyModel", back_populates="touchpoints")


class CustomerJourneyVariantModel(BaseModel):
    """Discovered path variant across historical customer journey trajectories."""
    __tablename__ = "customer_journey_variants"

    journey_type = Column(String(64), nullable=False)
    variant_name = Column(String(128), nullable=False)
    path_signature = Column(Text, nullable=False)  # e.g., Website -> Contact -> Meeting -> Proposal -> Won
    frequency_count = Column(Integer, nullable=False, default=1)
    conversion_rate = Column(Float, nullable=False, default=0.65)
    average_duration_days = Column(Float, nullable=False, default=14.0)
    friction_points_count = Column(Integer, nullable=False, default=0)


class CustomerFrictionPointModel(BaseModel):
    """Identified point of friction, delay, confusion, or drop-off in customer journey."""
    __tablename__ = "customer_friction_points"

    journey_id = Column(String(36), ForeignKey("customer_journeys.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(String(36), nullable=False, index=True)
    friction_type = Column(String(64), nullable=False)  # LONG_WAIT, REPEATED_QUESTIONS, CONFUSING_UX, FAILED_ACTIONS, SUPPORT_ESCALATION, PAYMENT_ISSUE, DOCUMENTATION_GAP
    stage = Column(String(64), nullable=False)
    severity = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=True, default=list)
    customer_impact = Column(String(64), nullable=False, default="MODERATE")
    business_impact = Column(String(64), nullable=False, default="MODERATE")
    confidence = Column(Float, nullable=False, default=0.85)
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, MITIGATING, RESOLVED, ACCEPTED

    journey = relationship("CustomerJourneyModel", back_populates="frictions")


class CustomerEffortRecordModel(BaseModel):
    """Customer effort score (CES) and complexity metrics for interactions."""
    __tablename__ = "customer_effort_records"

    customer_id = Column(String(36), nullable=False, index=True)
    journey_id = Column(String(36), nullable=True)
    interaction_type = Column(String(64), nullable=False)
    effort_score = Column(Float, nullable=False, default=2.0)  # 1 (very low effort) to 5 (very high effort)
    effort_tier = Column(String(32), nullable=False, default="LOW_EFFORT")  # LOW_EFFORT, MODERATE_EFFORT, HIGH_EFFORT, CRITICAL_FRICTION
    number_of_steps = Column(Integer, nullable=False, default=2)
    repeated_info_instances = Column(Integer, nullable=False, default=0)
    waiting_time_seconds = Column(Integer, nullable=False, default=120)
    manual_workarounds = Column(JSON, nullable=True, default=list)


class CustomerSentimentRecordModel(BaseModel):
    """Multimodal sentiment and emotion inference with confidence and model provenance."""
    __tablename__ = "customer_sentiment_records"

    customer_id = Column(String(36), nullable=False, index=True)
    source_channel = Column(String(64), nullable=False)
    raw_text_snippet = Column(Text, nullable=True)
    sentiment_label = Column(String(32), nullable=False, default="POSITIVE")  # POSITIVE, NEUTRAL, NEGATIVE, MIXED
    sentiment_score = Column(Float, nullable=False, default=0.75)  # -1.0 to 1.0
    detected_emotions = Column(JSON, nullable=True, default=list)  # Frustration, Confidence, Confusion, Satisfaction, Urgency
    confidence = Column(Float, nullable=False, default=0.88)
    model_version = Column(String(64), nullable=False, default="sentiment-v2.1")
    is_explicit_feedback = Column(Boolean, nullable=False, default=False)


class CustomerGoalModel(BaseModel):
    """Customer-stated business, product, or operational goals."""
    __tablename__ = "customer_goals"

    customer_id = Column(String(36), nullable=False, index=True)
    journey_id = Column(String(36), ForeignKey("customer_journeys.id", ondelete="CASCADE"), nullable=True)
    goal_type = Column(String(64), nullable=False, default="BUSINESS_GOAL")  # BUSINESS_GOAL, PRODUCT_GOAL, PROJECT_GOAL, OPERATIONAL_GOAL, FINANCIAL_GOAL
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    baseline_value = Column(Float, nullable=False, default=0.0)
    target_value = Column(Float, nullable=False, default=100.0)
    current_value = Column(Float, nullable=False, default=65.0)
    progress_percentage = Column(Float, nullable=False, default=65.0)
    status = Column(String(32), nullable=False, default="ON_TRACK")  # ON_TRACK, AT_RISK, ACHIEVED, MISSED

    journey = relationship("CustomerJourneyModel", back_populates="goals")


class CustomerExperienceHealthModel(BaseModel):
    """Composite 10-factor customer experience health evaluation."""
    __tablename__ = "customer_experience_health"

    customer_id = Column(String(36), nullable=False, index=True)
    composite_health_score = Column(Float, nullable=False, default=0.88)
    health_state = Column(String(32), nullable=False, default="HEALTHY")  # EXCELLENT, HEALTHY, STABLE, WATCH, AT_RISK, CRITICAL
    engagement_score = Column(Float, nullable=False, default=0.90)
    adoption_score = Column(Float, nullable=False, default=0.85)
    satisfaction_score = Column(Float, nullable=False, default=0.92)
    effort_efficiency_score = Column(Float, nullable=False, default=0.88)
    goal_progress_score = Column(Float, nullable=False, default=0.80)
    support_health_score = Column(Float, nullable=False, default=0.95)
    financial_health_score = Column(Float, nullable=False, default=0.98)
    relationship_strength_score = Column(Float, nullable=False, default=0.85)
    factors_breakdown = Column(JSON, nullable=False, default=dict)
    findings = Column(JSON, nullable=True, default=list)


class CustomerChurnPredictionModel(BaseModel):
    """Explainable churn risk prediction with feature attributions."""
    __tablename__ = "customer_churn_predictions"

    customer_id = Column(String(36), nullable=False, index=True)
    churn_probability = Column(Float, nullable=False, default=0.12)  # 0.0 to 1.0
    risk_level = Column(String(32), nullable=False, default="LOW")  # LOW, MODERATE, ELEVATED, CRITICAL
    top_risk_signals = Column(JSON, nullable=False, default=list)  # Usage Decline, Negative Sentiment, Support Escalations
    recommended_interventions = Column(JSON, nullable=True, default=list)
    confidence = Column(Float, nullable=False, default=0.89)
    model_version = Column(String(64), nullable=False, default="churn-ensemble-v3.0")


class CustomerRetentionOpportunityModel(BaseModel):
    """Targeted retention action and intervention plan."""
    __tablename__ = "customer_retention_opportunities"

    customer_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    root_cause = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    urgency = Column(String(32), nullable=False, default="HIGH")
    expected_ltv_impact_usd = Column(Float, nullable=False, default=15000.0)
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, IN_REVIEW, ACTIONED, RESOLVED


class CustomerExpansionOpportunityModel(BaseModel):
    """Upsell, cross-sell, and license expansion intelligence signal."""
    __tablename__ = "customer_expansion_opportunities"

    customer_id = Column(String(36), nullable=False, index=True)
    opportunity_type = Column(String(64), nullable=False)  # ADDITIONAL_PRODUCT, CAPACITY_UPGRADE, AI_MODULE, AUTOMATION_SUITE
    title = Column(String(255), nullable=False)
    rationale = Column(Text, nullable=False)
    estimated_arr_expansion_usd = Column(Float, nullable=False, default=24000.0)
    readiness_score = Column(Float, nullable=False, default=0.85)
    evidence = Column(JSON, nullable=True, default=list)
    status = Column(String(32), nullable=False, default="IDENTIFIED")  # IDENTIFIED, IN_DISCOVERY, PROPOSED, CLOSED_WON, DISMISSED


class CustomerAdvocacyRecordModel(BaseModel):
    """Customer testimonials, case studies, reviews, and advocacy activities."""
    __tablename__ = "customer_advocacy_records"

    customer_id = Column(String(36), nullable=False, index=True)
    advocacy_type = Column(String(64), nullable=False)  # TESTIMONIAL, CASE_STUDY, REVIEW, ADVISORY_BOARD, SPEAKER
    summary = Column(Text, nullable=False)
    permission_granted = Column(Boolean, nullable=False, default=True)
    is_public = Column(Boolean, nullable=False, default=False)
    sentiment_rating = Column(Float, nullable=False, default=5.0)


class CustomerReferralModel(BaseModel):
    """Referral attribution, pipeline contribution, and reward tracking."""
    __tablename__ = "customer_referrals"

    referrer_customer_id = Column(String(36), nullable=False, index=True)
    referred_organization_name = Column(String(255), nullable=False)
    referred_contact_email = Column(String(255), nullable=True)
    status = Column(String(32), nullable=False, default="QUALIFYING")  # SUBMITTED, QUALIFYING, PROPOSAL, WON, LOST
    pipeline_value_usd = Column(Float, nullable=False, default=35000.0)


class CustomerSegmentModel(BaseModel):
    """Behavioral and firmographic experience segment."""
    __tablename__ = "customer_segments"

    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    criteria = Column(JSON, nullable=False, default=dict)
    customer_count = Column(Integer, nullable=False, default=0)
    average_health_score = Column(Float, nullable=False, default=0.88)
    churn_rate = Column(Float, nullable=False, default=0.03)


class CustomerPersonaModel(BaseModel):
    """Evidence-grounded buyer and operator persona."""
    __tablename__ = "customer_personas"

    title = Column(String(128), nullable=False)  # Decision Maker, Technical Lead, Revenue Operator
    key_priorities = Column(JSON, nullable=True, default=list)
    primary_frictions = Column(JSON, nullable=True, default=list)
    preferred_channels = Column(JSON, nullable=True, default=list)
    evidence_count = Column(Integer, nullable=False, default=12)


class CustomerVoiceRecordModel(BaseModel):
    """Normalized Voice of Customer (VoC) feedback atom."""
    __tablename__ = "customer_voice_records"

    customer_id = Column(String(36), nullable=False, index=True)
    source_type = Column(String(64), nullable=False)  # MEETING, SUPPORT_TICKET, REVIEW, SURVEY, INTERVIEW, CHAT
    raw_content = Column(Text, nullable=False)
    classified_intent = Column(String(64), nullable=False, default="FEATURE_REQUEST")
    extracted_needs = Column(JSON, nullable=True, default=list)
    theme = Column(String(128), nullable=True)
    sentiment_score = Column(Float, nullable=False, default=0.5)


class CustomerVoiceThemeModel(BaseModel):
    """Aggregated Voice of Customer emergent thematic cluster."""
    __tablename__ = "customer_voice_themes"

    theme_name = Column(String(128), nullable=False)
    frequency = Column(Integer, nullable=False, default=1)
    severity = Column(String(32), nullable=False, default="MEDIUM")
    average_sentiment = Column(Float, nullable=False, default=0.4)
    sample_quotes = Column(JSON, nullable=True, default=list)
    affected_customer_ids = Column(JSON, nullable=True, default=list)


class CustomerExpectationGapModel(BaseModel):
    """Expectation gap analysis comparing PROMISED vs EXPECTED vs DELIVERED vs EXPERIENCED."""
    __tablename__ = "customer_expectation_gaps"

    customer_id = Column(String(36), nullable=False, index=True)
    journey_stage = Column(String(64), nullable=False)
    promised_statement = Column(Text, nullable=False)  # SOW/Proposal contract commitment
    expected_statement = Column(Text, nullable=False)  # Customer perceived expectation
    delivered_statement = Column(Text, nullable=False)  # Actual operational deliverable
    gap_severity = Column(String(32), nullable=False, default="LOW")  # LOW, MODERATE, CRITICAL
    mitigation_plan = Column(Text, nullable=True)


class CustomerExperienceExperimentModel(BaseModel):
    """A/B test and journey optimization experiment with guardrail metrics."""
    __tablename__ = "customer_experience_experiments"

    journey_stage = Column(String(64), nullable=False)
    title = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=False)
    primary_metric = Column(String(128), nullable=False)  # e.g., Onboarding Time Reduction
    control_flow = Column(Text, nullable=False)
    treatment_flow = Column(Text, nullable=False)
    guardrail_metrics = Column(JSON, nullable=True, default=list)
    sample_size = Column(Integer, nullable=False, default=200)
    p_value = Column(Float, nullable=True)
    status = Column(String(32), nullable=False, default="RUNNING")  # RUNNING, COMPLETED, CANCELLED


class CustomerExperienceAlertModel(BaseModel):
    """Real-time customer experience anomaly, churn risk, or escalation alert."""
    __tablename__ = "customer_experience_alerts"

    customer_id = Column(String(36), nullable=False, index=True)
    alert_type = Column(String(64), nullable=False)  # CHURN_RISK, HEALTH_DECLINE, HIGH_FRICTION, SUPPORT_ESCALATION, PAYMENT_ISSUE, GOAL_FAILURE
    severity = Column(String(32), nullable=False, default="WARNING")  # INFO, WARNING, CRITICAL, BLOCKING
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=True, default=list)
    is_acknowledged = Column(Boolean, nullable=False, default=False)
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, ACKNOWLEDGED, RESOLVED
