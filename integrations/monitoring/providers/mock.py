"""Mock Monitoring Provider for testing and local operation."""

from datetime import datetime, timezone
from typing import Any, Dict
from integrations.monitoring.base import BaseMonitoringProvider
from integrations.monitoring.models import HealthCheckResult, HealthMetric


class MockMonitoringProvider(BaseMonitoringProvider):
    """Mock monitoring provider generating deterministic observability signals."""

    async def check_health(self, project_id: str) -> HealthCheckResult:
        metrics = {
            "uptime": HealthMetric(signal_type="UPTIME", status="HEALTHY", value=99.98, unit="%"),
            "latency": HealthMetric(signal_type="LATENCY", status="HEALTHY", value=124.0, unit="ms"),
            "error_rate": HealthMetric(signal_type="ERROR_RATE", status="HEALTHY", value=0.02, unit="%"),
            "database": HealthMetric(signal_type="DATABASE", status="HEALTHY", value=15.0, unit="ms"),
        }

        return HealthCheckResult(
            project_id=project_id,
            overall_status="HEALTHY",
            uptime_percentage=99.98,
            active_incidents=0,
            metrics=metrics,
            checked_at=datetime.now(timezone.utc),
        )

    async def ingest_event(self, project_id: str, event_data: Dict[str, Any]) -> bool:
        return True
