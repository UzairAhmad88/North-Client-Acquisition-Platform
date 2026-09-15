"""
SQLAlchemy ORM models for Phase 66 — Autonomous Cybersecurity, Zero-Trust Security Operations & AI Defense Platform.
All tables are prefixed with 'czt_' and models with 'Czt' to prevent collisions and support multi-tenant isolation.
"""

from datetime import datetime, timezone
import uuid
from typing import Optional, Dict, Any, List

from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Boolean,
    DateTime,
    JSON,
)
from app.models.base import BaseModel, Base


# ----------------------------------------------------------------------
# 1. Assets & Topology
# ----------------------------------------------------------------------
class CztAssetModel(Base):
    """Enterprise hardware, cloud, service, database, container, or AI asset."""
    __tablename__ = "czt_assets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"asset_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    asset_type = Column(String(64), nullable=False)  # SERVER, CONTAINER, VM, DATABASE, APPLICATION, API, REPO, CLOUD_RESOURCE, DEVICE, SERVICE, MODEL, AGENT, DATASET
    owner = Column(String(128), nullable=False)
    environment = Column(String(32), default="PRODUCTION")  # PRODUCTION, STAGING, DEVELOPMENT
    criticality = Column(String(32), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    ip_address = Column(String(64), nullable=True)
    hostname = Column(String(256), nullable=True)
    location = Column(String(128), default="us-east-1")
    security_state = Column(String(32), default="SECURE")  # SECURE, AT_RISK, COMPROMISED, ISOLATED
    risk_score = Column(Float, default=0.1)
    tags = Column(JSON, default=list)
    metadata_context = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class CztAssetRelationshipModel(Base):
    """Dependency and communication topology between assets."""
    __tablename__ = "czt_asset_relationships"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"areln_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_asset_id = Column(String(64), nullable=False, index=True)
    target_asset_id = Column(String(64), nullable=False, index=True)
    relationship_type = Column(String(64), nullable=False)  # DEPENDS_ON, COMMUNICATES_WITH, HOSTS, DEPLOYS, ACCESSED_BY
    protocol = Column(String(32), default="HTTPS")
    port = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 2. Identity Security & Zero-Trust
# ----------------------------------------------------------------------
class CztIdentityModel(Base):
    """User, service account, workload, or bot identity."""
    __tablename__ = "czt_identities"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"ident_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    principal_id = Column(String(128), nullable=False, index=True)
    identity_type = Column(String(64), nullable=False)  # USER, SERVICE_ACCOUNT, AGENT, WORKLOAD, BOT, API_CLIENT
    email_or_handle = Column(String(256), nullable=True)
    display_name = Column(String(256), nullable=False)
    status = Column(String(32), default="ACTIVE")  # ACTIVE, SUSPENDED, REVOKED, LOCKED, QUARANTINED
    is_privileged = Column(Boolean, default=False)
    mfa_enforced = Column(Boolean, default=True)
    current_risk_level = Column(String(32), default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    risk_score = Column(Float, default=0.05)
    last_authenticated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)


class CztIdentityRoleModel(Base):
    """Role mapping for RBAC and permissions."""
    __tablename__ = "czt_identity_roles"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"idrole_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    identity_id = Column(String(64), nullable=False, index=True)
    role_name = Column(String(128), nullable=False)
    scope = Column(String(128), default="GLOBAL")
    granted_by = Column(String(128), nullable=False)
    granted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)


class CztIdentityRiskModel(Base):
    """Identity Risk Evaluation & UEBA profile."""
    __tablename__ = "czt_identity_risk"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"idrisk_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    identity_id = Column(String(64), nullable=False, index=True)
    anomaly_factor = Column(String(128), nullable=False)
    factor_score = Column(Float, default=0.0)
    evidence = Column(JSON, default=dict)
    evaluated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 3. Device Posture & Machine Identity
