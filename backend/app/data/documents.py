"""Document Management, SHA-256 Checksum Integrity & Classification."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional, Union
import uuid

from app.data.base import DataClassification


@dataclass
class DocumentMetadata:
    """Document record descriptor."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    name: str = ""
    doc_type: str = "REQUIREMENTS"  # REQUIREMENTS, PROPOSAL, CONTRACT, DESIGN, QA_EVIDENCE, UAT_EVIDENCE, SUPPORT_DOC
    mime_type: str = "application/pdf"
    size_bytes: int = 0
    checksum: str = ""
    classification: DataClassification = DataClassification.INTERNAL
    project_id: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "AVAILABLE"  # UPLOADING, SCANNING, VALIDATING, AVAILABLE, ARCHIVED, DELETED


class DocumentEngine:
    """Handles document integrity calculation, validation, and metadata management."""

    @staticmethod
    def calculate_sha256(content: Union[str, bytes]) -> str:
        """Compute cryptographic SHA-256 hash of file content."""
        if isinstance(content, str):
            content = content.encode("utf-8")
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def compute_sha256(content: Union[str, bytes]) -> str:
        """Alias for calculate_sha256."""
        return DocumentEngine.calculate_sha256(content)

    @staticmethod
    def verify_integrity(content: Union[str, bytes], expected_checksum: str) -> bool:
        """Verify that document content has not been tampered with."""
        actual_checksum = DocumentEngine.calculate_sha256(content)
        return actual_checksum.lower() == expected_checksum.lower().strip()
