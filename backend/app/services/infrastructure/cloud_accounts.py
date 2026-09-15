"""Cloud Accounts & Provider Abstraction Service."""
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class CloudAccountManagementService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._accounts: List[Dict[str, Any]] = []

    def register_account(self, provider: str, account_identifier: str, organization: str = "Uzaii Enterprise", environment: str = "PRODUCTION", default_region: str = "us-east-1", tenant_id: str = "default_tenant") -> Dict[str, Any]:
        rec = {
            "id": f"acc_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "provider": provider,
            "account_identifier": account_identifier,
            "organization": organization,
            "environment": environment,
            "default_region": default_region,
            "cost_center": "INFRA-CORE",
            "owner": "cloud-admin@enterprise.internal",
            "status": "ACTIVE",
            "security_state": "COMPLIANT",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._accounts.append(rec)
        return rec

    def list_accounts(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [a for a in self._accounts if a["tenant_id"] == tenant_id]
