"""
Phase 59: Unified Marketing Intelligence, Demand Generation, Content Strategy & Marketing Automation Platform Models
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MarketingAudienceModel(Base):
    __tablename__ = "marketing_audiences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_icp: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_size_tier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    buying_context: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    primary_pain_points: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    channel_preferences: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    total_market_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reachable_market_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class MarketingSegmentModel(Base):
    __tablename__ = "marketing_segments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audience_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    segment_type: Mapped[str] = mapped_column(String(50), default="BEHAVIORAL", nullable=False)
    criteria: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    account_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_revenue_potential_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingPersonaModel(Base):
    __tablename__ = "marketing_personas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audience_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    role_type: Mapped[str] = mapped_column(String(50), default="DECISION_MAKER", nullable=False)
    assumption_status: Mapped[str] = mapped_column(String(50), default="OBSERVED", nullable=False)
    core_responsibilities: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    top_priorities: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    key_objections: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    preferred_content_formats: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingPositioningModel(Base):
    __tablename__ = "marketing_positioning"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audience_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="CASCADE"), nullable=False)
    target_customer: Mapped[str] = mapped_column(String(255), nullable=False)
    problem_statement: Mapped[str] = mapped_column(Text, nullable=False)
    alternative_solution: Mapped[str] = mapped_column(Text, nullable=False)
    our_solution: Mapped[str] = mapped_column(Text, nullable=False)
    key_differentiators: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    value_statement: Mapped[str] = mapped_column(Text, nullable=False)
    proof_points: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingMessageHouseModel(Base):
    __tablename__ = "marketing_message_houses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    positioning_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_positioning.id", ondelete="CASCADE"), nullable=False)
    core_message: Mapped[str] = mapped_column(Text, nullable=False)
    pillar_1: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    pillar_2: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    pillar_3: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    call_to_action: Mapped[str] = mapped_column(String(255), nullable=False)
    forbidden_terms: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    preferred_terms: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ContentAssetModel(Base):
    __tablename__ = "content_assets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="ARTICLE", nullable=False)
    journey_stage: Mapped[str] = mapped_column(String(50), default="AWARENESS", nullable=False)
    target_audience_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    body_markdown: Mapped[str] = mapped_column(Text, default="", nullable=False)
    primary_cta: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    revenue_influenced_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ContentAssetVersionModel(Base):
    __tablename__ = "content_asset_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("content_assets.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(100), default="system", nullable=False)
    change_summary: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ContentBriefModel(Base):
    __tablename__ = "content_briefs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_topic: Mapped[str] = mapped_column(String(255), nullable=False)
    target_audience_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="SET NULL"), nullable=True)
    journey_stage: Mapped[str] = mapped_column(String(50), default="AWARENESS", nullable=False)
    search_intent: Mapped[str] = mapped_column(String(50), default="INFORMATIONAL", nullable=False)
    key_takeaways: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    primary_keywords: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    required_evidence_sources: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ContentClaimModel(Base):
    __tablename__ = "content_claims"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("content_assets.id", ondelete="CASCADE"), nullable=False)
    claim_text: Mapped[str] = mapped_column(Text, nullable=False)
    source_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    source_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence_pct: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    verification_status: Mapped[str] = mapped_column(String(50), default="VERIFIED", nullable=False)
    reviewer_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ContentApprovalModel(Base):
    __tablename__ = "content_approvals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("content_assets.id", ondelete="CASCADE"), nullable=False)
    approver: Mapped[str] = mapped_column(String(100), nullable=False)
    approval_type: Mapped[str] = mapped_column(String(50), default="EDITORIAL", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="APPROVED", nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ContentGapModel(Base):
    __tablename__ = "content_gaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    target_audience: Mapped[str] = mapped_column(String(100), nullable=False)
    journey_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    demand_volume: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)
    revenue_potential_usd: Mapped[float] = mapped_column(Float, default=50000.0, nullable=False)
    effort_tier: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)
    priority_score: Mapped[float] = mapped_column(Float, default=8.5, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class BrandVoiceProfileModel(Base):
    __tablename__ = "brand_voice_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), default="Default Brand Voice", nullable=False)
    primary_tone: Mapped[str] = mapped_column(String(50), default="AUTHORITATIVE_EMPATHETIC", nullable=False)
    reading_level: Mapped[str] = mapped_column(String(50), default="PROFESSIONAL", nullable=False)
    prohibited_claims: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    preferred_vocab: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingCampaignModel(Base):
    __tablename__ = "marketing_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    campaign_type: Mapped[str] = mapped_column(String(50), default="DEMAND_GENERATION", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False)
    target_audience_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="SET NULL"), nullable=True)
    allocated_budget_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    actual_spend_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    leads_generated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mql_generated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sql_generated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    opportunities_influenced: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pipeline_influenced_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    revenue_attributed_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    channels: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    owner: Mapped[str] = mapped_column(String(100), default="growth_lead", nullable=False)
    is_governance_approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class MarketingCampaignVersionModel(Base):
    __tablename__ = "marketing_campaign_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_campaigns.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingChannelModel(Base):
    __tablename__ = "marketing_channels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    channel_type: Mapped[str] = mapped_column(String(50), default="ORGANIC_SEARCH", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    total_spend_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_revenue_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_cac_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_roas: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingChannelMetricModel(Base):
    __tablename__ = "marketing_channel_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_channels.id", ondelete="CASCADE"), nullable=False)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    impressions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    leads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mql: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    spend_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    revenue_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EmailCampaignModel(Base):
    __tablename__ = "email_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_campaigns.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    subject_line: Mapped[str] = mapped_column(String(255), nullable=False)
    preview_text: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sender_name: Mapped[str] = mapped_column(String(100), default="North's Advisory", nullable=False)
    sender_email: Mapped[str] = mapped_column(String(150), default="insights@norths.io", nullable=False)
    recipients_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    delivered_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    opened_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    clicked_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    unsubscribed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EmailTemplateModel(Base):
    __tablename__ = "email_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="NURTURE", nullable=False)
    body_html: Mapped[str] = mapped_column(Text, nullable=False)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EmailSequenceModel(Base):
    __tablename__ = "email_sequences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_audience_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="SET NULL"), nullable=True)
    steps: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    enrolled_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EmailSuppressionModel(Base):
    __tablename__ = "email_suppressions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    reason: Mapped[str] = mapped_column(String(50), default="UNSUBSCRIBE", nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="user_opt_out", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingLeadModel(Base):
    __tablename__ = "marketing_leads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_channel: Mapped[str] = mapped_column(String(100), default="ORGANIC_SEARCH", nullable=False)
    first_touch_campaign: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_touch_campaign: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    fit_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    engagement_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    intent_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    composite_lead_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    qualification_stage: Mapped[str] = mapped_column(String(50), default="NEW", nullable=False)
    consent_obtained: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_suppressed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class MarketingLeadScoreModel(Base):
    __tablename__ = "marketing_lead_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_leads.id", ondelete="CASCADE"), nullable=False)
    fit_breakdown: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    engagement_breakdown: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    intent_breakdown: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingNurtureProgramModel(Base):
    __tablename__ = "marketing_nurture_programs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    goal: Mapped[str] = mapped_column(String(255), nullable=False)
    entry_conditions: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    exit_conditions: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    active_leads_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    converted_leads_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingFunnelMetricModel(Base):
    __tablename__ = "marketing_funnel_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    impressions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    visitors: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    leads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mql: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sql: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    opportunities: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    deals_won: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversion_rate_lead_to_mql_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    conversion_rate_mql_to_sql_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    conversion_rate_sql_to_won_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_funnel_velocity_days: Mapped[float] = mapped_column(Float, default=28.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingAttributionRecordModel(Base):
    __tablename__ = "marketing_attribution_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    deal_value_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    attribution_model: Mapped[str] = mapped_column(String(50), default="MULTI_TOUCH_W_SHAPED", nullable=False)
    touches: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    campaign_credits: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    channel_credits: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingBudgetModel(Base):
    __tablename__ = "marketing_budgets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    total_planned_budget_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_committed_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_spent_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    channel_allocations: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingRoiRecordModel(Base):
    __tablename__ = "marketing_roi_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    total_spend_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_attributed_revenue_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cost_per_lead_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cost_per_mql_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cost_per_acquisition_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    roas: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    roi_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingExperimentModel(Base):
    __tablename__ = "marketing_experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    experiment_type: Mapped[str] = mapped_column(String(50), default="LANDING_PAGE_CTA", nullable=False)
    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    variants: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    confidence_level_pct: Mapped[float] = mapped_column(Float, default=95.0, nullable=False)
    winner_variant: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="RUNNING", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class LandingPageModel(Base):
    __tablename__ = "landing_pages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    target_campaign_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_campaigns.id", ondelete="SET NULL"), nullable=True)
    visitors_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    submissions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversion_rate_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class SeoKeywordModel(Base):
    __tablename__ = "seo_keywords"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keyword: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    monthly_search_volume: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    keyword_difficulty: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    search_intent: Mapped[str] = mapped_column(String(50), default="INFORMATIONAL", nullable=False)
    current_ranking: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_content_asset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("content_assets.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingEventModel(Base):
    __tablename__ = "marketing_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), default="WEBINAR", nullable=False)
    registrations_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attendees_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    leads_generated_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingCalendarEventModel(Base):
    __tablename__ = "marketing_calendar_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), default="CAMPAIGN_LAUNCH", nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="EMAIL", nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    has_conflict: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingForecastModel(Base):
    __tablename__ = "marketing_forecasts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    scenario: Mapped[str] = mapped_column(String(50), default="BASE", nullable=False)
    p10_leads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p25_leads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p50_leads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p75_leads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p90_leads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p50_pipeline_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    p50_revenue_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), default="v1.0-monte-carlo", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingRiskRecordModel(Base):
    __tablename__ = "marketing_risks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    risk_category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)
    mitigation_strategy: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MarketingFatigueRecordModel(Base):
    __tablename__ = "marketing_fatigue_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audience_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("marketing_audiences.id", ondelete="SET NULL"), nullable=True)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    weekly_frequency: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    unsubscribe_rate_pct: Mapped[float] = mapped_column(Float, default=0.2, nullable=False)
    engagement_decay_pct: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    fatigue_level: Mapped[str] = mapped_column(String(50), default="NORMAL", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
