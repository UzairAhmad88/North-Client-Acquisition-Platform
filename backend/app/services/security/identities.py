"""Identity Security & Governance Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.autonomous_cybersecurity_zero_trust import CztIdentityModel, CztIdentityRiskModel

class IdentitySecurityService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self._identities: List[Dict[str, Any]] = []

    def create_identity(self, payload: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        ident_id = payload.get("id") or f"ident_{uuid.uuid4().hex[:12]}"
        record = {
            "id": ident_id,
            "tenant_id": tenant_id,
            "principal_id": payload.get("principal_id", f"user_{uuid.uuid4().hex[:8]}"),
            "identity_type": payload.get("identity_type", "USER"),
            "email_or_handle": payload.get("email_or_handle"),
            "display_name": payload.get("display_name", "Anonymous Principal"),
            "status": payload.get("status", "ACTIVE"),
            "is_privileged": payload.get("is_privileged", False),
            "mfa_enforced": payload.get("mfa_enforced", True),
            "current_risk_level": payload.get("current_risk_level", "LOW"),
            "risk_score": float(payload.get("risk_score", 0.05)),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._identities.append(record)
        return record

    def list_identities(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [i for i in self._identities if i["tenant_id"] == tenant_id]

    def update_risk(self, identity_id: str, new_score: float, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        for i in self._identities:
            if i["id"] == identity_id and i["tenant_id"] == tenant_id:
                i["risk_score"] = round(new_score, 3)
                i["current_risk_level"] = "CRITICAL" if new_score >= 0.8 else "HIGH" if new_score >= 0.6 else "MEDIUM" if new_score >= 0.3 else "LOW"
                return i
        return None
