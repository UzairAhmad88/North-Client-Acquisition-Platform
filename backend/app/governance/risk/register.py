"""
GRC Risk Register & Treatment Governance Engine (Section 19-21).
Enforces Inherent vs Residual Risk quantification and authorized human risk acceptance.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from backend.app.governance.base import (
    GovernanceRisk,
    RiskLevel,
    RiskTreatmentType,
)


class RiskRegister:
    """Enterprise risk register governing IT, privacy, AI, financial, and operational risks."""

    def __init__(self):
        self._risks: Dict[str, GovernanceRisk] = {}
        self._seed_default_risks()

    def _seed_default_risks(self) -> None:
        """Seeds canonical baseline risks."""
        self.register_risk(GovernanceRisk(
            risk_code="RSK_AI_PROMPT_INJECTION",
            title="Adversarial Prompt Injection & Tool Hijack in AI Agents",
            category="AI",
            threat="Malicious external inputs manipulate LLM to execute unauthorized tools.",
            vulnerability="Agents ingest untrusted client or web documents.",
            likelihood=0.6,
            impact=0.8,
            inherent_risk_score=75.0,
            residual_risk_score=25.0,
            risk_level=RiskLevel.MEDIUM,
            treatment=RiskTreatmentType.MITIGATE,
            owner_id="ai_security_officer",
            mitigating_controls=["CTL_AI_HUMAN_APPROVAL", "CTL_SEC_SECRET_SCRUBBING"]
        ))

        self.register_risk(GovernanceRisk(
            risk_code="RSK_SEC_CROSS_TENANT",
            title="Cross-Tenant Data Exposure or IDOR Vulnerability",
            category="SECURITY",
            threat="Multi-tenant queries or cache leakage exposes client data.",
            vulnerability="Improper tenant filtering or IDOR in API endpoints.",
            likelihood=0.3,
            impact=0.9,
            inherent_risk_score=80.0,
            residual_risk_score=20.0,
            risk_level=RiskLevel.LOW,
            treatment=RiskTreatmentType.MITIGATE,
            owner_id="ciso",
            mitigating_controls=["CTL_SEC_TENANT_ISOLATION", "CTL_SEC_MFA"]
        ))

    def register_risk(self, risk: GovernanceRisk) -> None:
        if not risk.owner_id:
            raise ValueError("All registered risks must have an assigned accountable owner.")
        # Calculate scores if not set
        if risk.inherent_risk_score == 50.0 and (risk.likelihood or risk.impact):
            risk.inherent_risk_score = round(risk.likelihood * risk.impact * 100.0, 1)
        self._risks[risk.risk_code] = risk

    def get_risk(self, risk_code: str) -> Optional[GovernanceRisk]:
        return self._risks.get(risk_code)

    def list_risks(self, category: Optional[str] = None) -> List[GovernanceRisk]:
        risks = list(self._risks.values())
        if category:
            risks = [r for r in risks if r.category == category]
        return risks

    def accept_risk(
        self,
        risk_code: str,
        approver_id: str,
        justification: str,
        is_ai_agent: bool = False
    ) -> GovernanceRisk:
        """Formal risk acceptance. Strictly requires authorized human decision-making."""
        if is_ai_agent:
            raise PermissionError("Safety violation: AI agents are strictly prohibited from accepting organizational risk.")
        if not approver_id:
            raise ValueError("Risk acceptance requires an authorized human approver ID.")
        if not justification or len(justification.strip()) < 15:
            raise ValueError("Detailed business justification (>15 chars) is mandatory for risk acceptance.")

        risk = self.get_risk(risk_code)
        if not risk:
            raise KeyError(f"Risk '{risk_code}' not found.")

        # Non-negotiable Separation of Duties: Risk Requester/Owner cannot unilaterally self-accept critical risks without an independent approver
        if risk.risk_level == RiskLevel.CRITICAL and risk.owner_id == approver_id:
            raise PermissionError("Separation of duties violation: Critical risk acceptance requires independent authorization (Approver != Owner).")

        risk.treatment = RiskTreatmentType.ACCEPT
        risk.accepted_by = approver_id
        risk.accepted_at = datetime.now(timezone.utc)
        risk.status = "ACCEPTED"
        return risk
