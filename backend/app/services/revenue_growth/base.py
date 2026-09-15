"""Base definitions, enums, data structures, and helper classes for Unified Revenue Growth."""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class SalesMotion(str, Enum):
    SELF_SERVE = "self_serve"
    FOUNDER_LED = "founder_led"
    CONSULTATIVE = "consultative"
    ENTERPRISE = "enterprise"
    PARTNER_LED = "partner_led"
    PRODUCT_LED = "product_led"
    SERVICE_LED = "service_led"
    HYBRID = "hybrid"


class PipelineStage(str, Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    DISCOVERY = "discovery"
    REQUIREMENTS = "requirements"
    SOLUTION = "solution"
    ESTIMATE = "estimate"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CONTRACT = "contract"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    ON_HOLD = "on_hold"
    DORMANT = "dormant"


class OpportunityHealthState(str, Enum):
    HEALTHY = "healthy"
    WATCH = "watch"
    AT_RISK = "at_risk"
    BLOCKED = "blocked"
    DORMANT = "dormant"


class ForecastScenario(str, Enum):
    CONSERVATIVE = "conservative"
    BASE = "base"
    OPTIMISTIC = "optimistic"
    STRESS = "stress"


class DealRiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DiscountStatus(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class AttributionModelType(str, Enum):
    FIRST_TOUCH = "first_touch"
    LAST_TOUCH = "last_touch"
    MULTI_TOUCH_LINEAR = "multi_touch_linear"
    MULTI_TOUCH_W_SHAPED = "multi_touch_w_shaped"
    TIME_DECAY = "time_decay"


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
        if item in self:
            return self[item]
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


def generate_rev_id(prefix: str = "rev") -> str:
    """Generate unique ID with given prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def current_utc_time() -> datetime:
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)
