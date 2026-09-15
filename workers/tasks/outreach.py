"""Worker task executing guarded outreach send operations."""

import asyncio
import uuid
from typing import Optional
from sqlalchemy.orm import Session

from app.models.outreach import OutreachDraft
from app.services.outreach.communication_service import CommunicationService


async def execute_outreach_send_task(
    db: Session,
    draft_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    """Asynchronous worker task executing guarded outreach send."""
    draft = db.query(OutreachDraft).filter(OutreachDraft.id == draft_id).first()
    if not draft:
        return

    await CommunicationService.send_outreach(db, draft_id, user_id)


def run_outreach_send_task_sync(
    db: Session,
    draft_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    asyncio.run(execute_outreach_send_task(db, draft_id, user_id))
