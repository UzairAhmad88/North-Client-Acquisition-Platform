"""Unified Communication Service Layer.

Provides high-level business logic orchestration for notifications, inbox management,
conversations/messaging, preferences, real-time collaboration, and delivery auditing.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.communication.base import (
    CommunicationType,
    ConversationType,
    DeliveryChannel,
    DeliveryStatus,
    InboxState,
    MessageVisibility,
    NotificationPriority,
)
from app.communication.engine import CommunicationEngine
from app.messaging.conversations import MessagingManager
from app.notifications.service import NotificationManager
from app.realtime.gateway import RealtimeGateway
from app.repositories.communication import CommunicationRepository
from app.schemas.communication import (
    ConversationCreateRequest,
    ConversationMessageCreateRequest,
    ConversationMessageEditRequest,
    DeliveryRetryRequest,
    InboxBulkUpdateRequest,
    InboxItemUpdateRequest,
    NotificationCreateRequest,
    NotificationPreferenceUpdateRequest,
)


class CommunicationService:
    """Service layer orchestrator for all Phase 37 unified communication capabilities."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = CommunicationRepository(db)
        self.engine = CommunicationEngine(db)
        self.notification_manager = NotificationManager(db)
        self.messaging_manager = MessagingManager(db)
        self.realtime_gateway = RealtimeGateway(db)

    # -------------------------------------------------------------------------
    # Notifications
    # -------------------------------------------------------------------------

    def create_notification(
        self,
        tenant_id: UUID,
        request: NotificationCreateRequest,
        actor_id: Optional[UUID] = None,
    ) -> Dict[str, Any]:
        """Dispatch a notification using the unified communication engine."""
        return self.engine.dispatch_notification(
            tenant_id=tenant_id,
            notification_type=request.notification_type,
            title=request.title,
            body=request.body,
            priority=request.priority,
            source_module=request.source_module,
            source_event_id=request.source_event_id,
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            action_url=request.action_url,
            actor_id=actor_id,
            recipients=request.recipients,
            channels=request.channels,
            idempotency_key=request.idempotency_key,
            metadata=request.metadata,
        )

    def get_notification(
        self, tenant_id: UUID, notification_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a single notification record by ID."""
        rec = self.repo.get_notification(tenant_id, notification_id)
        if not rec:
            return None
        return {
            "id": rec.id,
            "tenant_id": rec.tenant_id,
            "notification_type": rec.notification_type,
            "priority": rec.priority,
            "title": rec.title,
            "body": rec.body,
            "source_module": rec.source_module,
            "source_event_id": rec.source_event_id,
            "entity_type": rec.entity_type,
            "entity_id": rec.entity_id,
            "action_url": rec.action_url,
            "actor_id": rec.actor_id,
            "idempotency_key": rec.idempotency_key,
            "metadata": rec.metadata_ or {},
            "created_at": rec.created_at,
        }

    def list_notifications(
        self,
        tenant_id: UUID,
        source_module: Optional[str] = None,
        priority: Optional[NotificationPriority] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List notification records for a tenant."""
        records = self.repo.list_notifications(
            tenant_id=tenant_id,
            source_module=source_module,
            priority=priority,
            limit=limit,
            offset=offset,
        )
        return [
            {
                "id": rec.id,
                "tenant_id": rec.tenant_id,
                "notification_type": rec.notification_type,
                "priority": rec.priority,
                "title": rec.title,
                "body": rec.body,
                "source_module": rec.source_module,
                "source_event_id": rec.source_event_id,
                "entity_type": rec.entity_type,
                "entity_id": rec.entity_id,
                "action_url": rec.action_url,
                "actor_id": rec.actor_id,
                "idempotency_key": rec.idempotency_key,
                "metadata": rec.metadata_ or {},
                "created_at": rec.created_at,
            }
            for rec in records
        ]

    # -------------------------------------------------------------------------
    # Unified Inbox
    # -------------------------------------------------------------------------

    def list_inbox_items(
        self,
        tenant_id: UUID,
        recipient_id: UUID,
        state: Optional[InboxState] = None,
        is_read: Optional[bool] = None,
        is_pinned: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List personal inbox items for a user."""
        items = self.repo.list_inbox_items(
            tenant_id=tenant_id,
            recipient_id=recipient_id,
            state=state,
            is_read=is_read,
            is_pinned=is_pinned,
            limit=limit,
            offset=offset,
        )
        return [
            {
                "id": item.id,
                "tenant_id": item.tenant_id,
                "recipient_id": item.recipient_id,
                "notification_id": item.notification_id,
                "conversation_message_id": item.conversation_message_id,
                "item_type": item.item_type,
                "title": item.title,
                "summary": item.summary,
                "priority": item.priority,
                "state": item.state,
                "is_read": item.is_read,
                "is_starred": item.is_starred,
                "is_pinned": item.is_pinned,
                "read_at": item.read_at,
                "snoozed_until": item.snoozed_until,
                "action_url": item.action_url,
                "entity_type": item.entity_type,
                "entity_id": item.entity_id,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]

    def update_inbox_item(
        self,
        tenant_id: UUID,
        recipient_id: UUID,
        inbox_item_id: UUID,
        request: InboxItemUpdateRequest,
    ) -> Optional[Dict[str, Any]]:
        """Update read, starred, pinned, or state flags on an inbox item."""
        updated = self.notification_manager.update_inbox_item_state(
            tenant_id=tenant_id,
            recipient_id=recipient_id,
            inbox_item_id=inbox_item_id,
            state=request.state,
            is_read=request.is_read,
            is_starred=request.is_starred,
            is_pinned=request.is_pinned,
            snoozed_until=request.snoozed_until,
        )
        if not updated:
            return None
        return {
            "id": updated.id,
            "tenant_id": updated.tenant_id,
            "recipient_id": updated.recipient_id,
            "notification_id": updated.notification_id,
            "conversation_message_id": updated.conversation_message_id,
            "item_type": updated.item_type,
            "title": updated.title,
            "summary": updated.summary,
            "priority": updated.priority,
            "state": updated.state,
            "is_read": updated.is_read,
            "is_starred": updated.is_starred,
            "is_pinned": updated.is_pinned,
            "read_at": updated.read_at,
            "snoozed_until": updated.snoozed_until,
            "action_url": updated.action_url,
            "entity_type": updated.entity_type,
            "entity_id": updated.entity_id,
            "created_at": updated.created_at,
            "updated_at": updated.updated_at,
        }

    def bulk_update_inbox(
        self,
        tenant_id: UUID,
        recipient_id: UUID,
        request: InboxBulkUpdateRequest,
    ) -> Dict[str, Any]:
        """Perform bulk state transitions across multiple inbox items."""
        count = self.notification_manager.bulk_update_inbox(
            tenant_id=tenant_id,
            recipient_id=recipient_id,
            item_ids=request.item_ids,
            state=request.state,
            is_read=request.is_read,
            is_starred=request.is_starred,
            is_pinned=request.is_pinned,
            snoozed_until=request.snoozed_until,
        )
        return {
            "updated_count": count,
            "tenant_id": tenant_id,
            "recipient_id": recipient_id,
        }

    def get_inbox_unread_count(self, tenant_id: UUID, recipient_id: UUID) -> int:
        """Get the total count of unread inbox items."""
        return self.repo.get_inbox_unread_count(tenant_id, recipient_id)

    # -------------------------------------------------------------------------
    # Conversations & Messaging
    # -------------------------------------------------------------------------

    def create_conversation(
        self,
        tenant_id: UUID,
        creator_id: UUID,
        request: ConversationCreateRequest,
    ) -> Dict[str, Any]:
        """Create a new unified conversation thread."""
        return self.messaging_manager.create_conversation(
            tenant_id=tenant_id,
            title=request.title,
            conversation_type=request.conversation_type,
            creator_id=creator_id,
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            initial_members=request.initial_members,
            metadata=request.metadata,
        )

    def list_conversations(
        self,
        tenant_id: UUID,
        user_id: UUID,
        conversation_type: Optional[ConversationType] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List active conversations that the user is a member of."""
        records = self.repo.list_conversations_for_user(
            tenant_id=tenant_id,
            user_id=user_id,
            conversation_type=conversation_type,
            entity_type=entity_type,
            entity_id=entity_id,
            limit=limit,
            offset=offset,
        )
        return [
            {
                "id": rec.id,
                "tenant_id": rec.tenant_id,
                "title": rec.title,
                "conversation_type": rec.conversation_type,
                "entity_type": rec.entity_type,
                "entity_id": rec.entity_id,
                "created_by": rec.created_by,
                "is_closed": rec.is_closed,
                "closed_at": rec.closed_at,
                "closed_by": rec.closed_by,
                "metadata": rec.metadata_ or {},
                "created_at": rec.created_at,
                "updated_at": rec.updated_at,
            }
            for rec in records
        ]

    def get_conversation_details(
        self,
        tenant_id: UUID,
        conversation_id: UUID,
        user_id: UUID,
        is_client_user: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve complete conversation thread with messages filtered by visibility."""
        return self.messaging_manager.get_conversation_thread(
            tenant_id=tenant_id,
            conversation_id=conversation_id,
            user_id=user_id,
            is_client_user=is_client_user,
        )

    def post_message(
        self,
        tenant_id: UUID,
        conversation_id: UUID,
        sender_id: UUID,
        request: ConversationMessageCreateRequest,
        is_client_user: bool = False,
    ) -> Dict[str, Any]:
        """Post a new message or note to a conversation."""
        return self.messaging_manager.post_message(
            tenant_id=tenant_id,
            conversation_id=conversation_id,
            sender_id=sender_id,
            body=request.body,
            visibility=request.visibility,
            parent_id=request.parent_id,
            is_client_user=is_client_user,
            attachments=request.attachments,
            metadata=request.metadata,
        )

    def edit_message(
        self,
        tenant_id: UUID,
        message_id: UUID,
        actor_id: UUID,
        request: ConversationMessageEditRequest,
    ) -> Dict[str, Any]:
        """Edit a message with immutable audit version snapshotting."""
        return self.messaging_manager.edit_message(
            tenant_id=tenant_id,
            message_id=message_id,
            actor_id=actor_id,
            new_body=request.new_body,
            edit_reason=request.edit_reason,
        )

    # -------------------------------------------------------------------------
    # Notification Preferences
    # -------------------------------------------------------------------------

    def get_user_preferences(
        self, tenant_id: UUID, user_id: UUID
    ) -> List[Dict[str, Any]]:
        """List all notification category preferences for a user."""
        prefs = self.repo.list_user_preferences(tenant_id, user_id)
        return [
            {
                "id": p.id,
                "tenant_id": p.tenant_id,
                "user_id": p.user_id,
                "notification_type": p.notification_type,
                "in_app_enabled": p.in_app_enabled,
                "email_enabled": p.email_enabled,
                "sms_enabled": p.sms_enabled,
                "webhook_enabled": p.webhook_enabled,
                "push_enabled": p.push_enabled,
                "quiet_hours_start": p.quiet_hours_start,
                "quiet_hours_end": p.quiet_hours_end,
                "timezone": p.timezone,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            }
            for p in prefs
        ]

    def update_user_preference(
        self,
        tenant_id: UUID,
        user_id: UUID,
        request: NotificationPreferenceUpdateRequest,
    ) -> Dict[str, Any]:
        """Update or create a notification preference for a specific notification type."""
        pref = self.repo.upsert_preference(
            tenant_id=tenant_id,
            user_id=user_id,
            notification_type=request.notification_type,
            in_app_enabled=request.in_app_enabled,
            email_enabled=request.email_enabled,
            sms_enabled=request.sms_enabled,
            webhook_enabled=request.webhook_enabled,
            push_enabled=request.push_enabled,
            quiet_hours_start=request.quiet_hours_start,
            quiet_hours_end=request.quiet_hours_end,
            timezone=request.timezone,
        )
        return {
            "id": pref.id,
            "tenant_id": pref.tenant_id,
            "user_id": pref.user_id,
            "notification_type": pref.notification_type,
            "in_app_enabled": pref.in_app_enabled,
            "email_enabled": pref.email_enabled,
            "sms_enabled": pref.sms_enabled,
            "webhook_enabled": pref.webhook_enabled,
            "push_enabled": pref.push_enabled,
            "quiet_hours_start": pref.quiet_hours_start,
            "quiet_hours_end": pref.quiet_hours_end,
            "timezone": pref.timezone,
            "created_at": pref.created_at,
            "updated_at": pref.updated_at,
        }

    # -------------------------------------------------------------------------
    # Communication Delivery Auditing & Retries
    # -------------------------------------------------------------------------

    def list_deliveries(
        self,
        tenant_id: UUID,
        status: Optional[DeliveryStatus] = None,
        channel: Optional[DeliveryChannel] = None,
        recipient_id: Optional[UUID] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List delivery audit records with filtering."""
        records = self.repo.list_deliveries(
            tenant_id=tenant_id,
            status=status,
            channel=channel,
            recipient_id=recipient_id,
            limit=limit,
            offset=offset,
        )
        return [
            {
                "id": rec.id,
                "tenant_id": rec.tenant_id,
                "notification_id": rec.notification_id,
                "recipient_id": rec.recipient_id,
                "channel": rec.channel,
                "status": rec.status,
                "provider": rec.provider,
                "provider_message_id": rec.provider_message_id,
                "retry_count": rec.retry_count,
                "max_retries": rec.max_retries,
                "next_retry_at": rec.next_retry_at,
                "sent_at": rec.sent_at,
                "delivered_at": rec.delivered_at,
                "failed_at": rec.failed_at,
                "error_details": rec.error_details or {},
                "created_at": rec.created_at,
            }
            for rec in records
        ]

    def retry_delivery(
        self,
        tenant_id: UUID,
        request: DeliveryRetryRequest,
    ) -> Dict[str, Any]:
        """Manually trigger retry for a failed or dead-letter delivery."""
        delivery = self.repo.get_delivery(tenant_id, request.delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {request.delivery_id} not found in tenant")

        if delivery.status not in (DeliveryStatus.FAILED, DeliveryStatus.DEAD_LETTER):
            raise ValueError(f"Delivery is in state {delivery.status}, only failed/DLQ can be retried")

        delivery.status = DeliveryStatus.QUEUED
        delivery.retry_count = 0
        delivery.next_retry_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(delivery)

        return {
            "delivery_id": delivery.id,
            "status": delivery.status,
            "message": "Delivery requeued for processing",
        }
