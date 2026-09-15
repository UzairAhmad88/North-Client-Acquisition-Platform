"""Engineering Projects Management Service."""
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class EngineeringProjectService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._projects: List[Dict[str, Any]] = []

    def create_project(self, payload: Any, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        data = payload if isinstance(payload, dict) else payload.dict() if hasattr(payload, "dict") else payload.model_dump()
        proj_id = data.get("id") or f"proj_{uuid.uuid4().hex[:12]}"
        record = {
            "id": proj_id,
            "tenant_id": tenant_id,
            "name": data.get("name", "Core Platform"),
            "description": data.get("description", "Enterprise software platform"),
            "owner": data.get("owner", "platform-lead@corp.internal"),
            "team": data.get("team", "Core Platform Team"),
            "status": "ACTIVE",
            "tech_stack": data.get("tech_stack", ["Python", "FastAPI", "TypeScript", "Next.js", "Docker"]),
            "environments": data.get("environments", ["DEVELOPMENT", "STAGING", "PRODUCTION"]),
            "budget_usd": float(data.get("budget_usd", 50000.0)),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._projects.append(record)
        return record

    def list_projects(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [p for p in self._projects if p["tenant_id"] == tenant_id]
