"""Base domain definitions, enums, and dataclasses for Phase 39 Document & Asset platform."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FileStatus(str, Enum):
    """Lifecycle status of raw binary file."""
    UPLOADING = "UPLOADING"
    UPLOADED = "UPLOADED"
    SCANNING = "SCANNING"
    VALIDATED = "VALIDATED"
    AVAILABLE = "AVAILABLE"
    QUARANTINED = "QUARANTINED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"
    BLOCKED = "BLOCKED"
    CORRUPTED = "CORRUPTED"
    EXPIRED = "EXPIRED"


class DocumentStatus(str, Enum):
    """Business lifecycle status of document entity."""
    DRAFT = "DRAFT"
    SUBMITTED_FOR_REVIEW = "SUBMITTED_FOR_REVIEW"
    IN_REVIEW = "IN_REVIEW"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"


class DocumentClassification(str, Enum):
    """Categorical classification of document content."""
    GENERAL = "GENERAL"
    BUSINESS_RECORD = "BUSINESS_RECORD"
    CLIENT_DOCUMENT = "CLIENT_DOCUMENT"
    REQUIREMENTS = "REQUIREMENTS"
    PROPOSAL = "PROPOSAL"
    ESTIMATE = "ESTIMATE"
    CONTRACT = "CONTRACT"
    PROJECT_DOCUMENT = "PROJECT_DOCUMENT"
    TECHNICAL_DOCUMENT = "TECHNICAL_DOCUMENT"
    DESIGN_ASSET = "DESIGN_ASSET"
    SOURCE_CODE = "SOURCE_CODE"
    TEST_EVIDENCE = "TEST_EVIDENCE"
    DELIVERABLE = "DELIVERABLE"
    SUPPORT_ATTACHMENT = "SUPPORT_ATTACHMENT"
    KNOWLEDGE_SOURCE = "KNOWLEDGE_SOURCE"
    INVOICE = "INVOICE"
    RECEIPT = "RECEIPT"
    SECURITY_DOCUMENT = "SECURITY_DOCUMENT"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class SensitivityLevel(str, Enum):
    """Data sensitivity and access tier."""
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class WorkspaceType(str, Enum):
    """Logical workspace context."""
    PERSONAL = "PERSONAL"
    ORGANIZATION = "ORGANIZATION"
    CLIENT = "CLIENT"
    PROJECT = "PROJECT"
    LEAD = "LEAD"
    OPPORTUNITY = "OPPORTUNITY"
    PROPOSAL = "PROPOSAL"
    CONTRACT = "CONTRACT"
    SUPPORT = "SUPPORT"
    KNOWLEDGE = "KNOWLEDGE"
    SYSTEM = "SYSTEM"


class DocumentVisibility(str, Enum):
    """Access visibility scope."""
    INTERNAL = "INTERNAL"
    CLIENT_VISIBLE = "CLIENT_VISIBLE"
    RESTRICTED = "RESTRICTED"
    SYSTEM = "SYSTEM"


class ShareType(str, Enum):
    """Mechanism for sharing documents."""
    USER_SHARE = "USER_SHARE"
    TEAM_SHARE = "TEAM_SHARE"
    PROJECT_SHARE = "PROJECT_SHARE"
    CLIENT_SHARE = "CLIENT_SHARE"
    LINK_SHARE = "LINK_SHARE"


class SharePermission(str, Enum):
    """Granular permissions granted on a share."""
    VIEW = "VIEW"
    DOWNLOAD = "DOWNLOAD"
    COMMENT = "COMMENT"
    EDIT = "EDIT"
    SHARE = "SHARE"
    APPROVE = "APPROVE"


class RetentionStatus(str, Enum):
    """Lifecycle state under data retention policy."""
    ACTIVE = "ACTIVE"
    RETENTION = "RETENTION"
    ARCHIVED = "ARCHIVED"
    LEGAL_HOLD = "LEGAL_HOLD"
    PENDING_DELETION = "PENDING_DELETION"
    DELETED = "DELETED"


class ExtractionSource(str, Enum):
    """Extraction source origin."""
    NATIVE_TEXT = "NATIVE_TEXT"
    OCR_EXTRACTED = "OCR_EXTRACTED"
    METADATA_PARSED = "METADATA_PARSED"
    AI_INFERRED = "AI_INFERRED"


class FileValidationResult(BaseModel):
    """Validation report on an uploaded file."""
    is_valid: bool
    mime_type: str
    detected_extension: str
    size_bytes: int
    checksum_sha256: str
    is_executable: bool = False
    validation_errors: List[str] = Field(default_factory=list)


class ExtractedChunk(BaseModel):
    """Indexed content chunk preserving provenance."""
    chunk_index: int
    content: str
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    start_char: int = 0
    end_char: int = 0
    source_type: ExtractionSource = ExtractionSource.NATIVE_TEXT
    confidence: float = 1.0
