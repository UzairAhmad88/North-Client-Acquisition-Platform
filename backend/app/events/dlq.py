"""Dead Letter Queue manager for capturing and triaging failed messages."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.events.base import DomainEvent
from app.models.orchestration import DeadLetterMessage, DLQStatus


class DLQManager:
    """Manages recording, triaging, and replaying poisoned messages in the Dead Letter Queue."""

    @staticmethod
    async def record_dead_letter(
        db: AsyncSession,
        event: DomainEvent,
        consumer: str,
        attempt_count: int,
        failure_type: str,
        error_summary: str,
        workflow_id: Optional[str] = None,
    ) -> DeadLetterMessage:
        """Persist a failed message into the Dead Letter Queue."""
        dlq_entry = DeadLetterMessage(
            id=str(uuid.uuid4()),
            event_id=event.event_id,
            event_type=event.event_type,
            workflow_id=workflow_id,
            consumer=consumer,
            attempt_count=attempt_count,
            failure_type=failure_type,
            error_summary=error_summary,
            payload=event.payload,
            status=DLQStatus.PENDING,
            last_error_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        db.add(dlq_entry)
        await db.commit()
        return dlq_entry

    @staticmethod
    async def update_status(
        db: AsyncSession,
        dlq_id: str,
        new_status: DLQStatus,
    ) -> Optional[DeadLetterMessage]:
        """Update the triage status of a DLQ record."""
        stmt = select(DeadLetterMessage).where(DeadLetterMessage.id == dlq_id)
        result = await db.execute(stmt)
        entry = result.scalar_one_or_none()
        if entry:
            entry.status = new_status
            await db.commit()
        return entry
