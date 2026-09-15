"""Document retention, archiving, and legal hold policy manager."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.documents.base import RetentionStatus


class DocumentRetentionManager:
    """Enforces document retention schedules, soft deletion, and legal hold constraints."""

    def can_delete_document(self, has_legal_hold: bool, retention_status: str) -> tuple[bool, Optional[str]]:
        """Verify whether a document is eligible for soft or permanent deletion."""
        if has_legal_hold or retention_status == RetentionStatus.LEGAL_HOLD.value:
            return False, "Deletion blocked: Document is under active LEGAL_HOLD."
        return True, None

    def apply_legal_hold(self, document_id: str, hold_reason: str, applied_by: str) -> Dict[str, Any]:
        return {
            "document_id": document_id,
            "legal_hold": True,
            "retention_status": RetentionStatus.LEGAL_HOLD.value,
            "hold_reason": hold_reason,
            "applied_by": applied_by,
            "applied_at": datetime.now(timezone.utc).isoformat(),
        }

    def release_legal_hold(self, document_id: str, released_by: str) -> Dict[str, Any]:
        return {
            "document_id": document_id,
            "legal_hold": False,
            "retention_status": RetentionStatus.ACTIVE.value,
            "released_by": released_by,
            "released_at": datetime.now(timezone.utc).isoformat(),
        }

    def mark_soft_deleted(self, document_id: str, deleted_by: str, reason: str) -> Dict[str, Any]:
        return {
            "document_id": document_id,
            "is_deleted": True,
            "retention_status": RetentionStatus.DELETED.value,
            "deleted_by": deleted_by,
            "deletion_reason": reason,
            "deleted_at": datetime.now(timezone.utc).isoformat(),
        }

    def restore_deleted_document(self, document_id: str, restored_by: str) -> Dict[str, Any]:
        return {
            "document_id": document_id,
            "is_deleted": False,
            "retention_status": RetentionStatus.ACTIVE.value,
            "restored_by": restored_by,
            "restored_at": datetime.now(timezone.utc).isoformat(),
        }
