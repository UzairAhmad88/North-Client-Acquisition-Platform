"""Metadata Management service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class MetadataService:
    """Stores Technical, Business, Operational, Security, and Lineage metadata."""

    def __init__(self):
        self._metadata_store: Dict[str, Dict[str, Any]] = {}

    def attach_metadata(
        self, asset_id: str, category: str, properties: Dict[str, Any], tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        mid = f"meta_{uuid.uuid4().hex[:12]}"
        record = {
            "id": mid,
            "tenant_id": tenant_id,
            "asset_id": asset_id,
            "category": category,  # TECHNICAL, BUSINESS, OPERATIONAL, SECURITY, AI, LINEAGE
            "properties": properties,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._metadata_store[mid] = record
        return record

    def get_asset_metadata(self, asset_id: str, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [m for m in self._metadata_store.values() if m.get("tenant_id") == tenant_id and m.get("asset_id") == asset_id]
