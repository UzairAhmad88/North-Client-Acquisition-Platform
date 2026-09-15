"""Data Sources service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class SourcesService:
    """Manages enterprise data source registry, connectivity credentials, and metadata."""

    def __init__(self):
        self._sources: Dict[str, Dict[str, Any]] = {}

    def register_source(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        source_id = data.get("id") or f"src_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        record = {
            "id": source_id,
            "tenant_id": tenant_id,
            "name": data.get("name", "Unnamed Source"),
            "source_type": data.get("source_type", "DATABASE"),
            "provider": data.get("provider", "POSTGRES"),
            "owner": data.get("owner", "data-team@uzaii.com"),
            "team": data.get("team", "Data Engineering"),
            "environment": data.get("environment", "PRODUCTION"),
            "connection_config": data.get("connection_config", {}),
            "auth_ref": data.get("auth_ref") or f"vault://keys/{source_id}",
            "schema_definition": data.get("schema_definition", {}),
            "refresh_rate": data.get("refresh_rate", "HOURLY"),
            "sensitivity": data.get("sensitivity", "INTERNAL"),
            "classification": data.get("classification", "CONFIDENTIAL"),
            "status": "ACTIVE",
            "last_sync_at": now_iso,
            "created_at": now_iso,
        }
        self._sources[source_id] = record
        return record

    def get_source(self, source_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        src = self._sources.get(source_id)
        if src and src.get("tenant_id") == tenant_id:
            return src
        return None

    def list_sources(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [s for s in self._sources.values() if s.get("tenant_id") == tenant_id]

    def update_source_status(self, source_id: str, status: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        src = self.get_source(source_id, tenant_id)
        if src:
            src["status"] = status
            src["last_sync_at"] = datetime.now(timezone.utc).isoformat()
            return src
        return None
