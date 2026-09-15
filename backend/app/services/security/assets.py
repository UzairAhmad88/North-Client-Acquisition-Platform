"""Asset Security Management Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.autonomous_cybersecurity_zero_trust import CztAssetModel, CztAssetRelationshipModel

class AssetSecurityService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self._assets: List[Dict[str, Any]] = []
        self._relationships: List[Dict[str, Any]] = []

    def register_asset(self, payload: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        asset_id = payload.get("id") or f"asset_{uuid.uuid4().hex[:12]}"
        record = {
            "id": asset_id,
            "tenant_id": tenant_id,
            "name": payload.get("name", "Unnamed Asset"),
            "asset_type": payload.get("asset_type", "SERVER"),
            "owner": payload.get("owner", "security-team"),
            "environment": payload.get("environment", "PRODUCTION"),
            "criticality": payload.get("criticality", "HIGH"),
            "ip_address": payload.get("ip_address"),
            "hostname": payload.get("hostname"),
            "location": payload.get("location", "us-east-1"),
            "security_state": payload.get("security_state", "SECURE"),
            "risk_score": float(payload.get("risk_score", 0.1)),
            "tags": payload.get("tags", []),
            "metadata_context": payload.get("metadata_context", {}),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._assets.append(record)
        return record

    def list_assets(self, tenant_id: str = "default_tenant", asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        return [a for a in self._assets if a["tenant_id"] == tenant_id and (asset_type is None or a["asset_type"] == asset_type)]

    def link_assets(self, source_id: str, target_id: str, relationship_type: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        rel = {
            "id": f"areln_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "source_asset_id": source_id,
            "target_asset_id": target_id,
            "relationship_type": relationship_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._relationships.append(rel)
        return rel
