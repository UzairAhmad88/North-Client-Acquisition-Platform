"""
Phase 67: Autonomous DevSecOps, AI Software Factory, CI/CD Intelligence & Self-Healing Engineering Schemas.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# 1. Projects & Repositories
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner: str
    team: str
    tech_stack: List[str] = Field(default_factory=list)
    environments: List[str] = Field(default_factory=lambda: ["DEVELOPMENT", "STAGING", "PRODUCTION"])
    budget_usd: float = 50000.0


class ProjectResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    description: Optional[str] = None
    owner: str
    team: str
    status: str
    tech_stack: List[str]
    environments: List[str]
    budget_usd: float
    created_at: Optional[Any] = None

    class Config:
        from_attributes = True


class RepositoryIndexRequest(BaseModel):
    project_id: str
    name: str
    repo_url: str
    default_branch: str = "main"
    visibility: str = "PRIVATE"


class RepositoryResponse(BaseModel):
    id: str
    tenant_id: str
    project_id: str
    name: str
    default_branch: str
    repo_url: str
    visibility: str
    is_indexed: bool
    total_commits: int
    open_prs_count: int
    vulnerabilities_count: int
    created_at: Optional[Any] = None

    class Config:
        from_attributes = True


# 2. Codebase Knowledge Graph & Planning
class CodebaseGraphQuery(BaseModel):
    repository_id: str
    entity_name: str
    depth: int = 2


class TaskPlanRequest(BaseModel):
    project_id: str
    title: str
    requirement_summary: str
    affected_files: Optional[List[str]] = None
    security_context: Optional[Dict[str, Any]] = None


class TaskPlanResponse(BaseModel):
    id: str
    project_id: str
    title: str
    requirement_summary: str
    files_to_change: List[str]
    architecture_impact: Optional[str] = None
    security_considerations: List[str]
    testing_strategy: Optional[str] = None
    rollback_plan: Optional[str] = None
    status: str
    created_at: Optional[Any] = None


# 3. AI Coding Agents & Sandboxed Execution
class CodingExecutionRequest(BaseModel):
    agent_id: str
    task_id: str
    repository_id: str
    instruction: str
    target_files: List[str]
    sandbox_mode: bool = True


class CodingExecutionResponse(BaseModel):
    execution_id: str
    status: str  # COMPLETED, REQUIRES_APPROVAL, BLOCKED
    files_changed: List[str]
    diff_stat: Dict[str, int]
    test_run_status: str
    security_gate_passed: bool
    requires_human_approval: bool


class AgentApprovalRequest(BaseModel):
    approval_id: str
    decision: str  # APPROVED, REJECTED
    approver_email: str
    notes: Optional[str] = None


# 4. Code Review & Change Risk
class CodeReviewRequest(BaseModel):
    repository_id: str
    pull_request_number: int
    diff_content: Optional[str] = None


class CodeReviewFindingResponse(BaseModel):
    id: str
    file_path: str
    line_number: Optional[int] = None
    dimension: str
    severity: str
    evidence: str
    recommendation: str
    confidence: float


class ChangeRiskEvaluationRequest(BaseModel):
    repository_id: str
    files_changed: List[str]
    lines_added: int
    lines_deleted: int
    service_criticality: str = "HIGH"


class ChangeRiskEvaluationResponse(BaseModel):
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    risk_score: float
    factors: List[str]
    required_reviewers_count: int
    canary_required: bool


# 5. Test Intelligence & Flakiness
class TestImpactRequest(BaseModel):
    repository_id: str
    changed_files: List[str]


class TestImpactResponse(BaseModel):
    affected_test_suites: List[str]
    recommended_test_set_size: int
    reduction_percentage: float
    estimated_duration_seconds: float


# 6. CI/CD Pipelines & Build Caching
class PipelineRunRequest(BaseModel):
    repository_id: str
    pipeline_name: str = "main-ci"
    commit_sha: str = "HEAD"
    branch: str = "main"


class PipelineRunResponse(BaseModel):
    run_id: str
    status: str
    stages: List[Dict[str, Any]]
    duration_seconds: int
    cache_hit_rate: float
    artifacts_produced: List[str]


# 7. Artifact Provenance & Supply Chain
class ArtifactProvenanceResponse(BaseModel):
    artifact_id: str
    name: str
    version: str
    sha256_checksum: str
    signature_verified: bool
    sbom_scanned: bool
    critical_vulnerabilities: int
    provenance_chain: Dict[str, Any]


# 8. Releases & Progressive Deployment
class ReleaseCreateRequest(BaseModel):
    project_id: str
    version: str
    commit_sha: str
    artifact_id: str
    release_notes: Optional[str] = None


class DeploymentExecuteRequest(BaseModel):
    release_id: str
    environment: str = "PRODUCTION"
    strategy: str = "CANARY"
    traffic_percentage: int = 10


class DeploymentResponse(BaseModel):
    deployment_id: str
    environment: str
    strategy: str
    traffic_percentage: int
    status: str
    error_rate: float
    p99_latency_ms: float
    rollback_available: bool


# 9. Observability, SLOs & Incident Response
class SloStatusResponse(BaseModel):
    service_name: str
    target_percentage: float
    actual_percentage: float
    error_budget_remaining_pct: float
    burn_rate_1h: float
    status: str


class IncidentRcaResponse(BaseModel):
    incident_id: str
    service_id: str
    severity: str
    likely_root_cause: str
    confidence: float
    recent_deployments: List[str]
    recommended_runbook_id: str


class RunbookExecuteRequest(BaseModel):
    runbook_id: str
    incident_id: str
    approver_email: Optional[str] = None


# 10. Closed-Loop Software Factory
class SoftwareFactoryLoopRequest(BaseModel):
    project_id: str
    requirement: str
    target_environment: str = "STAGING"


class SoftwareFactoryLoopResponse(BaseModel):
    cycle_id: str
    status: str
    phases_completed: List[str]
    plan_id: str
    build_id: str
    deployment_id: str
    duration_ms: int


# Dsops Aliases
DsopsProjectCreate = ProjectCreate
DsopsProjectResponse = ProjectResponse
DsopsRepositoryRegister = RepositoryIndexRequest
DsopsRepositoryResponse = RepositoryResponse
DsopsTaskPlanCreate = TaskPlanRequest
DsopsTaskPlanResponse = TaskPlanResponse
DsopsCodeGenerationRequest = CodingExecutionRequest
DsopsCodeGenerationResponse = CodingExecutionResponse
DsopsCodeReviewRequest = CodeReviewRequest
DsopsCodeReviewResponse = CodeReviewFindingResponse
DsopsTestRunRequest = TestImpactRequest
DsopsTestRunResponse = TestImpactResponse
DsopsPipelineCreate = PipelineRunRequest
DsopsPipelineResponse = PipelineRunResponse
DsopsBuildRequest = PipelineRunRequest
DsopsBuildResponse = PipelineRunResponse
DsopsArtifactProvenanceCreate = ArtifactProvenanceResponse
DsopsArtifactProvenanceResponse = ArtifactProvenanceResponse
DsopsReleaseCreate = ReleaseCreateRequest
DsopsReleaseResponse = ReleaseCreateRequest
DsopsDeploymentCreate = DeploymentExecuteRequest
DsopsDeploymentResponse = DeploymentResponse
DsopsServiceCatalogCreate = SloStatusResponse
DsopsServiceCatalogResponse = SloStatusResponse
DsopsSloCreate = SloStatusResponse
DsopsSloResponse = SloStatusResponse
DsopsIncidentCreate = IncidentRcaResponse
DsopsIncidentResponse = IncidentRcaResponse
DsopsRunbookCreate = RunbookExecuteRequest
DsopsRunbookResponse = RunbookExecuteRequest
DsopsRunbookExecuteRequest = RunbookExecuteRequest
DsopsAgentApprovalCreate = AgentApprovalRequest
DsopsAgentApprovalResponse = AgentApprovalRequest
DsopsCycleRunRequest = SoftwareFactoryLoopRequest
DsopsCycleRunResponse = SoftwareFactoryLoopResponse

