"""Security Incident Response Lifecycle Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class IncidentResponseLifecycleService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._incidents: List[Dict[str, Any]] = []

    def create_incident(self, title: str, severity: str = "HIGH", affected_assets: Optional[List[str]] = None, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        inc_id = f"inc_{uuid.uuid4().hex[:12]}"
        record = {
            "id": inc_id,
            "tenant_id": tenant_id,
            "title": title,
            "severity": severity,
            "status": "TRIAGE",
            "affected_assets": affected_assets or [],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._incidents.append(record)
        return record

    def transition_stage(self, incident_id: str, new_status: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        for inc in self._incidents:
            if inc["id"] == incident_id and inc["tenant_id"] == tenant_id:
                inc["status"] = new_status
                return inc
        return None

    def list_incidents(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [i for i in self._incidents if i["tenant_id"] == tenant_id]
