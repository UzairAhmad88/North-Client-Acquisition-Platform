"""Controlled Event Replay Engine with side-effect safeguards."""

import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.events.base import DomainEvent
from app.models.orchestration import EventOutbox, EventReplay, ReplayMode


# Sensitive domain actions that must NEVER execute side effects during replay
SENSITIVE_REPLAY_BLOCKS = {
    "outreach.sent",
    "contract.signed",
    "proposal.accepted",
    "delivery.accepted",
    "change.approved",
}


class EventReplayEngine:
    """Safely executes historical domain event replay while blocking sensitive external side-effects."""

    @staticmethod
    async def execute_replay(
        db: AsyncSession,
        tenant_id: str,
        event_type: str,
        replay_mode: ReplayMode,
        triggered_by: str,
        handler: Optional[Callable[[DomainEvent], Any]] = None,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> EventReplay:
        """Execute replay for historical events matching filter criteria."""
        filter_criteria = filter_criteria or {}

        # 1. Query historical outbox events
        stmt = (
            select(EventOutbox)
            .where(
                EventOutbox.tenant_id == tenant_id,
                EventOutbox.event_type == event_type,
            )
            .order_by(EventOutbox.created_at.asc())
        )
        result = await db.execute(stmt)
        events = result.scalars().all()

        replayed_count = 0
        for entry in events:
            domain_event = DomainEvent(
                event_id=f"replay_{entry.event_id}",
                event_type=entry.event_type,
                event_version=entry.event_version,
                tenant_id=entry.tenant_id,
                aggregate_type=entry.aggregate_type,
                aggregate_id=entry.aggregate_id,
                occurred_at=entry.created_at,
                producer=f"replay_engine_{triggered_by}",
                correlation_id=entry.correlation_id,
                causation_id=entry.event_id,
                payload=entry.payload,
            )

            # Enforce Replay Safety Guard
            if replay_mode in (ReplayMode.READ_ONLY, ReplayMode.DRY_RUN):
                # Never execute handlers with side effects
                replayed_count += 1
            elif replay_mode in (ReplayMode.REBUILD_PROJECTION, ReplayMode.CONTROLLED_REEXECUTION):
                if entry.event_type in SENSITIVE_REPLAY_BLOCKS:
                    # Explicitly block sensitive external communication during replay
                    replayed_count += 1
                    continue

                if handler and callable(handler):
                    import asyncio
                    if asyncio.iscoroutinefunction(handler):
                        await handler(domain_event)
                    else:
                        handler(domain_event)
                replayed_count += 1

        # 2. Record replay log
        replay_record = EventReplay(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            event_type=event_type,
            filter_criteria=filter_criteria,
            replay_mode=replay_mode,
            events_replayed_count=replayed_count,
            triggered_by=triggered_by,
            status="COMPLETED",
            created_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
        )
        db.add(replay_record)
        await db.commit()
        return replay_record
