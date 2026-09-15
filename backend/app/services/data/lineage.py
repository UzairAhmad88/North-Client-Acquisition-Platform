"""Data Lineage & Column-Level Lineage service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class LineageService:
    """Manages end-to-end dataset DAG lineage and column-level dependency graphs."""

    def __init__(self):
        self._dataset_edges: List[Dict[str, Any]] = []
        self._column_edges: List[Dict[str, Any]] = []
        self._seed_default_lineage()

    def _seed_default_lineage(self):
        # Default chain: PostgreSQL Source -> Bronze Raw -> Silver Cleaned -> Gold Data Product -> Metric -> Executive Dashboard
        chain = [
            ("SOURCE", "postgres_crm_leads", "DATASET", "lake_leads_bronze", "Ingestion Job"),
            ("DATASET", "lake_leads_bronze", "DATASET", "lake_leads_silver", "Cleanse & Deduplicate"),
            ("DATASET", "lake_leads_silver", "PRODUCT", "customer_360_product", "Curate & Feature Enrich"),
            ("PRODUCT", "customer_360_product", "METRIC", "metric_qualified_lead_rate", "Aggregate Formula"),
            ("METRIC", "metric_qualified_lead_rate", "DASHBOARD", "executive_growth_command_center", "Visualization Widget"),
        ]
        for s_type, s_id, t_type, t_id, logic in chain:
            self._dataset_edges.append({
                "id": f"edge_{uuid.uuid4().hex[:8]}",
                "tenant_id": "default_tenant",
                "source_type": s_type,
                "source_id": s_id,
                "target_type": t_type,
                "target_id": t_id,
                "transformation_logic": logic,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })

        # Column lineage
        col_chain = [
            ("crm_leads", "email", "leads_bronze", "raw_email", "direct_copy"),
            ("leads_bronze", "raw_email", "leads_silver", "cleaned_email", "lower(trim(raw_email))"),
            ("leads_silver", "cleaned_email", "customer_360", "canonical_email", "hash_or_mask_if_unauthorized"),
        ]
        for s_tab, s_col, t_tab, t_col, expr in col_chain:
            self._column_edges.append({
                "id": f"coledge_{uuid.uuid4().hex[:8]}",
                "tenant_id": "default_tenant",
                "source_table": s_tab,
                "source_column": s_col,
                "target_table": t_tab,
                "target_column": t_col,
                "transform_expression": expr,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })

    def add_edge(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        d = dict(data)
        if "source" in d and "source_id" not in d:
            d["source_id"] = d["source"]
        if "target" in d and "target_id" not in d:
            d["target_id"] = d["target"]
        if "transformation" in d and "transformation_logic" not in d:
            d["transformation_logic"] = d["transformation"]
        edge = self.add_lineage_edge(d, tenant_id)
        edge["source"] = edge["source_id"]
        edge["target"] = edge["target_id"]
        return edge

    def add_lineage_edge(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        edge = {
            "id": f"edge_{uuid.uuid4().hex[:8]}",
            "tenant_id": tenant_id,
            "source_type": data.get("source_type", "DATASET"),
            "source_id": data.get("source_id"),
            "target_type": data.get("target_type", "DATASET"),
            "target_id": data.get("target_id"),
            "transformation_logic": data.get("transformation_logic", "ETL"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._dataset_edges.append(edge)
        return edge

    def add_column_lineage_edge(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        edge = {
            "id": f"coledge_{uuid.uuid4().hex[:8]}",
            "tenant_id": tenant_id,
            "source_table": data.get("source_table"),
            "source_column": data.get("source_column"),
            "target_table": data.get("target_table"),
            "target_column": data.get("target_column"),
            "transform_expression": data.get("transform_expression", "DIRECT"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._column_edges.append(edge)
        return edge

    def get_dataset_lineage(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [e for e in self._dataset_edges if e.get("tenant_id") == tenant_id]

    def get_column_lineage(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [c for c in self._column_edges if c.get("tenant_id") == tenant_id]
