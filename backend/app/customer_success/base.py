"""Base domain enums, dataclasses, and schemas for Phase 41 Customer Success & Relationship Intelligence."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ClientLifecycleStage(str, Enum):
    """Lifecycle stages for a client relationship."""
    PROSPECT = "PROSPECT"
    QUALIFIED = "QUALIFIED"
    OPPORTUNITY = "OPPORTUNITY"
    ONBOARDING = "ONBOARDING"
    ACTIVE = "ACTIVE"
    SUCCESS = "SUCCESS"
    RENEWAL = "RENEWAL"
    EXPANSION = "EXPANSION"
    AT_RISK = "AT_RISK"
    ON_HOLD = "ON_HOLD"
    INACTIVE = "INACTIVE"
    CHURNED = "CHURNED"
    ARCHIVED = "ARCHIVED"


class RelationshipStrength(str, Enum):
    """Evidence-based strength of the customer relationship."""
    NEW = "NEW"
    DEVELOPING = "DEVELOPING"
    ESTABLISHED = "ESTABLISHED"
    STRONG = "STRONG"
    AT_RISK = "AT_RISK"
    UNKNOWN = "UNKNOWN"


class DecisionRole(str, Enum):
    """Organizational contact decision roles."""
    DECISION_MAKER = "DECISION_MAKER"
    INFLUENCER = "INFLUENCER"
    CHAMPION = "CHAMPION"
    USER = "USER"
    TECHNICAL_CONTACT = "TECHNICAL_CONTACT"
    FINANCE_CONTACT = "FINANCE_CONTACT"
    ADMIN = "ADMIN"
    UNKNOWN = "UNKNOWN"


class HealthBand(str, Enum):
    """Calibrated client health score ranges."""
    EXCELLENT = "EXCELLENT"   # 90 - 100
    GOOD = "GOOD"             # 80 - 89
    HEALTHY = "HEALTHY"       # 80 - 100
    STABLE = "STABLE"         # 60 - 79
    WATCH = "WATCH"           # 40 - 59
    AT_RISK = "AT_RISK"       # 20 - 39
    CRITICAL = "CRITICAL"     # 0 - 19
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class RiskCategory(str, Enum):
    """Categories of detected client risks."""
    RELATIONSHIP = "RELATIONSHIP"
    FINANCIAL = "FINANCIAL"
    PROJECT = "PROJECT"
    SUPPORT = "SUPPORT"
    ENGAGEMENT = "ENGAGEMENT"
    SATISFACTION = "SATISFACTION"
    RENEWAL = "RENEWAL"
    DELIVERY = "DELIVERY"
    SCOPE = "SCOPE"
    COMMUNICATION = "COMMUNICATION"
    CHURN = "CHURN"
    PAYMENT = "PAYMENT"
    CONTRACT = "CONTRACT"


class OpportunityType(str, Enum):
    """Expansion and commercial opportunity types."""
    EXPANSION = "EXPANSION"
    CROSS_SELL = "CROSS_SELL"
    UPSELL = "UPSELL"
    NEW_PROJECT = "NEW_PROJECT"
    MAINTENANCE = "MAINTENANCE"
    AI_ASSISTANT = "AI_ASSISTANT"
    AUTOMATION = "AUTOMATION"
    SECURITY = "SECURITY"
    REFERRAL = "REFERRAL"


class RenewalStatus(str, Enum):
    """Lifecycle of a contract or service renewal."""
    UPCOMING = "UPCOMING"
    PREPARATION = "PREPARATION"
    REVIEW = "REVIEW"
    NEGOTIATION = "NEGOTIATION"
    RENEWED = "RENEWED"
    AT_RISK = "AT_RISK"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class SurveyType(str, Enum):
    """Customer satisfaction survey classifications."""
    ONBOARDING = "ONBOARDING"
    PROJECT_COMPLETION = "PROJECT_COMPLETION"
    SUPPORT_RESOLUTION = "SUPPORT_RESOLUTION"
    QUARTERLY_HEALTH = "QUARTERLY_HEALTH"
    RENEWAL = "RENEWAL"
    NPS = "NPS"
    CSAT = "CSAT"
    CES = "CES"


class SentimentLabel(str, Enum):
    """Client sentiment classifications."""
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"


class GoalStatus(str, Enum):
    """Status of client business goals."""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    ACHIEVED = "ACHIEVED"
    CANCELLED = "CANCELLED"


class SuccessPlanStatus(str, Enum):
    """Status of customer success plans."""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    AT_RISK = "AT_RISK"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"


# --- Data Structures & Results ---

class HealthFactorScore(BaseModel):
    """Score and evidence for an individual health factor."""
    factor_name: str
    weight: Decimal
    score: Optional[Decimal] = None  # None indicates INSUFFICIENT_DATA
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW, UNKNOWN
    evidence_summary: Optional[str] = None
    data_source: str = "SYSTEM"


class HealthCalculationResult(BaseModel):
    """Overall multi-factor health calculation and explanation."""
    client_id: str
    overall_score: Decimal
    health_band: HealthBand
    confidence: str
    trend: str  # IMPROVING, STABLE, DECLINING, UNKNOWN
    factors: List[HealthFactorScore]
    positive_factors: List[str]
    risk_factors: List[str]
    explanation: str
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TimelineEventData(BaseModel):
    """Unified client chronological event."""
    id: str
    client_id: str
    event_type: str
    title: str
    description: Optional[str] = None
    actor_type: str = "SYSTEM"  # SYSTEM, USER, CLIENT, AI
    actor_id: Optional[str] = None
    source_entity_type: Optional[str] = None
    source_entity_id: Optional[str] = None
    occurred_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
