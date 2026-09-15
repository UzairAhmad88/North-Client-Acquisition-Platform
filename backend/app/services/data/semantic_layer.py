"""Semantic Layer service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class SemanticLayerService:
    """Manages semantic entity models, attributes, dimensions, and joins."""

    def __init__(self):
        self._models: Dict[str, Dict[str, Any]] = {}
        self._seed_default_models()

    def _seed_default_models(self):
        self._models["customer"] = {
            "id": "sem_customer",
            "tenant_id": "default_tenant",
            "entity_name": "customer",
            "underlying_source": "dim_customers",
            "attributes": [
                {"name": "customer_id", "type": "string", "is_pk": True},
                {"name": "name", "type": "string"},
                {"name": "revenue_arr", "type": "number"},
                {"name": "lifetime_value", "type": "number"},
                {"name": "status", "type": "string"},
                {"name": "churn_risk", "type": "string"},
            ],
            "primary_key": "customer_id",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._models["order"] = {
            "id": "sem_order",
            "tenant_id": "default_tenant",
            "entity_name": "order",
            "underlying_source": "fact_sales_transactions",
            "attributes": [
                {"name": "order_id", "type": "string", "is_pk": True},
                {"name": "customer_id", "type": "string", "is_fk": True},
                {"name": "amount", "type": "number"},
                {"name": "order_date", "type": "timestamp"},
            ],
            "primary_key": "order_id",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def register_model(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        entity_name = data.get("entity_name", "custom_entity")
        model_id = f"sem_{entity_name.lower()}"
        record = {
            "id": model_id,
            "tenant_id": tenant_id,
            "entity_name": entity_name,
            "underlying_source": data.get("underlying_source", f"table_{entity_name}"),
            "attributes": data.get("attributes", []),
            "primary_key": data.get("primary_key", "id"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._models[entity_name] = record
        return record

    def get_model(self, entity_name: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        m = self._models.get(entity_name)
        if m and m.get("tenant_id") == tenant_id:
            return m
        return None

    def list_models(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [m for m in self._models.values() if m.get("tenant_id") == tenant_id]
