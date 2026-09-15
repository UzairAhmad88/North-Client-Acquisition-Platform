"""Abstract base class for Monitoring and Observability providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict
from integrations.monitoring.models import HealthCheckResult


class BaseMonitoringProvider(ABC):
    """Abstract interface for system monitoring providers."""

    @abstractmethod
    async def check_health(self, project_id: str) -> HealthCheckResult:
        """Perform synthetic health check on target project environment."""
        pass

    @abstractmethod
    async def ingest_event(self, project_id: str, event_data: Dict[str, Any]) -> bool:
        """Ingest external monitoring event or webhook payload."""
        pass
