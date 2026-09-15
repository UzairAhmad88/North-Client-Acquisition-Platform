"""
Phase 67: Autonomous DevSecOps, AI Software Factory, CI/CD Intelligence & Self-Healing Engineering Models.
All tables prefixed with `dsops_` to guarantee zero collisions with Phase 61 (`engineering_*`) and Phase 64 (`eng_*`).
"""

import uuid
from datetime import datetime, timezone
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
from app.models.base import Base


# ----------------------------------------------------------------------
# 1. Software Factory Projects & Repository Intelligence
# ----------------------------------------------------------------------

class DsopsProjectModel(Base):
    """Software Factory project entity."""
    __tablename__ = "dsops_factory_projects"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"proj_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(128), nullable=False)
    team = Column(String(128), nullable=False)
    status = Column(String(32), default="ACTIVE")  # ACTIVE, PLANNING, ARCHIVED
    tech_stack = Column(JSON, default=list)
    environments = Column(JSON, default=list)
    budget_usd = Column(Float, default=50000.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsRepositoryModel(Base):
    """Indexed Git repository metadata."""
    __tablename__ = "dsops_repositories"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"repo_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    default_branch = Column(String(64), default="main")
    repo_url = Column(String(512), nullable=False)
    visibility = Column(String(32), default="PRIVATE")  # PRIVATE, INTERNAL, PUBLIC
    is_indexed = Column(Boolean, default=True)
    total_commits = Column(Integer, default=0)
    active_branches = Column(Integer, default=1)
    open_prs_count = Column(Integer, default=0)
    vulnerabilities_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsCodebaseKnowledgeGraphModel(Base):
    """Semantic graph linking files, functions, packages, and architecture."""
    __tablename__ = "dsops_codebase_graphs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"kg_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), nullable=False, index=True)
    source_entity = Column(String(256), nullable=False)
    source_type = Column(String(64), nullable=False)  # FILE, MODULE, FUNCTION, PACKAGE, SERVICE
    target_entity = Column(String(256), nullable=False)
    target_type = Column(String(64), nullable=False)
    relationship_type = Column(String(64), nullable=False)  # CONTAINS, CALLS, DEPENDS_ON, RUNS_ON, IMPLEMENTS
    metadata_context = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ----------------------------------------------------------------------
# 2. AI Engineering Agents, Planning & Governance
# ----------------------------------------------------------------------

class DsopsEngineeringAgentModel(Base):
    """Registered AI Engineering agent identity and boundary envelope."""
    __tablename__ = "dsops_engineering_agents"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"eng_agt_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    agent_id = Column(String(64), nullable=False)
    name = Column(String(128), nullable=False)
    role = Column(String(64), nullable=False)  # PLANNER, CODER, REVIEWER, SRE, RELEASE, INCIDENT, REMEDIATION
    allowed_tools = Column(JSON, default=list)
    repo_scope = Column(JSON, default=list)
    action_limit = Column(String(32), default="MEDIUM_RISK_WRITE")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsAgentApprovalModel(Base):
    """Human approval gate for high-impact AI coding/deployment actions."""
    __tablename__ = "dsops_agent_approvals"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"appr_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    agent_id = Column(String(64), nullable=False)
    action_type = Column(String(64), nullable=False)  # DEPLOY_PRODUCTION, MERGE_PROTECTED, DB_MIGRATION, ROTATE_KEY
    target_resource = Column(String(256), nullable=False)
    justification = Column(Text, nullable=False)
    risk_level = Column(String(32), default="HIGH")
    status = Column(String(32), default="PENDING")  # PENDING, APPROVED, REJECTED, EXPIRED
    approver_email = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    decided_at = Column(DateTime, nullable=True)


class DsopsTaskPlanModel(Base):
    """AI-synthesized technical implementation plan."""
    __tablename__ = "dsops_task_plans"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"plan_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    requirement_summary = Column(Text, nullable=False)
    files_to_change = Column(JSON, default=list)
    architecture_impact = Column(Text, nullable=True)
    security_considerations = Column(JSON, default=list)
    testing_strategy = Column(Text, nullable=True)
    rollback_plan = Column(Text, nullable=True)
    status = Column(String(32), default="APPROVED")  # DRAFT, APPROVED, IN_PROGRESS, COMPLETED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ----------------------------------------------------------------------
# 3. Code Review, Change Risk & Test Intelligence
# ----------------------------------------------------------------------

class DsopsCodeReviewFindingModel(Base):
    """9-factor AI and static analysis code review finding."""
    __tablename__ = "dsops_review_findings"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"rev_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), nullable=False, index=True)
    pull_request_number = Column(Integer, default=1)
    file_path = Column(String(512), nullable=False)
    line_number = Column(Integer, nullable=True)
    dimension = Column(String(64), default="SECURITY")  # CORRECTNESS, ARCHITECTURE, SECURITY, PERFORMANCE, MAINTAINABILITY, TESTING
    severity = Column(String(32), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    evidence = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    confidence = Column(Float, default=0.95)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsTestIntelligenceModel(Base):
    """Test suite execution, coverage, and flakiness tracker."""
    __tablename__ = "dsops_test_intelligence"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"tst_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), nullable=False, index=True)
    test_suite_name = Column(String(256), nullable=False)
    test_type = Column(String(64), default="UNIT")  # UNIT, INTEGRATION, API, E2E, CONTRACT, PERFORMANCE
    pass_rate = Column(Float, default=1.0)
    flakiness_score = Column(Float, default=0.01)  # 0.0 to 1.0
    runtime_seconds = Column(Float, default=2.4)
    last_run_status = Column(String(32), default="PASSED")  # PASSED, FAILED, FLAKY, SKIPPED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ----------------------------------------------------------------------
# 4. CI/CD Engine, Builds & Artifact Provenance
# ----------------------------------------------------------------------

class DsopsPipelineModel(Base):
    """Versioned CI/CD pipeline definition."""
    __tablename__ = "dsops_pipelines"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"pipe_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    repository_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    trigger = Column(String(64), default="PUSH")  # PUSH, PULL_REQUEST, SCHEDULE, MANUAL
    stages = Column(JSON, default=list)  # ["checkout", "lint", "build", "test", "security_scan", "publish"]
    status = Column(String(32), default="SUCCESS")  # RUNNING, SUCCESS, FAILED, BLOCKED
    last_run_id = Column(String(64), nullable=True)
    duration_seconds = Column(Integer, default=180)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsBuildModel(Base):
    """Build execution record with layer and test caching."""
    __tablename__ = "dsops_builds"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"bld_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    pipeline_id = Column(String(64), nullable=False, index=True)
    commit_sha = Column(String(64), nullable=False)
    branch = Column(String(128), default="main")
    status = Column(String(32), default="SUCCESS")
    cache_hit_rate = Column(Float, default=0.88)
    cpu_cores_used = Column(Float, default=4.0)
    memory_mb = Column(Integer, default=4096)
    duration_seconds = Column(Integer, default=74)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsArtifactProvenanceModel(Base):
    """Immutable software supply-chain artifact with cryptographic provenance."""
    __tablename__ = "dsops_artifacts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"art_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    build_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    version = Column(String(64), nullable=False)
    artifact_type = Column(String(64), default="CONTAINER_IMAGE")  # CONTAINER_IMAGE, WHEEL, BINARY, SBOM
    sha256_checksum = Column(String(64), nullable=False)
    signature_verified = Column(Boolean, default=True)
    sbom_scanned = Column(Boolean, default=True)
    critical_vulnerabilities = Column(Integer, default=0)
    provenance_chain = Column(JSON, default=dict)  # {"req_id": ..., "commit_sha": ..., "build_id": ...}
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ----------------------------------------------------------------------
# 5. Release Engine, Deployment & Progressive Delivery
# ----------------------------------------------------------------------

class DsopsReleaseModel(Base):
    """Production release package with multi-risk assessment."""
    __tablename__ = "dsops_releases"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"rel_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), nullable=False, index=True)
    version = Column(String(64), nullable=False)
    release_notes = Column(Text, nullable=True)
    risk_score = Column(Float, default=0.15)  # 0.0 to 1.0
    risk_level = Column(String(32), default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    approval_status = Column(String(32), default="APPROVED")
    status = Column(String(32), default="ACTIVE")  # DRAFT, READY, DEPLOYED, ROLLED_BACK
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsDeploymentModel(Base):
    """Canary, blue-green, and progressive rollout execution."""
    __tablename__ = "dsops_deployments"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"dep_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    release_id = Column(String(64), nullable=False, index=True)
    environment = Column(String(64), default="PRODUCTION")  # DEVELOPMENT, STAGING, PRODUCTION
    strategy = Column(String(64), default="CANARY")  # CANARY, BLUE_GREEN, ROLLING, SHADOW
    traffic_percentage = Column(Integer, default=100)  # 1% -> 5% -> 25% -> 50% -> 100%
    status = Column(String(32), default="HEALTHY")  # IN_PROGRESS, HEALTHY, DEGRADED, ROLLED_BACK
    rollback_available = Column(Boolean, default=True)
    error_rate = Column(Float, default=0.0002)
    p99_latency_ms = Column(Float, default=42.5)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsEnvironmentModel(Base):
    """Environment configuration and drift detection."""
    __tablename__ = "dsops_environments"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"env_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(64), nullable=False)  # DEVELOPMENT, STAGING, PRODUCTION, DR
    cluster_provider = Column(String(64), default="KUBERNETES")
    version_deployed = Column(String(64), default="v1.0.0")
    drift_detected = Column(Boolean, default=False)
    drift_details = Column(JSON, default=dict)
    health_status = Column(String(32), default="HEALTHY")  # HEALTHY, WARNING, CRITICAL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ----------------------------------------------------------------------
# 6. Observability, SRE, SLOs & Error Budgets
# ----------------------------------------------------------------------

class DsopsServiceCatalogModel(Base):
    """Service catalog and dependency topology."""
    __tablename__ = "dsops_services"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"svc_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    owner_team = Column(String(128), nullable=False)
    repository_id = Column(String(64), nullable=True)
    dependencies = Column(JSON, default=list)  # ["svc_billing", "db_postgres"]
    health_status = Column(String(32), default="HEALTHY")  # HEALTHY, DEGRADED, OUTAGE
    current_error_rate = Column(Float, default=0.0001)
    current_latency_ms = Column(Float, default=24.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsSloModel(Base):
    """SLO target and error budget burn rate tracker."""
    __tablename__ = "dsops_slos"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"slo_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    service_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)  # Availability, Latency P99
    target_percentage = Column(Float, default=99.9)
    actual_percentage = Column(Float, default=99.98)
    error_budget_total = Column(Float, default=100.0)
    error_budget_consumed = Column(Float, default=4.2)
    burn_rate_1h = Column(Float, default=0.8)  # 1.0 = normal consumption
    status = Column(String(32), default="HEALTHY")  # HEALTHY, WARNING, EXHAUSTED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ----------------------------------------------------------------------
# 7. SRE Incidents, Automated RCA & Self-Healing Runbooks
# ----------------------------------------------------------------------

class DsopsIncidentModel(Base):
    """Production engineering incident record."""
    __tablename__ = "dsops_incidents"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"inc_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    service_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    severity = Column(String(32), default="P2")  # P0, P1, P2, P3
    status = Column(String(32), default="RESOLVED")  # DETECTED, INVESTIGATING, MITIGATED, RESOLVED
    recent_deployments = Column(JSON, default=list)
    likely_root_cause = Column(Text, nullable=True)
    remediation_status = Column(String(32), default="AUTOMATED_ROLLBACK_VERIFIED")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime, nullable=True)


class DsopsRunbookModel(Base):
    """Self-healing runbook with pre-approved execution bounds."""
    __tablename__ = "dsops_runbooks"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"rb_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    target_symptom = Column(String(256), nullable=False)
    remediation_action = Column(String(128), nullable=False)  # CANARY_ROLLBACK, RESTART_POD, SCALE_REPLICAS, PURGE_CACHE
    requires_human_approval = Column(Boolean, default=False)
    success_rate = Column(Float, default=0.98)
    times_executed = Column(Integer, default=14)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ----------------------------------------------------------------------
# 8. Technical Debt, DORA & Engineering Analytics
# ----------------------------------------------------------------------

class DsopsTechnicalDebtModel(Base):
    """Technical debt and architecture drift findings."""
    __tablename__ = "dsops_technical_debt"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"td_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    category = Column(String(64), default="COMPLEXITY")  # DUPLICATION, OUTDATED_DEP, COMPLEXITY, DEAD_CODE, ARCH_VIOLATION
    effort_estimate_days = Column(Float, default=2.0)
    priority = Column(String(32), default="MEDIUM")
    status = Column(String(32), default="OPEN")  # OPEN, IN_PROGRESS, RESOLVED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsDoraMetricsModel(Base):
    """DORA metrics snapshot (Deployment Frequency, Lead Time, CFR, MTTR)."""
    __tablename__ = "dsops_dora_metrics"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"dora_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), nullable=False, index=True)
    deployment_frequency_per_day = Column(Float, default=4.2)
    lead_time_for_changes_hours = Column(Float, default=2.4)
    change_failure_rate_pct = Column(Float, default=0.8)
    time_to_restore_service_minutes = Column(Float, default=12.0)
    dora_tier = Column(String(32), default="ELITE")  # ELITE, HIGH, MEDIUM, LOW
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DsopsAuditEventModel(Base):
    """Audit trail for all engineering actions and AI modifications."""
    __tablename__ = "dsops_audit_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"eng_aud_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    actor_id = Column(String(128), nullable=False)
    actor_type = Column(String(32), default="AI_AGENT")  # HUMAN, AI_AGENT, CI_SYSTEM
    action = Column(String(128), nullable=False)
    target_resource = Column(String(256), nullable=False)
    approval_ref = Column(String(64), nullable=True)
    status = Column(String(32), default="SUCCESS")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
