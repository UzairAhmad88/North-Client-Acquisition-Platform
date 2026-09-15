"""Pydantic Schemas for Phase 58: Unified Revenue Growth, Go-to-Market Intelligence & Optimization Platform."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GtmStrategyCreateRequest(BaseModel):
    name: str = Field(..., description="GTM Strategy name")
    target_market: str = Field(..., description="Target market definition")
    sales_motion: str = Field(default="consultative", description="consultative | enterprise | inbound | partner_led")
    positioning: Optional[str] = None
    value_proposition: Optional[str] = None
    channels: Optional[List[str]] = None
    metrics_targets: Optional[Dict[str, Any]] = None


class SegmentCreateRequest(BaseModel):
    name: str = Field(..., description="Segment name")
    industry: str = Field(..., description="Target industry")
    company_size_tier: str = Field(default="enterprise", description="enterprise | mid_market | smb")
    estimated_tam_usd: float = Field(default=100000000.0)
    estimated_sam_usd: float = Field(default=25000000.0)
    priority_tier: str = Field(default="tier_1")
    description: Optional[str] = None
    strategy_id: Optional[str] = None


class IcpCreateRequest(BaseModel):
    name: str = Field(..., description="ICP profile name")
    target_industries: List[str] = Field(...)
    min_employee_count: int = Field(default=250)
    max_employee_count: int = Field(default=10000)
    min_arr_usd: float = Field(default=10000000.0)
    required_tech_profile: Optional[List[str]] = None
    pain_points: Optional[List[str]] = None
    buying_signals: Optional[List[str]] = None
    exclusions: Optional[List[str]] = None
    segment_id: Optional[str] = None


class TargetAccountCreateRequest(BaseModel):
    company_name: str = Field(..., description="Company name")
    domain: Optional[str] = None
    industry: Optional[str] = "FinTech"
    employee_count: int = Field(default=500)
    estimated_annual_revenue: float = Field(default=45000000.0)
    country: str = Field(default="US")
    priority_level: str = Field(default="high")
    assigned_rep: Optional[str] = "Sarah Chen"


class TargetAccountScoreRequest(BaseModel):
    account_id: str = Field(...)
    icp_fit: float = Field(default=0.90)
    business_need: float = Field(default=0.85)
    digital_gap: float = Field(default=0.80)
    revenue_potential: float = Field(default=0.92)
    buying_signal: float = Field(default=0.88)


class OpportunityCreateRequest(BaseModel):
    account_id: str = Field(...)
    title: str = Field(...)
    estimated_arr_value: float = Field(...)
    stage: str = Field(default="qualified")
    win_probability: float = Field(default=0.25)
    owner_name: str = Field(default="Sarah Chen")
    sales_motion: str = Field(default="consultative")
    primary_need: Optional[str] = None
    pipeline_id: Optional[str] = None


class StageAdvanceRequest(BaseModel):
    next_stage: str = Field(..., description="Target next pipeline stage")


class ActivityLogRequest(BaseModel):
    activity_type: str = Field(default="meeting", description="meeting | email | call | proposal | demo")
    summary: str = Field(...)
    opportunity_id: Optional[str] = None
    outcome: Optional[str] = None
    actor_name: str = Field(default="Sarah Chen")


class ForecastGenerateRequest(BaseModel):
    forecast_period: str = Field(default="Q4-2026")
    scenario: str = Field(default="base", description="conservative | base | optimistic | stress")
    pipeline_total_usd: float = Field(default=3850000.0)
    weighted_pipeline_usd: float = Field(default=1420000.0)
    assumptions: Optional[Dict[str, Any]] = None


class RevenueTargetCreateRequest(BaseModel):
    period: str = Field(...)
    target_amount_usd: float = Field(...)
    actual_amount_usd: float = Field(default=0.0)
    target_type: str = Field(default="company_arr")


class CapacityPlanCreateRequest(BaseModel):
    period: str = Field(...)
    rep_count: int = Field(default=6)
    quota_per_rep_usd: float = Field(default=600000.0)
    ramp_factor: float = Field(default=0.85)


class PricingTierSetRequest(BaseModel):
    product_or_service: str = Field(...)
    tier_name: str = Field(...)
    list_price_usd: float = Field(...)
    billing_frequency: str = Field(default="annual")
    average_discount_pct: float = Field(default=10.0)
    target_gross_margin_pct: float = Field(default=78.0)
    willingness_to_pay_evidence: Optional[Dict[str, Any]] = None


class DiscountSubmitRequest(BaseModel):
    opportunity_id: str = Field(...)
    requested_discount_pct: float = Field(...)
    original_price_usd: float = Field(...)
    justification: str = Field(...)


class DiscountApprovalRequest(BaseModel):
    approver_name: str = Field(...)
    approval_notes: Optional[str] = None


class DealRiskRecordRequest(BaseModel):
    opportunity_id: str = Field(...)
    risk_category: str = Field(default="decision_maker")
    severity: str = Field(default="medium")
    description: str = Field(...)
    mitigation_strategy: Optional[str] = None


class NextBestActionRequest(BaseModel):
    opportunity_id: str = Field(...)
    recommended_action: str = Field(...)
    action_type: str = Field(default="schedule_technical_deep_dive")
    rationale: str = Field(...)
    confidence: float = Field(default=0.90)


class RevenueSimulationRequest(BaseModel):
    conversion_rate_delta_pct: float = Field(default=5.0)
    lead_volume_delta_pct: float = Field(default=10.0)
    average_deal_size_delta_pct: float = Field(default=0.0)


class RevenueCopilotQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language question for Revenue Intelligence Copilot")
