"""Service Catalog & Dependency Topology Service."""
import uuid
from typing import Dict, Any, List, Optional

class ServiceCatalogTopologyService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._services: List[Dict[str, Any]] = [
            {"id": "svc_api_gateway", "name": "API Gateway", "owner_team": "Platform", "dependencies": ["svc_auth", "svc_billing"], "health_status": "HEALTHY"},
            {"id": "svc_billing", "name": "Billing Engine", "owner_team": "Finance Eng", "dependencies": ["db_postgres"], "health_status": "HEALTHY"},
        ]

    def list_services(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return self._services
