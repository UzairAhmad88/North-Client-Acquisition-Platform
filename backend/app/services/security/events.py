"""Security Event Pipeline & Log Collection Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class SecurityEventPipelineService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._events: List[Dict[str, Any]] = []

    def ingest_event(self, source: str, actor_id: str, action: str, target_resource: str, status: str = "SUCCESS", severity: str = "INFORMATIONAL", ip: Optional[str] = None, payload: Optional[Dict[str, Any]] = None, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        evt = {
            "id": f"event_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "source": source,
            "actor_id": actor_id,
            "action": action,
            "target_resource": target_resource,
            "status": status,
            "severity": severity,
            "ip_address": ip,
            "payload": payload or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._events.append(evt)
        return evt

    def list_events(self, tenant_id: str = "default_tenant", limit: int = 100) -> List[Dict[str, Any]]:
        return [e for e in self._events if e["tenant_id"] == tenant_id][-limit:]
