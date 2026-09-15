"""REST API schemas for Phase 29 — Quality Assurance, UAT, Delivery Acceptance & Handover System."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Test Plan & Cases ---
class TestPlanCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    plan_type: str = Field(default="SYSTEM")


class TestCaseCreateSchema(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    category: str = "FUNCTIONAL"
    priority: str = "MEDIUM"
    execution_type: str = "MANUAL"
    preconditions: Optional[str] = None
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    expected_results: str
    is_regression: bool = True
    requirement_id: Optional[str] = None
    deliverable_id: Optional[str] = None


class TestCaseResponseSchema(BaseModel):
    id: str
    test_plan_id: str
    code: str
    title: str
    description: Optional[str] = None
    category: str
    priority: str
    execution_type: str
    preconditions: Optional[str] = None
    steps: Optional[List[Dict[str, Any]]] = None
    expected_results: str
    is_regression: bool
    requirement_id: Optional[str] = None
    deliverable_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TestPlanResponseSchema(BaseModel):
    id: str
    project_id: str
    title: str
    description: Optional[str] = None
    plan_type: str
    status: str
    created_by: str
    created_at: datetime
    test_cases: List[TestCaseResponseSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


# --- Test Runs & Results ---
class TestRunCreateSchema(BaseModel):
    test_plan_id: str
    name: str
    environment: str = Field(default="STAGING")


class TestResultRecordSchema(BaseModel):
    test_case_id: str
    status: str  # PASSED, FAILED, BLOCKED, SKIPPED
    actual_results: Optional[str] = None
    execution_notes: Optional[str] = None
    evidence_files: Optional[List[Dict[str, str]]] = None


class TestRunResponseSchema(BaseModel):
    id: str
    project_id: str
    test_plan_id: str
    name: str
    environment: str
    status: str
    executed_by: Optional[str] = None
    passed_count: int
    failed_count: int
    blocked_count: int
    skipped_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Defects ---
class DefectCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    reported_by: str = Field(default="QA Engineer")
    test_case_id: Optional[str] = None
    test_run_id: Optional[str] = None
    deliverable_id: Optional[str] = None
    requirement_id: Optional[str] = None
    is_against_spec: bool = True


class DefectStatusUpdateSchema(BaseModel):
    status: str  # OPEN, IN_PROGRESS, RESOLVED, CLOSED, VERIFIED
    resolution_summary: Optional[str] = None


class DefectResponseSchema(BaseModel):
    id: str
    defect_number: str
    project_id: str
    title: str
    description: str
    severity: str
    priority: str
    status: str
    classification: str
    reported_by: str
    assigned_to: Optional[str] = None
    resolution_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Client UAT & Signoff ---
class UATSessionCreateSchema(BaseModel):
    client_account_id: str
    title: str
    scope_description: Optional[str] = None


class UATFeedbackCreateSchema(BaseModel):
    comments: str
    deliverable_id: Optional[str] = None
    feedback_type: str = "COMMENT"  # COMMENT, ISSUE, APPROVAL
    rating: Optional[int] = None
    create_defect_if_issue: bool = False


class UATSignoffSchema(BaseModel):
    client_signer_id: str
    signoff_statement: str


class UATSessionResponseSchema(BaseModel):
    id: str
    project_id: str
    client_account_id: str
    title: str
    scope_description: Optional[str] = None
    status: str
    approved_by_client: bool
    client_signoff_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Release Gates & Packages ---
class ReleaseVersionCreateSchema(BaseModel):
    version_tag: str
    target_environment: str = "PRODUCTION"
    release_notes: Optional[str] = None


class DeliveryPackageCreateSchema(BaseModel):
    package_name: str
    storage_url: str
    file_size_bytes: int
    release_version_id: Optional[str] = None


class ReleaseVersionResponseSchema(BaseModel):
    id: str
    project_id: str
    version_tag: str
    target_environment: str
    status: str
    release_notes: Optional[str] = None
    qa_approval_status: str
    client_approval_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Handover ---
class HandoverSignoffSchema(BaseModel):
    client_signer_id: str
    signoff_statement: str
