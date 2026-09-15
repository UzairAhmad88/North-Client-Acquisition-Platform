"""Idempotent Consumer Inbox for deduplicated message processing."""

import uuid
from datetime import datetime
from typing import Any, Callable, Dict, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.events.base import DomainEvent
from app.models.orchestration import EventInbox


class InboxConsumer:
    """Ensures each event is processed exactly once per named consumer."""

    @staticmethod
    async def is_duplicate(
        db: AsyncSession,
        event_id: str,
        consumer_name: str,
    ) -> bool:
        """Check if an event has already been successfully recorded in the consumer inbox."""
        stmt = (
            select(EventInbox)
            .where(
                EventInbox.event_id == event_id,
                EventInbox.consumer_name == consumer_name,
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def record_consumption(
        db: AsyncSession,
        event: DomainEvent,
        consumer_name: str,
    ) -> EventInbox:
        """Record successful consumption of a domain event in the inbox."""
        inbox_entry = EventInbox(
            id=str(uuid.uuid4()),
            event_id=event.event_id,
            event_type=event.event_type,
            consumer_name=consumer_name,
            tenant_id=event.tenant_id,
            status="PROCESSED",
            processed_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        db.add(inbox_entry)
        await db.flush()
        return inbox_entry

    @classmethod
    async def process_idempotent(
        cls,
        db: AsyncSession,
        event: DomainEvent,
        consumer_name: str,
        handler: Callable[[DomainEvent], Any],
    ) -> Dict[str, Any]:
        """Execute handler only if event has not yet been processed by consumer."""
        if await cls.is_duplicate(db, event.event_id, consumer_name):
            return {
                "status": "DUPLICATE_IGNORED",
                "event_id": event.event_id,
                "consumer": consumer_name,
            }

        # Execute handler
        try:
            if callable(handler):
                import asyncio
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(event)
                else:
                    result = handler(event)
            else:
                result = None

            await cls.record_consumption(db, event, consumer_name)
            await db.commit()
            return {
                "status": "PROCESSED",
                "event_id": event.event_id,
                "consumer": consumer_name,
                "result": result,
            }
        except Exception as e:
            await db.rollback()
            raise e
