"""Schema Registry & Evolution service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class SchemaRegistryService:
    """Tracks schema evolution, backward/forward compatibility, and breaking changes."""

    def __init__(self):
        self._schemas: Dict[str, Dict[str, Any]] = {}

    def register_schema(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        subject = data.get("subject", "events-default")
        schema_id = data.get("id") or f"schema_{uuid.uuid4().hex[:12]}"
        record = {
            "id": schema_id,
            "tenant_id": tenant_id,
            "subject": subject,
            "schema_type": data.get("schema_type", "JSON"),
            "version": data.get("version", "v1.0.0"),
            "fields": data.get("fields", [
                {"name": "id", "type": "string", "required": True},
                {"name": "timestamp", "type": "string", "required": True},
            ]),
            "compatibility": data.get("compatibility", "BACKWARD"),
            "producer": data.get("producer", "system-producer@uzaii.com"),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._schemas[subject] = record
        return record

    def get_schema(self, subject: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        s = self._schemas.get(subject)
        if s and s.get("tenant_id") == tenant_id:
            return s
        return None

    def list_schemas(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [s for s in self._schemas.values() if s.get("tenant_id") == tenant_id]

    def check_compatibility(self, subject: str, new_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        existing = self._schemas.get(subject)
        if not existing:
            return {"compatible": True, "breaking_changes": []}
        
        old_fields = {f["name"] for f in existing.get("fields", []) if f.get("required")}
        new_names = {f["name"] for f in new_fields}
        removed_required = list(old_fields - new_names)

        is_compat = len(removed_required) == 0
        return {
            "compatible": is_compat,
            "mode": existing.get("compatibility", "BACKWARD"),
            "breaking_changes": [f"Removed required field: {f}" for f in removed_required],
        }
