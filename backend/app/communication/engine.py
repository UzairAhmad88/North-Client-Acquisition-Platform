"""Central Communication Engine orchestrating policies, channels, and delivery."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.communication.audience import AudienceResolver
from app.communication.base import (
    CommunicationType,
    DeliveryChannel,
    DeliveryPayload,
    DeliveryStatus,
    NotificationPriority,
)
from app.communication.deduplication import DeduplicationEngine
from app.communication.policies import CommunicationPolicyEngine, QuietHoursPolicy


class CommunicationEngine:
    """Core router and dispatcher for unified platform notifications and messaging."""

    def __init__(self):
        self.policy_engine = CommunicationPolicyEngine()
        self.audience_resolver = AudienceResolver()
        self.dedup_engine = DeduplicationEngine()

    def process_event_notification(
        self,
        event_type: str,
        tenant_id: str,
        recipients: List[str],
        title: str,
        message: str,
        category: CommunicationType = CommunicationType.OPERATIONAL,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        channels: Optional[List[DeliveryChannel]] = None,
        action_url: Optional[str] = None,
        action_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        quiet_hours: Optional[QuietHoursPolicy] = None,
        recent_deliveries: Optional[List[Dict[str, Any]]] = None,
    ) -> List[DeliveryPayload]:
        """Transform event into validated, deduplicated delivery payloads."""
        if channels is None:
            channels = [DeliveryChannel.IN_APP]

        if quiet_hours is None:
            quiet_hours = QuietHoursPolicy(enabled=False)

        # 1. Quiet hours check
        suppress, reason = self.policy_engine.should_suppress_for_quiet_hours(
            priority=priority, category=category, quiet_hours=quiet_hours
        )

        deliveries: List[DeliveryPayload] = []

        for recipient in recipients:
            dedup_key = (
                self.dedup_engine.generate_deduplication_key(event_type, resource_id, recipient)
                if resource_id
                else None
            )

            if dedup_key and recent_deliveries:
                is_duplicate, _ = self.dedup_engine.should_deduplicate(
                    dedup_key, recent_deliveries
                )
                if is_duplicate:
                    continue  # Skip duplicate

            for channel in channels:
                # If suppressed by quiet hours and not in-app, skip or delay external channel
                if suppress and channel != DeliveryChannel.IN_APP:
                    continue

                payload = DeliveryPayload(
                    recipient_id=recipient,
                    tenant_id=tenant_id,
                    subject=title,
                    body=message,
                    channel=channel,
                    priority=priority,
                    category=category,
                    action_url=action_url,
                    action_type=action_type,
                    metadata={"event_type": event_type, "resource_id": resource_id},
                    deduplication_key=dedup_key,
                )
                deliveries.append(payload)

        return deliveries

    def validate_external_communication_boundary(
        self,
        channel: DeliveryChannel,
        is_external: bool,
        has_human_approval: bool,
        risk_level: str,
    ) -> bool:
        """Enforce strict guardrail: external communication cannot send without human approval and risk check."""
        if is_external and channel in (DeliveryChannel.EMAIL, DeliveryChannel.MESSAGING):
            if not has_human_approval:
                return False
            if risk_level.upper() in ("BLOCK", "CRITICAL", "HIGH_RISK"):
                return False
        return True
