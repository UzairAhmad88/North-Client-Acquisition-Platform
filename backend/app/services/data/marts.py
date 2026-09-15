"""Domain Data Marts service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class MartsService:
    """Manages domain-specific Data Marts (Sales, Finance, Customers, Operations, Engineering, AI)."""

    def __init__(self):
        self._marts: Dict[str, Dict[str, Any]] = {}
        self._seed_default_marts()

    def _seed_default_marts(self):
        domains = ["Sales", "Finance", "Marketing", "Customers", "Operations", "Engineering", "AI", "Risk"]
        for d in domains:
            mid = f"mart_{d.lower()}"
            self._marts[mid] = {
                "id": mid,
                "tenant_id": "default_tenant",
                "name": f"{d} Data Mart",
                "domain": d,
                "description": f"Curated dimensional aggregates and facts for {d} team.",
                "underlying_tables": [f"fact_{d.lower()}_events", f"dim_{d.lower()}_entities"],
                "target_audiences": [f"{d.lower()}-analysts", "leadership", "ai-agents"],
                "status": "ACTIVE",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

    def register_mart(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        mart_id = data.get("id") or f"mart_{uuid.uuid4().hex[:12]}"
        record = {
            "id": mart_id,
            "tenant_id": tenant_id,
            "name": data.get("name", "Custom Mart"),
            "domain": data.get("domain", "Operations"),
            "description": data.get("description", ""),
            "underlying_tables": data.get("underlying_tables", []),
            "target_audiences": data.get("target_audiences", ["analysts"]),
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._marts[mart_id] = record
        return record

    def list_marts(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [m for m in self._marts.values() if m.get("tenant_id") == tenant_id]
