import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AuditJobCreate(BaseModel):
    business_id: uuid.UUID
    target_url: Optional[str] = None
    requested_categories: List[str] = Field(default_factory=lambda: ["ALL"])
    pages_requested: int = Field(default=10, ge=1, le=50)


class AuditJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    target_url: Optional[str] = None
    status: str
    requested_categories: List[str]
    pages_requested: int
    pages_analyzed: int
    findings_count: int
    warnings_count: int
    errors_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AuditFindingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    audit_id: uuid.UUID
    code: str
    category: str
    severity: str
    confidence: str
    title: str
    description: str
    evidence: Dict[str, Any]
    affected_page: Optional[str] = None
    created_at: datetime


class AuditPageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    audit_id: uuid.UUID
    url: str
    status_code: int
    response_time_ms: int
    title: Optional[str] = None
    content_type: Optional[str] = None
    meta_description: Optional[str] = None
    is_homepage: bool
    has_contact_form: bool
    created_at: datetime


class BusinessAuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    research_record_id: Optional[uuid.UUID] = None
    audit_job_id: Optional[uuid.UUID] = None
    target_url: Optional[str] = None
    audit_version: str
    status: str
    overall_health: str
    summary: Optional[str] = None
    categories: Dict[str, Any]
    findings: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    warnings: List[str]
    errors: List[str]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class BusinessAuditHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    business_id: uuid.UUID
    total_audits: int
    latest_audit: Optional[BusinessAuditResponse] = None
    audits: List[BusinessAuditResponse] = Field(default_factory=list)
