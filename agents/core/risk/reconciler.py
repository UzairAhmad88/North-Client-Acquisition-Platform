"""Risk reconciler combining deterministic findings and AI semantic reviews into final decision."""

from typing import List, Tuple
from agents.core.risk.models import RiskAssessmentResult, RiskFindingDetail
from agents.core.risk.policies import RiskPolicy


class RiskReconciler:
    """Enforces strict deterministic safety precedence over AI evaluation."""

    @staticmethod
    def reconcile(
        deterministic_findings: List[RiskFindingDetail],
        ai_risk_level: str,
        ai_findings: List[RiskFindingDetail],
        policy: RiskPolicy,
    ) -> Tuple[str, str]:
        """
        Reconcile deterministic findings and AI semantic findings.
        Returns (decision, risk_level).
        Decision is PASS, REVIEW, or BLOCK.
        Risk Level is LOW, MEDIUM, HIGH, or BLOCKED.
        """
        all_findings = deterministic_findings + ai_findings

        # 1. Check for CRITICAL or BLOCKED severity in deterministic findings -> Immediate BLOCK
        has_critical = any(f.severity in ("CRITICAL", "BLOCKED") for f in deterministic_findings)
        if has_critical:
            return "BLOCK", "BLOCKED"

        # 2. Check for HIGH severity findings
        has_high_det = any(f.severity == "HIGH" for f in deterministic_findings)
        has_high_ai = ai_risk_level in ("HIGH", "BLOCKED") or any(f.severity == "HIGH" for f in ai_findings)

        if has_high_det:
            return "BLOCK", "HIGH"

        if has_high_ai:
            return "REVIEW", "HIGH"

        # 3. Check for MEDIUM severity findings
        has_med = any(f.severity == "MEDIUM" for f in all_findings) or ai_risk_level == "MEDIUM"
        if has_med:
            return "REVIEW", "MEDIUM"

        # 4. Low/No findings -> PASS
        return "PASS", "LOW"
