"""SQLAlchemy ORM Models for Phase 58: Unified Revenue Growth, Go-to-Market Intelligence & Commercial Optimization Platform."""
from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class GtmStrategyModel(Base):
    __tablename__ = "gtm_strategies"

    id = Column(String(64), primary_key=True, default=lambda: f"gtm-{uuid.uuid4().hex[:12]}")
    name = Column(String(255), nullable=False)
    target_market = Column(String(255), nullable=False)
    sales_motion = Column(String(64), nullable=False, default="consultative")
    positioning = Column(Text, nullable=True)
    value_proposition = Column(Text, nullable=True)
    status = Column(String(64), nullable=False, default="active")
    channels = Column(JSON, nullable=True)
    metrics_targets = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class GtmSegmentModel(Base):
    __tablename__ = "gtm_segments"

    id = Column(String(64), primary_key=True, default=lambda: f"seg-{uuid.uuid4().hex[:12]}")
    strategy_id = Column(String(64), ForeignKey("gtm_strategies.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    industry = Column(String(128), nullable=True)
    company_size_tier = Column(String(64), nullable=False, default="mid_market")
    estimated_tam_usd = Column(Float, nullable=False, default=0.0)
    estimated_sam_usd = Column(Float, nullable=False, default=0.0)
    priority_tier = Column(String(32), nullable=False, default="tier_1")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class GtmIcpModel(Base):
    __tablename__ = "gtm_icps"

    id = Column(String(64), primary_key=True, default=lambda: f"icp-{uuid.uuid4().hex[:12]}")
    segment_id = Column(String(64), ForeignKey("gtm_segments.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    target_industries = Column(JSON, nullable=True)
    min_employee_count = Column(Integer, nullable=False, default=50)
    max_employee_count = Column(Integer, nullable=False, default=5000)
    min_arr_usd = Column(Float, nullable=False, default=5000000.0)
    required_tech_profile = Column(JSON, nullable=True)
    pain_points = Column(JSON, nullable=True)
    buying_signals = Column(JSON, nullable=True)
    exclusions = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class TargetAccountModel(Base):
    __tablename__ = "target_accounts"

    id = Column(String(64), primary_key=True, default=lambda: f"acc-{uuid.uuid4().hex[:12]}")
    company_name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=True, index=True)
    industry = Column(String(128), nullable=True)
    employee_count = Column(Integer, nullable=False, default=100)
    estimated_annual_revenue = Column(Float, nullable=False, default=0.0)
    country = Column(String(64), nullable=True)
    icp_fit_score = Column(Float, nullable=False, default=0.0)
    priority_level = Column(String(32), nullable=False, default="medium")
    coverage_status = Column(String(64), nullable=False, default="discovered")
    assigned_rep = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class TargetAccountScoreModel(Base):
    __tablename__ = "target_account_scores"

    id = Column(String(64), primary_key=True, default=lambda: f"sc-{uuid.uuid4().hex[:12]}")
    account_id = Column(String(64), ForeignKey("target_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    icp_fit = Column(Float, nullable=False, default=0.0)
    business_need = Column(Float, nullable=False, default=0.0)
    digital_gap = Column(Float, nullable=False, default=0.0)
    revenue_potential = Column(Float, nullable=False, default=0.0)
    buying_signal = Column(Float, nullable=False, default=0.0)
    composite_score = Column(Float, nullable=False, default=0.0)
    scored_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class MarketCoverageRecordModel(Base):
    __tablename__ = "market_coverage_records"

    id = Column(String(64), primary_key=True, default=lambda: f"cov-{uuid.uuid4().hex[:12]}")
    segment = Column(String(128), nullable=False)
    territory = Column(String(128), nullable=False)
    accounts_discovered = Column(Integer, nullable=False, default=0)
    accounts_researched = Column(Integer, nullable=False, default=0)
    qualified_accounts = Column(Integer, nullable=False, default=0)
    contacted_accounts = Column(Integer, nullable=False, default=0)
    active_opportunities = Column(Integer, nullable=False, default=0)
    won_accounts = Column(Integer, nullable=False, default=0)
    coverage_percentage = Column(Float, nullable=False, default=0.0)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class TerritoryDefinitionModel(Base):
    __tablename__ = "territory_definitions"

    id = Column(String(64), primary_key=True, default=lambda: f"ter-{uuid.uuid4().hex[:12]}")
    name = Column(String(255), nullable=False)
    geography = Column(String(128), nullable=False)
    industry_focus = Column(JSON, nullable=True)
    account_tier = Column(String(64), nullable=False, default="tier_1")
    owner_name = Column(String(128), nullable=True)
    revenue_potential_usd = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SalesPipelineModel(Base):
    __tablename__ = "sales_pipelines"

    id = Column(String(64), primary_key=True, default=lambda: f"pipe-{uuid.uuid4().hex[:12]}")
    name = Column(String(255), nullable=False)
    pipeline_type = Column(String(64), nullable=False, default="enterprise_new_business")
    is_active = Column(Boolean, nullable=False, default=True)
    stages = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SalesOpportunityModel(Base):
    __tablename__ = "sales_opportunities"

    id = Column(String(64), primary_key=True, default=lambda: f"opp-{uuid.uuid4().hex[:12]}")
    account_id = Column(String(64), ForeignKey("target_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    pipeline_id = Column(String(64), ForeignKey("sales_pipelines.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    stage = Column(String(64), nullable=False, default="qualified")
    estimated_arr_value = Column(Float, nullable=False, default=0.0)
    win_probability = Column(Float, nullable=False, default=0.2)
    weighted_value = Column(Float, nullable=False, default=0.0)
    expected_close_date = Column(DateTime(timezone=True), nullable=True)
    owner_name = Column(String(128), nullable=False, default="Account Executive")
    sales_motion = Column(String(64), nullable=False, default="consultative")
    primary_need = Column(Text, nullable=True)
    risk_status = Column(String(32), nullable=False, default="healthy")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SalesOpportunityHealthModel(Base):
    __tablename__ = "sales_opportunity_health"

    id = Column(String(64), primary_key=True, default=lambda: f"hlth-{uuid.uuid4().hex[:12]}")
    opportunity_id = Column(String(64), ForeignKey("sales_opportunities.id", ondelete="CASCADE"), nullable=False, index=True)
    engagement_score = Column(Float, nullable=False, default=80.0)
    decision_access_score = Column(Float, nullable=False, default=75.0)
    budget_evidence_score = Column(Float, nullable=False, default=85.0)
    overall_health_score = Column(Float, nullable=False, default=80.0)
    health_state = Column(String(32), nullable=False, default="healthy")
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SalesActivityModel(Base):
    __tablename__ = "sales_activities"

    id = Column(String(64), primary_key=True, default=lambda: f"act-{uuid.uuid4().hex[:12]}")
    opportunity_id = Column(String(64), ForeignKey("sales_opportunities.id", ondelete="CASCADE"), nullable=True, index=True)
    activity_type = Column(String(64), nullable=False, default="meeting")
    summary = Column(String(255), nullable=False)
    outcome = Column(String(128), nullable=True)
    actor_name = Column(String(128), nullable=False, default="Sales Rep")
    occurred_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SalesForecastModel(Base):
    __tablename__ = "sales_forecasts"

    id = Column(String(64), primary_key=True, default=lambda: f"fc-{uuid.uuid4().hex[:12]}")
    forecast_period = Column(String(64), nullable=False)
    model_version = Column(String(64), nullable=False, default="probabilistic-ensemble-v3")
    p10_usd = Column(Float, nullable=False, default=0.0)
    p25_usd = Column(Float, nullable=False, default=0.0)
    p50_usd = Column(Float, nullable=False, default=0.0)
    p75_usd = Column(Float, nullable=False, default=0.0)
    p90_usd = Column(Float, nullable=False, default=0.0)
    pipeline_total_usd = Column(Float, nullable=False, default=0.0)
    weighted_pipeline_usd = Column(Float, nullable=False, default=0.0)
    scenario = Column(String(64), nullable=False, default="base")
    assumptions = Column(JSON, nullable=True)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RevenueTargetModel(Base):
    __tablename__ = "revenue_targets"

    id = Column(String(64), primary_key=True, default=lambda: f"tgt-{uuid.uuid4().hex[:12]}")
    period = Column(String(64), nullable=False)
    target_type = Column(String(64), nullable=False, default="company_arr")
    target_amount_usd = Column(Float, nullable=False)
    actual_amount_usd = Column(Float, nullable=False, default=0.0)
    variance_usd = Column(Float, nullable=False, default=0.0)
    variance_pct = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SalesCapacityPlanModel(Base):
    __tablename__ = "sales_capacity_plans"

    id = Column(String(64), primary_key=True, default=lambda: f"cap-{uuid.uuid4().hex[:12]}")
    period = Column(String(64), nullable=False)
    rep_count = Column(Integer, nullable=False, default=5)
    quota_per_rep_usd = Column(Float, nullable=False, default=500000.0)
    total_capacity_usd = Column(Float, nullable=False, default=2500000.0)
    ramp_factor = Column(Float, nullable=False, default=0.85)
    effective_capacity_usd = Column(Float, nullable=False, default=2125000.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PricingIntelligenceModel(Base):
    __tablename__ = "pricing_intelligence"

    id = Column(String(64), primary_key=True, default=lambda: f"prc-{uuid.uuid4().hex[:12]}")
    product_or_service = Column(String(255), nullable=False)
    tier_name = Column(String(128), nullable=False)
    list_price_usd = Column(Float, nullable=False)
    billing_frequency = Column(String(32), nullable=False, default="annual")
    average_discount_pct = Column(Float, nullable=False, default=10.0)
    target_gross_margin_pct = Column(Float, nullable=False, default=75.0)
    willingness_to_pay_evidence = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DiscountRequestModel(Base):
    __tablename__ = "discount_requests"

    id = Column(String(64), primary_key=True, default=lambda: f"dsc-{uuid.uuid4().hex[:12]}")
    opportunity_id = Column(String(64), ForeignKey("sales_opportunities.id", ondelete="CASCADE"), nullable=False, index=True)
    requested_discount_pct = Column(Float, nullable=False)
    original_price_usd = Column(Float, nullable=False)
    proposed_price_usd = Column(Float, nullable=False)
    margin_impact_pct = Column(Float, nullable=False)
    justification = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="pending_approval")
    approver_name = Column(String(128), nullable=True)
    approval_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class DealRiskModel(Base):
    __tablename__ = "deal_risks"

    id = Column(String(64), primary_key=True, default=lambda: f"drsk-{uuid.uuid4().hex[:12]}")
    opportunity_id = Column(String(64), ForeignKey("sales_opportunities.id", ondelete="CASCADE"), nullable=False, index=True)
    risk_category = Column(String(64), nullable=False, default="decision_maker")
    severity = Column(String(32), nullable=False, default="medium")
    description = Column(Text, nullable=False)
    mitigation_strategy = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="open")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NextBestActionModel(Base):
    __tablename__ = "next_best_actions"

    id = Column(String(64), primary_key=True, default=lambda: f"nba-{uuid.uuid4().hex[:12]}")
    opportunity_id = Column(String(64), ForeignKey("sales_opportunities.id", ondelete="CASCADE"), nullable=False, index=True)
    recommended_action = Column(String(255), nullable=False)
    action_type = Column(String(64), nullable=False, default="schedule_technical_deep_dive")
    rationale = Column(Text, nullable=False)
    evidence_signals = Column(JSON, nullable=True)
    confidence = Column(Float, nullable=False, default=0.88)
    status = Column(String(32), nullable=False, default="recommended")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class LeadRoutingRuleModel(Base):
    __tablename__ = "lead_routing_rules"

    id = Column(String(64), primary_key=True, default=lambda: f"rule-{uuid.uuid4().hex[:12]}")
    rule_name = Column(String(255), nullable=False)
    criteria = Column(JSON, nullable=False)
    target_rep_or_team = Column(String(128), nullable=False)
    priority_order = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ChannelDefinitionModel(Base):
    __tablename__ = "channel_definitions"

    id = Column(String(64), primary_key=True, default=lambda: f"chn-{uuid.uuid4().hex[:12]}")
    name = Column(String(128), nullable=False, unique=True)
    channel_type = Column(String(64), nullable=False, default="outbound_direct")
    leads_count = Column(Integer, nullable=False, default=0)
    opportunities_count = Column(Integer, nullable=False, default=0)
    revenue_won_usd = Column(Float, nullable=False, default=0.0)
    cac_usd = Column(Float, nullable=False, default=0.0)
    conversion_rate = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class AttributionRecordModel(Base):
    __tablename__ = "attribution_records"

    id = Column(String(64), primary_key=True, default=lambda: f"attr-{uuid.uuid4().hex[:12]}")
    opportunity_id = Column(String(64), ForeignKey("sales_opportunities.id", ondelete="CASCADE"), nullable=False, index=True)
    attribution_model = Column(String(64), nullable=False, default="multi_touch_w_shaped")
    touchpoints_breakdown = Column(JSON, nullable=False)
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class CustomerAcquisitionEconomicsModel(Base):
    __tablename__ = "customer_acquisition_economics"

    id = Column(String(64), primary_key=True, default=lambda: f"econ-{uuid.uuid4().hex[:12]}")
    period = Column(String(64), nullable=False)
    blended_cac_usd = Column(Float, nullable=False, default=8500.0)
    average_ltv_usd = Column(Float, nullable=False, default=48000.0)
    ltv_to_cac_ratio = Column(Float, nullable=False, default=5.65)
    payback_period_months = Column(Float, nullable=False, default=6.5)
    gross_margin_pct = Column(Float, nullable=False, default=78.0)
    calculated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RevenueWaterfallModel(Base):
    __tablename__ = "revenue_waterfalls"

    id = Column(String(64), primary_key=True, default=lambda: f"wat-{uuid.uuid4().hex[:12]}")
    period = Column(String(64), nullable=False)
    beginning_arr_usd = Column(Float, nullable=False, default=0.0)
    new_arr_usd = Column(Float, nullable=False, default=0.0)
    expansion_arr_usd = Column(Float, nullable=False, default=0.0)
    contraction_arr_usd = Column(Float, nullable=False, default=0.0)
    churn_arr_usd = Column(Float, nullable=False, default=0.0)
    ending_arr_usd = Column(Float, nullable=False, default=0.0)
    net_retention_pct = Column(Float, nullable=False, default=112.0)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RevenueRiskRecordModel(Base):
    __tablename__ = "revenue_risk_records"

    id = Column(String(64), primary_key=True, default=lambda: f"rrsk-{uuid.uuid4().hex[:12]}")
    risk_type = Column(String(64), nullable=False, default="customer_concentration")
    severity = Column(String(32), nullable=False, default="medium")
    description = Column(Text, nullable=False)
    potential_revenue_impact_usd = Column(Float, nullable=False, default=0.0)
    evidence_data = Column(JSON, nullable=True)
    status = Column(String(32), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RevenueGrowthOpportunityModel(Base):
    __tablename__ = "revenue_growth_opportunities"

    id = Column(String(64), primary_key=True, default=lambda: f"ropp-{uuid.uuid4().hex[:12]}")
    opportunity_type = Column(String(64), nullable=False, default="cross_sell_ai_workforce")
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    estimated_arr_potential_usd = Column(Float, nullable=False, default=0.0)
    target_segment = Column(String(128), nullable=True)
    confidence = Column(Float, nullable=False, default=0.85)
    status = Column(String(32), nullable=False, default="identified")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PartnerProfileModel(Base):
    __tablename__ = "partner_profiles"

    id = Column(String(64), primary_key=True, default=lambda: f"part-{uuid.uuid4().hex[:12]}")
    partner_name = Column(String(255), nullable=False)
    partner_type = Column(String(64), nullable=False, default="solution_integrator")
    region = Column(String(128), nullable=True)
    referred_leads_count = Column(Integer, nullable=False, default=0)
    influenced_revenue_usd = Column(Float, nullable=False, default=0.0)
    tier = Column(String(32), nullable=False, default="gold")
    status = Column(String(32), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
