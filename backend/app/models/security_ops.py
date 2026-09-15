"""
ORM models for Phase 46 Unified Security Operations, Threat Detection, Security Intelligence, and Automated Defense.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from app.models.base import BaseModel
except ImportError:
    from app.models.base import BaseModel


class SecurityDetectionModel(BaseModel):
    """Normalized security threat detection produced by detection engine."""

    __tablename__ = "security_detections"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    rule_name: Mapped[str] = mapped_column(String(200), nullable=False)
    anomaly_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), default="medium", nullable=False, index=True)
    risk_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    mitre_technique_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    mitre_tactic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_events: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )


class SecurityDetectionRuleModel(BaseModel):
    """Detection rule definitions and dynamic configuration."""

    __tablename__ = "security_detection_rules"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    rule_type: Mapped[str] = mapped_column(String(50), default="DETERMINISTIC", nullable=False)  # DETERMINISTIC, THRESHOLD, VELOCITY, BEHAVIORAL, SEQUENCE
    severity: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    anomaly_type: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    parameters: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)


class SecurityAlertModel(BaseModel):
    """Security alert raised when detection thresholds or correlation criteria are met."""

    __tablename__ = "security_alerts"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    detection_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="medium", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="DETECTED", nullable=False, index=True)
    anomaly_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    mitre_technique_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    mitre_tactic: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    risk_score: Mapped[float] = mapped_column(Float, default=50.0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    affected_actor_id: Mapped[Optional[str]] = mapped_column(String(150), nullable=True, index=True)
    affected_target_id: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)


class SecurityAlertEventModel(BaseModel):
    """Mapping between alerts and underlying security telemetry events."""

    __tablename__ = "security_alert_events"

    alert_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("security_alerts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    security_event_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)


class SecurityIncidentModel(BaseModel):
    """Confirmed or high-priority security incident requiring active response."""

    __tablename__ = "security_incidents"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="high", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="detected", nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), default="INCIDENT", nullable=False, index=True)
    detection_source: Mapped[str] = mapped_column(String(100), default="detection_engine", nullable=False)
    affected_tenants: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_users: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_services: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_resources: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    timeline: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    containment_actions: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    remediation_actions: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    business_impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    security_impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    approvals: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    postmortem: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class SecurityIncidentEventModel(BaseModel):
    """Association of events to a confirmed security incident."""

    __tablename__ = "security_incident_events"

    incident_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    security_event_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)


class SecurityInvestigationModel(BaseModel):
    """Investigation workspace record for incident root-cause analysis."""

    __tablename__ = "security_investigations"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)  # OPEN, IN_PROGRESS, CONCLUDED
    lead_investigator: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    summary: Mapped[str] = mapped_column(Text, default="", nullable=False)
    hypotheses: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    investigation_steps: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    evidence_graph: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class SecurityAttackChainModel(BaseModel):
    """Correlated multi-stage attack chains linking diverse detections."""

    __tablename__ = "security_attack_chains"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("security_incidents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    stages: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    affected_principal: Mapped[Optional[str]] = mapped_column(String(150), nullable=True, index=True)
    supporting_evidence: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    contradicting_evidence: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    recommended_investigation_steps: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)


class SecurityBlastRadiusModel(BaseModel):
    """Blast radius assessment across multi-tenant assets and dependencies."""

    __tablename__ = "security_blast_radius"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=True, index=True
    )
    overall_impact_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    affected_users: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_clients: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_tenants: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_services: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_projects: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_documents: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_financial_records: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_integrations: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_ai_agents: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    affected_workflows: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    narrative_summary: Mapped[str] = mapped_column(Text, default="", nullable=False)


class SecurityRunbookModel(BaseModel):
    """Standard operating procedure runbooks for incident response."""

    __tablename__ = "security_runbooks"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0", nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="INCIDENT_RESPONSE", nullable=False)
    trigger_anomaly: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requires_dual_approval: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    steps: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    rollback_steps: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)


class SecurityRemediationRunModel(BaseModel):
    """Audited execution of a containment or remediation action."""

    __tablename__ = "security_remediation_runs"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("security_incidents.id", ondelete="CASCADE"), nullable=True, index=True
    )
    action_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_id: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending_approval", nullable=False, index=True)
    requested_by: Mapped[str] = mapped_column(String(150), nullable=False)
    approved_by: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    parameters: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    execution_result: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class SecurityThreatIndicatorModel(BaseModel):
    """External or internal threat intelligence indicator of compromise (IOC)."""

    __tablename__ = "security_threat_indicators"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    indicator_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # IP, DOMAIN, URL, HASH, EMAIL, USER_AGENT
    indicator_value: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    threat_category: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="INTERNAL", nullable=False)
    reputation: Mapped[int] = mapped_column(Integer, default=80, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class SecurityBehaviorBaselineModel(BaseModel):
    """Behavioral analytics baseline for anomaly detection."""

    __tablename__ = "security_behavior_baselines"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # USER, AGENT, API_CLIENT, TENANT
    entity_id: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    baseline_mean: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    baseline_stddev: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )


class SecurityPostureSnapshotModel(BaseModel):
    """Snapshot of overall enterprise security posture, risk grade, and SOC metrics."""

    __tablename__ = "security_posture_snapshots"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    posture_grade: Mapped[str] = mapped_column(String(10), default="A", nullable=False)  # A+, A, B, C, D, F
    composite_risk_score: Mapped[float] = mapped_column(Float, default=15.0, nullable=False)
    overall_status: Mapped[str] = mapped_column(String(50), default="HEALTHY", nullable=False)
    open_critical_incidents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    high_risk_alerts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    domain_scores: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class SecurityAIRunModel(BaseModel):
    """Audited AI security copilot execution records and recommendations."""

    __tablename__ = "security_ai_runs"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    run_type: Mapped[str] = mapped_column(String(100), default="INVESTIGATION_SUMMARY", nullable=False)
    query_or_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    response_summary: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.85, nullable=False)
    evidence_sources: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    recommendations: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    prohibited_actions_checked: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    execution_time_ms: Mapped[int] = mapped_column(Integer, default=250, nullable=False)


class SecurityAuditRecordModel(BaseModel):
    """Immutable audit trail specifically for SOC administrative actions."""

    __tablename__ = "security_audit_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    actor_id: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    actor_role: Mapped[str] = mapped_column(String(100), default="SECURITY_OPERATOR", nullable=False)
    target_resource: Mapped[str] = mapped_column(String(200), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )
