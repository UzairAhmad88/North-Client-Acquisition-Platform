"""Notification and Unified Inbox Management Service."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.communication.base import (
    CommunicationType,
    InboxState,
    NotificationPriority,
)


class NotificationManager:
    """Handles notification lifecycle and inbox item aggregation."""

    @staticmethod
    def create_inbox_item(
        recipient_id: str,
        tenant_id: str,
        title: str,
        body: str,
        category: CommunicationType = CommunicationType.OPERATIONAL,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        source_type: Optional[str] = None,
        source_id: Optional[str] = None,
        action_url: Optional[str] = None,
        action_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Construct a unified inbox item record."""
        return {
            "id": str(uuid.uuid4()),
            "recipient_id": recipient_id,
            "tenant_id": tenant_id,
            "title": title,
            "body": body,
            "category": category.value if hasattr(category, "value") else str(category),
            "priority": priority.value if hasattr(priority, "value") else str(priority),
            "source_type": source_type,
            "source_id": source_id,
            "action_url": action_url,
            "action_type": action_type,
            "state": InboxState.UNREAD.value,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "read_at": None,
            "archived_at": None,
            "snoozed_until": None,
        }

    @staticmethod
    def transition_inbox_state(
        item: Dict[str, Any], target_state: InboxState, snooze_until: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Update inbox state (Read != Approval)."""
        item["state"] = target_state.value if hasattr(target_state, "value") else str(target_state)
        now_iso = datetime.now(timezone.utc).isoformat()

        if target_state == InboxState.READ:
            item["read_at"] = now_iso
        elif target_state == InboxState.ARCHIVED:
            item["archived_at"] = now_iso
        elif target_state == InboxState.SNOOZED and snooze_until:
            item["snoozed_until"] = snooze_until.isoformat()

        return item
