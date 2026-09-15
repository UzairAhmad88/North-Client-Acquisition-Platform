"""
Phase 59: Pydantic Schemas for Marketing Platform API
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AudienceCreateRequest(BaseModel):
    name: str = Field(..., example="Mid-Market Law Firms")
    description: str = Field(..., example="Law firms with 50-250 partners")
    target_icp: str = Field(..., example="Professional Services")
    industry: str = Field(..., example="Legal")
    company_size_tier: str = Field("MID_MARKET", example="MID_MARKET")
    buying_context: str = Field("Modernizing client intake", example="Modernizing client intake")
    primary_pain_points: List[str] = Field(default_factory=list)
    channel_preferences: List[str] = Field(default_factory=list)
    total_market_size: int = 10000
    reachable_market_size: int = 3500


class PositioningCreateRequest(BaseModel):
    audience_id: str
    target_customer: str
    problem_statement: str
    alternative_solution: str
    our_solution: str
    key_differentiators: List[str]
    value_statement: str
    proof_points: List[str]


class ContentAssetCreateRequest(BaseModel):
    title: str
    content_type: str = "ARTICLE"
    journey_stage: str = "AWARENESS"
    target_audience_id: Optional[str] = None
    body_markdown: str = ""
    primary_cta: Optional[str] = None


class ClaimRecordRequest(BaseModel):
    asset_id: str
    claim_text: str
    source_reference: str
    source_date: Optional[str] = "2026-09"
    confidence_pct: float = 90.0
    verification_status: str = "VERIFIED"
    reviewer_notes: Optional[str] = None


class CampaignCreateRequest(BaseModel):
    name: str
    campaign_type: str = "DEMAND_GENERATION"
    target_audience_id: Optional[str] = None
    allocated_budget_usd: float = 25000.0
    channels: List[str] = Field(default_factory=lambda: ["EMAIL", "LINKEDIN", "ORGANIC_SEARCH"])
    owner: str = "growth_lead"


class LeadCaptureRequest(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None
    source_channel: str = "ORGANIC_SEARCH"
    first_touch_campaign: Optional[str] = None


class LeadScoreCalculateRequest(BaseModel):
    lead_id: str
    company_size_tier: str = "MID_MARKET"
    industry_match: bool = True
    budget_signal: bool = True
    page_views: int = 5
    content_downloads: int = 2
    webinar_attended: bool = False
    pricing_page_visits: int = 1
    demo_requested: bool = False


class AttributionCalculateRequest(BaseModel):
    opportunity_id: str
    deal_value_usd: float
    touches: List[Dict[str, Any]]
    attribution_model: str = "MULTI_TOUCH_W_SHAPED"


class BudgetSimulationRequest(BaseModel):
    current_budget_usd: float = 150000.0
    budget_shift_pct: float = 20.0
    target_focus_channel: str = "LINKEDIN_ABM"


class CopilotQueryRequest(BaseModel):
    query: str = Field(..., example="What campaigns are performing best?")
