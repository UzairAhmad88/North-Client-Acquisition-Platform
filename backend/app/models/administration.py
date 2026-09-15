"""SQLAlchemy ORM Models for Unified Platform Administration, Configuration, Policies & Controls."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text

from app.models.base import Base

JSON_TYPE = JSON


class ConfigurationDefinitionModel(Base):
    """Centralized configuration key definitions and metadata."""
    __tablename__ = "configuration_definitions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    config_type = Column(String(50), nullable=False)  # STRING, INTEGER, DECIMAL, BOOLEAN, etc.
    category = Column(String(100), nullable=False, index=True)
    scope = Column(String(50), nullable=False, default="GLOBAL")
    default_value_json = Column(JSON_TYPE, nullable=True)
    current_value_json = Column(JSON_TYPE, nullable=True)
    validation_rules_json = Column(JSON_TYPE, nullable=True)
    sensitive = Column(Boolean, default=False, nullable=False)
    mutable = Column(Boolean, default=True, nullable=False)
    restart_required = Column(Boolean, default=False, nullable=False)
    policy_controlled = Column(Boolean, default=False, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE", index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ConfigurationVersionModel(Base):
    """Immutable audit trail of previous configuration states."""
    __tablename__ = "configuration_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    config_key = Column(String(100), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    value_json = Column(JSON_TYPE, nullable=True)
    changed_by = Column(String(100), nullable=False)
    change_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class ConfigurationValueModel(Base):
    """Scoped overrides for configurations (e.g. per Organization, Environment, or Service)."""
    __tablename__ = "configuration_values"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    config_key = Column(String(100), nullable=False, index=True)
    scope = Column(String(50), nullable=False)  # SERVICE, ENVIRONMENT, ORGANIZATION
    scope_identifier = Column(String(100), nullable=False, index=True)
    value_json = Column(JSON_TYPE, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class ConfigurationChangeRequestModel(Base):
    """Formal change proposals requiring multi-party authorization."""
    __tablename__ = "configuration_change_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    change_id = Column(String(100), unique=True, nullable=False, index=True)
    config_key = Column(String(100), nullable=False, index=True)
    old_value_json = Column(JSON_TYPE, nullable=True)
    new_value_json = Column(JSON_TYPE, nullable=False)
    reason = Column(Text, nullable=False)
    requested_by = Column(String(100), nullable=False)
    reviewed_by = Column(String(100), nullable=True)
    approved_by = Column(String(100), nullable=True)
    risk_level = Column(String(50), nullable=False, default="MEDIUM")
    status = Column(String(50), nullable=False, default="PENDING_APPROVAL", index=True)
    effective_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class PlatformPolicyModel(Base):
    """Enterprise policy declarations and constraints."""
    __tablename__ = "platform_policies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    policy_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(50), nullable=False, index=True)  # AI, SECURITY, COMMUNICATION, FINANCE, DATA, etc.
    description = Column(Text, nullable=True)
    scope = Column(String(50), nullable=False, default="GLOBAL")
    priority = Column(Integer, nullable=False, default=100)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="ACTIVE", index=True)
    approval_required = Column(Boolean, default=False, nullable=False)
    created_by = Column(String(100), nullable=False, default="system")
    effective_from = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    effective_until = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class PlatformPolicyVersionModel(Base):
    """Audit versions of platform policies."""
    __tablename__ = "platform_policy_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    policy_id = Column(String(100), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    policy_json = Column(JSON_TYPE, nullable=False)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class PlatformPolicyRuleModel(Base):
    """Individual conditions and actions comprising a policy."""
    __tablename__ = "platform_policy_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id = Column(String(100), unique=True, nullable=False, index=True)
    policy_id = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    condition = Column(Text, nullable=False)
    action = Column(String(50), nullable=False)  # ALLOW, REVIEW, BLOCK
    reason = Column(Text, nullable=False)
    is_mandatory_security = Column(Boolean, default=False, nullable=False)


class AdminFeatureFlagModel(Base):
    """Feature flag definitions and global states."""
    __tablename__ = "admin_feature_flags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="DISABLED", index=True)
    rollout_type = Column(String(50), nullable=False, default="BOOLEAN")
    rollout_percentage = Column(Integer, default=0, nullable=False)
    allowed_tiers_json = Column(JSON_TYPE, nullable=True)
    environment = Column(String(50), nullable=False, default="PRODUCTION")
    owner = Column(String(100), nullable=False, default="admin")
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AdminFeatureFlagRuleModel(Base):
    """Granular activation rules for feature flags."""
    __tablename__ = "admin_feature_flag_rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    flag_key = Column(String(100), nullable=False, index=True)
    target_type = Column(String(50), nullable=False)  # USER, TENANT, REGION, ROLE
    target_value = Column(String(255), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)


class EnvironmentRecordModel(Base):
    """Registered application environments."""
    __tablename__ = "environment_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    env_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    env_type = Column(String(50), nullable=False)
    is_production = Column(Boolean, default=False, nullable=False)
    requires_approval = Column(Boolean, default=False, nullable=False)
    allow_mock_providers = Column(Boolean, default=True, nullable=False)
    allow_chaos_testing = Column(Boolean, default=False, nullable=False)
    allow_real_financial_execution = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), nullable=False, default="ACTIVE")
    active_version = Column(String(50), nullable=False, default="v1.0.0")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class IntegrationRegistryModel(Base):
    """External provider and third-party integration registry."""
    __tablename__ = "integration_registry"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    base_url = Column(String(255), nullable=False)
    secret_reference = Column(String(255), nullable=False)  # secret://...
    timeout_seconds = Column(Integer, default=30, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    rate_limit_rpm = Column(Integer, default=600, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    health_status = Column(String(50), default="HEALTHY", nullable=False)
    latency_ms = Column(Float, default=0.0, nullable=False)
    error_rate_percentage = Column(Float, default=0.0, nullable=False)
    last_health_check = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SecretReferenceModel(Base):
    """Metadata tracking external vault secret references (NO raw secrets stored)."""
    __tablename__ = "secret_references"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    secret_uri = Column(String(255), unique=True, nullable=False, index=True)  # secret://...
    display_name = Column(String(255), nullable=False)
    provider_name = Column(String(100), nullable=False)
    last_rotated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    rotation_period_days = Column(Integer, default=90, nullable=False)
    status = Column(String(50), default="ACTIVE", nullable=False)


class MaintenanceWindowModel(Base):
    """Planned maintenance intervals and operational degradation records."""
    __tablename__ = "maintenance_windows"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    window_id = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    mode = Column(String(50), nullable=False, default="NORMAL")
    is_active = Column(Boolean, default=False, nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    internal_banner = Column(Text, nullable=True)
    client_portal_banner = Column(Text, nullable=True)
    initiated_by = Column(String(100), nullable=False)
    affected_services_json = Column(JSON_TYPE, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class SystemControlModel(Base):
    """System-wide emergency kill switches and layered disablement states."""
    __tablename__ = "system_control_states"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    switch_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    level = Column(String(50), nullable=False)  # GLOBAL, DOMAIN, SERVICE, AGENT, MODEL, TOOL, etc.
    target_identifier = Column(String(100), nullable=False)
    state = Column(String(50), default="DISARMED", nullable=False, index=True)
    reason = Column(Text, nullable=True)
    activated_by = Column(String(100), nullable=True)
    activated_at = Column(DateTime(timezone=True), nullable=True)


class AdministrativeAuditModel(Base):
    """Immutable audit trail for all control plane and administrative actions."""
    __tablename__ = "administrative_audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    actor = Column(String(100), nullable=False, index=True)
    actor_type = Column(String(50), nullable=False, default="USER")
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    resource_id = Column(String(100), nullable=False)
    old_value_json = Column(JSON_TYPE, nullable=True)
    new_value_json = Column(JSON_TYPE, nullable=True)
    reason = Column(Text, nullable=True)
    authorization_status = Column(String(50), default="AUTHORIZED", nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class ConfigurationDriftModel(Base):
    """Detected divergences between versioned configurations and actual runtime environments."""
    __tablename__ = "configuration_drift_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    drift_id = Column(String(100), unique=True, nullable=False, index=True)
    config_key = Column(String(100), nullable=False, index=True)
    expected_value_json = Column(JSON_TYPE, nullable=True)
    actual_value_json = Column(JSON_TYPE, nullable=True)
    severity = Column(String(50), nullable=False, default="WARNING")
    environment = Column(String(50), nullable=False, default="PRODUCTION")
    resolved = Column(Boolean, default=False, nullable=False, index=True)
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
