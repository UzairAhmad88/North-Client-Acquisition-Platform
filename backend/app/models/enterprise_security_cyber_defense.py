"""
Phase 80: Enterprise Security Operations, Cyber Defense, Identity Intelligence, Threat Detection, Zero-Trust Enforcement & Autonomous Security Response Models.
Zero-collision namespace and extend_existing=True for maximum compatibility with existing tables.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, Base


# --- SECURITY ASSETS & CRITICALITY ---
class SecAssetModel(BaseModel):
    """Enterprise Asset Inventory."""
    __tablename__ = "security_assets"
    __table_args__ = {"extend_existing": True}

    asset_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    asset_type = Column(String(64), nullable=False)  # SERVER, WORKSTATION, CONTAINER, DATABASE, API, CLOUD_RES, AI_AGENT, MODEL
    owner = Column(String(255), nullable=False)
    department = Column(String(128), nullable=False)
    environment = Column(String(32), default="PRODUCTION", nullable=False)
    criticality = Column(String(32), default="HIGH", nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    ip_address = Column(String(64), nullable=True)
    software_version = Column(String(64), nullable=True)
    security_status = Column(String(32), default="PROTECTED", nullable=False)
    risk_score = Column(Float, default=15.0, nullable=False)
    metadata_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAssetVersionModel(BaseModel):
    """Asset configuration versioning."""
    __tablename__ = "security_asset_versions"
    __table_args__ = {"extend_existing": True}

    asset_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    state_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAssetDependencyModel(BaseModel):
    """Asset dependency graph."""
    __tablename__ = "security_asset_dependencies"
    __table_args__ = {"extend_existing": True}

    asset_code = Column(String(128), nullable=False, index=True)
    depends_on_asset = Column(String(128), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAssetCriticalityModel(BaseModel):
    """Asset business impact scoring."""
    __tablename__ = "security_asset_criticality"
    __table_args__ = {"extend_existing": True}

    asset_code = Column(String(128), nullable=False, index=True)
    business_impact = Column(Float, default=85.0, nullable=False)
    data_sensitivity = Column(String(32), default="RESTRICTED", nullable=False)
    availability_req = Column(String(32), default="99.99%", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- EVENTS, LOGS & SIEM ---
class SecEventModel(BaseModel):
    """Normalized security telemetry events."""
    __tablename__ = "security_events"
    __table_args__ = {"extend_existing": True}

    event_id_str = Column(String(128), unique=True, nullable=False, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    source_system = Column(String(128), nullable=False)
    actor_identity = Column(String(255), nullable=False, index=True)
    target_asset = Column(String(128), nullable=True, index=True)
    action = Column(String(128), nullable=False)
    result = Column(String(32), default="SUCCESS", nullable=False)  # SUCCESS, FAILURE, DENIED
    severity = Column(String(32), default="INFORMATIONAL", nullable=False)
    raw_payload = Column(JSON, default=dict, nullable=False)
    enriched_payload = Column(JSON, default=dict, nullable=False)
    event_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecEventSourceModel(BaseModel):
    """Log collector source registrations."""
    __tablename__ = "security_event_sources"
    __table_args__ = {"extend_existing": True}

    source_name = Column(String(128), unique=True, nullable=False, index=True)
    collector_type = Column(String(64), nullable=False)  # SYSLOG, KAFKA, CLOUD_TRAIL, AUTH_LOG, API, AGENT
    status = Column(String(32), default="HEALTHY", nullable=False)
    events_per_sec = Column(Float, default=1250.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecEventEnrichmentModel(BaseModel):
    """Enrichment pipeline rules."""
    __tablename__ = "security_event_enrichment"
    __table_args__ = {"extend_existing": True}

    rule_name = Column(String(128), unique=True, nullable=False, index=True)
    enrichment_type = Column(String(64), nullable=False)  # GEOIP, USER_CONTEXT, ASSET_CRITICALITY, THREAT_INTEL
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecEventRelationshipModel(BaseModel):
    """Cross-event correlation links."""
    __tablename__ = "security_event_relationships"
    __table_args__ = {"extend_existing": True}

    parent_event_id = Column(String(128), nullable=False, index=True)
    child_event_id = Column(String(128), nullable=False, index=True)
    relationship = Column(String(64), nullable=False)  # TRIGGERED, CORRELATED, CAUSAL
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecLogModel(BaseModel):
    """Raw SIEM log records."""
    __tablename__ = "security_logs"
    __table_args__ = {"extend_existing": True}

    log_id_str = Column(String(128), unique=True, nullable=False, index=True)
    source_type = Column(String(64), nullable=False)
    log_line = Column(Text, nullable=False)
    parsed_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecLogSourceModel(BaseModel):
    """Log collector specs."""
    __tablename__ = "security_log_sources"
    __table_args__ = {"extend_existing": True}

    source_code = Column(String(128), unique=True, nullable=False, index=True)
    collector_endpoint = Column(String(255), nullable=False)
    protocol = Column(String(32), default="HTTPS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecLogPipelineModel(BaseModel):
    """SIEM ingestion pipelines."""
    __tablename__ = "security_log_pipelines"
    __table_args__ = {"extend_existing": True}

    pipeline_code = Column(String(128), unique=True, nullable=False, index=True)
    status = Column(String(32), default="RUNNING", nullable=False)
    bytes_per_sec = Column(Integer, default=5242880, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- IDENTITY, PAM & ZERO TRUST ---
class SecIdentityModel(BaseModel):
    """Identity Inventory."""
    __tablename__ = "security_identities"
    __table_args__ = {"extend_existing": True}

    identity_code = Column(String(128), unique=True, nullable=False, index=True)
    user_email = Column(String(255), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    department = Column(String(128), nullable=False)
    role = Column(String(64), nullable=False)
    risk_score = Column(Float, default=12.5, nullable=False)
    mfa_enabled = Column(Boolean, default=True, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAccountModel(BaseModel):
    """Associated target system accounts."""
    __tablename__ = "security_accounts"
    __table_args__ = {"extend_existing": True}

    account_code = Column(String(128), unique=True, nullable=False, index=True)
    identity_code = Column(String(128), nullable=False, index=True)
    target_system = Column(String(128), nullable=False)
    account_type = Column(String(64), default="STANDARD", nullable=False)  # STANDARD, PRIVILEGED, SERVICE, BREAK_GLASS
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecRoleModel(BaseModel):
    """Security roles definition."""
    __tablename__ = "security_roles"
    __table_args__ = {"extend_existing": True}

    role_code = Column(String(64), unique=True, nullable=False, index=True)
    role_name = Column(String(128), nullable=False)
    permissions_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecPermissionModel(BaseModel):
    """Granular permissions registry."""
    __tablename__ = "security_permissions"
    __table_args__ = {"extend_existing": True}

    permission_code = Column(String(128), unique=True, nullable=False, index=True)
    resource = Column(String(128), nullable=False)
    action = Column(String(64), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecSessionModel(BaseModel):
    """Active user sessions tracking."""
    __tablename__ = "security_sessions"
    __table_args__ = {"extend_existing": True}

    session_id_str = Column(String(128), unique=True, nullable=False, index=True)
    identity_code = Column(String(128), nullable=False, index=True)
    ip_address = Column(String(64), nullable=False)
    device_id = Column(String(128), nullable=False)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    risk_score = Column(Float, default=10.0, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecPrivilegedAccessModel(BaseModel):
    """Privileged Access Management (PAM) & JIT requests."""
    __tablename__ = "security_privileged_access"
    __table_args__ = {"extend_existing": True}

    pam_code = Column(String(128), unique=True, nullable=False, index=True)
    identity_code = Column(String(128), nullable=False, index=True)
    target_resource = Column(String(128), nullable=False)
    requested_duration_mins = Column(Integer, default=60, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(32), default="APPROVED", nullable=False)  # PENDING, APPROVED, EXPIRED, REVOKED
    approved_by = Column(String(255), nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAccessRequestModel(BaseModel):
    """Access requests tracking."""
    __tablename__ = "security_access_requests"
    __table_args__ = {"extend_existing": True}

    request_code = Column(String(64), unique=True, nullable=False, index=True)
    identity_code = Column(String(128), nullable=False, index=True)
    resource = Column(String(128), nullable=False)
    status = Column(String(32), default="PENDING", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecZeroTrustPolicyModel(BaseModel):
    """Zero Trust Policy Rules."""
    __tablename__ = "security_zero_trust_policies"
    __table_args__ = {"extend_existing": True}

    policy_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    conditions_json = Column(JSON, default=dict, nullable=False)
    action = Column(String(32), default="ALLOW_WITH_MFA", nullable=False)  # ALLOW, DENY, STEP_UP, LIMITED, HUMAN_APPROVAL
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAccessDecisionModel(BaseModel):
    """Evaluated zero trust access decision log."""
    __tablename__ = "security_access_decisions"
    __table_args__ = {"extend_existing": True}

    decision_code = Column(String(128), unique=True, nullable=False, index=True)
    identity_code = Column(String(128), nullable=False, index=True)
    resource = Column(String(128), nullable=False)
    decision = Column(String(32), nullable=False)  # ALLOWED, DENIED, STEP_UP_REQUIRED
    risk_score = Column(Float, nullable=False)
    evaluated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDeviceTrustModel(BaseModel):
    """Device posture and trust state."""
    __tablename__ = "security_device_trust"
    __table_args__ = {"extend_existing": True}

    device_id = Column(String(128), unique=True, nullable=False, index=True)
    owner_email = Column(String(255), nullable=False)
    is_managed = Column(Boolean, default=True, nullable=False)
    is_compliant = Column(Boolean, default=True, nullable=False)
    disk_encrypted = Column(Boolean, default=True, nullable=False)
    trust_score = Column(Float, default=95.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- DETECTIONS & THREAT INTEL ---
class SecDetectionModel(BaseModel):
    """Threat detection rule outputs."""
    __tablename__ = "security_detections"
    __table_args__ = {"extend_existing": True}

    rule_id_str = Column(String(128), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    severity = Column(String(32), default="HIGH", nullable=False)
    mitre_tactic = Column(String(64), default="INITIAL_ACCESS", nullable=False)
    mitre_technique = Column(String(64), default="T1078", nullable=False)
    confidence = Column(Float, default=0.90, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    evidence_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDetectionVersionModel(BaseModel):
    """Detection rule versions."""
    __tablename__ = "security_detection_versions"
    __table_args__ = {"extend_existing": True}

    rule_id_str = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    logic_code = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDetectionTestModel(BaseModel):
    """Detection rule unit test cases."""
    __tablename__ = "security_detection_tests"
    __table_args__ = {"extend_existing": True}

    test_code = Column(String(128), unique=True, nullable=False, index=True)
    rule_id_str = Column(String(128), nullable=False, index=True)
    passed = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDetectionCoverageModel(BaseModel):
    """MITRE ATT&CK coverage tracking."""
    __tablename__ = "security_detection_coverage"
    __table_args__ = {"extend_existing": True}

    technique_id = Column(String(64), primary_key=True)
    technique_name = Column(String(255), nullable=False)
    coverage_pct = Column(Float, default=85.0, nullable=False)
    rule_count = Column(Integer, default=4, nullable=False)


class SecThreatModel(BaseModel):
    """Threat Actors and Campaigns."""
    __tablename__ = "security_threats"
    __table_args__ = {"extend_existing": True}

    threat_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    threat_actor = Column(String(128), nullable=False)
    confidence = Column(Float, default=0.85, nullable=False)
    description = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIndicatorModel(BaseModel):
    """Indicators of Compromise (IOCs)."""
    __tablename__ = "security_indicators"
    __table_args__ = {"extend_existing": True}

    indicator_code = Column(String(128), unique=True, nullable=False, index=True)
    indicator_type = Column(String(32), nullable=False)  # IP, DOMAIN, HASH, URL, EMAIL
    indicator_value = Column(String(255), nullable=False, index=True)
    confidence = Column(Float, default=0.92, nullable=False)
    source = Column(String(128), nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIndicatorSourceModel(BaseModel):
    """Threat intel feed source."""
    __tablename__ = "security_indicator_sources"
    __table_args__ = {"extend_existing": True}

    source_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    reliability = Column(Float, default=95.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecThreatCampaignModel(BaseModel):
    """Threat Campaign tracking."""
    __tablename__ = "security_threat_campaigns"
    __table_args__ = {"extend_existing": True}

    campaign_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    target_sector = Column(String(128), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecTechniqueModel(BaseModel):
    """MITRE ATT&CK technique catalog."""
    __tablename__ = "security_techniques"
    __table_args__ = {"extend_existing": True}

    technique_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    tactic = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)


# --- ALERTS, INCIDENTS & EVIDENCE ---
class SecAlertModel(BaseModel):
    """Prioritized security alerts."""
    __tablename__ = "security_alerts"
    __table_args__ = {"extend_existing": True}

    alert_code = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    severity = Column(String(32), default="HIGH", nullable=False)
    confidence = Column(Float, default=0.88, nullable=False)
    asset_code = Column(String(128), nullable=True, index=True)
    identity_code = Column(String(128), nullable=True, index=True)
    status = Column(String(32), default="NEW", nullable=False)  # NEW, INVESTIGATING, GROUPED, RESOLVED
    evidence_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAlertGroupModel(BaseModel):
    """Deduplicated alert groups."""
    __tablename__ = "security_alert_groups"
    __table_args__ = {"extend_existing": True}

    group_code = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    alert_count = Column(Integer, default=1, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIncidentModel(BaseModel):
    """Security Incident Cases."""
    __tablename__ = "security_incidents"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    severity = Column(String(32), default="CRITICAL", nullable=False)
    confidence = Column(Float, default=0.95, nullable=False)
    owner = Column(String(255), nullable=False)
    status = Column(String(32), default="TRIAGED", nullable=False)  # TRIAGED, INVESTIGATING, CONTAINED, RESOLVED
    lead_analyst = Column(String(255), nullable=True)
    root_cause = Column(Text, nullable=True)
    summary = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIncidentEventModel(BaseModel):
    """Events tied to incident timeline."""
    __tablename__ = "security_incident_events"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), nullable=False, index=True)
    event_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    description = Column(Text, nullable=False)
    actor = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIncidentEntityModel(BaseModel):
    """Affected users, devices, IPs tied to incident."""
    __tablename__ = "security_incident_entities"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False)  # USER, DEVICE, IP, APPLICATION
    entity_value = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIncidentEvidenceModel(BaseModel):
    """Tamper-evident forensic artifacts for incidents."""
    __tablename__ = "security_incident_evidence"
    __table_args__ = {"extend_existing": True}

    evidence_code = Column(String(128), unique=True, nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    artifact_name = Column(String(255), nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    content_type = Column(String(64), nullable=False)
    custody_notes = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIncidentActionModel(BaseModel):
    """Containment and response actions taken."""
    __tablename__ = "security_incident_actions"
    __table_args__ = {"extend_existing": True}

    action_code = Column(String(128), unique=True, nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    action_type = Column(String(64), nullable=False)  # REVOKE_SESSION, DISABLE_ACCOUNT, QUARANTINE_ENDPOINT, BLOCK_IP
    target = Column(String(255), nullable=False)
    status = Column(String(32), default="EXECUTED", nullable=False)
    executed_by = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecIncidentApprovalModel(BaseModel):
    """Human approvals for high-impact actions."""
    __tablename__ = "security_incident_approvals"
    __table_args__ = {"extend_existing": True}

    approval_code = Column(String(128), unique=True, nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    requested_action = Column(String(64), nullable=False)
    approved_by = Column(String(255), nullable=False)
    status = Column(String(32), default="APPROVED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- SOAR PLAYBOOKS & RESPONSE ROLLBACK ---
class SecPlaybookModel(BaseModel):
    """SOAR Automated Response Playbooks."""
    __tablename__ = "security_playbooks"
    __table_args__ = {"extend_existing": True}

    playbook_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    trigger_condition = Column(String(255), nullable=False)
    autonomy_level_req = Column(String(16), default="L3", nullable=False)  # L0 to L5
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecPlaybookVersionModel(BaseModel):
    """Playbook logic versions."""
    __tablename__ = "security_playbook_versions"
    __table_args__ = {"extend_existing": True}

    playbook_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    steps_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecPlaybookRunModel(BaseModel):
    """Playbook execution runs."""
    __tablename__ = "security_playbook_runs"
    __table_args__ = {"extend_existing": True}

    run_code = Column(String(128), unique=True, nullable=False, index=True)
    playbook_code = Column(String(128), nullable=False, index=True)
    status = Column(String(32), default="COMPLETED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecPlaybookStepModel(BaseModel):
    """Individual playbook execution step."""
    __tablename__ = "security_playbook_steps"
    __table_args__ = {"extend_existing": True}

    run_code = Column(String(128), nullable=False, index=True)
    step_number = Column(Integer, nullable=False)
    step_name = Column(String(128), nullable=False)
    status = Column(String(32), default="SUCCESS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecResponseActionModel(BaseModel):
    """Response action log."""
    __tablename__ = "security_response_actions"
    __table_args__ = {"extend_existing": True}

    action_id_str = Column(String(128), unique=True, nullable=False, index=True)
    action_type = Column(String(64), nullable=False)
    target = Column(String(255), nullable=False)
    risk_level = Column(String(32), default="MEDIUM", nullable=False)
    status = Column(String(32), default="EXECUTED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecResponseApprovalModel(BaseModel):
    """Approval records for response actions."""
    __tablename__ = "security_response_approvals"
    __table_args__ = {"extend_existing": True}

    action_id_str = Column(String(128), nullable=False, index=True)
    approved_by = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecResponseRollbackModel(BaseModel):
    """Reversible action state tracking for rollbacks."""
    __tablename__ = "security_response_rollbacks"
    __table_args__ = {"extend_existing": True}

    action_id_str = Column(String(128), unique=True, nullable=False, index=True)
    previous_state = Column(JSON, default=dict, nullable=False)
    new_state = Column(JSON, default=dict, nullable=False)
    status = Column(String(32), default="READY", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- VULNERABILITIES & CONFIGURATION ---
class SecVulnerabilityModel(BaseModel):
    """Vulnerability management tracking."""
    __tablename__ = "security_vulnerabilities"
    __table_args__ = {"extend_existing": True}

    cve_id = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    cvss_score = Column(Float, default=8.5, nullable=False)
    exploitability = Column(String(32), default="HIGH", nullable=False)
    affected_asset_count = Column(Integer, default=12, nullable=False)
    status = Column(String(32), default="OPEN", nullable=False)
    remediation_sla_days = Column(Integer, default=7, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecVulnerabilityAssetModel(BaseModel):
    """Affected asset mapping to vulnerabilities."""
    __tablename__ = "security_vulnerability_assets"
    __table_args__ = {"extend_existing": True}

    cve_id = Column(String(64), nullable=False, index=True)
    asset_code = Column(String(128), nullable=False, index=True)
    status = Column(String(32), default="OPEN", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecRemediationModel(BaseModel):
    """Remediation tracking for vulnerabilities."""
    __tablename__ = "security_remediations"
    __table_args__ = {"extend_existing": True}

    rem_code = Column(String(128), unique=True, nullable=False, index=True)
    cve_id = Column(String(64), nullable=False, index=True)
    patch_version = Column(String(64), nullable=False)
    owner = Column(String(255), nullable=False)
    status = Column(String(32), default="SCHEDULED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecPatchModel(BaseModel):
    """Software patch catalog."""
    __tablename__ = "security_patches"
    __table_args__ = {"extend_existing": True}

    patch_code = Column(String(128), unique=True, nullable=False, index=True)
    vendor = Column(String(128), nullable=False)
    patch_name = Column(String(255), nullable=False)
    severity = Column(String(32), default="CRITICAL", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecConfigurationModel(BaseModel):
    """Security Configuration Baselines."""
    __tablename__ = "security_configurations"
    __table_args__ = {"extend_existing": True}

    config_code = Column(String(128), unique=True, nullable=False, index=True)
    asset_code = Column(String(128), nullable=False, index=True)
    baseline_version = Column(String(32), default="1.0.0", nullable=False)
    status = Column(String(32), default="COMPLIANT", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecConfigurationBaselineModel(BaseModel):
    """Approved baseline rules."""
    __tablename__ = "security_configuration_baselines"
    __table_args__ = {"extend_existing": True}

    baseline_code = Column(String(128), unique=True, nullable=False, index=True)
    target_platform = Column(String(64), nullable=False)  # OS, CLOUD, KUBERNETES, DATABASE
    rules_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecConfigurationDriftModel(BaseModel):
    """Detected configuration drift events."""
    __tablename__ = "security_configuration_drift"
    __table_args__ = {"extend_existing": True}

    drift_code = Column(String(128), unique=True, nullable=False, index=True)
    asset_code = Column(String(128), nullable=False, index=True)
    parameter_changed = Column(String(128), nullable=False)
    expected_value = Column(String(255), nullable=False)
    actual_value = Column(String(255), nullable=False)
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- CLOUD, APPLICATION, NETWORK & AI SECURITY ---
class SecCloudAccountModel(BaseModel):
    """Cloud Account posture."""
    __tablename__ = "security_cloud_accounts"
    __table_args__ = {"extend_existing": True}

    cloud_account_id = Column(String(128), unique=True, nullable=False, index=True)
    provider = Column(String(32), nullable=False)  # AWS, GCP, AZURE
    name = Column(String(255), nullable=False)
    risk_score = Column(Float, default=18.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecCloudResourceModel(BaseModel):
    """Cloud resource registry."""
    __tablename__ = "security_cloud_resources"
    __table_args__ = {"extend_existing": True}

    resource_arn = Column(String(255), unique=True, nullable=False, index=True)
    cloud_account_id = Column(String(128), nullable=False, index=True)
    resource_type = Column(String(64), nullable=False)
    publicly_accessible = Column(Boolean, default=False, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecCloudFindingModel(BaseModel):
    """Cloud misconfiguration findings."""
    __tablename__ = "security_cloud_findings"
    __table_args__ = {"extend_existing": True}

    finding_code = Column(String(128), unique=True, nullable=False, index=True)
    resource_arn = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    severity = Column(String(32), default="HIGH", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecApplicationModel(BaseModel):
    """Application Security registry."""
    __tablename__ = "security_applications"
    __table_args__ = {"extend_existing": True}

    app_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    repository_url = Column(String(255), nullable=False)
    sast_status = Column(String(32), default="PASSING", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecApplicationFindingModel(BaseModel):
    """SAST/DAST vulnerabilities."""
    __tablename__ = "security_application_findings"
    __table_args__ = {"extend_existing": True}

    finding_code = Column(String(128), unique=True, nullable=False, index=True)
    app_code = Column(String(128), nullable=False, index=True)
    vulnerability_type = Column(String(128), nullable=False)  # SQL_INJECTION, XSS, SECRET_LEAK, DEPENDENCY
    file_path = Column(String(255), nullable=False)
    line_number = Column(Integer, nullable=True)
    severity = Column(String(32), default="HIGH", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDependencyModel(BaseModel):
    """Software supply chain dependencies."""
    __tablename__ = "security_dependencies"
    __table_args__ = {"extend_existing": True}

    dep_code = Column(String(128), unique=True, nullable=False, index=True)
    package_name = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    cve_id = Column(String(64), nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecSecretModel(BaseModel):
    """Secret metadata registry (No plaintext secrets stored!)."""
    __tablename__ = "security_secrets"
    __table_args__ = {"extend_existing": True}

    secret_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    secret_type = Column(String(64), nullable=False)  # API_KEY, OAUTH_TOKEN, CERT, DB_CRED
    owner = Column(String(255), nullable=False)
    rotation_days = Column(Integer, default=90, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecCertificateModel(BaseModel):
    """TLS Certificate monitoring."""
    __tablename__ = "security_certificates"
    __table_args__ = {"extend_existing": True}

    cert_code = Column(String(128), unique=True, nullable=False, index=True)
    domain_name = Column(String(255), nullable=False, index=True)
    issuer = Column(String(255), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecNetworkEventModel(BaseModel):
    """Network connection events."""
    __tablename__ = "security_network_events"
    __table_args__ = {"extend_existing": True}

    net_event_id = Column(String(128), unique=True, nullable=False, index=True)
    src_ip = Column(String(64), nullable=False, index=True)
    dest_ip = Column(String(64), nullable=False, index=True)
    port = Column(Integer, nullable=False)
    bytes_transferred = Column(Integer, default=0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDnsEventModel(BaseModel):
    """DNS Query security events."""
    __tablename__ = "security_dns_events"
    __table_args__ = {"extend_existing": True}

    dns_event_id = Column(String(128), unique=True, nullable=False, index=True)
    query_domain = Column(String(255), nullable=False, index=True)
    resolved_ip = Column(String(64), nullable=True)
    is_suspicious = Column(Boolean, default=False, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecEmailEventModel(BaseModel):
    """Email telemetry signals."""
    __tablename__ = "security_email_events"
    __table_args__ = {"extend_existing": True}

    email_event_id = Column(String(128), unique=True, nullable=False, index=True)
    sender = Column(String(255), nullable=False, index=True)
    recipient = Column(String(255), nullable=False)
    phishing_score = Column(Float, default=0.05, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDataAccessModel(BaseModel):
    """Sensitive data access telemetry."""
    __tablename__ = "security_data_access"
    __table_args__ = {"extend_existing": True}

    access_event_id = Column(String(128), unique=True, nullable=False, index=True)
    dataset_code = Column(String(128), nullable=False, index=True)
    actor_email = Column(String(255), nullable=False, index=True)
    rows_accessed = Column(Integer, default=1, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDataExportModel(BaseModel):
    """Data export events for exfiltration detection."""
    __tablename__ = "security_data_exports"
    __table_args__ = {"extend_existing": True}

    export_event_id = Column(String(128), unique=True, nullable=False, index=True)
    actor_email = Column(String(255), nullable=False, index=True)
    export_bytes = Column(Integer, default=0, nullable=False)
    destination = Column(String(255), nullable=False)
    risk_score = Column(Float, default=20.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecDataSecurityEventModel(BaseModel):
    """DLP / Exfiltration security events."""
    __tablename__ = "security_data_security_events"
    __table_args__ = {"extend_existing": True}

    sec_event_id = Column(String(128), unique=True, nullable=False, index=True)
    event_type = Column(String(64), nullable=False)  # BULK_DOWNLOAD, EXPORT_TO_UNTRUSTED, ANOMALOUS_ACCESS
    severity = Column(String(32), default="HIGH", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAiEventModel(BaseModel):
    """Phase 76 AI Agent Security telemetry events."""
    __tablename__ = "security_ai_events"
    __table_args__ = {"extend_existing": True}

    ai_event_id = Column(String(128), unique=True, nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    tool_name = Column(String(128), nullable=False)
    prompt_injection_detected = Column(Boolean, default=False, nullable=False)
    status = Column(String(32), default="ALLOWED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAgentPermissionModel(BaseModel):
    """AI Agent tool permission boundaries."""
    __tablename__ = "security_agent_permissions"
    __table_args__ = {"extend_existing": True}

    agent_id = Column(String(128), nullable=False, index=True)
    allowed_tool = Column(String(128), nullable=False)
    max_autonomy = Column(String(16), default="L3", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAgentActionModel(BaseModel):
    """Agent tool action execution audit log."""
    __tablename__ = "security_agent_actions"
    __table_args__ = {"extend_existing": True}

    action_id_str = Column(String(128), unique=True, nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    tool_name = Column(String(128), nullable=False)
    autonomy_level = Column(String(16), nullable=False)
    approved_by = Column(String(255), nullable=True)
    status = Column(String(32), default="SUCCESS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAgentSecurityEventModel(BaseModel):
    """Agent policy violation events."""
    __tablename__ = "security_agent_security_events"
    __table_args__ = {"extend_existing": True}

    violation_id = Column(String(128), unique=True, nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    violation_type = Column(String(64), nullable=False)  # PROMPT_INJECTION, PERMISSION_EXCEEDED, HIGH_RISK_BLOCKED
    severity = Column(String(32), default="HIGH", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- FORENSICS & THREAT HUNTING ---
class SecForensicsCaseModel(BaseModel):
    """Digital Forensics Case records."""
    __tablename__ = "security_forensics_cases"
    __table_args__ = {"extend_existing": True}

    case_code = Column(String(64), unique=True, nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    lead_investigator = Column(String(255), nullable=False)
    status = Column(String(32), default="OPEN", nullable=False)
    findings_summary = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecForensicArtifactModel(BaseModel):
    """Forensic memory/disk/log artifacts."""
    __tablename__ = "security_forensic_artifacts"
    __table_args__ = {"extend_existing": True}

    artifact_code = Column(String(128), unique=True, nullable=False, index=True)
    case_code = Column(String(64), nullable=False, index=True)
    artifact_type = Column(String(64), nullable=False)  # MEMORY_DUMP, PCAP, DISK_IMAGE, LOG_EXTRACT
    file_path = Column(String(255), nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecForensicEvidenceModel(BaseModel):
    """Evidence custody records."""
    __tablename__ = "security_forensic_evidence"
    __table_args__ = {"extend_existing": True}

    evidence_id_str = Column(String(128), unique=True, nullable=False, index=True)
    case_code = Column(String(64), nullable=False, index=True)
    description = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecHuntModel(BaseModel):
    """Threat Hunting Workspaces."""
    __tablename__ = "security_hunts"
    __table_args__ = {"extend_existing": True}

    hunt_code = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=False)
    hunter = Column(String(255), nullable=False)
    status = Column(String(32), default="CONCLUDED", nullable=False)
    findings_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecHuntQueryModel(BaseModel):
    """Threat hunting queries."""
    __tablename__ = "security_hunt_queries"
    __table_args__ = {"extend_existing": True}

    query_code = Column(String(128), unique=True, nullable=False, index=True)
    hunt_code = Column(String(128), nullable=False, index=True)
    query_text = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecHuntFindingModel(BaseModel):
    """Discoveries made during hunting."""
    __tablename__ = "security_hunt_findings"
    __table_args__ = {"extend_existing": True}

    finding_code = Column(String(128), unique=True, nullable=False, index=True)
    hunt_code = Column(String(128), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- RISK, CONTROLS & AUDIT ---
class SecRiskScoreModel(BaseModel):
    """Security Risk Scores."""
    __tablename__ = "security_risk_scores"
    __table_args__ = {"extend_existing": True}

    entity_code = Column(String(128), unique=True, nullable=False, index=True)
    entity_type = Column(String(64), nullable=False)  # ASSET, IDENTITY, DEPARTMENT, ENTERPRISE
    risk_score = Column(Float, default=24.5, nullable=False)
    trend = Column(String(16), default="STABLE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecRiskFactorModel(BaseModel):
    """Factors contributing to risk score."""
    __tablename__ = "security_risk_factors"
    __table_args__ = {"extend_existing": True}

    entity_code = Column(String(128), nullable=False, index=True)
    factor_name = Column(String(128), nullable=False)
    impact_score = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAttackPathModel(BaseModel):
    """Attack path modeling links."""
    __tablename__ = "security_attack_paths"
    __table_args__ = {"extend_existing": True}

    path_code = Column(String(128), unique=True, nullable=False, index=True)
    start_node = Column(String(128), nullable=False)
    target_node = Column(String(128), nullable=False)
    hops_json = Column(JSON, default=list, nullable=False)
    risk_score = Column(Float, default=78.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecControlModel(BaseModel):
    """Security Controls Framework."""
    __tablename__ = "security_controls"
    __table_args__ = {"extend_existing": True}

    control_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False)  # IAM, ZERO_TRUST, SIEM, ENDPOINT, ENCRYPTION
    effectiveness = Column(Float, default=96.5, nullable=False)
    status = Column(String(32), default="EFFECTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecControlMappingModel(BaseModel):
    """Controls mapped to compliance frameworks (NIST, CIS, ISO27001)."""
    __tablename__ = "security_control_mappings"
    __table_args__ = {"extend_existing": True}

    control_code = Column(String(64), nullable=False, index=True)
    framework = Column(String(64), nullable=False)  # NIST_CSF, CIS_CONTROLS, ISO27001, SOC2
    requirement_id = Column(String(64), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecControlTestModel(BaseModel):
    """Automated security control tests."""
    __tablename__ = "security_control_tests"
    __table_args__ = {"extend_existing": True}

    test_code = Column(String(128), unique=True, nullable=False, index=True)
    control_code = Column(String(64), nullable=False, index=True)
    passed = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecControlEffectivenessModel(BaseModel):
    """Control performance metrics."""
    __tablename__ = "security_control_effectiveness"
    __table_args__ = {"extend_existing": True}

    control_code = Column(String(64), nullable=False, index=True)
    pass_rate = Column(Float, default=99.2, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecMetricModel(BaseModel):
    """SOC operational metrics (MTTD, MTTR)."""
    __tablename__ = "security_metrics"
    __table_args__ = {"extend_existing": True}

    metric_name = Column(String(64), primary_key=True)
    metric_value = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAlertRuleModel(BaseModel):
    """Alert threshold rules."""
    __tablename__ = "security_alert_rules"
    __table_args__ = {"extend_existing": True}

    rule_name = Column(String(128), unique=True, nullable=False, index=True)
    condition = Column(String(255), nullable=False)
    severity = Column(String(32), default="HIGH", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecNotificationModel(BaseModel):
    """SOC Notification log."""
    __tablename__ = "security_notifications"
    __table_args__ = {"extend_existing": True}

    notif_id = Column(String(128), unique=True, nullable=False, index=True)
    channel = Column(String(32), default="PAGER_DUTY", nullable=False)
    recipient = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecEscalationModel(BaseModel):
    """Incident escalation tree."""
    __tablename__ = "security_escalations"
    __table_args__ = {"extend_existing": True}

    escalation_code = Column(String(128), unique=True, nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    escalated_to = Column(String(255), nullable=False)  # CISO, EXECUTIVE, SECURITY_LEAD
    reason = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecAuditEventModel(BaseModel):
    """Tamper-evident security audit log."""
    __tablename__ = "security_audit_events"
    __table_args__ = {"extend_existing": True}

    audit_code = Column(String(128), unique=True, nullable=False, index=True)
    actor_email = Column(String(255), nullable=False, index=True)
    action = Column(String(128), nullable=False)
    target_resource = Column(String(255), nullable=False)
    payload_sha256 = Column(String(64), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class SecTamperEventModel(BaseModel):
    """Log tamper detection alerts."""
    __tablename__ = "security_tamper_events"
    __table_args__ = {"extend_existing": True}

    tamper_code = Column(String(128), unique=True, nullable=False, index=True)
    target_log_id = Column(String(128), nullable=False)
    tamper_type = Column(String(64), nullable=False)  # HASH_MISMATCH, SEQUENCE_GAP, UNEXPLAINED_DELETION
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)
