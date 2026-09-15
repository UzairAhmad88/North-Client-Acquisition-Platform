"""Webhook security validator enforcing signature verification, replay protection, and idempotency."""

import hmac
import hashlib
import time
from typing import Any, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.response import InboundEventLog
from integrations.inbound.models import WebhookVerificationResult


class WebhookSecurityGuard:
    """Enforces webhook security, replay protection, and idempotency deduplication."""

    REPLAY_WINDOW_SECONDS = 300  # 5 minutes

    @staticmethod
    def verify_signature(
        raw_body: bytes,
        signature: Optional[str],
        secret: str,
        timestamp_header: Optional[str] = None,
    ) -> WebhookVerificationResult:
        """Verify HMAC-SHA256 signature and timestamp freshness."""
        if not signature:
            return WebhookVerificationResult(
                is_valid=False, error_code="MISSING_SIGNATURE", reason="Webhook signature header missing"
            )

        if timestamp_header:
            try:
                ts = float(timestamp_header)
                if abs(time.time() - ts) > WebhookSecurityGuard.REPLAY_WINDOW_SECONDS:
                    return WebhookVerificationResult(
                        is_valid=False, error_code="REPLAY_ATTACK", reason="Webhook timestamp outside replay window"
                    )
            except ValueError:
                return WebhookVerificationResult(
                    is_valid=False, error_code="INVALID_TIMESTAMP", reason="Invalid timestamp header format"
                )

        computed = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(computed, signature):
            return WebhookVerificationResult(
                is_valid=False, error_code="SIGNATURE_MISMATCH", reason="Webhook signature verification failed"
            )

        return WebhookVerificationResult(is_valid=True)

    @staticmethod
    def is_duplicate_event(db: Session, provider: str, provider_event_id: str) -> Tuple[bool, Optional[str]]:
        """Check if provider event ID was already processed (idempotency check)."""
        existing = (
            db.query(InboundEventLog)
            .filter(
                (InboundEventLog.provider == provider)
                & (InboundEventLog.provider_event_id == provider_event_id)
            )
            .first()
        )
        if existing:
            return True, f"Duplicate provider event '{provider}:{provider_event_id}' already processed."
        return False, None
