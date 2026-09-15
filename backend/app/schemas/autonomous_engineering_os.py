"""Phase 64 — Autonomous Engineering OS Pydantic Request & Response Schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EngineeringProjectWorkspaceCreate(BaseModel):
    name: str = Field(..., description="Project workspace name")
    owner: str = Field(..., description="Owner username or email")
    team: str = Field(..., description="Engineering team name")
    description: Optional[str] = None
    repository_url: Optional[str] = None
    tech_stack: Optional[List[str]] = Field(default_factory=lambda: ["Python", "FastAPI", "Next.js", "Docker"])
    budget_allocated_usd: float = 20000.0


class EngineeringRequirementCreate(BaseModel):
    project_id: str = Field(..., description="Project workspace ID")
    title: str = Field(..., description="Requirement title")
    description: str = Field(..., description="Requirement detail")
    owner: str = Field(..., description="Author or owner")
    requirement_type: str = "FUNCTIONAL"
    priority: str = "HIGH"
    dependencies: Optional[List[str]] = Field(default_factory=list)


class RequirementAcceptanceCriteriaCreate(BaseModel):
    requirement_id: str
    given_clause: str
    when_clause: str
    then_clause: str
    is_automated_test_created: bool = False


class ArchitectureComponentCreate(BaseModel):
    project_id: str
    name: str
    component_type: str
    owner_team: str
    runtime_environment: str = "KUBERNETES"
    slo_target_latency_p95_ms: float = 50.0
    slo_target_availability_pct: float = 99.95
    dependencies: Optional[List[str]] = Field(default_factory=list)


class CodeRepositoryCreate(BaseModel):
    name: str
    organization: str = "uzaii-enterprise"
    provider: str = "GITHUB"
    default_branch: str = "main"
    language: str = "Python/TypeScript"


class CodeSymbolCreate(BaseModel):
    repository_id: str
    name: str
    file_path: str
    symbol_type: str = "FUNCTION"
    line_start: int = 1
    line_end: int = 1
    docstring: Optional[str] = None
    called_by: Optional[List[str]] = Field(default_factory=list)
    calls: Optional[List[str]] = Field(default_factory=list)


class TaskPlanningRequest(BaseModel):
    requirement_id: str
    task_breakdown: Optional[List[Dict[str, Any]]] = None


class SandboxedCodingRequest(BaseModel):
    task_id: str
    agent_id: str = "coding_agent"
    modified_files: Optional[List[str]] = None
    diff_additions: int = 42
    diff_deletions: int = 5
    tokens_used: int = 3800


class PullRequestCreate(BaseModel):
    repository_id: str
    title: str
    source_branch: str
    author: str
    task_id: Optional[str] = None
    target_branch: str = "main"
    session_id: Optional[str] = None


class MergePullRequestRequest(BaseModel):
    merged_by: str = Field(..., description="Authorizing human engineer")


class CiPipelineCreate(BaseModel):
    repository_id: str
    pipeline_name: str
    trigger_event: str = "PUSH"
    stages: Optional[List[str]] = None


class CiBuildRunCreate(BaseModel):
    pipeline_id: str
    commit_sha: str
    branch: str = "main"
    build_number: int = 1
    duration_seconds: float = 38.5
    status: str = "SUCCESS"


class TestSuiteCreate(BaseModel):
    repository_id: str
    suite_name: str
    suite_type: str = "UNIT"
    total_tests: int = 150
    passed_tests: int = 150
    failed_tests: int = 0
    flaky_rate_pct: float = 0.0
    duration_seconds: float = 14.2


class TestImpactRequest(BaseModel):
    repository_id: str
    changed_files: List[str]


class SbomPackageCreate(BaseModel):
    repository_id: str
    package_name: str
    version: str
    license_type: str = "MIT"
    is_license_compliant: bool = True
    vulnerabilities_count: int = 0


class DeploymentCreate(BaseModel):
    service_name: str
    version: str
    environment: str = "PRODUCTION"
    strategy: str = "CANARY"
    traffic_weight_pct: float = 10.0
    rollback_target_version: Optional[str] = None


class VerifyDeploymentRequest(BaseModel):
    synthetic_error_rate_pct: float = 0.01
    synthetic_latency_p95_ms: float = 42.0


class ServiceCatalogEntryCreate(BaseModel):
    name: str
    owner_team: str
    repository_id: Optional[str] = None
    slo_target_availability_pct: float = 99.95
    current_availability_pct: float = 99.98
    error_budget_remaining_pct: float = 85.0
    p95_latency_ms: float = 32.0


class IncidentCreate(BaseModel):
    service_name: str
    title: str
    severity: str = "SEV2"
    description: Optional[str] = None
    correlated_root_cause: Optional[str] = None


class SelfHealingRunbookCreate(BaseModel):
    name: str
    trigger_condition: str
    target_service: str
    action_type: str = "CANARY_ROLLBACK"
    is_autonomous_approved: bool = True


class ExecuteSelfHealingRequest(BaseModel):
    incident_id: str
    runbook_id: str


class FinopsCostCreate(BaseModel):
    project_id: str
    cost_category: str = "CI_BUILD_MINUTES"
    amount_usd: float = 12.50
    units_consumed: float = 250.0
    period_date: Optional[str] = None


class DigitalTwinSimulationRequest(BaseModel):
    scenario_type: str = "TRAFFIC_SPIKE_2X"
    target_service: str = "api-gateway"
    simulated_parameters: Optional[Dict[str, Any]] = None


class SoftwareFactoryCopilotRequest(BaseModel):
    query: str