# ----------------------------------------------------------------------
class CztDeviceModel(Base):
    """Registered endpoint or device."""
    __tablename__ = "czt_devices"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"dev_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    device_name = Column(String(256), nullable=False)
    owner_identity_id = Column(String(64), nullable=False, index=True)
    platform = Column(String(64), default="LINUX")  # WINDOWS, MACOS, LINUX, IOS, ANDROID
    os_version = Column(String(128), nullable=True)
    is_managed = Column(Boolean, default=True)
    is_encrypted = Column(Boolean, default=True)
    edr_installed = Column(Boolean, default=True)
    posture_status = Column(String(32), default="COMPLIANT")  # COMPLIANT, NON_COMPLIANT, HIGH_RISK, UNKNOWN
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztDevicePostureModel(Base):
    """Device posture assessment logs."""
    __tablename__ = "czt_device_posture"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"posture_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    device_id = Column(String(64), nullable=False, index=True)
    firewall_enabled = Column(Boolean, default=True)
    patches_up_to_date = Column(Boolean, default=True)
    secure_boot_enabled = Column(Boolean, default=True)
    compromise_indicators_detected = Column(Boolean, default=False)
    details = Column(JSON, default=dict)
    evaluated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztServiceIdentityModel(Base):
    """Isolated Machine-to-Machine service credentials and identities."""
    __tablename__ = "czt_service_identities"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"svcid_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    service_name = Column(String(128), nullable=False, index=True)
    namespace = Column(String(128), default="default")
    allowed_endpoints = Column(JSON, default=list)
    certificate_thumbprint = Column(String(128), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztAgentIdentityModel(Base):
    """Autonomous AI Agent identity and execution permissions."""
    __tablename__ = "czt_agent_identities"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"agtid_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    agent_name = Column(String(256), nullable=False)
    allowed_tools = Column(JSON, default=list)
    data_access_scopes = Column(JSON, default=list)
    max_risk_tolerance = Column(Float, default=0.5)
    requires_human_approval = Column(Boolean, default=True)
    is_sandboxed = Column(Boolean, default=True)
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 4. Zero-Trust Policy & JIT Access
# ----------------------------------------------------------------------
class CztZeroTrustPolicyModel(Base):
    """Zero-Trust ABAC / context access policy."""
    __tablename__ = "czt_policies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"pol_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    effect = Column(String(32), default="ALLOW")  # ALLOW, DENY, REQUIRE_APPROVAL, STEP_UP_AUTHENTICATION, ISOLATE
    target_resource = Column(String(256), nullable=False)
    action_pattern = Column(String(128), default="*")
    conditions = Column(JSON, default=dict)  # device posture, max risk score, allowed IPs, time window
    is_enabled = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztPolicyDecisionModel(Base):
    """Audit log of dynamic Zero-Trust access decisions."""
    __tablename__ = "czt_policy_decisions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"dec_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    subject_id = Column(String(128), nullable=False)
    subject_type = Column(String(64), nullable=False)  # USER, AGENT, SERVICE
    resource = Column(String(256), nullable=False)
    action = Column(String(128), nullable=False)
    decision = Column(String(32), nullable=False)  # ALLOW, DENY, STEP_UP, APPROVAL_PENDING
    eval_reasons = Column(JSON, default=list)
    context_snapshot = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztPrivilegedAccessRequestModel(Base):
    """Just-in-Time (JIT) Privileged Access Requests."""
    __tablename__ = "czt_privileged_access_requests"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"jit_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    requester_id = Column(String(128), nullable=False)
    target_role = Column(String(128), nullable=False)
    justification = Column(Text, nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(String(32), default="PENDING")  # PENDING, APPROVED, REJECTED, EXPIRED, REVOKED
    approved_by = Column(String(128), nullable=True)
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)


# ----------------------------------------------------------------------
# 5. Secrets, Sessions & Certificates
# ----------------------------------------------------------------------
class CztSessionModel(Base):
    """Authenticated user or agent session."""
    __tablename__ = "czt_sessions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"sess_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    identity_id = Column(String(64), nullable=False, index=True)
    device_id = Column(String(64), nullable=True)
    session_token_hash = Column(String(128), nullable=False, unique=True)
    ip_address = Column(String(64), nullable=True)
    user_agent = Column(String(512), nullable=True)
    is_valid = Column(Boolean, default=True)
    requires_step_up = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)


