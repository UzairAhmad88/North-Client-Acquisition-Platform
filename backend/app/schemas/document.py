"""Pydantic V2 Schemas for Unified Document, File and Digital Asset Management."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class FileResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    workspace_id: str
    folder_id: Optional[str] = None
    name: str
    extension: Optional[str] = None
    mime_type: str
    size_bytes: int
    checksum: str
    storage_provider: str
    storage_key: str
    status: str
    classification: str
    sensitivity: str
    visibility: str
    owner_id: Optional[str] = None
    created_by: str
    created_at: datetime
    updated_at: datetime


class FileUploadResponseSchema(BaseModel):
    success: bool
    file_id: Optional[str] = None
    tenant_id: str
    workspace_id: str
    filename: str
    mime_type: str
    size_bytes: int
    checksum_sha256: str
    storage_key: Optional[str] = None
    status: str
    classification: str
    sensitivity: str
    visibility: str
    extracted_text: Optional[str] = None
    chunks_count: int = 0
    preview: Optional[Dict[str, Any]] = None
    validation_errors: List[str] = Field(default_factory=list)


class DocumentVersionResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    document_id: str
    version_number: int
    file_id: Optional[str] = None
    checksum: str
    storage_key: Optional[str] = None
    change_summary: Optional[str] = None
    status: str
    created_by: str
    created_at: datetime


class ManagedDocumentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    workspace_id: str
    folder_id: Optional[str] = None
    title: str
    current_version_id: Optional[str] = None
    current_version_number: int
    status: str
    classification: str
    sensitivity: str
    visibility: str
    retention_status: str
    legal_hold: bool
    created_by: str
    created_at: datetime
    updated_at: datetime


class DocumentCreateRequestSchema(BaseModel):
    workspace_id: str
    title: str
    classification: Optional[str] = "GENERAL"
    sensitivity: Optional[str] = "INTERNAL"
    visibility: Optional[str] = "INTERNAL"
    folder_id: Optional[str] = None


class DocumentReviewRequestSchema(BaseModel):
    reviewer_id: Optional[str] = None
    notes: Optional[str] = None


class DocumentApprovalRequestSchema(BaseModel):
    version_id: str
    version_number: int
    checksum: str
    decision_notes: Optional[str] = None


class ShareLinkCreateRequestSchema(BaseModel):
    expires_in_hours: int = 24
    allow_download: bool = False
    passcode: Optional[str] = None


class ShareLinkResponseSchema(BaseModel):
    link_id: str
    token: str
    document_id: str
    permissions: List[str]
    expires_at: datetime
    created_by: str
    access_url: str
