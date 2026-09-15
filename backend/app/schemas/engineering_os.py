"""Phase 61: Pydantic Request/Response Schemas for Engineering Operating System API."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OrganizationCreateRequest(BaseModel):
    name: str = Field(..., example="Uzaii Core Engineering")
    slug: str = Field(..., example="uzaii-core-eng")
    description: str = Field("", example="Core engineering org")
    head_of_engineering_email: str = Field("vp-eng@uzaii.com", example="vp-eng@uzaii.com")


class TeamCreateRequest(BaseModel):
    org_id: Optional[str] = None
    name: str = Field(..., example="Platform & SRE Team")
    team_type: str = Field("PLATFORM", example="PLATFORM")
    lead_email: str = Field("tech-lead@uzaii.com", example="tech-lead@uzaii.com")
    member_count: int = 8


class RepositoryCreateRequest(BaseModel):
    project_id: Optional[str] = None
    name: str = Field(..., example="uzaii-develop-by-norths")
    provider: str = Field("GITHUB", example="GITHUB")
    default_branch: str = Field("main", example="main")
    primary_language: str = Field("Python / TypeScript", example="Python / TypeScript")
    is_private: bool = True


class PullRequestCreateRequest(BaseModel):
    repository_id: str
    pr_number: int
    title: str
    author: str
    source_branch: str
    target_branch: str = "main"
    linked_work_item: Optional[str] = None
    files_changed_count: int = 5
    additions: int = 150
    deletions: int = 20


class CodeReviewSubmitRequest(BaseModel):
    pr_id: str
    reviewer_email: str = "reviewer@uzaii.com"
    decision: str = "APPROVED"
    findings: List[Dict[str, Any]] = Field(default_factory=list)
    security_findings_count: int = 0
    architecture_notes: str = ""


class CodeQualityEvaluateRequest(BaseModel):
    repository_id: str
    commit_sha: str
    static_analysis_score: float = 95.0
    test_coverage_pct: float = 90.0
    cyclomatic_complexity_avg: float = 4.0
    code_duplication_pct: float = 1.5
    dependency_vulnerability_count: int = 0


class ServiceRegisterRequest(BaseModel):
    name: str
    service_tier: str = "TIER_1"
    owner_team: str = "Core Platform"
    runtime: str = "FASTAPI_PYTHON_311"
    target_slo_availability: float = 99.95
    dependencies: List[str] = Field(default_factory=list)
    description: str = ""


class ApiContractRegisterRequest(BaseModel):
    service_id: str
    name: str
    version: str = "v1"
    protocol: str = "REST_OPENAPI"
    auth_mechanism: str = "BEARER_JWT"
    rate_limit_rpm: int = 1200
    is_deprecated: bool = False


class EnvironmentRegisterRequest(BaseModel):
    name: str = "PRODUCTION"
    is_production: bool = True
    cluster_region: str = "us-east-1"
    access_tier: str = "RESTRICTED_VP_APPROVAL"


class PipelineRegisterRequest(BaseModel):
    repository_id: str
    name: str
    pipeline_type: str = "CI_BUILD_TEST_DEPLOY"
    stages: List[str] = Field(default_factory=list)


class DeploymentExecuteRequest(BaseModel):
    service_id: str
    environment: str = "PRODUCTION"
    strategy: str = "CANARY"
    version_tag: str = "v2.4.0"
    commit_sha: str
    operator_email: str = "release-manager@uzaii.com"
    approved_by: Optional[str] = "vp-eng@uzaii.com"


class ReleaseReadinessEvaluateRequest(BaseModel):
    version_tag: str
    service_name: str
    checklists: Optional[Dict[str, bool]] = None


class FlakyTestDetectRequest(BaseModel):
    test_identifier: str
    execution_count: int = 50
    flip_count: int = 5


class SloBudgetCalculateRequest(BaseModel):
    service_name: str
    slo_target_pct: float = 99.95
    measured_uptime_pct: float = 99.98
    timeframe_days: int = 30


class IncidentDeclareRequest(BaseModel):
    title: str
    severity: str = "SEV2"
    affected_service: str
    incident_commander: str = "sre-oncall@uzaii.com"


class PostmortemCreateRequest(BaseModel):
    incident_id: str
    root_cause_summary: str
    five_whys: List[str] = Field(default_factory=list)
    corrective_actions: List[Dict[str, Any]] = Field(default_factory=list)
    author_email: str = "sre-lead@uzaii.com"


class ChangeRequestSubmitRequest(BaseModel):
    title: str
    change_type: str = "INFRASTRUCTURE_UPDATE"
    risk_level: str = "HIGH"
    rollback_plan: str
    owner_email: str = "eng-lead@uzaii.com"


class VulnerabilityRecordRequest(BaseModel):
    cve_id: str
    package_name: str
    current_version: str
    fixed_version: Optional[str] = None
    severity: str = "HIGH"
    status: str = "OPEN"


class SecretScanRequest(BaseModel):
    content_snippet: str


class TechnicalDebtLogRequest(BaseModel):
    title: str
    area: str = "ARCHITECTURE"
    severity: str = "HIGH"
    effort_person_days: float = 5.0
    remediation_strategy: str = ""


class DoraMetricsCalculateRequest(BaseModel):
    timeframe_days: int = 30
    deployment_frequency_per_day: float = 4.5
    lead_time_for_changes_hours: float = 2.4
    change_failure_rate_pct: float = 1.8
    time_to_restore_service_minutes: float = 22.0


class CloudCostRecordRequest(BaseModel):
    service_name: str
    environment: str = "PRODUCTION"
    monthly_cost_usd: float = 1200.0
    waste_estimate_usd: float = 150.0
    cost_trend_pct: float = 3.5


class EngineeringRiskLogRequest(BaseModel):
    category: str = "RELIABILITY"
    title: str
    probability: float = 0.3
    impact_score: float = 7.0
    severity: str = "HIGH"
    mitigation_strategy: str = ""
    owner: str = "lead-eng@uzaii.com"


class TwinSimulationRunRequest(BaseModel):
    scenario_type: str = "TRAFFIC_SPIKE_5X"
    parameters: Optional[Dict[str, Any]] = None


class DeveloperCopilotQueryRequest(BaseModel):
    query: str
    tenant_id: Optional[str] = "default_tenant"
