"""Pydantic schemas for Unified Reliability, SRE, Disaster Recovery, and Operations Platform."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Health & Diagnostics ---

class ComponentHealthCheckSchema(BaseModel):
    component_name: str
    component_type: str
    status: str
    latency_ms: float
    is_critical: bool = True
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    checked_at: Optional[str] = None


class DeepHealthResultSchema(BaseModel):
    status: str
    active_circuit_breakers: int = 0
    open_incidents: int = 0
    components: Dict[str, ComponentHealthCheckSchema]
    timestamp: str


class LivenessResponse(BaseModel):
    status: str = "ALIVE"
    timestamp: str


class ReadinessResponse(BaseModel):
    status: str = "READY"
    timestamp: str
    checks: Dict[str, bool]


# --- Circuit Breakers ---

class CircuitBreakerStatusSchema(BaseModel):
    service_name: str
    state: str
    failure_count: int
    success_count: int
    failure_threshold: int
    recovery_timeout: float
    last_state_change: Optional[str] = None


class CircuitBreakerResetRequest(BaseModel):
    service_name: str


# --- SLO & Error Budgets ---

class SLOCreateSchema(BaseModel):
    slo_type: str
    name: str
    description: Optional[str] = None
    target_percentage: float = Field(default=99.9, ge=0.0, le=100.0)
    window_days: int = Field(default=30, gt=0)
    service_tier: str = "CRITICAL"


class SLOMetricSnapshotSchema(BaseModel):
    slo_type: str
    name: str
    target_slo: float
    current_sli: float
    error_budget_remaining_pct: float
    burn_rate_1h: float
    burn_rate_24h: float
    budget_status: str
    total_events: int
    bad_events: int
    recorded_at: str


class ErrorBudgetSummarySchema(BaseModel):
    overall_status: str
    slos: List[SLOMetricSnapshotSchema]
    generated_at: str


# --- Incidents & Postmortems ---

class IncidentCreateSchema(BaseModel):
    title: str
    severity: str
    affected_services: List[str]
    impact_summary: str
    lead_responder: Optional[str] = None
    responders: List[str] = Field(default_factory=list)


class IncidentUpdateSchema(BaseModel):
    title: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    impact_summary: Optional[str] = None
    lead_responder: Optional[str] = None
    responders: Optional[List[str]] = None


class IncidentTimelineEventAddSchema(BaseModel):
    description: str
    actor: str


class IncidentMitigationStepAddSchema(BaseModel):
    step: str
    completed: bool = True


class IncidentResponseSchema(BaseModel):
    id: str
    title: str
    severity: str
    status: str
    affected_services: List[str]
    lead_responder: Optional[str] = None
    responders: List[str]
    impact_summary: str
    timeline_events: List[Dict[str, Any]]
    mitigation_steps: List[Dict[str, Any]]
    started_at: str
    acknowledged_at: Optional[str] = None
    mitigated_at: Optional[str] = None
    resolved_at: Optional[str] = None
    created_at: Optional[str] = None


class PostmortemCreateSchema(BaseModel):
    incident_id: str
    summary: str
    root_cause: str
    five_whys: List[str] = Field(default_factory=list)
    what_went_well: List[str] = Field(default_factory=list)
    what_could_improve: List[str] = Field(default_factory=list)
    action_items: List[Dict[str, Any]] = Field(default_factory=list)
    owner: str


class PostmortemResponseSchema(BaseModel):
    id: str
    incident_id: str
    summary: str
    root_cause: str
    five_whys: List[str]
    timeline_events: List[Dict[str, Any]]
    what_went_well: List[str]
    what_could_improve: List[str]
    action_items: List[Dict[str, Any]]
    owner: str
    created_at: str


# --- Backups & Restore Verification ---

class BackupTriggerSchema(BaseModel):
    backup_type: str = "DATABASE_FULL"
    storage_location: Optional[str] = None
    retention_days: int = 30


class BackupRecordSchema(BaseModel):
    id: str
    backup_type: str
    status: str
    size_bytes: int
    storage_location: str
    checksum_sha256: str
    verified: bool
    retention_days: int
    started_at: str
    completed_at: Optional[str] = None


class RestoreVerificationTriggerSchema(BaseModel):
    backup_id: str
    environment: str = "ISOLATED_SANDBOX"


class RestoreVerificationResponseSchema(BaseModel):
    test_id: str
    backup_id: str
    environment: str
    status: str
    rto_achieved_seconds: int
    data_integrity_passed: bool
    tables_restored_count: int
    records_verified_count: int
    logs: List[Dict[str, Any]]
    executed_at: str


# --- Disaster Recovery Plans & Drills ---

class DRPlanSchema(BaseModel):
    plan_name: str
    scenario: str
    target_rpo_minutes: int
    target_rto_minutes: int
    primary_region: str
    secondary_region: str
    status: str
    recovery_steps: List[Dict[str, Any]]


class DRDrillTriggerSchema(BaseModel):
    scenario: str
    initiated_by: str
    plan_name: Optional[str] = None


class DRDrillResponseSchema(BaseModel):
    drill_id: str
    scenario: str
    initiated_by: str
    status: str
    actual_rto_minutes: float
    data_loss_minutes: float
    step_results: List[Dict[str, Any]]
    observations: str
    lessons_learned: List[str]
    started_at: str
    completed_at: str


# --- Operations: Deployments, Rollbacks, Feature Flags ---

class DeploymentRecordCreateSchema(BaseModel):
    version: str
    deployed_by: str
    environment: str = "PRODUCTION"
    git_commit_sha: Optional[str] = None
    release_notes: Optional[str] = None


class DeploymentRecordSchema(BaseModel):
    id: str
    version: str
    environment: str
    deployed_by: str
    git_commit_sha: str
    status: str
    smoke_tests_passed: bool
    migrations_applied: bool
    release_notes: Optional[str] = None
    deployed_at: str


class RollbackTriggerSchema(BaseModel):
    current_version: str
    target_version: str
    error_rate_pct: float
    p99_latency_ms: float
    smoke_tests_passed: bool
    initiated_by: str
    reason: Optional[str] = None


class FeatureFlagCreateUpdateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    enabled: bool = True
    percentage_rollout: int = Field(default=100, ge=0, le=100)
    allowed_tiers: List[str] = Field(default_factory=list)
    tenant_whitelist: List[str] = Field(default_factory=list)
    tenant_blacklist: List[str] = Field(default_factory=list)


class FeatureFlagEvaluationRequest(BaseModel):
    flag_name: str
    tenant_id: Optional[str] = None
    tenant_tier: Optional[str] = None
