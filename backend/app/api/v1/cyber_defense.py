"""Phase 80 Enterprise Security Operations & Cyber Defense API Router."""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

from app.services.security.siem import SecuritySiemService
from app.services.security.soar import SecuritySoarService
from app.services.security.prompt_injection import SecurityPromptInjectionService
from app.agents.security import (
    SecurityOrchestratorAgent,
    SecurityCopilotAgent,
    AlertTriageAgent,
    IncidentInvestigatorAgent,
)

router = APIRouter(prefix="/cyber-defense", tags=["Enterprise Cyber Defense"])


class CopilotQueryRequest(BaseModel):
    prompt: str


class SoarActionRequest(BaseModel):
    action_type: str
    target: str
    autonomy_level: Optional[str] = "L3"
    approved_by: Optional[str] = None


class PromptCheckRequest(BaseModel):
    payload_text: str
    source_context: Optional[str] = "DOCUMENT_ATTACHMENT"


class AgentExecuteRequest(BaseModel):
    agent_id: str
    task_input: str


@router.get("/command-center")
def get_security_command_center():
    """Retrieve security posture, active threats, open incidents & SIEM metrics."""
    return {
        "status": "HEALTHY",
        "security_posture_score": 88.4,
        "active_threat_level": "ELEVATED",
        "metrics": {
            "mean_time_to_detect_mins": 4.2,
            "mean_time_to_respond_mins": 12.5,
            "open_critical_incidents": 1,
            "high_priority_alerts": 4,
            "active_agents": 13,
            "zero_trust_compliance_pct": 98.2
        },
        "siem_overview": SecuritySiemService.get_siem_overview(),
    }


@router.get("/siem/overview")
def get_siem_overview():
    return {"data": SecuritySiemService.get_siem_overview()}


@router.get("/siem/logs")
def search_siem_logs(query: str = Query("*"), limit: int = Query(50)):
    return {"data": SecuritySiemService.search_logs(query=query, limit=limit)}


@router.get("/zero-trust/evaluate")
def evaluate_zero_trust(identity: str = Query(...), resource: str = Query(...), device_id: str = Query("DEV-UNKNOWN")):
    return {
        "data": {
            "identity": identity,
            "resource": resource,
            "device_id": device_id,
            "decision": "ALLOWED",
            "risk_score": 12.4,
            "evaluated_conditions": ["MFA_VERIFIED", "MANAGED_DEVICE", "COMPLIANT_PATCH_LEVEL"],
            "policy_matched": "ZT-POL-SENSITIVE-DATA"
        }
    }


@router.get("/alerts")
def list_security_alerts():
    return {
        "data": [
            {
                "alert_code": "ALT-2026-901",
                "title": "Impossible Travel Login Signal",
                "severity": "HIGH",
                "confidence": 0.92,
                "identity": "john.doe@enterprise.com",
                "status": "INVESTIGATING",
                "evidence": ["Login London 14:00", "Login Tokyo 14:15"]
            },
            {
                "alert_code": "ALT-2026-902",
                "title": "AWS CloudTrail IAM Policy Mutation",
                "severity": "MEDIUM",
                "confidence": 0.85,
                "identity": "service-account-ci",
                "status": "NEW",
                "evidence": ["AttachUserPolicy AdministratorAccess"]
            }
        ]
    }


@router.get("/incidents")
def list_incidents():
    return {
        "data": [
            {
                "incident_code": "INC-2026-092",
                "title": "Suspicious API Credential Access & Potential Data Exfiltration Signal",
                "severity": "CRITICAL",
                "confidence": 0.96,
                "owner": "SOC Tier-2 Analyst",
                "status": "INVESTIGATING",
                "root_cause": "Leaked test API key used from unmanaged external IP.",
                "summary": "Multiple unauthorized data export attempts flagged by Phase 79 Data Security Guard."
            }
        ]
    }


@router.post("/copilot/query")
def query_security_copilot(req: CopilotQueryRequest):
    copilot = SecurityCopilotAgent()
    return {"data": copilot.run_task(req.prompt)}


@router.get("/playbooks")
def list_soar_playbooks():
    return {"data": SecuritySoarService.list_playbooks()}


@router.post("/soar/execute")
def execute_soar_action(req: SoarActionRequest):
    result = SecuritySoarService.execute_action(
        action_type=req.action_type,
        target=req.target,
        autonomy_level=req.autonomy_level,
        approved_by=req.approved_by
    )
    if not result.get("success"):
        raise HTTPException(status_code=403, detail=result.get("message"))
    return {"data": result}


@router.post("/ai-security/prompt-check")
def inspect_prompt_injection(req: PromptCheckRequest):
    return {"data": SecurityPromptInjectionService.inspect_input(req.payload_text, req.source_context)}


@router.get("/agents")
def list_security_agents():
    agents = [
        {"agent_id": "security_orchestrator", "name": "Security Orchestrator Agent", "autonomy_level": "L5", "status": "ACTIVE"},
        {"agent_id": "soc_analyst", "name": "SOC Analyst Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "alert_triage", "name": "Alert Triage Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "incident_investigator", "name": "Incident Investigator Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "threat_intelligence", "name": "Threat Intelligence Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "identity_risk", "name": "Identity Risk Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "vulnerability", "name": "Vulnerability Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "cloud_security", "name": "Cloud Security Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "application_security", "name": "Application Security Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "data_security", "name": "Data Security Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "detection_engineering", "name": "Detection Engineering Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "security_compliance", "name": "Security Compliance Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "security_copilot", "name": "Security Copilot Agent", "autonomy_level": "L4", "status": "ACTIVE"}
    ]
    return {"data": agents}
