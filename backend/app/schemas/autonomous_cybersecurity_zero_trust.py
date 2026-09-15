"""
Pydantic Schemas for Phase 66 — Autonomous Cybersecurity, Zero-Trust Security Operations & AI Defense Platform.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# 1. Assets
class AssetCreate(BaseModel):
    name: str
    asset_type: str
    owner: str
    environment: str = "PRODUCTION"
    criticality: str = "HIGH"
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    location: str = "us-east-1"
    tags: List[str] = Field(default_factory=list)
    metadata_context: Dict[str, Any] = Field(default_factory=dict)


class AssetResponse(AssetCreate):
    id: str
    tenant_id: str
    security_state: str = "SECURE"
    risk_score: float = 0.1
    created_at: Optional[datetime] = None


# 2. Zero-Trust Access Evaluation
class ZeroTrustAccessRequest(BaseModel):
    subject_id: str
    subject_type: str = "USER"  # USER, AGENT, SERVICE
    resource: str
    action: str = "READ"
    ip_address: Optional[str] = None
    device_id: Optional[str] = None
    context_data: Dict[str, Any] = Field(default_factory=dict)


class ZeroTrustAccessDecision(BaseModel):
    decision: str  # ALLOW, DENY, REQUIRE_APPROVAL, STEP_UP_AUTHENTICATION, ISOLATE
    subject_id: str
    resource: str
    action: str
    risk_score: float
    reasons: List[str] = Field(default_factory=list)
    evaluated_at: datetime


# 3. Privileged Access Management (JIT)
class PrivilegedAccessRequestCreate(BaseModel):
    requester_id: str
    target_role: str
    justification: str
    duration_minutes: int = 60


class PrivilegedAccessResponse(BaseModel):
    id: str
    tenant_id: str
    requester_id: str
    target_role: str
    justification: str
    status: str
    approved_by: Optional[str] = None
    expires_at: Optional[datetime] = None


# 4. Secrets & Certificates
class SecretCreate(BaseModel):
    secret_name: str
    vault_reference_key: str
    secret_type: str = "API_KEY"
    owner: str
    rotation_period_days: int = 90


class SecretResponse(BaseModel):
    id: str
    tenant_id: str
    secret_name: str
    secret_type: str
    owner: str
    status: str
    last_rotated_at: Optional[datetime] = None


class CertificateResponse(BaseModel):
    id: str
    domain_name: str
    issuer: str
    thumbprint_sha256: str
    valid_until: datetime
    status: str
    days_to_expiration: int


# 5. Security Telemetry & SIEM Detections
class SecurityEventIngest(BaseModel):
    source: str
    actor_id: str
    action: str
    target_resource: str
    status: str = "SUCCESS"
    severity: str = "INFORMATIONAL"
    ip_address: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


class DetectionRuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    severity: str = "HIGH"
    rule_type: str = "THRESHOLD"
    query_condition: Dict[str, Any] = Field(default_factory=dict)
    window_seconds: int = 300
    threshold_count: int = 5
    mitre_attack_id: Optional[str] = None


class SecurityAlertResponse(BaseModel):
    id: str
    title: str
    severity: str
    status: str
    actor_id: str
    affected_asset_id: Optional[str] = None
    confidence_score: float
    evidence: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None


# 6. Threat Intelligence
class ThreatIndicatorCreate(BaseModel):
    indicator_type: str  # IP, DOMAIN, URL, HASH_SHA256
    value: str
    threat_actor: Optional[str] = None
    confidence: float = 0.8
    severity: str = "HIGH"
    source_feed: str = "COMMUNITY_FEED"


# 7. Vulnerabilities & SBOM
class VulnerabilityResponse(BaseModel):
    id: str
    cve_id: str
    title: str
    cvss_score: float
    severity: str
    affected_asset_id: str
    remediation_status: str


class SbomScanRequest(BaseModel):
    application_name: str
    packages: List[Dict[str, str]] = Field(default_factory=list)


# 8. Incident Response & Forensics
class IncidentCreate(BaseModel):
    title: str
    severity: str = "HIGH"
    assigned_analyst: Optional[str] = None
    affected_assets: List[str] = Field(default_factory=list)
    impact_summary: Optional[str] = None


class IncidentResponse(IncidentCreate):
    id: str
    status: str
    created_at: Optional[datetime] = None


class IncidentEvidenceCreate(BaseModel):
    evidence_type: str
    description: str
    sha256_hash: str
    storage_uri: Optional[str] = None


# 9. AI Security & Defense
class AiPromptSecurityCheck(BaseModel):
    agent_id: str
    prompt_text: str
    user_context: Dict[str, Any] = Field(default_factory=dict)


class AiPromptSecurityResponse(BaseModel):
    is_safe: bool
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    detected_threats: List[str] = Field(default_factory=list)
    sanitized_prompt: Optional[str] = None
    action: str  # ALLOW, SANITIZE, BLOCK


class AgentToolValidationRequest(BaseModel):
    agent_id: str
    tool_name: str
    tool_arguments: Dict[str, Any] = Field(default_factory=dict)
    target_data_scope: Optional[str] = None


class AgentToolValidationResponse(BaseModel):
    is_allowed: bool
    requires_human_approval: bool
    risk_score: float
    reason: str


# 10. Security Graph Query
class SecurityGraphQuery(BaseModel):
    query_type: str  # BLAST_RADIUS, EXPOSURE_PATH, ACCESS_PATH, VULN_DEPENDENCY
    entity_id: str
    max_hops: int = 3


# 11. Defense Loop Execution
class DefenseLoopRequest(BaseModel):
    trigger_source: str = "SCHEDULED_SWEEP"
    asset_id: Optional[str] = None
    incident_id: Optional[str] = None


class DefenseLoopResponse(BaseModel):
    status: str
    loop_cycle_id: str
    phases_executed: List[str] = Field(default_factory=list)
    findings_count: int
    containment_actions_taken: List[str] = Field(default_factory=list)
    executed_at: datetime
