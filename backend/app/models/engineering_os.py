"""SQLAlchemy ORM models for Phase 61: Unified Engineering, SDLC, DevOps, CI/CD & Technical Operations OS."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class EngineeringOrganizationModel(Base):
    """Engineering organization entity."""
    __tablename__ = "engineering_organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    head_of_engineering_email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class EngineeringTeamModel(Base):
    """Engineering team (e.g. Platform, Backend, SRE, Security, AI)."""
    __tablename__ = "engineering_teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    org_id = Column(UUID(as_uuid=True), ForeignKey("engineering_organizations.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(255), nullable=False)
    team_type = Column(String(50), nullable=False, default="BACKEND")  # BACKEND, FRONTEND, PLATFORM, SRE, SECURITY, QA
    lead_email = Column(String(255), nullable=True)
    member_count = Column(Integer, default=5, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class EngineeringProjectModel(Base):
    """Engineering project linked to product initiatives and repositories."""
    __tablename__ = "engineering_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey("engineering_teams.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    key = Column(String(50), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="ACTIVE")  # ACTIVE, PAUSED, COMPLETED, ARCHIVED
    linked_product_initiative_id = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class EngineeringRepositoryModel(Base):
    """Source code repository tracked within the engineering OS."""
    __tablename__ = "engineering_repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("engineering_projects.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False, default="GITHUB")  # GITHUB, GITLAB, BITBUCKET
    default_branch = Column(String(100), nullable=False, default="main")
    primary_language = Column(String(100), nullable=False, default="Python")
    is_private = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class PullRequestModel(Base):
    """Pull request tracked for review, checks, and deployment traceability."""
    __tablename__ = "engineering_pull_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("engineering_repositories.id", ondelete="CASCADE"), nullable=False)
    pr_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    source_branch = Column(String(100), nullable=False)
    target_branch = Column(String(100), nullable=False, default="main")
    status = Column(String(50), nullable=False, default="OPEN")  # OPEN, MERGED, CLOSED, CHANGES_REQUESTED
    risk_score = Column(Float, default=0.0, nullable=False)
    linked_work_item = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    merged_at = Column(DateTime, nullable=True)


class ServiceCatalogModel(Base):
    """Service catalog entry with runtime ownership and SLO bindings."""
    __tablename__ = "engineering_services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    name = Column(String(255), nullable=False, unique=True)
    service_tier = Column(String(20), nullable=False, default="TIER_1")  # TIER_0, TIER_1, TIER_2, TIER_3
    owner_team = Column(String(100), nullable=False, default="Core Platform")
    runtime = Column(String(50), nullable=False, default="FASTAPI_PYTHON")
    target_slo_availability = Column(Float, default=99.9, nullable=False)
    current_health_state = Column(String(50), default="HEALTHY", nullable=False)  # HEALTHY, DEGRADED, FAILING
    dependencies = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class ApiCatalogModel(Base):
    """API contract specifications and deprecation policies."""
    __tablename__ = "engineering_apis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("engineering_services.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False, default="v1")
    protocol = Column(String(50), nullable=False, default="REST_OPENAPI")  # REST_OPENAPI, GRPC, GRAPHQL
    is_deprecated = Column(Boolean, default=False, nullable=False)
    auth_mechanism = Column(String(100), default="BEARER_JWT", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class EnvironmentModel(Base):
    """Deployment environments (Local, Dev, Staging, Canary, Production, DR)."""
    __tablename__ = "engineering_environments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    name = Column(String(50), nullable=False)  # DEVELOPMENT, STAGING, CANARY, PRODUCTION, DR
    is_production = Column(Boolean, default=False, nullable=False)
    cluster_region = Column(String(100), default="us-east-1", nullable=False)
    status = Column(String(50), default="READY", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class CicdPipelineModel(Base):
    """CI/CD pipeline definition and execution history."""
    __tablename__ = "engineering_pipelines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("engineering_repositories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    pipeline_type = Column(String(50), nullable=False, default="CI_BUILD_TEST")
    last_status = Column(String(50), default="SUCCESS", nullable=False)  # SUCCESS, FAILED, RUNNING, CANCELLED
    duration_seconds = Column(Float, default=120.0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DeploymentRecordModel(Base):
    """Audited deployment record with strategy, approval status, and rollback pointers."""
    __tablename__ = "engineering_deployments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("engineering_services.id", ondelete="CASCADE"), nullable=False)
    environment = Column(String(50), nullable=False, default="PRODUCTION")
    strategy = Column(String(50), nullable=False, default="CANARY")  # CANARY, BLUE_GREEN, ROLLING
    version_tag = Column(String(100), nullable=False)
    commit_sha = Column(String(64), nullable=False)
    operator_email = Column(String(255), nullable=False)
    approved_by = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="DEPLOYED")  # DEPLOYED, FAILED, ROLLED_BACK
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentRecordModel(Base):
    """SEV0–SEV4 incident management with response timeline and root cause postmortem."""
    __tablename__ = "engineering_incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    title = Column(String(255), nullable=False)
    severity = Column(String(20), nullable=False, default="SEV2")  # SEV0, SEV1, SEV2, SEV3, SEV4
    status = Column(String(50), nullable=False, default="DETECTED")  # DETECTED, MITIGATED, RESOLVED, POSTMORTEM_COMPLETED
    affected_service = Column(String(100), nullable=False)
    root_cause_summary = Column(Text, nullable=True)
    duration_minutes = Column(Float, default=30.0, nullable=False)
    incident_commander = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime, nullable=True)


class ChangeManagementModel(Base):
    """Governed engineering change record with risk assessment and approval gates."""
    __tablename__ = "engineering_changes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    title = Column(String(255), nullable=False)
    change_type = Column(String(50), nullable=False, default="INFRASTRUCTURE_UPDATE")
    risk_level = Column(String(20), nullable=False, default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), nullable=False, default="PENDING_APPROVAL")  # PENDING_APPROVAL, APPROVED, REJECTED, EXECUTED
    rollback_plan = Column(Text, nullable=False)
    approver = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class DependencyVulnerabilityModel(Base):
    """Software supply chain CVE vulnerabilities and SBOM tracking."""
    __tablename__ = "engineering_vulnerabilities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    cve_id = Column(String(50), nullable=False)
    package_name = Column(String(100), nullable=False)
    current_version = Column(String(50), nullable=False)
    fixed_version = Column(String(50), nullable=True)
    severity = Column(String(20), nullable=False, default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), nullable=False, default="OPEN")  # OPEN, MITIGATED, PATCHED, ACCEPTED_RISK
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class TechnicalDebtItemModel(Base):
    """Technical debt registry with estimated remediation effort and risk impact."""
    __tablename__ = "engineering_technical_debt"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    title = Column(String(255), nullable=False)
    area = Column(String(100), nullable=False, default="ARCHITECTURE")  # ARCHITECTURE, CODE, INFRA, TESTING, SECURITY
    severity = Column(String(20), nullable=False, default="MEDIUM")
    effort_person_days = Column(Float, default=5.0, nullable=False)
    remediation_status = Column(String(50), default="LOGGED", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class CloudCostRecordModel(Base):
    """Cloud resource allocation and FinOps cost records."""
    __tablename__ = "engineering_cloud_costs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    service_name = Column(String(100), nullable=False)
    environment = Column(String(50), nullable=False, default="PRODUCTION")
    monthly_cost_usd = Column(Float, nullable=False, default=1200.0)
    waste_estimate_usd = Column(Float, nullable=False, default=150.0)
    cost_trend_pct = Column(Float, nullable=False, default=3.5)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class EngineeringRiskModel(Base):
    """Engineering risk register."""
    __tablename__ = "engineering_risks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="default_tenant", index=True)
    category = Column(String(100), nullable=False, default="DELIVERY")  # DELIVERY, RELIABILITY, SECURITY, COMPLIANCE
    title = Column(String(255), nullable=False)
    probability = Column(Float, default=0.3, nullable=False)
    impact_score = Column(Float, default=7.0, nullable=False)
    exposure_score = Column(Float, default=2.1, nullable=False)
    severity = Column(String(20), default="HIGH", nullable=False)
    mitigation_strategy = Column(Text, nullable=True)
    owner = Column(String(255), default="lead-eng@uzaii.com", nullable=False)
    status = Column(String(50), default="OPEN", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
