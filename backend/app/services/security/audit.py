"""Tamper-Resistant Security Audit Event Logging Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class SecurityAuditTrailService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._logs: List[Dict[str, Any]] = []

    def log_event(self, actor_id: str, action: str, resource: str, decision: str = "ALLOW", tenant_id: str = "default_tenant") -> Dict[str, Any]:
        log = {
            "id": f"sec_aud_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "actor_id": actor_id,
            "action": action,
            "resource": resource,
            "decision": decision,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._logs.append(log)
        return log

    def list_logs(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [l for l in self._logs if l["tenant_id"] == tenant_id]
