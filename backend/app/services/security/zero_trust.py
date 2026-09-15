"""Continuous Zero-Trust Evaluation Engine."""
from typing import Dict, Any, List, Optional, Optional, List
from datetime import datetime, timezone

class ZeroTrustEvaluationService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def evaluate_access(
        self,
        subject_id: str,
        subject_type: str,
        resource: str,
        action: str,
        device_compliant: bool = True,
        risk_score: float = 0.1,
        user_roles: Optional[List[str]] = None,
        tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        reasons = []
        decision = "ALLOW"

        # 1. Device Posture Gate
        if not device_compliant:
            decision = "DENY"
            reasons.append("Device non-compliant with security posture requirements.")

        # 2. Risk Gate
        elif risk_score >= 0.8:
            decision = "ISOLATE"
            reasons.append(f"Excessive subject risk score ({risk_score:.2f}) triggers containment.")
        elif risk_score >= 0.5:
            decision = "STEP_UP_AUTHENTICATION"
            reasons.append("Elevated risk requires MFA step-up verification.")

        # 3. Sensitive Action Gate
        if decision == "ALLOW" and action in ["DELETE", "EXPORT", "ROTATE_SECRET", "DEPLOY_PRODUCTION"]:
            decision = "REQUIRE_APPROVAL"
            reasons.append("High-impact action requires dual authorization.")

        return {
            "decision": decision,
            "subject_id": subject_id,
            "subject_type": subject_type,
            "resource": resource,
            "action": action,
            "risk_score": risk_score,
            "reasons": reasons,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
