"""SQLAlchemy ORM Models for Unified Document, File and Digital Asset Management."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text

from app.models.base import Base

JSON_TYPE = JSON


class FileRecord(Base):
    """Raw binary file asset tracking."""
    __tablename__ = "files"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workspace_id = Column(String(36), nullable=False, index=True)
    folder_id = Column(String(36), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    extension = Column(String(50), nullable=True)
    mime_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False, default=0)
    checksum = Column(String(64), nullable=False, index=True)  # SHA-256
    storage_provider = Column(String(50), nullable=False, default="LOCAL")
    storage_key = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False, default="AVAILABLE", index=True)
    classification = Column(String(50), nullable=False, default="GENERAL", index=True)
    sensitivity = Column(String(50), nullable=False, default="INTERNAL")
    visibility = Column(String(50), nullable=False, default="INTERNAL")
    owner_id = Column(String(36), nullable=True)
    created_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)


class FileVersionRecord(Base):
    """File binary versions."""
    __tablename__ = "file_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String(36), ForeignKey("files.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    checksum = Column(String(64), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    storage_key = Column(String(500), nullable=False)
    change_summary = Column(String(500), nullable=True)
    status = Column(String(50), default="AVAILABLE", nullable=False)
    created_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FileMetadataRecord(Base):
    """Rich metadata, dimensions, tags for files."""
    __tablename__ = "file_metadata"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String(36), ForeignKey("files.id", ondelete="CASCADE"), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    tags_json = Column(JSON_TYPE, nullable=True)
    page_count = Column(Integer, nullable=True)
    dimensions_json = Column(JSON_TYPE, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    encoding = Column(String(50), nullable=True)
    source = Column(String(100), nullable=True)
    custom_metadata_json = Column(JSON_TYPE, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class FileScanRecord(Base):
    """Security and malware scan audits."""
    __tablename__ = "file_scans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String(36), ForeignKey("files.id", ondelete="CASCADE"), nullable=False, index=True)
    scanner_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    threat_name = Column(String(200), nullable=True)
    threat_category = Column(String(100), nullable=True)
    confidence_score = Column(Float, default=1.0, nullable=False)
    scan_duration_ms = Column(Integer, default=0, nullable=False)
    raw_output = Column(Text, nullable=True)
    scanned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FileAccessLogRecord(Base):
    """File access and download audit trail."""
    __tablename__ = "file_access_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    file_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    action = Column(String(50), nullable=False)  # VIEW, DOWNLOAD, PREVIEW, SHARE, DELETE
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    result = Column(String(50), nullable=False, default="ALLOW")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class FolderRecord(Base):
    """Logical folders within workspaces."""
    __tablename__ = "folders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workspace_id = Column(String(36), nullable=False, index=True)
    parent_id = Column(String(36), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    path = Column(String(1000), nullable=False)
    created_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)


class ManagedDocumentRecord(Base):
    """Governed business document entities with lifecycles."""
    __tablename__ = "managed_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    workspace_id = Column(String(36), nullable=False, index=True)
    folder_id = Column(String(36), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    current_version_id = Column(String(36), nullable=True)
    current_version_number = Column(Integer, default=1, nullable=False)
    status = Column(String(50), default="DRAFT", nullable=False, index=True)
    classification = Column(String(50), default="GENERAL", nullable=False, index=True)
    sensitivity = Column(String(50), default="INTERNAL", nullable=False)
    visibility = Column(String(50), default="INTERNAL", nullable=False)
    retention_status = Column(String(50), default="ACTIVE", nullable=False)
    legal_hold = Column(Boolean, default=False, nullable=False, index=True)
    created_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)


class ManagedDocumentVersionRecord(Base):
    """Document version history snapshots."""
    __tablename__ = "managed_document_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    file_id = Column(String(36), nullable=True, index=True)
    checksum = Column(String(64), nullable=False)
    storage_key = Column(String(500), nullable=True)
    change_summary = Column(String(500), nullable=True)
    status = Column(String(50), default="DRAFT", nullable=False)
    created_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentExtractionRecord(Base):
    """Text, chunk, and OCR extraction records."""
    __tablename__ = "document_extractions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_id = Column(String(36), nullable=False, index=True)
    raw_text = Column(Text, nullable=True)
    chunks_json = Column(JSON_TYPE, nullable=True)
    extraction_source = Column(String(50), default="NATIVE_TEXT", nullable=False)
    confidence = Column(Float, default=1.0, nullable=False)
    extracted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentReviewRecord(Base):
    """Document review submissions and assignments."""
    __tablename__ = "document_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_id = Column(String(36), nullable=False, index=True)
    requested_by = Column(String(36), nullable=False)
    reviewer_id = Column(String(36), nullable=True)
    status = Column(String(50), default="SUBMITTED_FOR_REVIEW", nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)


class DocumentApprovalRecord(Base):
    """Immutable document approvals bound to exact version checksums."""
    __tablename__ = "document_approvals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_id = Column(String(36), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    checksum = Column(String(64), nullable=False)
    approver_id = Column(String(36), nullable=False)
    approver_role = Column(String(50), nullable=False)
    decision = Column(String(50), default="APPROVED", nullable=False)
    decision_notes = Column(Text, nullable=True)
    approved_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentComparisonRecord(Base):
    """Version diff comparisons."""
    __tablename__ = "document_comparisons"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    base_version_number = Column(Integer, nullable=False)
    target_version_number = Column(Integer, nullable=False)
    similarity_score = Column(Float, nullable=False)
    summary_diff = Column(Text, nullable=True)
    diff_details_json = Column(JSON_TYPE, nullable=True)
    created_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentShareRecord(Base):
    """Explicit collaborator document shares."""
    __tablename__ = "document_shares"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    shared_by = Column(String(36), nullable=False)
    share_type = Column(String(50), nullable=False)
    target_id = Column(String(36), nullable=False, index=True)
    permissions_json = Column(JSON_TYPE, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentShareLinkRecord(Base):
    """Secure expiring public/client share links."""
    __tablename__ = "document_share_links"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(128), unique=True, nullable=False, index=True)
    permissions_json = Column(JSON_TYPE, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(String(36), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    access_count = Column(Integer, default=0, nullable=False)
    has_passcode = Column(Boolean, default=False, nullable=False)
    passcode_hash = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentCommentRecord(Base):
    """Comments on documents and versions."""
    __tablename__ = "document_comments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_id = Column(String(36), nullable=True)
    parent_id = Column(String(36), nullable=True)
    user_id = Column(String(36), nullable=False)
    content = Column(Text, nullable=False)
    visibility = Column(String(50), default="INTERNAL", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentRetentionPolicyRecord(Base):
    """Configurable data retention policy schedules."""
    __tablename__ = "document_retention_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    classification = Column(String(50), nullable=False)
    retention_days = Column(Integer, nullable=False, default=365)
    action_on_expire = Column(String(50), default="ARCHIVE", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DocumentLegalHoldRecord(Base):
    """Legal hold records overriding retention deletions."""
    __tablename__ = "document_legal_holds"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    document_id = Column(String(36), ForeignKey("managed_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    applied_by = Column(String(36), nullable=False)
    applied_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    released_by = Column(String(36), nullable=True)
    released_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)


class AssetDerivativeRecord(Base):
    """Image / media derivatives (thumbnails, previews)."""
    __tablename__ = "asset_derivatives"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String(36), ForeignKey("files.id", ondelete="CASCADE"), nullable=False, index=True)
    derivative_type = Column(String(50), nullable=False)  # THUMBNAIL, PREVIEW, COMPRESSED
    storage_key = Column(String(500), nullable=False)
    mime_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ExportJobRecord(Base):
    """Document batch export jobs."""
    __tablename__ = "export_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    status = Column(String(50), default="PENDING", nullable=False)
    file_ids_json = Column(JSON_TYPE, nullable=False)
    export_storage_key = Column(String(500), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
