"""Data Catalog & Discovery service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class CatalogService:
    """Manages searchable enterprise data catalog across datasets, tables, models, and reports."""

    def __init__(self):
        self._assets: Dict[str, Dict[str, Any]] = {}
        self._seed_default_catalog()

    def _seed_default_catalog(self):
        seeds = [
            ("dim_customers", "TABLE", "Core customer master dimension table with LTV and segments.", "Customers", "INTERNAL", 99.2),
            ("fact_sales_transactions", "TABLE", "Hourly partitioned sales transactions and billing line items.", "Sales", "CONFIDENTIAL", 99.8),
            ("customer_churn_prediction_v2", "MODEL", "XGBoost classifier predicting 30-day customer churn risk.", "AI", "INTERNAL", 94.5),
            ("monthly_revenue_board_deck", "REPORT", "Certified monthly financial statements for board review.", "Finance", "RESTRICTED", 100.0),
            ("knowledge_rag_embeddings", "DATASET", "Vector embeddings of product and technical documentation.", "AI", "INTERNAL", 98.0),
        ]
        for name, a_type, desc, domain, sens, q in seeds:
            aid = f"cat_{name}"
            self._assets[aid] = {
                "id": aid,
                "tenant_id": "default_tenant",
                "name": name,
                "asset_type": a_type,
                "description": desc,
                "owner": "steward@uzaii.com",
                "domain": domain,
                "tags": [domain.lower(), a_type.lower(), "certified"],
                "sensitivity": sens,
                "quality_score": q,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }

    def register_asset(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        asset_id = data.get("id") or f"cat_{uuid.uuid4().hex[:12]}"
        record = {
            "id": asset_id,
            "tenant_id": tenant_id,
            "name": data.get("name", "Unnamed Asset"),
            "asset_type": data.get("asset_type", "DATASET"),
            "description": data.get("description", ""),
            "owner": data.get("owner", "steward@uzaii.com"),
            "domain": data.get("domain", "General"),
            "tags": data.get("tags", []),
            "sensitivity": data.get("sensitivity", "INTERNAL"),
            "quality_score": data.get("quality_score", 95.0),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._assets[asset_id] = record
        return record

    def search_catalog(self, query: str = "", domain: Optional[str] = None, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        results = [a for a in self._assets.values() if a.get("tenant_id") == tenant_id]
        if domain:
            results = [a for a in results if a.get("domain", "").lower() == domain.lower()]
        if query:
            q_lower = query.lower()
            results = [
                a for a in results
                if q_lower in a["name"].lower() or q_lower in (a.get("description") or "").lower() or any(q_lower in t.lower() for t in a.get("tags", []))
            ]
        return results

    def get_asset(self, asset_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        asset = self._assets.get(asset_id)
        if asset and asset.get("tenant_id") == tenant_id:
            return asset
        return None
