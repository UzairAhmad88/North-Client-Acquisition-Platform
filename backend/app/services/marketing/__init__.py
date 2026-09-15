"""
Phase 59: Unified Marketing Intelligence, Demand Generation, Content Strategy & Marketing Automation Services
"""

from backend.app.services.marketing.base import (
    AttrDict,
    CampaignStatus,
    CampaignType,
    ContentStatus,
    ContentType,
    JourneyStage,
    ClaimVerificationStatus,
    LeadQualificationStage,
    AttributionModelType,
    RiskSeverity,
    FatigueLevel,
    generate_id,
)
from backend.app.services.marketing.audiences_positioning import AudiencePositioningService
from backend.app.services.marketing.content_strategy_claims import ContentStrategyClaimsService
from backend.app.services.marketing.campaigns_channels_email import CampaignsChannelsEmailService
from backend.app.services.marketing.leads_nurture_funnel import LeadsNurtureFunnelService
from backend.app.services.marketing.attribution_roi_budgets import AttributionRoiBudgetsService
from backend.app.services.marketing.seo_social_events_calendar import SeoSocialEventsCalendarService
from backend.app.services.marketing.forecast_risks_fatigue import ForecastRisksFatigueService
from backend.app.services.marketing.service import MarketingPlatformService

__all__ = [
    "AttrDict",
    "CampaignStatus",
    "CampaignType",
    "ContentStatus",
    "ContentType",
    "JourneyStage",
    "ClaimVerificationStatus",
    "LeadQualificationStage",
    "AttributionModelType",
    "RiskSeverity",
    "FatigueLevel",
    "generate_id",
    "AudiencePositioningService",
    "ContentStrategyClaimsService",
    "CampaignsChannelsEmailService",
    "LeadsNurtureFunnelService",
    "AttributionRoiBudgetsService",
    "SeoSocialEventsCalendarService",
    "ForecastRisksFatigueService",
    "MarketingPlatformService",
]
