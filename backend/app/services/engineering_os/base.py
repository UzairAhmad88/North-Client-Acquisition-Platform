"""Base definitions, Enums, and Utility helpers for Phase 61 Engineering Operating System."""

import enum
import uuid
from typing import Any, Dict


class EnvironmentType(str, enum.Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"
    QA = "QA"
    STAGING = "STAGING"
    UAT = "UAT"
    CANARY = "CANARY"
    PRODUCTION = "PRODUCTION"
    DR = "DR"


class DeploymentStrategy(str, enum.Enum):
    ROLLING = "ROLLING"
    BLUE_GREEN = "BLUE_GREEN"
    CANARY = "CANARY"
    RECREATE = "RECREATE"
    FEATURE_FLAG = "FEATURE_FLAG"
    SHADOW = "SHADOW"
    A_B = "A_B"


class IncidentSeverity(str, enum.Enum):
    SEV0 = "SEV0"  # Critical platform down / data breach
    SEV1 = "SEV1"  # Major feature degraded
    SEV2 = "SEV2"  # Moderate customer impact
    SEV3 = "SEV3"  # Minor anomaly
    SEV4 = "SEV4"  # Informational


class ChangeRiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PullRequestStatus(str, enum.Enum):
    OPEN = "OPEN"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    APPROVED = "APPROVED"
    MERGED = "MERGED"
    CLOSED = "CLOSED"


class ServiceHealthState(str, enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    FAILING = "FAILING"


class AttrDict(dict):
    """Dictionary subclass enabling attribute-style key access."""
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


def generate_engineering_id(prefix: str = "eng") -> str:
    """Generate deterministic unique engineering resource identifier."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


generate_id = generate_engineering_id
