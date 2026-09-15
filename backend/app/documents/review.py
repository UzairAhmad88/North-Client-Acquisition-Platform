"""Document review and approval workflow engine."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from app.documents.base import DocumentStatus


class DocumentReviewEngine:
    """Manages document review requests, decisions, and immutable approval records."""

    def submit_for_review(
        self,
        document_id: str,
        version_id: str,
        version_number: int,
        requested_by: str,
        reviewer_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "review_id": str(uuid4()),
            "document_id": document_id,
            "version_id": version_id,
            "version_number": version_number,
            "status": DocumentStatus.SUBMITTED_FOR_REVIEW.value,
            "requested_by": requested_by,
            "reviewer_id": reviewer_id,
            "notes": notes,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def record_approval(
        self,
        document_id: str,
        version_id: str,
        version_number: int,
        checksum_sha256: str,
        approver_id: str,
        approver_role: str,
        decision_notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record immutable approval record for an exact document version and hash."""
        return {
            "approval_id": str(uuid4()),
            "document_id": document_id,
            "version_id": version_id,
            "version_number": version_number,
            "checksum_sha256": checksum_sha256,
            "approver_id": approver_id,
            "approver_role": approver_role,
            "decision": "APPROVED",
            "decision_notes": decision_notes,
            "approved_at": datetime.now(timezone.utc).isoformat(),
        }

    def record_rejection(
        self,
        document_id: str,
        version_id: str,
        version_number: int,
        approver_id: str,
        reason: str,
    ) -> Dict[str, Any]:
        """Record rejection decision."""
        return {
            "approval_id": str(uuid4()),
            "document_id": document_id,
            "version_id": version_id,
            "version_number": version_number,
            "approver_id": approver_id,
            "decision": "REJECTED",
            "decision_notes": reason,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def validate_approval_integrity(
        self,
        stored_approval_checksum: str,
        current_version_checksum: str,
    ) -> bool:
        """Validate that current version content matches the approved checksum exactly."""
        return stored_approval_checksum.lower() == current_version_checksum.lower()
