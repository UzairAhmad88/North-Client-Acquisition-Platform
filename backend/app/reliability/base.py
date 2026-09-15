"""Base domain models, enums, and dataclasses for Reliability, SRE, and Resilience."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ServiceHealthStatus(str, Enum):
    """Health status of an internal or platform service."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
    DISABLED = "DISABLED"


class DependencyStatus(str, Enum):
    """Health status of an external or infrastructure dependency."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
    DISABLED = "DISABLED"


class CircuitState(str, Enum):
    """Circuit breaker operational states."""
    CLOSED = "CLOSED"       # Normal operation, traffic passes
    OPEN = "OPEN"           # Tripped due to failures, traffic blocked/failed fast
    HALF_OPEN = "HALF_OPEN" # Testing recovery with limited traffic


class IncidentSeverity(str, Enum):
    """Severity levels for operational incidents."""
    SEV1_CRITICAL = "SEV-1"  # Total platform or core revenue/data outage
    SEV2_HIGH = "SEV-2"      # Major feature degraded or critical customer impacted
    SEV3_MEDIUM = "SEV-3"    # Partial non-critical impairment with workaround
    SEV4_LOW = "SEV-4"       # Minor glitch, cosmetic issue, or low-priority alert


class IncidentStatus(str, Enum):
    """Lifecycle stages for operational incidents."""
    DETECTED = "DETECTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    TRIAGED = "TRIAGED"
    INVESTIGATING = "INVESTIGATING"
    MITIGATING = "MITIGATING"
    RECOVERING = "RECOVERING"
    RESOLVED = "RESOLVED"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"


class SLOType(str, Enum):
    """Types of Service Level Objectives."""
    AVAILABILITY = "AVAILABILITY"
    LATENCY = "LATENCY"
    ERROR_RATE = "ERROR_RATE"
    THROUGHPUT = "THROUGHPUT"
    FRESHNESS = "FRESHNESS"
    COMPLETION_RATE = "COMPLETION_RATE"


class ErrorBudgetStatus(str, Enum):
    """Health status of an SLO error budget."""
    HEALTHY = "HEALTHY"       # > 50% budget remaining
    WARNING = "WARNING"       # 20% - 50% budget remaining
    EXHAUSTED = "EXHAUSTED"   # < 20% budget remaining
    BREACHED = "BREACHED"     # 0% budget remaining (SLO violated)


class BackupStatus(str, Enum):
    """Status of a database or storage backup snapshot."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    VERIFIED = "VERIFIED"
    CORRUPTED = "CORRUPTED"


class RestoreTestStatus(str, Enum):
    """Status of an isolated backup restoration verification test."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"


class DRPlanStatus(str, Enum):
    """Status of a Disaster Recovery or Business Continuity plan."""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    TESTED = "TESTED"
    ARCHIVED = "ARCHIVED"


class FailoverStatus(str, Enum):
    """Status of a multi-region or standby failover operation."""
    STANDBY = "STANDBY"
    INITIATED = "INITIATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


class DeploymentHealthStatus(str, Enum):
    """Status of an application release deployment."""
    PENDING = "PENDING"
    DEPLOYING = "DEPLOYING"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    ROLLED_BACK = "ROLLED_BACK"


class DrillStatus(str, Enum):
    """Status of a game-day or disaster recovery drill."""
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# --- Data Structures & Results ---

class ComponentHealthCheck(BaseModel):
    """Individual health result for a specific subsystem."""
    name: str
    status: ServiceHealthStatus
    latency_ms: float = 0.0
    message: Optional[str] = None
    last_checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = Field(default_factory=dict)


class DeepHealthResult(BaseModel):
    """Consolidated platform deep health report."""
    status: ServiceHealthStatus
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_components: int = 0
    healthy_count: int = 0
    degraded_count: int = 0
    unavailable_count: int = 0
    components: Dict[str, ComponentHealthCheck] = Field(default_factory=dict)
    summary: str = "All systems operational"
