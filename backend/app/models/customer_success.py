"""SQLAlchemy ORM Models for Unified Client Relationship Intelligence & Customer Success."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text

from app.models.base import Base

JSON_TYPE = JSON


class ClientProfileModel(Base):
    """Core customer success profile with lifecycle stage, ownership, and relationship strength."""
    __tablename__ = "client_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_account_id = Column(String(36), nullable=False, index=True)
    business_id = Column(String(36), nullable=True, index=True)
    business_name = Column(String(255), nullable=False)
    lifecycle_stage = Column(String(50), nullable=False, default="ACTIVE", index=True)
    relationship_strength = Column(String(50), nullable=False, default="ESTABLISHED")
    
    # Ownership mappings
    relationship_owner_id = Column(String(36), nullable=True)
    sales_owner_id = Column(String(36), nullable=True)
    project_owner_id = Column(String(36), nullable=True)
    cs_owner_id = Column(String(36), nullable=True)

    target_contract_value = Column(Numeric(18, 2), nullable=True)
    ltv_estimate = Column(Numeric(18, 2), nullable=True)
    churn_risk_band = Column(String(50), nullable=False, default="LOW")
    summary = Column(Text, nullable=True)
    metadata_json = Column(JSON_TYPE, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ClientRelationshipModel(Base):
    """Key organization contacts and their decision-making roles."""
    __tablename__ = "client_relationships"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    contact_id = Column(String(36), nullable=False, index=True)
    contact_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=True)
    role_title = Column(String(100), nullable=True)
    decision_role = Column(String(50), nullable=False, default="USER")  # DECISION_MAKER, CHAMPION, INFLUENCER, USER, etc.
    relationship_strength = Column(String(50), nullable=False, default="ESTABLISHED")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientTimelineEventModel(Base):
    """Chronological event stream across communications, delivery, financials, and support."""
    __tablename__ = "client_timeline_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    actor_type = Column(String(50), nullable=False, default="SYSTEM")
    actor_id = Column(String(36), nullable=True)
    source_entity_type = Column(String(100), nullable=True)
    source_entity_id = Column(String(36), nullable=True)
    payload = Column(JSON_TYPE, nullable=True)
    occurred_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientGoalModel(Base):
    """Strategic business outcomes and target metrics agreed upon with client."""
    __tablename__ = "client_goals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), nullable=False, default="MEDIUM")
    owner_id = Column(String(36), nullable=True)
    target_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), nullable=False, default="IN_PROGRESS")
    success_metric = Column(String(255), nullable=True)
    target_value = Column(String(100), nullable=True)
    current_value = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientSuccessPlanModel(Base):
    """Formal customer success plans and strategic action roadmaps."""
    __tablename__ = "client_success_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE")
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    target_completion_date = Column(DateTime(timezone=True), nullable=True)
    approved_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientSuccessTaskModel(Base):
    """Actionable tasks tied to customer success plans and goals."""
    __tablename__ = "client_success_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    plan_id = Column(String(36), ForeignKey("client_success_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = Column(String(36), nullable=True)
    client_profile_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), nullable=False, default="MEDIUM")
    status = Column(String(50), nullable=False, default="PENDING")
    assigned_to_user_id = Column(String(36), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientHealthScoreModel(Base):
    """Current calibrated multi-factor health score."""
    __tablename__ = "client_health_scores"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    overall_score = Column(Numeric(5, 2), nullable=False, default=0.00)
    health_band = Column(String(50), nullable=False, default="HEALTHY")
    confidence = Column(String(50), nullable=False, default="HIGH")
    trend = Column(String(50), nullable=False, default="STABLE")

    # Granular component factor scores
    engagement_score = Column(Numeric(5, 2), nullable=True)
    project_score = Column(Numeric(5, 2), nullable=True)
    support_score = Column(Numeric(5, 2), nullable=True)
    finance_score = Column(Numeric(5, 2), nullable=True)
    satisfaction_score = Column(Numeric(5, 2), nullable=True)
    relationship_score = Column(Numeric(5, 2), nullable=True)
    goal_score = Column(Numeric(5, 2), nullable=True)

    positive_factors = Column(JSON_TYPE, nullable=True)
    risk_factors = Column(JSON_TYPE, nullable=True)
    explanation = Column(Text, nullable=True)
    calculated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientHealthHistoryModel(Base):
    """Historical health snapshots for trend detection."""
    __tablename__ = "client_health_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Numeric(5, 2), nullable=False)
    health_band = Column(String(50), nullable=False)
    trend = Column(String(50), nullable=False)
    factor_breakdown = Column(JSON_TYPE, nullable=True)
    confidence = Column(String(50), nullable=False, default="HIGH")
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class ClientSurveyModel(Base):
    """Customer satisfaction surveys (CSAT, NPS, CES, Milestone, QBR)."""
    __tablename__ = "client_surveys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    survey_type = Column(String(50), nullable=False, default="CSAT")
    title = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="DRAFT")  # DRAFT, SCHEDULED, SENT, RESPONDED, ANALYZED
    scheduled_date = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    responses_count = Column(Integer, default=0, nullable=False)
    avg_score = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientSurveyResponseModel(Base):
    """Individual survey response and feedback ratings."""
    __tablename__ = "client_survey_responses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    survey_id = Column(String(36), ForeignKey("client_surveys.id", ondelete="CASCADE"), nullable=False, index=True)
    client_profile_id = Column(String(36), nullable=False, index=True)
    contact_id = Column(String(36), nullable=True)
    score = Column(Numeric(5, 2), nullable=False)
    csat = Column(Integer, nullable=True)
    nps = Column(Integer, nullable=True)
    ces = Column(Integer, nullable=True)
    raw_feedback = Column(Text, nullable=True)
    sentiment = Column(String(50), nullable=False, default="NEUTRAL")
    analyzed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientSentimentAnalysisModel(Base):
    """Evidence-grounded sentiment analysis derived from communications."""
    __tablename__ = "client_sentiment_analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    source_message_id = Column(String(36), nullable=True)
    source_type = Column(String(50), nullable=False, default="MESSAGE")  # MESSAGE, MEETING_NOTE, SURVEY, TICKET
    sentiment_label = Column(String(50), nullable=False, default="NEUTRAL")
    confidence = Column(String(50), nullable=False, default="MEDIUM")
    summary = Column(Text, nullable=True)
    model_version = Column(String(50), nullable=False, default="1.0")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientRiskModel(Base):
    """Proactively detected relationship, financial, delivery, or support risks."""
    __tablename__ = "client_risks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    risk_category = Column(String(50), nullable=False, default="RELATIONSHIP")
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(50), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), nullable=False, default="OPEN")  # OPEN, IN_REVIEW, MITIGATED, RESOLVED
    confidence = Column(String(50), nullable=False, default="MEDIUM")
    evidence = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    assigned_to_user_id = Column(String(36), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientOpportunityModel(Base):
    """Evidence-backed expansion, cross-sell, and upsell candidate recommendations."""
    __tablename__ = "client_opportunities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    opportunity_type = Column(String(50), nullable=False, default="EXPANSION")
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    estimated_value = Column(Numeric(18, 2), nullable=True)
    confidence = Column(String(50), nullable=False, default="MEDIUM")
    status = Column(String(50), nullable=False, default="IDENTIFIED")  # IDENTIFIED, IN_REVIEW, QUALIFIED, CONVERTED, DECLINED
    evidence = Column(Text, nullable=True)
    recommended_next_step = Column(Text, nullable=True)
    target_service_id = Column(String(36), nullable=True)
    linked_requirement_id = Column(String(36), nullable=True)
    created_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientRenewalModel(Base):
    """Contract renewal tracking, preparation, and negotiation lifecycles."""
    __tablename__ = "client_renewals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    contract_id = Column(String(36), nullable=True)
    expiration_date = Column(DateTime(timezone=True), nullable=False)
    renewal_window_start = Column(DateTime(timezone=True), nullable=False)
    renewal_window_end = Column(DateTime(timezone=True), nullable=False)
    contract_value = Column(Numeric(18, 2), nullable=False)
    status = Column(String(50), nullable=False, default="UPCOMING")
    probability_pct = Column(Numeric(5, 2), nullable=True)
    owner_id = Column(String(36), nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientReferralModel(Base):
    """Referral attribution, referred business tracking, and commercial ROI."""
    __tablename__ = "client_referrals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    referred_business_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, default="IDENTIFIED")  # IDENTIFIED, INTRODUCED, CONTACTED, QUALIFIED, CONVERTED, LOST
    lead_id = Column(String(36), nullable=True)
    converted_revenue = Column(Numeric(18, 2), nullable=False, default=0.00)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientSegmentModel(Base):
    """Dynamic client categorization rules and segment governance."""
    __tablename__ = "client_segments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    segment_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    rules = Column(JSON_TYPE, nullable=False)
    is_dynamic = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientAccountPlanModel(Base):
    """Strategic account plans and organizational relationship maps."""
    __tablename__ = "client_account_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    status = Column(String(50), nullable=False, default="DRAFT")
    relationship_map = Column(JSON_TYPE, nullable=True)
    service_summary = Column(Text, nullable=True)
    risk_summary = Column(Text, nullable=True)
    opportunity_summary = Column(Text, nullable=True)
    next_steps = Column(Text, nullable=True)
    review_date = Column(DateTime(timezone=True), nullable=True)
    owner_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ClientReviewModel(Base):
    """Account reviews, QBRs, agendas, and documented outcomes."""
    __tablename__ = "client_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    client_profile_id = Column(String(36), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    review_type = Column(String(50), nullable=False, default="QBR")  # QBR, HEALTH_CHECK, ONBOARDING, RENEWAL
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    summary_notes = Column(Text, nullable=True)
    action_items = Column(JSON_TYPE, nullable=True)
    attendees = Column(JSON_TYPE, nullable=True)
    status = Column(String(50), nullable=False, default="SCHEDULED")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
