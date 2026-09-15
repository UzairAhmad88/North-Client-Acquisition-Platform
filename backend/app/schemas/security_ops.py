"""
Pydantic request and response schemas for Phase 46 Security Operations REST API.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

try:
    from app.security.base import (
        SecuritySeverity,
        AlertStatus,
        IncidentStatus,
        AnomalyType,
        MitreTactic,
        RunbookActionType,
        EmergencySecurityControl,
    )
except ImportError:
    from backend.app.security.base import (
        SecuritySeverity,
        AlertStatus,
        IncidentStatus,
        AnomalyType,
        MitreTactic,
        RunbookActionType,
        EmergencySecurityControl,
    )


# --- Telemetry Ingestion ---

class IngestSecurityEventRequest(BaseModel):
    event_type: str = Field(..., description="Type of event, e.g. auth.login, api.get, agent.tool_execution")
    source: str = Field("auth", description="Source subsystem: auth, api, agent, data, admin, finance, integration")
    principal_id: str = Field("anonymous", description="Actor or user ID")
    action: str = Field("execute", description="Action performed")
    status: str = Field("success", description="success, failure, blocked")
    tenant_id: str = Field("default_tenant", description="Tenant isolation boundary")
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    evidence: Dict[str, Any] = Field(default_factory=dict)


# --- Detections & Alerts ---

class SecurityAlertResponse(BaseModel):
    alert_id: str
    tenant_id: str
    title: str
    description: str
    severity: str
    status: str
    anomaly_type: str
    mitre_technique_id: Optional[str] = None
    mitre_tactic: Optional[str] = None
    risk_score: float
    confidence_score: float
    affected_actor_id: Optional[str] = None
    affected_target_id: Optional[str] = None
    evidence: Dict[str, Any]
    created_at: datetime


class UpdateAlertStatusRequest(BaseModel):
    status: AlertStatus


# --- Incidents ---

class CreateIncidentRequest(BaseModel):
    title: str
    description: str
    severity: SecuritySeverity = SecuritySeverity.HIGH
    affected_tenants: List[str] = Field(default_factory=lambda: ["default_tenant"])
    affected_users: List[str] = Field(default_factory=list)
    affected_services: List[str] = Field(default_factory=list)
    affected_resources: List[str] = Field(default_factory=list)
    owner: Optional[str] = None


class UpdateIncidentStatusRequest(BaseModel):
    status: IncidentStatus
    resolution: Optional[str] = None


class SecurityIncidentResponse(BaseModel):
    incident_id: str
    tenant_id: str
    title: str
    description: str
    severity: str
    status: str
    category: str
    detection_source: str
    affected_tenants: List[str]
    affected_users: List[str]
    affected_services: List[str]
    affected_resources: List[str]
    timeline: List[Dict[str, Any]]
    evidence: Dict[str, Any]
    root_cause: Optional[str] = None
    containment_actions: List[str]
    remediation_actions: List[str]
    business_impact: Optional[str] = None
    security_impact: Optional[str] = None
    owner: Optional[str] = None
    resolution: Optional[str] = None
    postmortem: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# --- Remediation & Controls ---

class RemediationExecuteRequest(BaseModel):
    alert_id: str
    action_name: str
    requested_by: str
    approved_by: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    idempotency_key: Optional[str] = None


class EmergencyControlToggleRequest(BaseModel):
    control: str
    enable: bool
    operator_id: str
    reason: str


# --- Threat Intelligence ---

class ThreatIndicatorCreateRequest(BaseModel):
    indicator_type: str  # IP, DOMAIN, URL, HASH, EMAIL
    indicator_value: str
    threat_category: str
    severity: SecuritySeverity = SecuritySeverity.MEDIUM
    confidence: float = 0.8
    source: str = "MANUAL_INPUT"
    reputation: int = 80


# --- Copilot ---

class SecurityCopilotQueryRequest(BaseModel):
    query: str
    context_id: Optional[str] = None
