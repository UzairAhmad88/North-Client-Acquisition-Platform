"""Base definitions, enums, data structures, and helper classes for Unified Customer Experience."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class JourneyType(str, Enum):
    SALES = "sales"
    ONBOARDING = "onboarding"
    PRODUCT = "product"
    SERVICE = "service"
    SUPPORT = "support"
    RENEWAL = "renewal"
    EXPANSION = "expansion"


class JourneyStage(str, Enum):
    AWARENESS = "awareness"
    DISCOVERY = "discovery"
    CONSIDERATION = "consideration"
    EVALUATION = "evaluation"
    PURCHASE = "purchase"
    ONBOARDING = "onboarding"
    ACTIVATION = "activation"
    ADOPTION = "adoption"
    VALUE = "value"
    SUPPORT = "support"
    RENEWAL = "renewal"
    EXPANSION = "expansion"
    ADVOCACY = "advocacy"


class LifecycleStatus(str, Enum):
    DISCOVER = "discover"
    ENGAGE = "engage"
    QUALIFY = "qualify"
    CONSIDER = "consider"
    DECIDE = "decide"
    ONBOARD = "onboard"
    ADOPT = "adopt"
    USE = "use"
    RECEIVE_VALUE = "receive_value"
    GET_SUPPORT = "get_support"
    RENEW = "renew"
    EXPAND = "expand"
    REFER = "refer"
    DROPPED = "dropped"
    INACTIVE = "inactive"
    AT_RISK = "at_risk"
    CHURNED = "churned"
    LOST = "lost"


class HealthState(str, Enum):
    EXCELLENT = "excellent"
    HEALTHY = "healthy"
    STABLE = "stable"
    WATCH = "watch"
    AT_RISK = "at_risk"
    CRITICAL = "critical"
    INSUFFICIENT_DATA = "insufficient_data"


class EffortTier(str, Enum):
    LOW_EFFORT = "low_effort"
    MODERATE_EFFORT = "moderate_effort"
    HIGH_EFFORT = "high_effort"
    CRITICAL_FRICTION = "critical_friction"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class FrictionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(str, Enum):
    HEALTH_DECLINE = "health_decline"
    CHURN_RISK = "churn_risk"
    HIGH_FRICTION = "high_friction"
    NEGATIVE_FEEDBACK = "negative_feedback"
    SUPPORT_ESCALATION = "support_escalation"
    PAYMENT_ISSUE = "payment_issue"
    ADOPTION_DROP = "adoption_drop"
    RENEWAL_RISK = "renewal_risk"
    GOAL_FAILURE = "goal_failure"
    CRITICAL_INCIDENT = "critical_incident"


class AttrDict(dict):
    """Dictionary supporting attribute-style access and dynamic alias keys."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in list(self.items()):
            if isinstance(v, dict) and not isinstance(v, AttrDict):
                self[k] = AttrDict(v)
            elif isinstance(v, list):
                self[k] = [AttrDict(i) if isinstance(i, dict) and not isinstance(i, AttrDict) else i for i in v]

    def __getattr__(self, item):
        # Support alias mappings if requested
        if item in self:
            return self[item]
        # Normalize underscores and hyphens
        alt = item.replace("_", "-")
        if alt in self:
            return self[alt]
        alt2 = item.replace("-", "_")
        if alt2 in self:
            return self[alt2]
        raise AttributeError(f"'AttrDict' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError(f"'AttrDict' object has no attribute '{key}'")


def generate_cx_id(prefix: str = "cx") -> str:
    """Generate unique ID with given prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def current_utc_time() -> datetime:
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)
