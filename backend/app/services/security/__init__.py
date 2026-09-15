import importlib.util
import os

# 1. Dynamically preserve legacy SecurityService from backend/app/services/security.py
_sec_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "security.py"))
if os.path.exists(_sec_file):
    _spec = importlib.util.spec_from_file_location("app.services.security_legacy", _sec_file)
    if _spec and _spec.loader:
        _sec_module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_sec_module)
        SecurityService = getattr(_sec_module, "SecurityService", None)
else:
    SecurityService = None

# 2. Phase 66 Modular Security Services
from backend.app.services.security.assets import AssetSecurityService
from backend.app.services.security.identities import IdentitySecurityService
from backend.app.services.security.devices import DeviceSecurityService
from backend.app.services.security.service_identity import ServiceIdentityService
from backend.app.services.security.agent_identity import AgentSecurityGovernanceService
from backend.app.services.security.authorization import AuthorizationService
from backend.app.services.security.zero_trust import ZeroTrustEvaluationService
from backend.app.services.security.privileged_access import PrivilegedAccessService
from backend.app.services.security.sessions import SessionSecurityService
from backend.app.services.security.tokens import TokenSecurityService
from backend.app.services.security.secrets import SecretGovernanceService
from backend.app.services.security.certificates import CertificateSecurityService
from backend.app.services.security.events import SecurityEventPipelineService
from backend.app.services.security.normalization import TelemetryNormalizationService
from backend.app.services.security.correlation import EventCorrelationService
from backend.app.services.security.detections import DetectionEngineService
from backend.app.services.security.alerts import SecurityAlertService
from backend.app.services.security.threat_intelligence import ThreatIntelligenceService
from backend.app.services.security.vulnerabilities import VulnerabilityManagementService
from backend.app.services.security.sbom import SbomService
from backend.app.services.security.application_security import ApplicationSecurityService
from backend.app.services.security.cloud_security import CloudSecurityService
from backend.app.services.security.data_security import DataSecurityDefenseService
from backend.app.services.security.ai_security import AiSecurityGuardrailsService
from backend.app.services.security.retrieval_security import RetrievalSecurityService
from backend.app.services.security.incident import IncidentResponseLifecycleService
from backend.app.services.security.investigation import SecurityInvestigationService
from backend.app.services.security.forensics import DigitalForensicsService
from backend.app.services.security.playbooks import SecurityPlaybookService
from backend.app.services.security.response import AutomatedResponseService
from backend.app.services.security.risk import SecurityRiskScoringService
from backend.app.services.security.compliance import ComplianceFrameworkService
from backend.app.services.security.policy import SecurityPolicyManagementService
from backend.app.services.security.audit import SecurityAuditTrailService
from backend.app.services.security.security_graph import SecurityGraphService
from backend.app.services.security.analytics import SecurityAnalyticsService
from backend.app.services.security.validation import SecurityInputValidationService
from backend.app.services.security.service import AutonomousCybersecurityZeroTrustService

__all__ = [
    "SecurityService",
    "AssetSecurityService",
    "IdentitySecurityService",
    "DeviceSecurityService",
    "ServiceIdentityService",
    "AgentSecurityGovernanceService",
    "AuthorizationService",
    "ZeroTrustEvaluationService",
    "PrivilegedAccessService",
    "SessionSecurityService",
    "TokenSecurityService",
    "SecretGovernanceService",
    "CertificateSecurityService",
    "SecurityEventPipelineService",
    "TelemetryNormalizationService",
    "EventCorrelationService",
    "DetectionEngineService",
    "SecurityAlertService",
    "ThreatIntelligenceService",
    "VulnerabilityManagementService",
    "SbomService",
    "ApplicationSecurityService",
    "CloudSecurityService",
    "DataSecurityDefenseService",
    "AiSecurityGuardrailsService",
    "RetrievalSecurityService",
    "IncidentResponseLifecycleService",
    "SecurityInvestigationService",
    "DigitalForensicsService",
    "SecurityPlaybookService",
    "AutomatedResponseService",
    "SecurityRiskScoringService",
    "ComplianceFrameworkService",
    "SecurityPolicyManagementService",
    "SecurityAuditTrailService",
    "SecurityGraphService",
    "SecurityAnalyticsService",
    "SecurityInputValidationService",
    "AutonomousCybersecurityZeroTrustService",
]
