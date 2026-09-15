"""Token Management & API Key Verification Service."""
import uuid, hashlib
from typing import Dict, Any, Optional, List, Optional, List
from datetime import datetime, timezone

class TokenSecurityService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._tokens: List[Dict[str, Any]] = []

    def create_token(self, identity_id: str, token_name: str, scopes: List[str], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        secret = f"czt_{uuid.uuid4().hex}"
        prefix = secret[:8]
        hashed = hashlib.sha256(secret.encode()).hexdigest()
        rec = {
            "id": f"tok_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "identity_id": identity_id,
            "token_name": token_name,
            "token_prefix": prefix,
            "hashed_secret": hashed,
            "scopes": scopes,
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._tokens.append(rec)
        return {"id": rec["id"], "token_name": token_name, "raw_secret": secret, "prefix": prefix}
