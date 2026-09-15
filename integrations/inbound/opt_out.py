"""Deterministic opt-out detector enforcing instant DNC registry entry before AI processing."""

import re
import uuid
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.services.outreach.dnc import DncService


class DeterministicOptOutDetector:
    """Scans inbound message body for explicit opt-out keywords."""

    OPT_OUT_PATTERNS = [
        r"\bstop\b",
        r"\bunsubscribe\b",
        r"don'?t\s+contact\s+me",
        r"remove\s+me",
        r"no\s+more\s+messages",
        r"do\s+not\s+contact",
        r"take\s+me\s+off\s+your\s+list",
    ]

    @staticmethod
    def is_opt_out_request(text: str) -> bool:
        clean = (text or "").lower().strip()
        for pat in DeterministicOptOutDetector.OPT_OUT_PATTERNS:
            if re.search(pat, clean):
                return True
        return False

    @staticmethod
    def process_opt_out_if_present(
        db: Session,
        text: str,
        sender_email: Optional[str] = None,
        sender_phone: Optional[str] = None,
        business_id: Optional[uuid.UUID] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        If opt-out keyword detected, immediately add entry to DNC registry and return True.
        """
        if not DeterministicOptOutDetector.is_opt_out_request(text):
            return False, None

        reason = "Inbound message contained explicit opt-out keyword"

        if sender_email:
            DncService.add_dnc_entry(db, scope="EMAIL", target_value=sender_email, reason=reason)

        if sender_phone:
            DncService.add_dnc_entry(db, scope="PHONE", target_value=sender_phone, reason=reason)

        if business_id:
            DncService.add_dnc_entry(db, scope="BUSINESS", target_value=str(business_id), reason=reason)

        return True, reason
