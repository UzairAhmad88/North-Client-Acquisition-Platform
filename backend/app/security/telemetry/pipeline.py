"""
Telemetry Ingestion and Streaming Pipeline.
"""

from typing import Dict, Any, List, Optional, Callable

try:
    from app.security.base import SecurityEvent
    from app.security.telemetry.normalizer import TelemetryNormalizer
    from app.security.telemetry.storage import TelemetryStorage
except ImportError:
    from backend.app.security.base import SecurityEvent
    from backend.app.security.telemetry.normalizer import TelemetryNormalizer
    from backend.app.security.telemetry.storage import TelemetryStorage


class TelemetryPipeline:
    """Ingests heterogeneous events, normalizes them, stores them in ledger, and streams to subscribers."""

    def __init__(self, storage: Optional[TelemetryStorage] = None):
        self.storage = storage or TelemetryStorage()
        self._subscribers: List[Callable[[SecurityEvent], None]] = []

    def subscribe(self, subscriber: Callable[[SecurityEvent], None]):
        self._subscribers.append(subscriber)

    def ingest_auth_event(self, raw_data: Dict[str, Any]) -> SecurityEvent:
        event = TelemetryNormalizer.normalize_auth_event(raw_data)
        return self._process_and_dispatch(event)

    def ingest_agent_event(self, raw_data: Dict[str, Any]) -> SecurityEvent:
        event = TelemetryNormalizer.normalize_agent_event(raw_data)
        return self._process_and_dispatch(event)

    def ingest_api_event(self, raw_data: Dict[str, Any]) -> SecurityEvent:
        event = TelemetryNormalizer.normalize_api_event(raw_data)
        return self._process_and_dispatch(event)

    def ingest_data_event(self, raw_data: Dict[str, Any]) -> SecurityEvent:
        event = TelemetryNormalizer.normalize_data_event(raw_data)
        return self._process_and_dispatch(event)

    def ingest_admin_event(self, raw_data: Dict[str, Any]) -> SecurityEvent:
        event = TelemetryNormalizer.normalize_admin_event(raw_data)
        return self._process_and_dispatch(event)

    def ingest_financial_event(self, raw_data: Dict[str, Any]) -> SecurityEvent:
        event = TelemetryNormalizer.normalize_financial_event(raw_data)
        return self._process_and_dispatch(event)

    def ingest_event(self, event: SecurityEvent) -> SecurityEvent:
        return self._process_and_dispatch(event)

    def ingest_raw(self, raw_data: Dict[str, Any]) -> SecurityEvent:
        event = TelemetryNormalizer.normalize(raw_data)
        return self._process_and_dispatch(event)

    def _process_and_dispatch(self, event: SecurityEvent) -> SecurityEvent:
        self.storage.append(event)
        for sub in self._subscribers:
            try:
                sub(event)
            except Exception:
                pass
        return event
