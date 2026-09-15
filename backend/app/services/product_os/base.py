"""Phase 60: Product Operating System Base Utilities, Enums, and Helper Classes."""

import enum
import uuid
from typing import Any, Dict


class ProductLifecycleState(str, enum.Enum):
    IDEA = "IDEA"
    DISCOVERY = "DISCOVERY"
    PLANNED = "PLANNED"
    DESIGN = "DESIGN"
    DEVELOPMENT = "DEVELOPMENT"
    BETA = "BETA"
    RELEASED = "RELEASED"
    MATURE = "MATURE"
    SUNSET_PLANNED = "SUNSET_PLANNED"
    SUNSET = "SUNSET"
    ARCHIVED = "ARCHIVED"


class ProblemValidationStatus(str, enum.Enum):
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    MEASURED = "MEASURED"
    INFERRED = "INFERRED"
    HYPOTHESIS = "HYPOTHESIS"
    VALIDATED = "VALIDATED"
    INVALIDATED = "INVALIDATED"


class PrioritizationFramework(str, enum.Enum):
    RICE = "RICE"
    WSJF = "WSJF"
    ICE = "ICE"
    VALUE_VS_EFFORT = "VALUE_VS_EFFORT"


class RoadmapHorizon(str, enum.Enum):
    NOW = "NOW"
    NEXT = "NEXT"
    LATER = "LATER"


class RequirementType(str, enum.Enum):
    FUNCTIONAL = "FUNCTIONAL"
    NON_FUNCTIONAL = "NON_FUNCTIONAL"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    RELIABILITY = "RELIABILITY"
    ACCESSIBILITY = "ACCESSIBILITY"
    COMPLIANCE = "COMPLIANCE"
    DATA = "DATA"
    UX = "UX"


class ProductHealthState(str, enum.Enum):
    HEALTHY = "HEALTHY"
    WATCH = "WATCH"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"


class ReleaseStrategy(str, enum.Enum):
    FULL_RELEASE = "FULL_RELEASE"
    PHASED_ROLLOUT = "PHASED_ROLLOUT"
    FEATURE_FLAGGED_PHASED = "FEATURE_FLAGGED_PHASED"
    BETA = "BETA"
    CANARY = "CANARY"


class RiskSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
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


def generate_id(prefix: str = "prd") -> str:
    """Generate a prefixed unique identifier."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


generate_product_id = generate_id
