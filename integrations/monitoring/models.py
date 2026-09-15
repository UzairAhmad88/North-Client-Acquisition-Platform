"""Data schemas for Monitoring & Observability subsystem."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class HealthMetric(BaseModel):
    """System health observation metric."""

    signal_type: str  # UPTIME, LATENCY, ERROR_RATE, CPU, MEMORY, DATABASE, API_HEALTH
    status: str = "HEALTHY"  # HEALTHY, DEGRADED, AT_RISK, DOWN
    value: float = 0.0
    unit: str = "ms"
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthCheckResult(BaseModel):
    """Overall system health evaluation output."""

    project_id: str
    overall_status: str = "HEALTHY"  # HEALTHY, DEGRADED, AT_RISK, DOWN
    uptime_percentage: float = 99.95
    active_incidents: int = 0
    metrics: Dict[str, HealthMetric] = Field(default_factory=dict)
    checked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
