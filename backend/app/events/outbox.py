"""Transactional Outbox implementation for atomic domain state updates and event publishing."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.events.base import DomainEvent
from app.events.bus import EventBus, global_event_bus
from app.models.orchestration import EventDeliveryStatus, EventOutbox, EventDeliveryAttempt


class OutboxPublisher:
    """Manages writing domain events to the outbox and reliable background dispatch."""

    def __init__(self, event_bus: EventBus = global_event_bus):
        self.event_bus = event_bus

    async def record_outbox_event(
        self,
        db: AsyncSession,
        event: DomainEvent,
    ) -> EventOutbox:
        """Stage a domain event into the transactional outbox table within active DB transaction."""
        outbox_entry = EventOutbox(
            id=str(uuid.uuid4()),
            event_id=event.event_id,
            event_type=event.event_type,
            event_version=event.event_version,
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            tenant_id=event.tenant_id,
            payload=event.payload,
            correlation_id=event.correlation_id,
            causation_id=event.causation_id,
            status=EventDeliveryStatus.PENDING,
            attempt_count=0,
            created_at=datetime.utcnow(),
        )
        db.add(outbox_entry)
        return outbox_entry

    async def process_pending_outbox_events(
        self,
        db: AsyncSession,
        batch_size: int = 50,
    ) -> int:
        """Query pending outbox events, publish to event bus, and update delivery status."""
        stmt = (
            select(EventOutbox)
            .where(EventOutbox.status == EventDeliveryStatus.PENDING)
            .order_by(EventOutbox.created_at.asc())
            .limit(batch_size)
        )
        result = await db.execute(stmt)
        events = result.scalars().all()

        published_count = 0
        for entry in events:
            domain_event = DomainEvent(
                event_id=entry.event_id,
                event_type=entry.event_type,
                event_version=entry.event_version,
                tenant_id=entry.tenant_id,
                aggregate_type=entry.aggregate_type,
                aggregate_id=entry.aggregate_id,
                occurred_at=entry.created_at,
                producer="outbox_publisher",
                correlation_id=entry.correlation_id,
                causation_id=entry.causation_id,
                payload=entry.payload,
            )

            start_time = datetime.utcnow()
            try:
                success = await self.event_bus.publish(domain_event)
                duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000.0

                if success:
                    entry.status = EventDeliveryStatus.PUBLISHED
                    entry.published_at = datetime.utcnow()
                    entry.attempt_count += 1
                    published_count += 1

                    attempt = EventDeliveryAttempt(
                        id=str(uuid.uuid4()),
                        outbox_id=entry.id,
                        attempt_number=entry.attempt_count,
                        status="SUCCESS",
                        duration_ms=duration_ms,
                        attempted_at=datetime.utcnow(),
                    )
                    db.add(attempt)
            except Exception as e:
                entry.attempt_count += 1
                if entry.attempt_count >= 3:
                    entry.status = EventDeliveryStatus.FAILED
                attempt = EventDeliveryAttempt(
                    id=str(uuid.uuid4()),
                    outbox_id=entry.id,
                    attempt_number=entry.attempt_count,
                    status="FAILED",
                    error_message=str(e),
                    duration_ms=(datetime.utcnow() - start_time).total_seconds() * 1000.0,
                    attempted_at=datetime.utcnow(),
                )
                db.add(attempt)

        if events:
            await db.commit()

        return published_count
