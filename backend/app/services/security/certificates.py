"""Certificate Inventory & Expiration Alerting Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timedelta, timezone

class CertificateSecurityService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._certs: List[Dict[str, Any]] = []

    def register_certificate(self, domain: str, issuer: str, days_valid: int = 90, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        rec = {
            "id": f"cert_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "domain_name": domain,
            "issuer": issuer,
            "thumbprint_sha256": uuid.uuid4().hex,
            "valid_from": now.isoformat(),
            "valid_until": (now + timedelta(days=days_valid)).isoformat(),
            "status": "VALID" if days_valid > 15 else "EXPIRING_SOON",
        }
        self._certs.append(rec)
        return rec

    def list_certificates(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [c for c in self._certs if c["tenant_id"] == tenant_id]
