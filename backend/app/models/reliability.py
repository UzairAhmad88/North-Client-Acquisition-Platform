"""SQLAlchemy ORM Models for Unified Reliability, SRE, Disaster Recovery, and Operations Platform."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, Numeric, String, Text

from app.models.base import Base

JSON_TYPE = JSON


class SystemHealthSnapshotModel(Base):
    """Periodic and on-demand deep health snapshots of the entire platform."""
    __tablename__ = "system_health_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String(50), nullable=False, default="HEALTHY", index=True)
    active_circuit_breakers = Column(Integer, default=0, nullable=False)
    open_incidents = Column(Integer, default=0, nullable=False)
    unhealthy_components = Column(Integer, default=0, nullable=False)
    summary = Column(Text, nullable=True)
    components_json = Column(JSON_TYPE, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class ComponentHealthModel(Base):
    """Individual component and dependency health check records."""
    __tablename__ = "component_health_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    component_name = Column(String(100), nullable=False, index=True)
    component_type = Column(String(50), nullable=False)  # DATABASE, CACHE, QUEUE, STORAGE, AI_PROVIDER, PAYMENT_GATEWAY
    status = Column(String(50), nullable=False, default="HEALTHY")
    latency_ms = Column(Float, nullable=False, default=0.0)
    is_critical = Column(Boolean, default=True, nullable=False)
    message = Column(Text, nullable=True)
    details_json = Column(JSON_TYPE, nullable=True)
    checked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class SLODefinitionModel(Base):
    """Service Level Objective definitions and targets."""
    __tablename__ = "slo_definitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slo_type = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_percentage = Column(Float, nullable=False, default=99.9)
    window_days = Column(Integer, nullable=False, default=30)
    service_tier = Column(String(50), nullable=False, default="CRITICAL")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SLOMetricSnapshotModel(Base):
    """Calculated SLI, error budget depletion, and burn rate snapshots."""
    __tablename__ = "slo_metric_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slo_id = Column(String(36), ForeignKey("slo_definitions.id", ondelete="CASCADE"), nullable=True, index=True)
    slo_type = Column(String(50), nullable=False, index=True)
    current_sli = Column(Float, nullable=False)
    target_slo = Column(Float, nullable=False)
    error_budget_remaining_pct = Column(Float, nullable=False)
    burn_rate_1h = Column(Float, nullable=False, default=1.0)
    burn_rate_24h = Column(Float, nullable=False, default=1.0)
    budget_status = Column(String(50), nullable=False, default="HEALTHY", index=True)
    total_events = Column(Integer, nullable=False, default=0)
    bad_events = Column(Integer, nullable=False, default=0)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class ReliabilityIncidentModel(Base):
    """Incidents with severity levels, lifecycle states, impacts, and responder notes."""
    __tablename__ = "reliability_incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False, index=True)  # SEV1_CRITICAL, SEV2_MAJOR, etc.
    status = Column(String(50), nullable=False, default="TRIGGERED", index=True)
    affected_services = Column(JSON_TYPE, nullable=False)  # List of service names
    lead_responder = Column(String(255), nullable=True)
    responders = Column(JSON_TYPE, nullable=True)
    impact_summary = Column(Text, nullable=False)
    timeline_events = Column(JSON_TYPE, nullable=True)
    mitigation_steps = Column(JSON_TYPE, nullable=True)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    mitigated_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class IncidentPostmortemModel(Base):
    """Blameless postmortems with timeline, five whys, action items, and lessons learned."""
    __tablename__ = "incident_postmortems"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String(36), ForeignKey("reliability_incidents.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    summary = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=False)
    five_whys = Column(JSON_TYPE, nullable=True)
    timeline_events = Column(JSON_TYPE, nullable=True)
    what_went_well = Column(JSON_TYPE, nullable=True)
    what_could_improve = Column(JSON_TYPE, nullable=True)
    action_items = Column(JSON_TYPE, nullable=True)
    owner = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SystemBackupRecordModel(Base):
    """System backups across databases, file storage, Redis, and configuration vaults."""
    __tablename__ = "system_backup_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    backup_type = Column(String(50), nullable=False, index=True)  # DATABASE_FULL, DATABASE_WAL, BLOB_STORAGE, etc.
    status = Column(String(50), nullable=False, default="COMPLETED", index=True)
    size_bytes = Column(Integer, nullable=False, default=0)
    storage_location = Column(String(512), nullable=False)
    checksum_sha256 = Column(String(64), nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    retention_days = Column(Integer, default=30, nullable=False)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class RestoreVerificationTestModel(Base):
    """Automated and manual restore verification executions in isolated scratch environments."""
    __tablename__ = "restore_verification_tests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    backup_id = Column(String(36), ForeignKey("system_backup_records.id", ondelete="SET NULL"), nullable=True, index=True)
    environment = Column(String(50), nullable=False, default="ISOLATED_SANDBOX")
    status = Column(String(50), nullable=False, default="COMPLETED", index=True)
    rto_achieved_seconds = Column(Integer, nullable=False, default=0)
    data_integrity_passed = Column(Boolean, default=True, nullable=False)
    tables_restored_count = Column(Integer, nullable=False, default=0)
    records_verified_count = Column(Integer, nullable=False, default=0)
    logs = Column(JSON_TYPE, nullable=True)
    executed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class DisasterRecoveryPlanModel(Base):
    """DR plans with RPO/RTO parameters, dependencies, and ordered recovery step sequences."""
    __tablename__ = "disaster_recovery_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_name = Column(String(255), nullable=False, unique=True)
    scenario = Column(String(100), nullable=False)  # PRIMARY_REGION_OUTAGE, DATABASE_CORRUPTION, RANSOMWARE, etc.
    target_rpo_minutes = Column(Integer, nullable=False, default=5)
    target_rto_minutes = Column(Integer, nullable=False, default=30)
    primary_region = Column(String(50), nullable=False, default="us-east-1")
    secondary_region = Column(String(50), nullable=False, default="us-west-2")
    status = Column(String(50), nullable=False, default="READY")
    recovery_steps = Column(JSON_TYPE, nullable=False)
    last_tested_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class DisasterRecoveryDrillModel(Base):
    """Simulated and live disaster recovery drill execution logs and scorecards."""
    __tablename__ = "disaster_recovery_drills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("disaster_recovery_plans.id", ondelete="CASCADE"), nullable=True, index=True)
    scenario = Column(String(100), nullable=False)
    initiated_by = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="COMPLETED", index=True)
    actual_rto_minutes = Column(Float, nullable=False, default=0.0)
    data_loss_minutes = Column(Float, nullable=False, default=0.0)
    step_results = Column(JSON_TYPE, nullable=False)
    observations = Column(Text, nullable=True)
    lessons_learned = Column(JSON_TYPE, nullable=True)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class DeploymentRecordModel(Base):
    """Deployment tracking, smoke test outcomes, and rollback status."""
    __tablename__ = "deployment_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    version = Column(String(50), nullable=False, index=True)
    environment = Column(String(50), nullable=False, default="PRODUCTION", index=True)
    deployed_by = Column(String(255), nullable=False)
    git_commit_sha = Column(String(64), nullable=False)
    status = Column(String(50), nullable=False, default="HEALTHY")
    smoke_tests_passed = Column(Boolean, default=True, nullable=False)
    migrations_applied = Column(Boolean, default=True, nullable=False)
    release_notes = Column(Text, nullable=True)
    deployed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class FeatureFlagModel(Base):
    """Feature flag definitions, kill switches, and tenant targeting rules."""
    __tablename__ = "feature_flags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    percentage_rollout = Column(Integer, default=100, nullable=False)
    allowed_tiers = Column(JSON_TYPE, nullable=True)
    tenant_whitelist = Column(JSON_TYPE, nullable=True)
    tenant_blacklist = Column(JSON_TYPE, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class CircuitBreakerStateModel(Base):
    """Persistent telemetry snapshot for circuit breakers across external services."""
    __tablename__ = "circuit_breaker_states"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    service_name = Column(String(100), nullable=False, unique=True, index=True)
    state = Column(String(50), nullable=False, default="CLOSED")
    failure_count = Column(Integer, default=0, nullable=False)
    success_count = Column(Integer, default=0, nullable=False)
    last_failure_reason = Column(Text, nullable=True)
    last_state_change = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class IdempotencyRecordModel(Base):
    """Idempotency tokens to protect critical financial and state transitions from duplicate processing."""
    __tablename__ = "idempotency_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String(255), nullable=False, unique=True, index=True)
    action_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="PROCESSING")  # PROCESSING, COMPLETED, FAILED
    response_payload = Column(JSON_TYPE, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
