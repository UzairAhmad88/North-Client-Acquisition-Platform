"""Digital Forensics Evidence Locker Service."""
import uuid, hashlib
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class DigitalForensicsService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._evidence: List[Dict[str, Any]] = []

    def preserve_evidence(self, incident_id: str, evidence_type: str, description: str, raw_content: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        sha = hashlib.sha256(raw_content.encode()).hexdigest()
        rec = {
            "id": f"evid_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "incident_id": incident_id,
            "evidence_type": evidence_type,
            "description": description,
            "sha256_hash": sha,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }
        self._evidence.append(rec)
        return rec
