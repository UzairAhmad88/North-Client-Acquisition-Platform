"""REST API schemas for Phase 30 — Post-Delivery Support, Maintenance, Warranty & Client Success System."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Support Requests ---
class SupportRequestCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    project_id: Optional[str] = None
    client_account_id: Optional[str] = None
    business_id: Optional[str] = None
    submitted_by: Optional[str] = None


class SupportRequestUpdateStatusSchema(BaseModel):
    status: str
    notes: Optional[str] = None
    rejection_reason: Optional[str] = None


class SupportRequestEvidenceCreateSchema(BaseModel):
    evidence_type: str
    title: str
    file_path: Optional[str] = None
    file_size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    data_payload: Optional[Dict[str, Any]] = None


class SupportRequestVersionResponseSchema(BaseModel):
    id: str
    support_request_id: str
    version_number: int
    title: str
    description: str
    status: str
    created_by: str
    change_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SupportRequestEventResponseSchema(BaseModel):
    id: str
    support_request_id: str
    event_type: str
    actor_id: str
    actor_role: str
    details: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SupportRequestEvidenceResponseSchema(BaseModel):
    id: str
    support_request_id: str
    evidence_type: str
    title: str
    file_path: Optional[str] = None
    file_size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    sha256_checksum: Optional[str] = None
    data_payload: Optional[Dict[str, Any]] = None
    uploaded_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class SupportRequestResponseSchema(BaseModel):
    id: str
    project_id: Optional[str] = None
    client_account_id: Optional[str] = None
    business_id: Optional[str] = None
    title: str
    description: str
    request_type: str
    classification_confidence: float
    classification_reason: Optional[str] = None
    priority: str
    status: str
    is_warranty_covered: Optional[bool] = None
    warranty_evaluated_by: Optional[str] = None
    warranty_evaluation_notes: Optional[str] = None
    routed_change_request_id: Optional[str] = None
    sla_status: str
    current_version: int
    submitted_by: Optional[str] = None
    assigned_to: Optional[str] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SupportRequestDetailResponseSchema(SupportRequestResponseSchema):
    versions: List[SupportRequestVersionResponseSchema] = Field(default_factory=list)
    events: List[SupportRequestEventResponseSchema] = Field(default_factory=list)
    evidence: List[SupportRequestEvidenceResponseSchema] = Field(default_factory=list)


# --- AI Troubleshooting & Opportunity ---
class TroubleshootingRequestSchema(BaseModel):
    logs: Optional[List[str]] = Field(default_factory=list)


class TroubleshootingResponseSchema(BaseModel):
    possible_root_causes: List[str]
    suggested_steps: List[str]
    confidence: float
    prevention_tips: List[str]


class WarrantyEvaluationDecisionSchema(BaseModel):
    approve_warranty: bool
    exclusion_reason: Optional[str] = None


class RouteToChangeRequestSchema(BaseModel):
    change_request_id: Optional[str] = None
    notes: Optional[str] = None


# --- Incidents ---
class IncidentCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    summary: str
    severity: str = "SEV-2"
    project_id: Optional[str] = None
    lead_incident_commander: Optional[str] = None


class IncidentTimelineResponseSchema(BaseModel):
    id: str
    incident_id: str
    timestamp: datetime
    phase: str
    message: str
    actor_id: str

    class Config:
        from_attributes = True


class IncidentUpdateStatusSchema(BaseModel):
    status: str
    message: str
    root_cause: Optional[str] = None
    resolution_summary: Optional[str] = None


class IncidentResponseSchema(BaseModel):
    id: str
    project_id: Optional[str] = None
    title: str
    severity: str
    status: str
    summary: str
    root_cause: Optional[str] = None
    resolution_summary: Optional[str] = None
    lead_incident_commander: Optional[str] = None
    is_postmortem_completed: bool
    started_at: datetime
    contained_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    timelines: List[IncidentTimelineResponseSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


# --- Warranties ---
class WarrantyCreateSchema(BaseModel):
    project_id: str
    contract_id: Optional[str] = None
    client_account_id: Optional[str] = None
    title: str = "Standard Delivery Warranty"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    coverage_terms: Optional[str] = None
    covered_defect_categories: Optional[List[str]] = None
    excluded_conditions: Optional[List[str]] = None


class WarrantyResponseSchema(BaseModel):
    id: str
    project_id: str
    contract_id: Optional[str] = None
    client_account_id: Optional[str] = None
    title: str
    start_date: datetime
    end_date: datetime
    status: str
    coverage_terms: Optional[str] = None
    covered_defect_categories: Optional[List[str]] = None
    excluded_conditions: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Maintenance Plans & Work Orders ---
class MaintenancePlanCreateSchema(BaseModel):
    project_id: str
    title: str
    plan_type: str = "PREVENTIVE"
    cadence: str = "MONTHLY"
    client_account_id: Optional[str] = None
    contract_id: Optional[str] = None
    scope_summary: Optional[str] = None
    tasks_checklist: Optional[List[Dict[str, Any]]] = None


class MaintenanceWorkOrderScheduleSchema(BaseModel):
    title: str
    scheduled_for: datetime
    project_id: Optional[str] = None
    assigned_to: Optional[str] = None
    tasks_to_execute: Optional[List[Dict[str, Any]]] = None


class MaintenanceWorkOrderCompleteSchema(BaseModel):
    execution_notes: str
    checklist_results: Optional[List[Dict[str, Any]]] = None


class MaintenanceWorkOrderResponseSchema(BaseModel):
    id: str
    plan_id: str
    project_id: str
    title: str
    status: str
    scheduled_start: datetime
    actual_end: Optional[datetime] = None
    assigned_to: Optional[str] = None
    tasks_to_execute: Optional[List[Dict[str, Any]]] = None
    checklist_results: Optional[List[Dict[str, Any]]] = None
    execution_notes: Optional[str] = None
    signoff_by: Optional[str] = None
    signoff_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MaintenancePlanResponseSchema(BaseModel):
    id: str
    project_id: str
    client_account_id: Optional[str] = None
    contract_id: Optional[str] = None
    title: str
    plan_type: str
    cadence: str
    status: str
    scope_summary: Optional[str] = None
    tasks_checklist: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    updated_at: datetime
    work_orders: List[MaintenanceWorkOrderResponseSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


# --- SLA Policies ---
class SLAPolicyCreateSchema(BaseModel):
    project_id: str
    tier: str = "STANDARD"
    contract_id: Optional[str] = None
    target_response_hours: Optional[Dict[str, float]] = None
    target_resolution_hours: Optional[Dict[str, float]] = None
    coverage_hours_type: str = "24/7"


class SLAPolicyResponseSchema(BaseModel):
    id: str
    project_id: str
    contract_id: Optional[str] = None
    tier: str
    target_response_hours: Optional[Dict[str, float]] = None
    target_resolution_hours: Optional[Dict[str, float]] = None
    coverage_hours_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Knowledge Articles ---
class KnowledgeArticleCreateSchema(BaseModel):
    title: str
    content: str
    category: str
    business_id: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None


class KnowledgeArticleResponseSchema(BaseModel):
    id: str
    business_id: Optional[str] = None
    title: str
    summary: Optional[str] = None
    content: str
    category: str
    tags: Optional[List[str]] = None
    is_published: bool
    author_id: Optional[str] = None
    helpful_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Client Health & Opportunities ---
class ClientHealthResponseSchema(BaseModel):
    id: str
    client_account_id: str
    health_score: float
    status: str
    active_tickets_count: int
    unresolved_incidents_count: int
    sla_breaches_last_30d: int
    csat_average: float
    snapshot_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class SupportOpportunityResponseSchema(BaseModel):
    id: str
    client_account_id: str
    project_id: Optional[str] = None
    opportunity_type: str
    title: str
    description: str
    confidence_score: float
    estimated_value_cents: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
