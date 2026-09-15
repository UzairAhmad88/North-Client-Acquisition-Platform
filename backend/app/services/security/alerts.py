"""Security Alert Triage & Notification Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class SecurityAlertService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._alerts: List[Dict[str, Any]] = []

    def create_alert(self, title: str, severity: str, actor_id: str, evidence: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        alert = {
            "id": f"alert_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "title": title,
            "severity": severity,
            "status": "OPEN",
            "actor_id": actor_id,
            "confidence_score": 0.88,
            "evidence": evidence,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._alerts.append(alert)
        return alert

    def list_alerts(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [a for a in self._alerts if a["tenant_id"] == tenant_id]
