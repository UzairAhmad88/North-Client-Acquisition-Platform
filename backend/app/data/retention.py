"""Data Retention Policies, Expiration Rules, and Legal Hold Enforcement."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
import uuid


@dataclass
class RetentionPolicy:
    """Configurable retention policy descriptor for a specific data domain."""

    domain: str
    retention_days: int = 365
    archive_after_days: Optional[int] = 180
    auto_delete: bool = False
    is_active: bool = True


class RetentionEngine:
    """Evaluates record expiration and blocks deletion when active legal holds exist."""

    @staticmethod
    def check_deletion_eligibility(
        entity_type: str,
        entity_id: str,
        created_at: datetime,
        retention_days: int = 365,
        active_holds: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Check if an entity can be purged, prioritizing active legal holds."""
        if active_holds:
            for h in active_holds:
                if h.get("active", False):
                    hold_type = h.get("entity_type")
                    hold_id = h.get("entity_id")
                    if (hold_type == entity_type or hold_type == "*") and (hold_id == entity_id or hold_id == "*"):
                        return {
                            "allowed": False,
                            "reason": "ACTIVE_LEGAL_HOLD",
                            "message": f"Entity is locked under legal hold '{h.get('case_reference')}'",
                        }

        now = datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        age_days = (now - created_at).days
        if age_days >= retention_days:
            return {
                "allowed": True,
                "reason": "RETENTION_EXPIRED",
                "message": f"Entity age ({age_days} days) exceeds retention period ({retention_days} days).",
            }

        return {
            "allowed": False,
            "reason": "WITHIN_RETENTION_WINDOW",
            "message": f"Entity is within retention window ({retention_days - age_days} days remaining).",
        }

    @staticmethod
    def is_eligible_for_deletion(
        created_at: datetime,
        retention_policy: RetentionPolicy,
        has_legal_hold: bool = False,
    ) -> Tuple[bool, str]:
        """Check if a record can be purged based on policy and legal hold status."""
        if has_legal_hold:
            return False, "DELETION_BLOCKED_BY_LEGAL_HOLD"

        now = datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        age = (now - created_at).days
        if age >= retention_policy.retention_days:
            return True, "ELIGIBLE_FOR_PURGE"

        return False, f"WITHIN_RETENTION_WINDOW ({retention_policy.retention_days - age} days remaining)"
