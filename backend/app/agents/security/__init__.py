"""
Phase 80: Autonomous Security Agents Module.
Inherits Phase 76 Agent OS governance & Autonomy Level Controls.
"""

from app.agents.security.security_orchestrator import SecurityOrchestratorAgent
from app.agents.security.soc_analyst import SocAnalystAgent
from app.agents.security.alert_triage import AlertTriageAgent
from app.agents.security.incident_investigator import IncidentInvestigatorAgent
from app.agents.security.threat_intelligence import ThreatIntelligenceAgent
from app.agents.security.identity_risk import IdentityRiskAgent
from app.agents.security.vulnerability import VulnerabilityAgent
from app.agents.security.cloud_security import CloudSecurityAgent
from app.agents.security.application_security import ApplicationSecurityAgent
from app.agents.security.data_security import DataSecurityAgent
from app.agents.security.detection_engineering import DetectionEngineeringAgent
from app.agents.security.security_compliance import SecurityComplianceAgent
from app.agents.security.security_copilot import SecurityCopilotAgent

__all__ = [
    "SecurityOrchestratorAgent",
    "SocAnalystAgent",
    "AlertTriageAgent",
    "IncidentInvestigatorAgent",
    "ThreatIntelligenceAgent",
    "IdentityRiskAgent",
    "VulnerabilityAgent",
    "CloudSecurityAgent",
    "ApplicationSecurityAgent",
    "DataSecurityAgent",
    "DetectionEngineeringAgent",
    "SecurityComplianceAgent",
    "SecurityCopilotAgent",
]
