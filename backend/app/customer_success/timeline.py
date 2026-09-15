"""Unified chronological event aggregator for client relationship timeline."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.customer_success.base import TimelineEventData


class ClientTimelineAggregator:
    """Consolidates domain events from projects, finance, support, communications, and customer success into a unified client timeline."""

    @staticmethod
    def create_timeline_event(
        client_id: str,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        actor_type: str = "SYSTEM",
        actor_id: Optional[str] = None,
        source_entity_type: Optional[str] = None,
        source_entity_id: Optional[str] = None,
        occurred_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Creates a standardized timeline event record."""
        now = occurred_at or datetime.now(timezone.utc)
        return {
            "id": str(uuid.uuid4()),
            "client_id": client_id,
            "event_type": event_type,
            "title": title,
            "description": description,
            "actor_type": actor_type,
            "actor_id": actor_id,
            "source_entity_type": source_entity_type,
            "source_entity_id": source_entity_id,
            "occurred_at": now.isoformat() if isinstance(now, datetime) else now,
            "metadata": metadata or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    @classmethod
    def aggregate_timeline(
        cls,
        events: List[Dict[str, Any]],
        limit: int = 50,
        event_type_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Sorts and filters client timeline events chronologically descending."""
        filtered = events
        if event_type_filter:
            filtered = [e for e in filtered if e.get("event_type") == event_type_filter]

        sorted_events = sorted(
            filtered,
            key=lambda x: x.get("occurred_at", ""),
            reverse=True
        )
        return sorted_events[:limit]
