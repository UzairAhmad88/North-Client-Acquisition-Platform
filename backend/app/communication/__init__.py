"""Phase 37 Unified Communication, Notification, Inbox & Real-Time Collaboration."""

from app.communication.audience import AudienceResolver
from app.communication.base import (
    CommunicationType,
    ConversationType,
    DeliveryChannel,
    DeliveryPayload,
    DeliveryStatus,
    InboxState,
    MessageVisibility,
    NotificationPriority,
)
from app.communication.deduplication import DeduplicationEngine
from app.communication.engine import CommunicationEngine
from app.communication.policies import CommunicationPolicyEngine, QuietHoursPolicy

__all__ = [
    "CommunicationType",
    "ConversationType",
    "DeliveryChannel",
    "DeliveryPayload",
    "DeliveryStatus",
    "InboxState",
    "MessageVisibility",
    "NotificationPriority",
    "AudienceResolver",
    "DeduplicationEngine",
    "CommunicationEngine",
    "CommunicationPolicyEngine",
    "QuietHoursPolicy",
]
