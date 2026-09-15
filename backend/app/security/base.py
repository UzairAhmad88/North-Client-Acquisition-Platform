"""
Base security enums, canonical schemas, and core data structures for Phase 46 Security Operations.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class SecuritySeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Backward compatibility aliases
ThreatSeverity = SecuritySeverity
IncidentSeverity = SecuritySeverity


class SecurityEventCategory(str, Enum):
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    IDENTITY = "IDENTITY"
    PRIVILEGE = "PRIVILEGE"
    API = "API"
    DATA_ACCESS = "DATA_ACCESS"
    ADMINISTRATION = "ADMINISTRATION"
    CONFIGURATION = "CONFIGURATION"
    AI_SECURITY = "AI_SECURITY"
    AGENT_SECURITY = "AGENT_SECURITY"
    TOOL_SECURITY = "TOOL_SECURITY"
    WORKFLOW_SECURITY = "WORKFLOW_SECURITY"
    COMMUNICATION_SECURITY = "COMMUNICATION_SECURITY"
    FINANCIAL_SECURITY = "FINANCIAL_SECURITY"
    INTEGRATION_SECURITY = "INTEGRATION_SECURITY"
    DOCUMENT_SECURITY = "DOCUMENT_SECURITY"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    POLICY = "POLICY"
    COMPLIANCE = "COMPLIANCE"
    INCIDENT = "INCIDENT"
    REMEDIATION = "REMEDIATION"


class SecuritySourceType(str, Enum):
    AUTH = "auth"
    API = "api"
    DATA = "data"
    AGENT = "agent"
    ADMIN = "admin"
    SYSTEM = "system"
    WORKER = "worker"
    INTEGRATION = "integration"
    FINANCE = "finance"
    COMMUNICATION = "communication"
    INFRASTRUCTURE = "infrastructure"
    EXTERNAL_FEED = "external_feed"


SourceType = SecuritySourceType


class ActorType(str, Enum):
    USER = "user"
    AGENT = "agent"
    SERVICE_ACCOUNT = "service_account"
    API_TOKEN = "api_token"
    SYSTEM = "system"
    ANONYMOUS = "anonymous"


class AlertStatus(str, Enum):
    DETECTED = "DETECTED"
    CREATED = "CREATED"
    TRIAGED = "TRIAGED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    CONFIRMED = "CONFIRMED"
    CONTAINMENT = "CONTAINMENT"
    REMEDIATION = "REMEDIATION"
    VERIFICATION = "VERIFICATION"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    DUPLICATE = "DUPLICATE"
    BENIGN = "BENIGN"
    SUPPRESSED = "SUPPRESSED"
    EXPIRED = "EXPIRED"
    ESCALATED = "ESCALATED"


class IncidentStatus(str, Enum):
    DETECTED = "detected"
    TRIAGED = "triaged"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    REMEDIATING = "remediating"
    RECOVERED = "recovered"
    CLOSED = "closed"


class MitreTactic(str, Enum):
    INITIAL_ACCESS = "TA0001_Initial_Access"
    EXECUTION = "TA0002_Execution"
    PERSISTENCE = "TA0003_Persistence"
    PRIVILEGE_ESCALATION = "TA0004_Privilege_Escalation"
    DEFENSE_EVASION = "TA0005_Defense_Evasion"
    CREDENTIAL_ACCESS = "TA0006_Credential_Access"
    DISCOVERY = "TA0007_Discovery"
    LATERAL_MOVEMENT = "TA0008_Lateral_Movement"
    COLLECTION = "TA0009_Collection"
    EXFILTRATION = "TA0010_Exfiltration"
    IMPACT = "TA0040_Impact"


class AnomalyType(str, Enum):
    CREDENTIAL_STUFFING = "credential_stuffing"
    BRUTE_FORCE = "brute_force"
    IMPOSSIBLE_TRAVEL = "impossible_travel"
    TOKEN_LEAK = "token_leak"
    DATA_EXFILTRATION = "data_exfiltration"
    AGENT_PROMPT_INJECTION = "agent_prompt_injection"
    AGENT_TOOL_HIJACK = "agent_tool_hijack"
    AGENT_RUNAWAY_SPEND = "agent_runaway_spend"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    SENSITIVE_CONFIG_TAMPERING = "sensitive_config_tampering"
    UNAUTHORIZED_RESOURCE_ACCESS = "unauthorized_resource_access"
    CROSS_TENANT_VIOLATION = "cross_tenant_violation"
    API_RATE_ABUSE = "api_rate_abuse"
    API_ENUMERATION = "api_enumeration"
    SUSPICIOUS_SEQUENCE = "suspicious_sequence"


class RunbookActionType(str, Enum):
    REVOKE_SESSION = "REVOKE_SESSION"
    DISABLE_API_KEY = "DISABLE_API_KEY"
    DISABLE_SERVICE_ACCOUNT = "DISABLE_SERVICE_ACCOUNT"
    REQUIRE_MFA = "REQUIRE_MFA"
    REMOVE_PERMISSION = "REMOVE_PERMISSION"
    DISABLE_WORKFLOW = "DISABLE_WORKFLOW"
    DISABLE_AGENT = "DISABLE_AGENT"
    DISABLE_TOOL = "DISABLE_TOOL"
    BLOCK_INTEGRATION = "BLOCK_INTEGRATION"
    PAUSE_AUTOMATION = "PAUSE_AUTOMATION"
    ROTATE_SECRET_REFERENCE = "ROTATE_SECRET_REFERENCE"
    ENABLE_MAINTENANCE_MODE = "ENABLE_MAINTENANCE_MODE"
    BLOCK_IP = "BLOCK_IP"
    LOCK_ACCOUNT = "LOCK_ACCOUNT"
    FORCE_PASSWORD_RESET = "FORCE_PASSWORD_RESET"
    NOTIFY_SOC_TEAM = "NOTIFY_SOC_TEAM"


class EmergencySecurityControl(str, Enum):
    GLOBAL_SECURITY_LOCKDOWN = "GLOBAL_SECURITY_LOCKDOWN"
    GLOBAL_EXTERNAL_INTEGRATIONS_OFF = "GLOBAL_EXTERNAL_INTEGRATIONS_OFF"
    GLOBAL_COMMUNICATION_OFF = "GLOBAL_COMMUNICATION_OFF"
    GLOBAL_PAYMENTS_OFF = "GLOBAL_PAYMENTS_OFF"
    GLOBAL_AI_OFF = "GLOBAL_AI_OFF"
    GLOBAL_WORKFLOWS_OFF = "GLOBAL_WORKFLOWS_OFF"
    GLOBAL_AUTOMATIONS_OFF = "GLOBAL_AUTOMATIONS_OFF"


class ActionExecutionStatus(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class PostureGrade(str, Enum):
    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class ThreatIndicatorType(str, Enum):
    IP = "IP"
    DOMAIN = "DOMAIN"
    URL = "URL"
    HASH = "HASH"
    EMAIL = "EMAIL"
    USER_AGENT = "USER_AGENT"
    API_PATTERN = "API_PATTERN"
    BEHAVIOR_PATTERN = "BEHAVIOR_PATTERN"


# --- Core Data Schemas ---

class SecurityActor(BaseModel):
    actor_id: str
    actor_type: str = "user"  # "user", "agent", "system", "anonymous", "api_token"
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    geo_country: Optional[str] = None
    geo_city: Optional[str] = None


class SecurityTarget(BaseModel):
    target_id: Optional[str] = None
    target_type: str = "resource"  # "table", "endpoint", "agent", "user", "tenant", "config"
    resource_name: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SecurityEvent(BaseModel):
    """
    Canonical Security Event per Section 6.
    Zero plaintext secrets allowed.
    """
    security_event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    event_category: SecurityEventCategory = SecurityEventCategory.AUTHENTICATION
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tenant_id: str = "default_tenant"
    organization_id: Optional[str] = None
    principal_id: str = "system"
    principal_type: str = "USER"
    user_id: Optional[str] = None
    service_account_id: Optional[str] = None
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    request_id: Optional[str] = None
    trace_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_metadata: Dict[str, Any] = Field(default_factory=dict)
    device_metadata: Dict[str, Any] = Field(default_factory=dict)
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    action: str = "access"
    result: str = "ALLOW"  # "ALLOW", "DENY", "BLOCK", "SUCCESS", "FAILURE"
    risk_level: SecuritySeverity = SecuritySeverity.LOW
    source: SecuritySourceType = SecuritySourceType.AUTH
    evidence: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: Optional[str] = None
    policy_version: str = "1.0"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Compatibility properties
    @property
    def id(self) -> str:
        return self.security_event_id

    @property
    def event_id(self) -> str:
        return self.security_event_id

    @property
    def source_type(self) -> SecuritySourceType:
        return self.source

    @property
    def severity(self) -> SecuritySeverity:
        return self.risk_level

    @property
    def actor(self) -> SecurityActor:
        return SecurityActor(
            actor_id=self.principal_id,
            actor_type=self.principal_type.lower(),
            ip_address=self.ip_metadata.get("ip_address"),
            user_agent=self.device_metadata.get("user_agent"),
            session_id=self.session_id,
            geo_country=self.ip_metadata.get("country"),
            geo_city=self.ip_metadata.get("city")
        )

    @property
    def status(self) -> str:
        return "success" if self.result in ("ALLOW", "SUCCESS") else "failure"

    @property
    def risk_score(self) -> float:
        if self.risk_level == SecuritySeverity.CRITICAL:
            return 90.0
        elif self.risk_level == SecuritySeverity.HIGH:
            return 75.0
        elif self.risk_level == SecuritySeverity.MEDIUM:
            return 50.0
        elif self.risk_level == SecuritySeverity.LOW:
            return 25.0
        return 5.0


class SecurityDetection(BaseModel):
    detection_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    rule_id: str
    rule_name: str
    anomaly_type: AnomalyType
    severity: SecuritySeverity
    risk_score: float = 50.0
    confidence: float = 0.8
    mitre_technique_id: Optional[str] = None
    mitre_tactic: Optional[str] = None
    description: str
    evidence_events: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SecurityAlert(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    title: str
    description: str
    severity: SecuritySeverity = SecuritySeverity.MEDIUM
    status: AlertStatus = AlertStatus.DETECTED
    anomaly_type: AnomalyType
    mitre_technique_id: Optional[str] = None
    mitre_tactic: Optional[str] = None
    risk_score: float = 50.0
    confidence_score: float = 0.8
    affected_actor_id: Optional[str] = None
    affected_target_id: Optional[str] = None
    evidence: Dict[str, Any] = Field(default_factory=dict)
    detection_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def id(self) -> str:
        return self.alert_id

    @property
    def actor_id(self) -> Optional[str]:
        return self.affected_actor_id


# Alias for backward compatibility
AnomalyAlert = SecurityAlert


class SecurityIncident(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    title: str
    description: str
    severity: SecuritySeverity = SecuritySeverity.HIGH
    status: IncidentStatus = IncidentStatus.DETECTED
    category: SecurityEventCategory = SecurityEventCategory.INCIDENT
    detection_source: str = "detection_engine"
    affected_tenants: List[str] = Field(default_factory=list)
    affected_users: List[str] = Field(default_factory=list)
    affected_services: List[str] = Field(default_factory=list)
    affected_resources: List[str] = Field(default_factory=list)
    timeline: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: Dict[str, Any] = Field(default_factory=dict)
    root_cause: Optional[str] = None
    containment_actions: List[str] = Field(default_factory=list)
    remediation_actions: List[str] = Field(default_factory=list)
    business_impact: Optional[str] = None
    security_impact: Optional[str] = None
    owner: Optional[str] = None
    approvals: List[Dict[str, Any]] = Field(default_factory=list)
    resolution: Optional[str] = None
    postmortem: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AttackChainStage(BaseModel):
    stage_name: str
    event_ids: List[str] = Field(default_factory=list)
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    description: str


class AttackChainHypothesis(BaseModel):
    chain_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    title: str
    confidence: float
    stages: List[AttackChainStage] = Field(default_factory=list)
    affected_principal: Optional[str] = None
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    recommended_investigation_steps: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BlastRadiusResult(BaseModel):
    radius_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: Optional[str] = None
    tenant_id: str = "default_tenant"
    overall_impact_score: float = 0.0  # 0.0 to 100.0
    affected_users: List[str] = Field(default_factory=list)
    affected_clients: List[str] = Field(default_factory=list)
    affected_tenants: List[str] = Field(default_factory=list)
    affected_services: List[str] = Field(default_factory=list)
    affected_projects: List[str] = Field(default_factory=list)
    affected_documents: List[str] = Field(default_factory=list)
    affected_financial_records: List[str] = Field(default_factory=list)
    affected_integrations: List[str] = Field(default_factory=list)
    affected_ai_agents: List[str] = Field(default_factory=list)
    affected_workflows: List[str] = Field(default_factory=list)
    narrative_summary: str = ""
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ThreatIndicator(BaseModel):
    indicator_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    indicator_type: ThreatIndicatorType
    indicator_value: str
    threat_category: str
    severity: SecuritySeverity
    confidence: float = 0.9
    source: str = "INTERNAL"
    reputation: int = 80  # 0 (safe) to 100 (malicious)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RiskAssessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    composite_risk_score: float = 0.0  # 0 to 100
    overall_severity: SecuritySeverity = SecuritySeverity.LOW
    identity_risk: float = 0.0
    ai_risk: float = 0.0
    data_risk: float = 0.0
    config_risk: float = 0.0
    integration_risk: float = 0.0
    financial_risk: float = 0.0
    calculation_formula: str = "Likelihood * Impact * EvidenceStrength * BlastRadius"
    policy_version: str = "1.0"
    assessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
