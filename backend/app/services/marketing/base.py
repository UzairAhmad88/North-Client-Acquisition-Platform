"""
Phase 59: Marketing Platform Base Utilities, Enums, and Helper Classes
"""

import enum
import uuid
from typing import Any, Dict


class CampaignStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    ANALYZING = "ANALYZING"
    ARCHIVED = "ARCHIVED"


class CampaignType(str, enum.Enum):
    AWARENESS = "AWARENESS"
    DEMAND_GENERATION = "DEMAND_GENERATION"
    LEAD_GENERATION = "LEAD_GENERATION"
    PRODUCT_LAUNCH = "PRODUCT_LAUNCH"
    EVENT = "EVENT"
    WEBINAR = "WEBINAR"
    RETENTION = "RETENTION"
    UPSELL = "UPSELL"
    CROSS_SELL = "CROSS_SELL"
    REFERRAL = "REFERRAL"
    REACTIVATION = "REACTIVATION"


class ContentStatus(str, enum.Enum):
    IDEA = "IDEA"
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class ContentType(str, enum.Enum):
    ARTICLE = "ARTICLE"
    BLOG = "BLOG"
    GUIDE = "GUIDE"
    CASE_STUDY = "CASE_STUDY"
    WHITEPAPER = "WHITEPAPER"
    REPORT = "REPORT"
    NEWSLETTER = "NEWSLETTER"
    EMAIL = "EMAIL"
    SOCIAL_POST = "SOCIAL_POST"
    LANDING_PAGE = "LANDING_PAGE"
    COMPARISON = "COMPARISON"
    PRODUCT_ANNOUNCEMENT = "PRODUCT_ANNOUNCEMENT"


class JourneyStage(str, enum.Enum):
    AWARENESS = "AWARENESS"
    EDUCATION = "EDUCATION"
    CONSIDERATION = "CONSIDERATION"
    EVALUATION = "EVALUATION"
    DECISION = "DECISION"
    ONBOARDING = "ONBOARDING"
    RETENTION = "RETENTION"
    ADVOCACY = "ADVOCACY"


class ClaimVerificationStatus(str, enum.Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    OUTDATED = "OUTDATED"
    CONFLICTING = "CONFLICTING"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


class LeadQualificationStage(str, enum.Enum):
    NEW = "NEW"
    ENGAGED = "ENGAGED"
    MQL = "MQL"
    SQL = "SQL"
    DISQUALIFIED = "DISQUALIFIED"
    NURTURE = "NURTURE"
    CONVERTED = "CONVERTED"


class AttributionModelType(str, enum.Enum):
    FIRST_TOUCH = "FIRST_TOUCH"
    LAST_TOUCH = "LAST_TOUCH"
    LINEAR = "LINEAR"
    POSITION_BASED = "POSITION_BASED"
    TIME_DECAY = "TIME_DECAY"
    MULTI_TOUCH_W_SHAPED = "MULTI_TOUCH_W_SHAPED"


class RiskSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FatigueLevel(str, enum.Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    CRITICAL = "CRITICAL"


class AttrDict(dict):
    """Dictionary subclass supporting attribute access."""
    def __getattr__(self, name: str) -> Any:
        try:
            val = self[name]
            if isinstance(val, dict) and not isinstance(val, AttrDict):
                val = AttrDict(val)
                self[name] = val
            return val
        except KeyError:
            raise AttributeError(f"'AttrDict' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value


def generate_id(prefix: str = "mkt") -> str:
    """Generate a prefixed unique identifier."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"
