"""Data Incident Management service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class IncidentsService:
    """Manages Data Incidents (Pipeline failures, quality degradation, schema breaks)."""

    def __init__(self):
        self._incidents: Dict[str, Dict[str, Any]] = {}

    def create_incident(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        incident_id = data.get("id") or f"dinc_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        record = {
            "id": incident_id,
            "tenant_id": tenant_id,
            "title": data.get("title", "Data Quality Degradation"),
            "dataset_name": data.get("dataset_name", "orders"),
            "pipeline_id": data.get("pipeline_id"),
            "severity": data.get("severity", "SEV2"),
            "impact_scope": data.get("impact_scope", "Downstream Sales Data Mart"),
            "owner": data.get("owner", "data-oncall@uzaii.com"),
            "root_cause": data.get("root_cause", ""),
            "status": "OPEN",  # OPEN, INVESTIGATING, MITIGATED, RESOLVED
            "events": [
                {"text": "Incident detected and on-call notified.", "actor": "system", "at": now_iso}
            ],
            "detected_at": now_iso,
            "resolved_at": None,
        }
        self._incidents[incident_id] = record
        return record

    def update_incident_status(
        self, incident_id: str, status: str, event_text: Optional[str] = None, actor: str = "engineer", tenant_id: str = "default_tenant"
    ) -> Optional[Dict[str, Any]]:
        inc = self._incidents.get(incident_id)
        if inc and inc.get("tenant_id") == tenant_id:
            inc["status"] = status
            now_iso = datetime.now(timezone.utc).isoformat()
            if status == "RESOLVED":
                inc["resolved_at"] = now_iso
            if event_text:
                inc["events"].append({"text": event_text, "actor": actor, "at": now_iso})
            return inc
        return None

    def list_incidents(self, status: Optional[str] = None, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        incidents = [i for i in self._incidents.values() if i.get("tenant_id") == tenant_id]
        if status:
            incidents = [i for i in incidents if i.get("status") == status.upper()]
        return incidents
