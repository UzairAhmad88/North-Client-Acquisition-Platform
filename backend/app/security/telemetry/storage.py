"""
Telemetry immutable in-memory / persistent buffer storage with cryptographic chain hashing.
"""

from typing import List, Dict, Any, Optional
import hashlib
from datetime import datetime

try:
    from app.security.base import SecurityEvent
except ImportError:
    from backend.app.security.base import SecurityEvent


class TelemetryStorage:
    """Stores security events in an append-only verifiable ledger with cryptographic hash chaining."""

    def __init__(self):
        self._events: List[SecurityEvent] = []
        self._event_hashes: List[str] = []
        self._last_hash: str = "0" * 64

    def append(self, event: SecurityEvent) -> str:
        """Appends a normalized event and computes its cryptographic hash chained to the previous event."""
        payload = event.model_dump_json()
        combined = f"{self._last_hash}:{payload}".encode("utf-8")
        current_hash = hashlib.sha256(combined).hexdigest()

        self._events.append(event)
        self._event_hashes.append(current_hash)
        self._last_hash = current_hash
        return current_hash

    def query(
        self,
        tenant_id: Optional[str] = None,
        source_type: Optional[str] = None,
        actor_id: Optional[str] = None,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[SecurityEvent]:
        """Queries events matching filter criteria."""
        results = []
        for evt in reversed(self._events):
            if tenant_id and evt.tenant_id != tenant_id:
                continue
            if source_type and evt.source.value != source_type and evt.source != source_type:
                continue
            if actor_id and evt.principal_id != actor_id:
                continue
            if since and evt.timestamp < since:
                continue
            results.append(evt)
            if len(results) >= limit:
                break
        return results

    def verify_integrity(self) -> bool:
        """Verifies the cryptographic chain integrity of all stored events."""
        last = "0" * 64
        for evt, recorded_hash in zip(self._events, self._event_hashes):
            payload = evt.model_dump_json()
            recomputed = hashlib.sha256(f"{last}:{payload}".encode("utf-8")).hexdigest()
            if recomputed != recorded_hash:
                return False
            last = recomputed
        return True

    def count(self) -> int:
        return len(self._events)
