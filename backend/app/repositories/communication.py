"""Repository layer for Phase 37: Unified Notification, Communication, Inbox & Real-Time Collaboration."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy import func, select, desc, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.communication import (
    NotificationRecord,
    NotificationTemplateRecord,
    NotificationPreferenceRecord,
    InboxItemRecord,
    ConversationRecord,
    ConversationMemberRecord,
    ConversationMessageRecord,
    ConversationMessageVersionRecord,
    ConversationAttachmentRecord,
    CommunicationDeliveryRecord,
    CommunicationAuditRecord,
    RealtimeSubscriptionRecord,
)
from app.communication.base import InboxState, MessageVisibility


class CommunicationRepository:
    """Database repository for Phase 37 Inbox, Notifications, Conversations, Messages, and Deliveries."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # -------------------------------------------------------------
    # 1. Unified Inbox
    # -------------------------------------------------------------
    async def list_inbox_items(
        self,
        tenant_id: str,
        recipient_id: str,
        state: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[InboxItemRecord]:
        stmt = (
            select(InboxItemRecord)
            .where(
                and_(
                    InboxItemRecord.tenant_id == tenant_id,
                    InboxItemRecord.recipient_id == recipient_id,
                )
            )
            .order_by(desc(InboxItemRecord.created_at))
        )
        if state:
            stmt = stmt.where(InboxItemRecord.state == state)
        if category:
            stmt = stmt.where(InboxItemRecord.category == category)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_unread_inbox_count(self, tenant_id: str, recipient_id: str) -> int:
        stmt = select(func.count(InboxItemRecord.id)).where(
            and_(
                InboxItemRecord.tenant_id == tenant_id,
                InboxItemRecord.recipient_id == recipient_id,
                InboxItemRecord.state == InboxState.UNREAD.value,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def get_inbox_item(self, item_id: str) -> Optional[InboxItemRecord]:
        stmt = select(InboxItemRecord).where(InboxItemRecord.id == item_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_inbox_item(self, item: InboxItemRecord) -> InboxItemRecord:
        self.db.add(item)
        await self.db.flush()
        return item

    # -------------------------------------------------------------
    # 2. Notifications & Preferences
    # -------------------------------------------------------------
    async def list_notifications(
        self,
        tenant_id: str,
        recipient_id: str,
        limit: int = 50,
    ) -> List[NotificationRecord]:
        stmt = (
            select(NotificationRecord)
            .where(
                and_(
                    NotificationRecord.tenant_id == tenant_id,
                    NotificationRecord.recipient_id == recipient_id,
                )
            )
            .order_by(desc(NotificationRecord.created_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_notification(self, notification_id: str) -> Optional[NotificationRecord]:
        stmt = select(NotificationRecord).where(NotificationRecord.id == notification_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_notification(self, notif: NotificationRecord) -> NotificationRecord:
        self.db.add(notif)
        await self.db.flush()
        return notif

    async def get_user_preferences(self, user_id: str) -> Optional[NotificationPreferenceRecord]:
        stmt = select(NotificationPreferenceRecord).where(NotificationPreferenceRecord.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_user_preferences(
        self, pref: NotificationPreferenceRecord
    ) -> NotificationPreferenceRecord:
        self.db.add(pref)
        await self.db.flush()
        return pref

    # -------------------------------------------------------------
    # 3. Conversations & Messages
    # -------------------------------------------------------------
    async def list_conversations(
        self,
        tenant_id: str,
        conversation_type: Optional[str] = None,
        project_id: Optional[str] = None,
        client_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[ConversationRecord]:
        stmt = (
            select(ConversationRecord)
            .options(
                selectinload(ConversationRecord.messages),
            )
            .where(ConversationRecord.tenant_id == tenant_id)
            .order_by(desc(ConversationRecord.created_at))
        )
        if conversation_type:
            stmt = stmt.where(ConversationRecord.conversation_type == conversation_type)
        if project_id:
            stmt = stmt.where(ConversationRecord.project_id == project_id)
        if client_id:
            stmt = stmt.where(ConversationRecord.client_id == client_id)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_conversation(self, conversation_id: uuid.UUID) -> Optional[ConversationRecord]:
        stmt = (
            select(ConversationRecord)
            .options(
                selectinload(ConversationRecord.messages).selectinload(ConversationMessageRecord.versions),
                selectinload(ConversationRecord.messages).selectinload(ConversationMessageRecord.attachments),
            )
            .where(ConversationRecord.id == conversation_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_conversation(self, conv: ConversationRecord) -> ConversationRecord:
        self.db.add(conv)
        await self.db.flush()
        return conv

    async def create_message(self, msg: ConversationMessageRecord) -> ConversationMessageRecord:
        self.db.add(msg)
        await self.db.flush()
        return msg

    async def add_message_version(
        self, ver: ConversationMessageVersionRecord
    ) -> ConversationMessageVersionRecord:
        self.db.add(ver)
        await self.db.flush()
        return ver

    async def get_message(self, message_id: uuid.UUID) -> Optional[ConversationMessageRecord]:
        stmt = (
            select(ConversationMessageRecord)
            .options(
                selectinload(ConversationMessageRecord.versions),
                selectinload(ConversationMessageRecord.attachments),
            )
            .where(ConversationMessageRecord.id == message_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # -------------------------------------------------------------
    # 4. Deliveries & Audit
    # -------------------------------------------------------------
    async def record_delivery(
        self, delivery: CommunicationDeliveryRecord
    ) -> CommunicationDeliveryRecord:
        self.db.add(delivery)
        await self.db.flush()
        return delivery

    async def list_deliveries(
        self, tenant_id: str, limit: int = 50
    ) -> List[CommunicationDeliveryRecord]:
        stmt = (
            select(CommunicationDeliveryRecord)
            .where(CommunicationDeliveryRecord.tenant_id == tenant_id)
            .order_by(desc(CommunicationDeliveryRecord.created_at))
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def record_audit(self, audit: CommunicationAuditRecord) -> CommunicationAuditRecord:
        self.db.add(audit)
        await self.db.flush()
        return audit
