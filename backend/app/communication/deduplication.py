"""Notification Deduplication & Aggregation Engine."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple


class DeduplicationEngine:
    """Detects repeated notifications and aggregates them within time windows."""

    @staticmethod
    def generate_deduplication_key(
        event_type: str,
        resource_id: str,
        recipient_id: str,
    ) -> str:
        """Construct deterministic deduplication key."""
        return f"{event_type}:{resource_id}:{recipient_id}"

    @staticmethod
    def should_deduplicate(
        deduplication_key: str,
        existing_deliveries: List[Dict[str, Any]],
        window_minutes: int = 60,
        now: Optional[datetime] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Check if an active notification with identical key was delivered recently."""
        if not deduplication_key or not existing_deliveries:
            return False, None

        if now is None:
            now = datetime.now(timezone.utc)

        threshold = now - timedelta(minutes=window_minutes)

        for d in existing_deliveries:
            if d.get("deduplication_key") == deduplication_key:
                created_at = d.get("created_at")
                if isinstance(created_at, str):
                    try:
                        created_at = datetime.fromisoformat(created_at)
                    except Exception:
                        continue
                if created_at and created_at.tzinfo is None:
                    created_at = created_at.replace(tzinfo=timezone.utc)

                if created_at and created_at >= threshold:
                    return True, d.get("id")

        return False, None
