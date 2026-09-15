"""REST API schemas for Phase 28 — Change Request, Scope Change & Commercial Change Management."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChangeRequestCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    category: str = Field(default="SCOPE")
    source: str = Field(default="CLIENT_PORTAL")
    reason: Optional[str] = None
    requested_by: str = Field(default="Client Stakeholder")


class ChangeApprovalSubmitSchema(BaseModel):
    approval_statement: str
    signer_id: str = Field(default="Client Representative")


class ChangeImpactSchema(BaseModel):
    id: str
    impact_type: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    impact_action: str
    impact_description: str
    confidence: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChangeVersionSchema(BaseModel):
    id: str
    version_number: int
    description: str
    scope_summary: Optional[str] = None
    commercial_summary: Optional[str] = None
    schedule_summary: Optional[str] = None
    impact_summary: Optional[str] = None
    content_hash: str
    created_at: datetime
    impacts: List[ChangeImpactSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ChangeRequestResponseSchema(BaseModel):
    id: str
    change_number: str
    project_id: str
    business_id: Optional[str] = None
    title: str
    description: str
    category: str
    classification: str
    status: str
    priority: str
    source: str
    requested_by: str
    requested_at: datetime
    impact_status: str
    approval_status: str
    client_approval_status: str
    implementation_status: str
    created_at: datetime
    versions: List[ChangeVersionSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True
