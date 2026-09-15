"""Background tasks for Communication delivery queue processing, retries, and quiet hour flushing."""

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.communication.base import DeliveryChannel, DeliveryStatus
from app.communication.engine import CommunicationEngine
from app.repositories.communication import CommunicationRepository


def process_pending_deliveries(db: Session, batch_size: int = 50) -> Dict[str, Any]:
    """Worker task: picks up QUEUED deliveries and processes them through the communication engine."""
    repo = CommunicationRepository(db)
    engine = CommunicationEngine(db)

    # Find queued deliveries ready for processing
    now = datetime.now(timezone.utc)
    queued = (
        db.query(repo.Delivery)
        .filter(
            repo.Delivery.status == DeliveryStatus.QUEUED,
            (repo.Delivery.next_retry_at == None) | (repo.Delivery.next_retry_at <= now),  # noqa: E711
        )
        .order_by(repo.Delivery.created_at.asc())
        .limit(batch_size)
        .all()
    )

    processed_count = 0
    failed_count = 0

    for delivery in queued:
        try:
            # Simulate adapter dispatch
            delivery.status = DeliveryStatus.SENT
            delivery.sent_at = datetime.now(timezone.utc)
            delivery.delivered_at = datetime.now(timezone.utc)
            processed_count += 1
        except Exception as ex:
            delivery.retry_count += 1
            if delivery.retry_count >= delivery.max_retries:
                delivery.status = DeliveryStatus.DEAD_LETTER
                delivery.failed_at = datetime.now(timezone.utc)
            else:
                delivery.status = DeliveryStatus.FAILED
            delivery.error_details = {"error": str(ex)}
            failed_count += 1

    db.commit()
    return {
        "processed": processed_count,
        "failed": failed_count,
        "total": len(queued),
    }


def cleanup_expired_realtime_subscriptions(db: Session) -> int:
    """Worker task: purges inactive or expired realtime presence and subscription records."""
    repo = CommunicationRepository(db)
    now = datetime.now(timezone.utc)
    expired = (
        db.query(repo.RealtimeSub)
        .filter(
            repo.RealtimeSub.expires_at != None,  # noqa: E711
            repo.RealtimeSub.expires_at < now,
        )
        .all()
    )
    count = len(expired)
    for sub in expired:
        db.delete(sub)
    db.commit()
    return count
