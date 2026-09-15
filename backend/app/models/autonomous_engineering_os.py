"""Phase 64 — Autonomous Engineering Operating System & AI Software Factory SQLAlchemy Models."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class EngineeringProjectWorkspaceModel(Base):
    """Engineering Project workspace entity."""
    __tablename__ = "eng_project_workspaces"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(128), nullable=False)
    team = Column(String(128), nullable=False)
    repository_url = Column(String(512), nullable=True)
    tech_stack = Column(JSON, default=list)  # ["Python", "FastAPI", "Next.js", "PostgreSQL", "Docker"]
    budget_allocated_usd = Column(Float, default=20000.0)
    budget_spent_usd = Column(Float, default=0.0)
    status = Column(String(32), default="ACTIVE", index=True)  # PLANNING, ACTIVE, BLOCKED, RELEASE, MAINTENANCE, DEPRECATED, ARCHIVED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class EngineeringRequirementModel(Base):
    """Versioned Engineering Requirement derived from Business/Product goals."""
    __tablename__ = "eng_requirements"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("eng_project_workspaces.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirement_type = Column(String(64), default="FUNCTIONAL")  # FUNCTIONAL, NON_FUNCTIONAL, SECURITY, PERFORMANCE, COMPLIANCE, INFRASTRUCTURE
    priority = Column(String(32), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    owner = Column(String(128), nullable=False)
    status = Column(String(32), default="APPROVED")  # DRAFT, IN_REVIEW, APPROVED, REJECTED, IMPLEMENTED
    ambiguity_score = Column(Float, default=0.05)  # 0.0 - 1.0 (AI analyzed)
    dependencies = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class RequirementAcceptanceCriteriaModel(Base):
    """Deterministic acceptance criteria linked to a requirement."""
    __tablename__ = "eng_acceptance_criteria"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    requirement_id = Column(String(64), ForeignKey("eng_requirements.id"), nullable=False, index=True)
    given_clause = Column(Text, nullable=False)
    when_clause = Column(Text, nullable=False)
    then_clause = Column(Text, nullable=False)
    is_automated_test_created = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ArchitectureComponentModel(Base):
    """System Architecture Registry Component."""
    __tablename__ = "eng_architecture_components"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("eng_project_workspaces.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    component_type = Column(String(64), nullable=False)  # SERVICE, API_GATEWAY, DATABASE, QUEUE, CACHE, FRONTEND, WORKER
    owner_team = Column(String(128), nullable=False)
    runtime_environment = Column(String(64), default="KUBERNETES")
    slo_target_latency_p95_ms = Column(Float, default=50.0)
    slo_target_availability_pct = Column(Float, default=99.95)
    dependencies_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CodeRepositoryModel(Base):
    """Registered Code Repository with Code Intelligence indexing."""
    __tablename__ = "eng_code_repositories"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    organization = Column(String(128), default="uzaii-enterprise")
    provider = Column(String(64), default="GITHUB")
    default_branch = Column(String(64), default="main")
    language = Column(String(64), default="Python/TypeScript")
    indexed_files_count = Column(Integer, default=0)
    indexed_symbols_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CodeSymbolModel(Base):
    """Indexed Code Intelligence Symbol (Function, Class, API endpoint)."""
    __tablename__ = "eng_code_symbols"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), ForeignKey("eng_code_repositories.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    symbol_type = Column(String(64), default="FUNCTION")  # FUNCTION, CLASS, MODULE, API_ENDPOINT, MODEL
    file_path = Column(String(512), nullable=False)
    line_start = Column(Integer, default=1)
    line_end = Column(Integer, default=1)
    docstring = Column(Text, nullable=True)
    called_by_symbols = Column(JSON, default=list)
    calls_symbols = Column(JSON, default=list)


class EngineeringTaskModel(Base):
    """Decomposed Engineering Task for AI Coding Agents or Human Engineers."""
    __tablename__ = "eng_tasks"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    requirement_id = Column(String(64), ForeignKey("eng_requirements.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    task_type = Column(String(64), default="FEATURE")  # FEATURE, BUGFIX, REFACTOR, SECURITY, PERFORMANCE, TECH_DEBT
    priority = Column(String(32), default="HIGH")
    assigned_agent = Column(String(128), default="coding_agent")
    assigned_human_reviewer = Column(String(128), nullable=True)
    status = Column(String(32), default="READY", index=True)  # READY, IN_PROGRESS, IN_REVIEW, COMPLETED, BLOCKED
    branch_name = Column(String(128), nullable=True)
    estimated_tokens = Column(Integer, default=5000)
    tokens_consumed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AgentCodingSessionModel(Base):
    """Sandboxed AI Coding Agent Session and Action Log."""
    __tablename__ = "eng_agent_coding_sessions"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    task_id = Column(String(64), ForeignKey("eng_tasks.id"), nullable=False, index=True)
    agent_id = Column(String(64), default="coding_agent")
    sandbox_workspace_path = Column(String(512), nullable=False)
    branch_created = Column(String(128), nullable=False)
    files_modified = Column(JSON, default=list)
    diff_stat_additions = Column(Integer, default=0)
    diff_stat_deletions = Column(Integer, default=0)
    unit_tests_passed = Column(Boolean, default=False)
    security_checks_passed = Column(Boolean, default=False)
    generated_pr_id = Column(String(64), nullable=True)
    session_cost_usd = Column(Float, default=0.0)
    status = Column(String(32), default="COMPLETED")  # ACTIVE, COMPLETED, FAILED, TERMINATED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EngineeringPullRequestModel(Base):
    """Pull Request with AI & Human Peer Review and 6-Dimension Risk Scorecard."""
    __tablename__ = "eng_pull_requests"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), ForeignKey("eng_code_repositories.id"), nullable=False, index=True)
    task_id = Column(String(64), nullable=True)
    title = Column(String(255), nullable=False)
    source_branch = Column(String(128), nullable=False)
    target_branch = Column(String(128), default="main")
    author = Column(String(128), nullable=False)
    status = Column(String(32), default="OPEN", index=True)  # OPEN, MERGED, CLOSED, DRAFT
    risk_score_composite = Column(Float, default=0.15)  # 0.0 - 1.0
    risk_breakdown_json = Column(JSON, default=dict)  # security, architecture, regression, performance, operational
    ci_pipeline_status = Column(String(32), default="PASSED")
    is_merged = Column(Boolean, default=False)
    merged_by = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CiPipelineModel(Base):
    """Multi-Stage Continuous Integration Pipeline."""
    __tablename__ = "eng_ci_pipelines"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), ForeignKey("eng_code_repositories.id"), nullable=False, index=True)
    pipeline_name = Column(String(255), nullable=False)
    trigger_event = Column(String(64), default="PUSH")  # PUSH, PULL_REQUEST, SCHEDULE, MANUAL
    stages_json = Column(JSON, default=list)  # ["lint", "type_check", "unit_test", "integration_test", "security_scan", "build", "publish"]
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CiBuildRunModel(Base):
    """Individual CI Build Execution."""
    __tablename__ = "eng_ci_build_runs"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    pipeline_id = Column(String(64), ForeignKey("eng_ci_pipelines.id"), nullable=False, index=True)
    commit_sha = Column(String(64), nullable=False)
    branch = Column(String(128), nullable=False)
    build_number = Column(Integer, default=1)
    duration_seconds = Column(Float, default=45.0)
    status = Column(String(32), default="SUCCESS")  # RUNNING, SUCCESS, FAILED, CANCELLED
    logs_uri = Column(String(512), nullable=True)
    artifacts_generated = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class TestSuiteModel(Base):
    """Automated Test Suite with Flakiness & Impact Tracking."""
    __tablename__ = "eng_test_suites"
    __test__ = False

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), ForeignKey("eng_code_repositories.id"), nullable=False, index=True)
    suite_name = Column(String(255), nullable=False)
    suite_type = Column(String(64), default="UNIT")  # UNIT, INTEGRATION, E2E, PERFORMANCE, MUTATION
    total_tests_count = Column(Integer, default=100)
    passed_tests_count = Column(Integer, default=100)
    failed_tests_count = Column(Integer, default=0)
    flaky_rate_pct = Column(Float, default=0.0)
    duration_seconds = Column(Float, default=12.5)
    last_run_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SbomPackageModel(Base):
    """Software Bill of Materials (SBOM) Package & License."""
    __tablename__ = "eng_sbom_packages"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), ForeignKey("eng_code_repositories.id"), nullable=False, index=True)
    package_name = Column(String(255), nullable=False)
    version = Column(String(64), nullable=False)
    license_type = Column(String(64), default="MIT")  # MIT, Apache-2.0, BSD-3-Clause
    is_license_compliant = Column(Boolean, default=True)
    vulnerabilities_count = Column(Integer, default=0)
    scanned_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AutonomousDeploymentModel(Base):
    """Autonomous Deployment with Verification Gates & Instant Rollback."""
    __tablename__ = "eng_deployments"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    service_name = Column(String(255), nullable=False)
    environment = Column(String(32), default="PRODUCTION", index=True)  # STAGING, PRODUCTION, CANARY
    strategy = Column(String(32), default="CANARY")  # CANARY, BLUE_GREEN, ROLLING, SHADOW
    version = Column(String(64), nullable=False)
    traffic_weight_pct = Column(Float, default=100.0)
    verification_status = Column(String(32), default="VERIFIED")  # PENDING_VERIFICATION, VERIFIED, FAILED_VERIFICATION, ROLLED_BACK
    status = Column(String(32), default="ACTIVE")
    rollback_target_version = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ServiceCatalogEntryModel(Base):
    """Production Service with SRE SLO Error Budget Monitoring."""
    __tablename__ = "eng_service_catalog"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    owner_team = Column(String(128), nullable=False)
    repository_id = Column(String(64), nullable=True)
    slo_target_availability_pct = Column(Float, default=99.95)
    current_availability_pct = Column(Float, default=99.98)
    error_budget_remaining_pct = Column(Float, default=85.0)  # 0.0 - 100.0%
    p95_latency_ms = Column(Float, default=32.0)
    status = Column(String(32), default="HEALTHY")  # HEALTHY, DEGRADED, BREACHED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EngineeringIncidentModel(Base):
    """Production Incident with Correlated Root Cause Analysis."""
    __tablename__ = "eng_incidents"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    service_name = Column(String(255), nullable=False)
    severity = Column(String(16), default="SEV2")  # SEV1, SEV2, SEV3, SEV4
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    correlated_root_cause_hypothesis = Column(Text, nullable=True)
    remediation_status = Column(String(32), default="CONTAINED")  # OPEN, INVESTIGATING, CONTAINED, REMEDIATED, RESOLVED
    mitigation_action_taken = Column(String(128), default="AUTOMATED_CANARY_ROLLBACK")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SelfHealingRunbookModel(Base):
    """Policy-controlled automated self-healing runbook."""
    __tablename__ = "eng_self_healing_runbooks"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    trigger_condition = Column(String(128), nullable=False)  # SLO_BREACH, LATENCY_SPIKE, POD_CRASH, HEALTH_CHECK_FAILED
    target_service = Column(String(255), nullable=False)
    action_type = Column(String(64), default="CANARY_ROLLBACK")  # RESTART_POD, SCALE_REPLICAS, CANARY_ROLLBACK, CLEAR_CACHE
    is_autonomous_approved = Column(Boolean, default=True)
    executions_count = Column(Integer, default=0)
    success_rate_pct = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EngineeringFinopsCostModel(Base):
    """Granular Engineering & CI/CD FinOps Cost Allocation."""
    __tablename__ = "eng_finops_costs"

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("eng_project_workspaces.id"), nullable=False, index=True)
    cost_category = Column(String(64), default="CI_BUILD_MINUTES")  # CI_BUILD_MINUTES, CD_DEPLOYMENT, K8S_COMPUTE, AI_CODING_TOKENS, TESTING_INFRA
    amount_usd = Column(Float, default=0.0)
    units_consumed = Column(Float, default=0.0)
    period_date = Column(String(10), default=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
