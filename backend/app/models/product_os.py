"""
Phase 60: Unified Product Management, Product Intelligence, Roadmap & Product Lifecycle Operating System Models
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


class ProductPortfolioItemModel(Base):
    __tablename__ = "product_portfolio_items"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_line: Mapped[str] = mapped_column(String(100), default="Core Platform", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lifecycle_state: Mapped[str] = mapped_column(String(50), default="DEVELOPMENT", nullable=False)
    target_market: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    owner: Mapped[str] = mapped_column(String(100), default="product_lead", nullable=False)
    arr_contribution_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    active_accounts_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ProductVisionModel(Base):
    __tablename__ = "product_visions"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    vision_statement: Mapped[str] = mapped_column(Text, nullable=False)
    target_users: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    core_differentiator: Mapped[str] = mapped_column(Text, nullable=False)
    strategic_fit: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductStrategyModel(Base):
    __tablename__ = "product_strategies"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    strategic_pillars: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    competitive_moat: Mapped[str] = mapped_column(Text, nullable=False)
    growth_motion: Mapped[str] = mapped_column(String(50), default="PRODUCT_LED_SALES_ASSISTED", nullable=False)
    product_bets: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductObjectiveModel(Base):
    __tablename__ = "product_objectives"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    objective_title: Mapped[str] = mapped_column(String(255), nullable=False)
    quarter: Mapped[str] = mapped_column(String(50), nullable=False)
    key_results: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    progress_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="IN_PROGRESS", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductProblemModel(Base):
    __tablename__ = "product_problems"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="SET NULL"), nullable=True)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    target_segment: Mapped[str] = mapped_column(String(100), nullable=False)
    validation_status: Mapped[str] = mapped_column(String(50), default="VALIDATED", nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), default="MEASURED", nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)
    cost_of_inaction_usd: Mapped[float] = mapped_column(Float, default=50000.0, nullable=False)
    customer_mentions_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductFeedbackItemModel(Base):
    __tablename__ = "product_feedback_items"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("product_problems.id", ondelete="SET NULL"), nullable=True)
    customer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    source_channel: Mapped[str] = mapped_column(String(50), default="SUPPORT", nullable=False)
    feedback_text: Mapped[str] = mapped_column(Text, nullable=False)
    feedback_category: Mapped[str] = mapped_column(String(50), default="USABILITY_ISSUE", nullable=False)
    arr_impact_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductFeedbackThemeModel(Base):
    __tablename__ = "product_feedback_themes"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    theme_title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="CORE_WORKFLOW", nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    affected_arr_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductInsightModel(Base):
    __tablename__ = "product_insights"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    insight_text: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_sources: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    confidence_pct: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    impact_area: Mapped[str] = mapped_column(String(100), default="User Activation", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductOpportunityModel(Base):
    __tablename__ = "product_opportunities"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    problem_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("product_problems.id", ondelete="SET NULL"), nullable=True)
    customer_value_score: Mapped[float] = mapped_column(Float, default=8.0, nullable=False)
    business_value_score: Mapped[float] = mapped_column(Float, default=8.5, nullable=False)
    strategic_fit_score: Mapped[float] = mapped_column(Float, default=9.0, nullable=False)
    estimated_arr_gain_usd: Mapped[float] = mapped_column(Float, default=100000.0, nullable=False)
    composite_opportunity_score: Mapped[float] = mapped_column(Float, default=8.5, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="IDENTIFIED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductPrioritizationScoreModel(Base):
    __tablename__ = "product_prioritization_scores"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_opportunities.id", ondelete="CASCADE"), nullable=False)
    framework: Mapped[str] = mapped_column(String(50), default="RICE", nullable=False)
    reach: Mapped[float] = mapped_column(Float, default=1000.0, nullable=False)
    impact: Mapped[float] = mapped_column(Float, default=3.0, nullable=False)
    confidence_pct: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)
    effort_person_weeks: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    final_score: Mapped[float] = mapped_column(Float, default=600.0, nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductRoadmapModel(Base):
    __tablename__ = "product_roadmaps"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductRoadmapItemModel(Base):
    __tablename__ = "product_roadmap_items"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_roadmaps.id", ondelete="CASCADE"), nullable=False)
    opportunity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("product_opportunities.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    horizon: Mapped[str] = mapped_column(String(50), default="NOW", nullable=False)
    quarter: Mapped[str] = mapped_column(String(50), default="2026-Q4", nullable=False)
    engineering_effort_weeks: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    dependencies: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    delivery_risk: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PLANNED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductRequirementItemModel(Base):
    __tablename__ = "product_requirements"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_item_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("product_roadmap_items.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    requirement_type: Mapped[str] = mapped_column(String(50), default="FUNCTIONAL", nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    target_persona: Mapped[str] = mapped_column(String(100), default="Managing Partner", nullable=False)
    is_governance_reviewed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="SPECIFIED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductUserStoryModel(Base):
    __tablename__ = "product_user_stories"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requirement_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_requirements.id", ondelete="CASCADE"), nullable=False)
    story_narrative: Mapped[str] = mapped_column(Text, nullable=False)
    given_clause: Mapped[str] = mapped_column(Text, nullable=False)
    when_clause: Mapped[str] = mapped_column(Text, nullable=False)
    then_clause: Mapped[str] = mapped_column(Text, nullable=False)
    story_points: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="READY_FOR_DEV", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductFeatureAdoptionModel(Base):
    __tablename__ = "product_feature_adoptions"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    feature_name: Mapped[str] = mapped_column(String(255), nullable=False)
    eligible_users: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active_users: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    adoption_rate_pct: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    frequency_per_week: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    customer_value_rating: Mapped[float] = mapped_column(Float, default=4.5, nullable=False)
    measured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductHealthScorecardModel(Base):
    __tablename__ = "product_health_scorecards"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    composite_health_state: Mapped[str] = mapped_column(String(50), default="HEALTHY", nullable=False)
    adoption_score: Mapped[float] = mapped_column(Float, default=85.0, nullable=False)
    retention_score: Mapped[float] = mapped_column(Float, default=92.0, nullable=False)
    reliability_score: Mapped[float] = mapped_column(Float, default=99.9, nullable=False)
    feedback_sentiment_score: Mapped[float] = mapped_column(Float, default=88.0, nullable=False)
    support_efficiency_score: Mapped[float] = mapped_column(Float, default=90.0, nullable=False)
    quality_score: Mapped[float] = mapped_column(Float, default=95.0, nullable=False)
    economics_margin_score: Mapped[float] = mapped_column(Float, default=84.0, nullable=False)
    measured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductLaunchPlanModel(Base):
    __tablename__ = "product_launch_plans"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    release_version: Mapped[str] = mapped_column(String(50), nullable=False)
    release_strategy: Mapped[str] = mapped_column(String(50), default="FEATURE_FLAGGED_PHASED", nullable=False)
    checklist: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_ready: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    scheduled_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductFeatureFlagModel(Base):
    __tablename__ = "product_feature_flags"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flag_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    rollout_pct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    target_environments: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    owner: Mapped[str] = mapped_column(String(100), default="release_engineer", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductUnitEconomicsModel(Base):
    __tablename__ = "product_unit_economics"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    arpu_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cogs_per_user_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    gross_margin_pct: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)
    support_cost_per_user_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    ltv_to_cac_ratio: Mapped[float] = mapped_column(Float, default=4.2, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductForecastModel(Base):
    __tablename__ = "product_forecasts"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="CASCADE"), nullable=False)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    scenario: Mapped[str] = mapped_column(String(50), default="BASE", nullable=False)
    p10_active_users: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p50_active_users: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p90_active_users: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    p50_arr_contribution_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), default="v1.0-monte-carlo", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ProductRiskRecordModel(Base):
    __tablename__ = "product_risks"
    __table_args__ = {"extend_existing": True}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("product_portfolio_items.id", ondelete="SET NULL"), nullable=True)
    risk_category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)
    mitigation_strategy: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
