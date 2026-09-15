"""
Control Catalog, Ownership & Component Implementation Mapping (Section 10-13).
"""

from typing import Dict, List, Optional
from backend.app.governance.base import (
    AutomationLevel,
    ControlDomain,
    ControlFrequency,
    ControlHealthStatus,
    ControlType,
    GovernanceControl,
)


class ControlCatalog:
    """Catalog of operational controls satisfying requirements and mapped to code implementations."""

    def __init__(self):
        self._controls: Dict[str, GovernanceControl] = {}
        self._seed_default_controls()

    def _seed_default_controls(self) -> None:
        """Seeds standard platform controls linked to existing subsystem implementations."""
        # 1. Multi-Factor Authentication Control
        self.register_control(GovernanceControl(
            control_code="CTL_SEC_MFA",
            name="Enforce Multi-Factor Authentication on Privileged Roles",
            objective="Ensure step-up authentication is mandatory for administrative and high-risk actions.",
            domain=ControlDomain.IDENTITY,
            control_type=ControlType.PREVENTIVE,
            frequency=ControlFrequency.CONTINUOUS,
            automation_level=AutomationLevel.CONTINUOUSLY_MONITORED,
            owner_id="iam_security_lead",
            operator_id="backend.app.security.service.MFAService",
            health_status=ControlHealthStatus.HEALTHY,
            test_method="AUTOMATED_PROBE",
            implementations=[
                "backend/app/security/service.py:MFAService",
                "backend/app/models/security.py:UserMFAMethod",
                "backend/app/api/v1/security.py:/mfa/verify"
            ]
        ))

        # 2. Tenant Isolation & IDOR Defense Control
        self.register_control(GovernanceControl(
            control_code="CTL_SEC_TENANT_ISOLATION",
            name="Cryptographic & Logical Multi-Tenant Boundary Isolation",
            objective="Strictly isolate data, workflows, agents, and queries by tenant_id.",
            domain=ControlDomain.ACCESS,
            control_type=ControlType.PREVENTIVE,
            frequency=ControlFrequency.CONTINUOUS,
            automation_level=AutomationLevel.CONTINUOUSLY_MONITORED,
            owner_id="platform_architect",
            operator_id="backend.app.security.base.AuthorizationContext",
            health_status=ControlHealthStatus.HEALTHY,
            test_method="AUTOMATED_SECURITY_TEST",
            implementations=[
                "backend/app/security/base.py:AuthorizationEngine",
                "backend/app/security/detection/rules.py:CrossTenantAccessRule",
                "backend/app/models/base.py:BaseModel.tenant_id"
            ]
        ))

        # 3. Telemetry Secret Scrubbing & Minimization
        self.register_control(GovernanceControl(
            control_code="CTL_SEC_SECRET_SCRUBBING",
            name="Zero Plaintext Secrets in Observability & Security Telemetry",
            objective="Prevent exposure of passwords, API keys, tokens, and credentials in logs and telemetry.",
            domain=ControlDomain.SECURITY,
            control_type=ControlType.PREVENTIVE,
            frequency=ControlFrequency.CONTINUOUS,
            automation_level=AutomationLevel.AUTOMATED,
            owner_id="appsec_engineer",
            operator_id="backend.app.security.telemetry.normalizer.sanitize_payload",
            health_status=ControlHealthStatus.HEALTHY,
            test_method="UNIT_AND_PAYLOAD_TEST",
            implementations=[
                "backend/app/security/telemetry/normalizer.py:sanitize_payload",
                "backend/app/security/detection/rules.py:TokenLeakRule"
            ]
        ))

        # 4. AI Agent Human-in-the-Loop Approval Gate
        self.register_control(GovernanceControl(
            control_code="CTL_AI_HUMAN_APPROVAL",
            name="Human Approval Requirement for External & High-Risk AI Actions",
            objective="Prohibit autonomous outbound sends, commercial commitments, and privileged state changes.",
            domain=ControlDomain.AI,
            control_type=ControlType.PREVENTIVE,
            frequency=ControlFrequency.CONTINUOUS,
            automation_level=AutomationLevel.CONTINUOUSLY_MONITORED,
            owner_id="ai_governance_lead",
            operator_id="agents.core.permissions.PROHIBITED_PERMISSIONS",
            health_status=ControlHealthStatus.HEALTHY,
            test_method="AGENT_SANDBOX_AUDIT",
            implementations=[
                "agents/core/permissions.py:validate_agent_permissions",
                "backend/app/orchestration/state_machine.py:WAITING_FOR_HUMAN_APPROVAL",
                "backend/app/security/remediation/engine.py:SeparationOfDutiesGuard"
            ]
        ))

        # 5. Immutable Configuration Fingerprinting & Drift Detection
        self.register_control(GovernanceControl(
            control_code="CTL_OPS_CONFIG_IMMUTABILITY",
            name="Immutable Security Fingerprinting & Configuration Drift Detection",
            objective="Detect and reconcile unauthorized changes to production security and reliability parameters.",
            domain=ControlDomain.OPERATIONS,
            control_type=ControlType.DETECTIVE,
            frequency=ControlFrequency.DAILY,
            automation_level=AutomationLevel.AUTOMATED,
            owner_id="devops_lead",
            operator_id="backend.app.administration.drift.ConfigurationDriftDetector",
            health_status=ControlHealthStatus.HEALTHY,
            test_method="DAILY_SCHEDULED_PROBE",
            implementations=[
                "backend/app/administration/drift.py:ConfigurationDriftDetector",
                "backend/app/models/administration.py:ConfigurationDriftModel"
            ]
        ))

        # 6. Automated Backup Cryptographic Verification & Disaster Recovery Drills
        self.register_control(GovernanceControl(
            control_code="CTL_REL_BACKUP_INTEGRITY",
            name="Cryptographic SHA-256 Backup Verification & Isolated Sandbox Restores",
            objective="Ensure database and file backups are verified for integrity and non-corruption daily.",
            domain=ControlDomain.RELIABILITY,
            control_type=ControlType.CORRECTIVE,
            frequency=ControlFrequency.DAILY,
            automation_level=AutomationLevel.AUTOMATED,
            owner_id="sre_lead",
            operator_id="backend.app.disaster_recovery.restore_verifier.RestoreVerifier",
            health_status=ControlHealthStatus.HEALTHY,
            test_method="AUTOMATED_RESTORE_SANDBOX",
            implementations=[
                "backend/app/disaster_recovery/backup_manager.py:BackupManager",
                "backend/app/disaster_recovery/restore_verifier.py:RestoreVerifier"
            ]
        ))

        # 7. Privacy Data Subject Request (DSAR) Fulfillment Lifecycle
        self.register_control(GovernanceControl(
            control_code="CTL_PRIV_DSAR_LIFECYCLE",
            name="Data Subject Request (DSAR) Scoping, Fulfillment & Verification",
            objective="Process data erasure, export, and access requests within 30-day statutory limits.",
            domain=ControlDomain.PRIVACY,
            control_type=ControlType.CORRECTIVE,
            frequency=ControlFrequency.CONTINUOUS,
            automation_level=AutomationLevel.SEMI_AUTOMATED,
            owner_id="dpo_lead",
            operator_id="backend.app.governance.privacy.engine.PrivacyEngine",
            health_status=ControlHealthStatus.HEALTHY,
            test_method="AUDIT_SAMPLE_INSPECTION",
            implementations=[
                "backend/app/governance/privacy/engine.py:PrivacyEngine",
                "backend/app/models/grc.py:PrivacyRequestModel"
            ]
        ))

    def register_control(self, control: GovernanceControl) -> None:
        if not control.owner_id:
            raise ValueError(f"Control '{control.control_code}' cannot be registered without an assigned accountable owner.")
        self._controls[control.control_code] = control

    def get_control(self, control_code: str) -> Optional[GovernanceControl]:
        return self._controls.get(control_code)

    def list_controls(self, domain: Optional[ControlDomain] = None) -> List[GovernanceControl]:
        controls = list(self._controls.values())
        if domain:
            controls = [c for c in controls if c.domain == domain]
        return controls

    def update_control_health(self, control_code: str, status: ControlHealthStatus) -> None:
        control = self.get_control(control_code)
        if control:
            control.health_status = status
