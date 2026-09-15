"""Feature Store service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class FeaturesService:
    """Curated feature store repository for machine learning and AI inference."""

    def __init__(self):
        self._features: Dict[str, Dict[str, Any]] = {}
        self._seed_default_features()

    def _seed_default_features(self):
        seeds = [
            ("customer_30d_spend_velocity", "CUSTOMER", "FLOAT", "SUM(amount) / 30", 60),
            ("customer_support_ticket_count", "CUSTOMER", "INTEGER", "COUNT(tickets)", 15),
            ("project_code_churn_rate", "PROJECT", "FLOAT", "AVG(lines_changed_per_pr)", 120),
            ("lead_engagement_score", "LEAD", "FLOAT", "weighted_sum(clicks, emails, visits)", 30),
        ]
        for name, ent, dtype, sql, fresh in seeds:
            fid = f"feat_{name}"
            self._features[fid] = {
                "id": fid,
                "tenant_id": "default_tenant",
                "name": name,
                "entity_name": ent,
                "data_type": dtype,
                "transformation_sql": sql,
                "freshness_minutes": fresh,
                "owner": "ml-eng@uzaii.com",
                "version": "v1.0.0",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

    def register_feature(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        fid = data.get("id") or f"feat_{uuid.uuid4().hex[:12]}"
        record = {
            "id": fid,
            "tenant_id": tenant_id,
            "name": data.get("name", "new_feature"),
            "entity_name": data.get("entity_name", "CUSTOMER"),
            "data_type": data.get("data_type", "FLOAT"),
            "transformation_sql": data.get("transformation_sql", "SELECT 1"),
            "freshness_minutes": data.get("freshness_minutes", 60),
            "owner": data.get("owner", "ml-eng@uzaii.com"),
            "version": data.get("version", "v1.0.0"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._features[fid] = record
        return record

    def list_features(self, entity_name: Optional[str] = None, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        feats = [f for f in self._features.values() if f.get("tenant_id") == tenant_id]
        if entity_name:
            feats = [f for f in feats if f.get("entity_name") == entity_name.upper()]
        return feats
