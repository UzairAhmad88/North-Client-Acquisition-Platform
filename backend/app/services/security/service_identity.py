"""Machine-to-Machine & Service Identity Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

class ServiceIdentityService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self._services: List[Dict[str, Any]] = []

    def register_service(self, service_name: str, allowed_endpoints: List[str], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        record = {
            "id": f"svcid_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "service_name": service_name,
            "allowed_endpoints": allowed_endpoints,
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._services.append(record)
        return record