class CztTokenModel(Base):
    """OAuth/API service token tracking."""
    __tablename__ = "czt_tokens"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"tok_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    identity_id = Column(String(64), nullable=False, index=True)
    token_name = Column(String(128), nullable=False)
    token_prefix = Column(String(16), nullable=False)
    hashed_secret = Column(String(128), nullable=False)
    scopes = Column(JSON, default=list)
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)


class CztSecretModel(Base):
    """Vault-referenced secret metadata (Never stores plaintext!)."""
    __tablename__ = "czt_secrets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"sec_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    secret_name = Column(String(256), nullable=False, index=True)
    vault_reference_key = Column(String(256), nullable=False)
    secret_type = Column(String(64), default="API_KEY")  # API_KEY, DB_CREDENTIAL, OAUTH_SECRET, SIGNING_KEY, ENCRYPTION_KEY
    owner = Column(String(128), nullable=False)
    rotation_period_days = Column(Integer, default=90)
    last_rotated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztCertificateModel(Base):
    """X.509 SSL/TLS and mTLS certificate tracking."""
    __tablename__ = "czt_certificates"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"cert_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    domain_name = Column(String(256), nullable=False)
    issuer = Column(String(256), nullable=False)
    thumbprint_sha256 = Column(String(128), nullable=False, unique=True)
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    status = Column(String(32), default="VALID")  # VALID, EXPIRING_SOON, EXPIRED, REVOKED
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 6. SIEM Events, Normalization & Detections
# ----------------------------------------------------------------------
class CztSecurityEventModel(Base):
    """Normalized security telemetry event."""
    __tablename__ = "czt_security_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"event_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source = Column(String(64), nullable=False)  # AUTH, API, DB, CLOUD, AGENT, NETWORK, EDR
    actor_id = Column(String(128), nullable=False, index=True)
    action = Column(String(128), nullable=False, index=True)
    target_resource = Column(String(256), nullable=False)
    status = Column(String(32), default="SUCCESS")  # SUCCESS, FAILURE, BLOCKED, ANOMALOUS
    severity = Column(String(32), default="INFORMATIONAL")  # INFORMATIONAL, LOW, MEDIUM, HIGH, CRITICAL
    ip_address = Column(String(64), nullable=True)
    payload = Column(JSON, default=dict)
    risk_score = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class CztDetectionRuleModel(Base):
    """Configurable detection logic and correlation rule."""
    __tablename__ = "czt_detection_rules"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"drule_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(32), default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    rule_type = Column(String(64), default="THRESHOLD")  # THRESHOLD, PATTERN, SEQUENCE, BEHAVIORAL, ANOMALY, ML
    query_condition = Column(JSON, default=dict)
    window_seconds = Column(Integer, default=300)
    threshold_count = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    mitre_attack_id = Column(String(64), nullable=True)  # T1078, T1110, etc.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztSecurityAlertModel(Base):
    """Security alert generated from detections and correlations."""
    __tablename__ = "czt_alerts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"alert_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    rule_id = Column(String(64), nullable=True, index=True)
    title = Column(String(256), nullable=False)
    severity = Column(String(32), default="HIGH")
    status = Column(String(32), default="OPEN")  # OPEN, INVESTIGATING, ESCALATED, RESOLVED, FALSE_POSITIVE
    actor_id = Column(String(128), nullable=False)
    affected_asset_id = Column(String(64), nullable=True)
    confidence_score = Column(Float, default=0.85)
    evidence = Column(JSON, default=dict)
    contributing_event_ids = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class CztAlertCorrelationModel(Base):
    """Correlated attack sequences linking multiple alerts."""
    __tablename__ = "czt_alert_correlations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"corr_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    correlation_pattern = Column(String(128), nullable=False)
    alert_ids = Column(JSON, default=list)
    composite_risk_score = Column(Float, default=0.9)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 7. Threat Intelligence & Indicators
