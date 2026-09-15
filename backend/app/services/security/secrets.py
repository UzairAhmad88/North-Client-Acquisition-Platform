"""Central Secret Management & Vault Reference Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class SecretGovernanceService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._secrets: List[Dict[str, Any]] = []

    def register_secret(self, secret_name: str, vault_reference_key: str, owner: str, secret_type: str = "API_KEY", tenant_id: str = "default_tenant") -> Dict[str, Any]:
        rec = {
            "id": f"sec_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "secret_name": secret_name,
            "vault_reference_key": vault_reference_key,
            "secret_type": secret_type,
            "owner": owner,
            "status": "ACTIVE",
            "last_rotated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._secrets.append(rec)
        return rec

    def rotate_secret(self, secret_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        for s in self._secrets:
            if s["id"] == secret_id and s["tenant_id"] == tenant_id:
                s["last_rotated_at"] = datetime.now(timezone.utc).isoformat()
                return s
        return None
