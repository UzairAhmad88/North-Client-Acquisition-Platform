"""Data Warehouse dimensional modeling service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class WarehouseService:
    """Manages dimensional models (Facts, Dimensions, Aggregations, Slowly Changing Dimensions)."""

    def __init__(self):
        self._tables: Dict[str, Dict[str, Any]] = {}

    def register_table(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        table_id = data.get("id") or f"wh_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        record = {
            "id": table_id,
            "tenant_id": tenant_id,
            "table_name": data.get("table_name", "fact_orders"),
            "model_type": data.get("model_type", "FACT"),  # FACT, DIMENSION, MEASURE, AGGREGATION, SCD2
            "schema_fields": data.get("schema_fields", []),
            "primary_keys": data.get("primary_keys", ["id"]),
            "surrogate_key": data.get("surrogate_key"),
            "is_scd": data.get("is_scd", False),
            "row_count": data.get("row_count", 500000),
            "created_at": now_iso,
        }
        self._tables[table_id] = record
        return record

    def list_tables(self, model_type: Optional[str] = None, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        tables = [t for t in self._tables.values() if t.get("tenant_id") == tenant_id]
        if model_type:
            tables = [t for t in tables if t.get("model_type") == model_type.upper()]
        return tables