# ----------------------------------------------------------------------
class CztThreatIndicatorModel(Base):
    """Indicator of Compromise (IoC) record."""
    __tablename__ = "czt_threat_indicators"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"ioc_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    indicator_type = Column(String(32), nullable=False)  # IP, DOMAIN, URL, HASH_SHA256, CERTIFICATE, EMAIL
    value = Column(String(512), nullable=False, index=True)
    threat_actor = Column(String(128), nullable=True)
    campaign = Column(String(128), nullable=True)
    confidence = Column(Float, default=0.8)
    severity = Column(String(32), default="HIGH")
    source_feed = Column(String(128), default="COMMUNITY_FEED")
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(32), default="ACTIVE")  # ACTIVE, DEPRECATED, WHITELISTED


# ----------------------------------------------------------------------
# 8. Vulnerability Management & SBOM
# ----------------------------------------------------------------------
class CztVulnerabilityModel(Base):
    """Tracked CVE and software vulnerability."""
    __tablename__ = "czt_vulnerabilities"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"vuln_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    cve_id = Column(String(64), nullable=False, index=True)  # CVE-2026-1234
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    cvss_score = Column(Float, default=7.5)
    severity = Column(String(32), default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    affected_asset_id = Column(String(64), nullable=False, index=True)
    package_name = Column(String(128), nullable=True)
    fixed_version = Column(String(64), nullable=True)
    exploitability = Column(String(32), default="FUNCTIONAL")  # UNPROVEN, PROOF_OF_CONCEPT, FUNCTIONAL, HIGH
    remediation_status = Column(String(32), default="OPEN")  # OPEN, IN_PROGRESS, RESOLVED, RISK_ACCEPTED
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztSbomComponentModel(Base):
    """Software Bill of Materials dependency component."""
    __tablename__ = "czt_sbom_components"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"sbom_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    application_name = Column(String(128), nullable=False, index=True)
    component_name = Column(String(128), nullable=False)
    version = Column(String(64), nullable=False)
    license = Column(String(64), default="MIT")
    vulnerabilities_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 9. Incident Response & Forensics
# ----------------------------------------------------------------------
class CztSecurityIncidentModel(Base):
    """Security incident container."""
    __tablename__ = "czt_incidents"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"inc_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    severity = Column(String(32), default="HIGH")  # INFORMATIONAL, LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(32), default="TRIAGE")  # DETECT, TRIAGE, INVESTIGATE, CONTAIN, ERADICATE, RECOVER, VERIFY, CLOSED
    assigned_analyst = Column(String(128), nullable=True)
    affected_assets = Column(JSON, default=list)
    impact_summary = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    containment_action = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    resolved_at = Column(DateTime, nullable=True)


class CztIncidentTimelineModel(Base):
    """Chronological event log for incident timeline reconstruction."""
    __tablename__ = "czt_incident_timeline"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"time_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    incident_id = Column(String(64), nullable=False, index=True)
    event_title = Column(String(256), nullable=False)
    event_type = Column(String(64), default="EVIDENCE_DISCOVERY")
    description = Column(Text, nullable=True)
    source = Column(String(64), default="AI_INVESTIGATOR")
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztIncidentEvidenceModel(Base):
    """Digital forensics evidence locker."""
    __tablename__ = "czt_incident_evidence"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"evid_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    incident_id = Column(String(64), nullable=False, index=True)
    evidence_type = Column(String(64), nullable=False)  # LOG_EXTRACT, DISK_SNAPSHOT, PACKET_CAPTURE, HASH, AGENT_TRANSCRIPT
    description = Column(String(512), nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    storage_uri = Column(String(512), nullable=True)
    chain_of_custody = Column(JSON, default=list)
    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 10. Playbooks & Safe Automated Response
# ----------------------------------------------------------------------
class CztPlaybookModel(Base):
    """Security orchestration, automation, and response (SOAR) playbook."""
    __tablename__ = "czt_playbooks"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"pb_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    trigger_type = Column(String(64), default="ALERT")  # ALERT, INCIDENT, MANUAL, SCHEDULED
    steps = Column(JSON, default=list)
    requires_human_signoff = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztPlaybookRunModel(Base):
    """Execution record for security playbook."""
    __tablename__ = "czt_playbook_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"pbrun_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    playbook_id = Column(String(64), nullable=False, index=True)
    incident_id = Column(String(64), nullable=True)
    status = Column(String(32), default="RUNNING")  # RUNNING, COMPLETED, FAILED, AWAITING_APPROVAL
    executed_steps = Column(JSON, default=list)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)


# ----------------------------------------------------------------------
# 11. AI Security & Defense
# ----------------------------------------------------------------------
class CztAiSecurityEventModel(Base):
    """Telemetry for Prompt Injection, Malicious Tool Usage, or Output Leakage."""
    __tablename__ = "czt_ai_security_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"aisec_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    event_category = Column(String(64), nullable=False)  # PROMPT_INJECTION, TOOL_ABUSE, EXFILTRATION, UNSAFE_OUTPUT
    detected_payload = Column(Text, nullable=True)
    risk_level = Column(String(32), default="HIGH")
    action_taken = Column(String(32), default="BLOCKED")  # BLOCKED, SANITIZED, FLAGGED
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 12. Security Graph
# ----------------------------------------------------------------------
class CztSecurityGraphNodeModel(Base):
    """Security Graph Entity node."""
    __tablename__ = "czt_graph_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"gnode_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False)  # USER, DEVICE, APP, SERVICE, DATASET, AGENT, THREAT, VULN, INCIDENT
    entity_name = Column(String(256), nullable=False)
    risk_score = Column(Float, default=0.0)
    attributes = Column(JSON, default=dict)


class CztSecurityGraphEdgeModel(Base):
    """Security Graph Relationship edge."""
    __tablename__ = "czt_graph_edges"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"gedge_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_node_id = Column(String(64), nullable=False, index=True)
    target_node_id = Column(String(64), nullable=False, index=True)
    relationship_type = Column(String(64), nullable=False)  # ACCESSES, AUTHENTICATES, DEPENDS_ON, TARGETS, EXPOSES, CONTAINS, TRIGGERS
    attributes = Column(JSON, default=dict)


# ----------------------------------------------------------------------
# 13. Compliance & Audit
# ----------------------------------------------------------------------
class CztComplianceControlModel(Base):
    """Security compliance controls (SOC2, ISO27001, HIPAA, GDPR)."""
    __tablename__ = "czt_compliance_controls"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"ctrl_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    framework = Column(String(64), nullable=False)  # SOC2, ISO27001, NIST_CSF, GDPR, HIPAA
    control_code = Column(String(64), nullable=False)  # CC6.1, AC-2, etc.
    title = Column(String(256), nullable=False)
    status = Column(String(32), default="COMPLIANT")  # COMPLIANT, DEFICIENT, IN_REVIEW, EXEMPT
    automated_check = Column(Boolean, default=True)
    last_evaluated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CztSecurityAuditEventModel(Base):
    """Immutable security audit record."""
    __tablename__ = "czt_audit_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"sec_aud_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    actor_id = Column(String(128), nullable=False)
    action = Column(String(128), nullable=False)
    resource = Column(String(256), nullable=False)
    decision = Column(String(32), default="ALLOW")
    ip_address = Column(String(64), nullable=True)
    metadata_context = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# Backward-Compatible Convenience Aliases
# ----------------------------------------------------------------------
SecurityAssetModel = CztAssetModel
SecurityIdentityModel = CztIdentityModel
SecurityDeviceModel = CztDeviceModel
SecurityPolicyModel = CztZeroTrustPolicyModel
SecuritySessionModel = CztSessionModel
SecurityIncidentModel = CztSecurityIncidentModel
SecurityAlertModel = CztSecurityAlertModel
SecurityThreatIndicatorModel = CztThreatIndicatorModel
SecurityVulnerabilityModel = CztVulnerabilityModel
SecurityAuditEventModel = CztSecurityAuditEventModel
