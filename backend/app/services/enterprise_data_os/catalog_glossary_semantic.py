"""Data Catalog, Business Glossary, and Centralized Semantic Layer Service.

Powers unified catalog search with natural language indexing, standardizes business terms,
and manages the single source of truth semantic metrics layer.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.enterprise_data_os.base import (
        AttrDict,
        DataClassification,
        generate_data_id,
    )
except ImportError:
    from app.services.enterprise_data_os.base import (
        AttrDict,
        DataClassification,
        generate_data_id,
    )

logger = logging.getLogger(__name__)


class CatalogGlossarySemanticService:
    """Manages data catalog discovery, business glossary, and semantic metrics layer."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._assets: Dict[str, Dict[str, Any]] = {}
        self._glossary: Dict[str, Dict[str, Any]] = {}
        self._semantic_metrics: Dict[str, Dict[str, Any]] = {}

    def register_catalog_asset(
        self,
        tenant_id: str = "default_tenant",
        asset_name: str = "gold_customer_arr_mart",
        asset_type: str = "TABLE",  # DATASET, TABLE, COLUMN, METRIC, DASHBOARD
        domain_name: str = "Finance & Revenue",
        owner_email: str = "rev-ops@uzaii.com",
        classification: str = DataClassification.INTERNAL.value,
        quality_score: float = 96.5,
        tags: Optional[List[str]] = None,
        description: str = "Aggregated monthly and annual recurring revenue by customer and subscription tier.",
    ) -> AttrDict:
        asset_id = generate_data_id("ast")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "asset_id": asset_id,
            "id": asset_id,
            "tenant_id": tenant_id,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "domain_name": domain_name,
            "owner_email": owner_email,
            "classification": classification,
            "quality_score": quality_score,
            "tags": tags or ["revenue", "finance", "arr", "customer360"],
            "description": description,
            "indexed_at": now,
        }
        self._assets[asset_id] = record
        return AttrDict(record)

    def define_glossary_term(
        self,
        tenant_id: str = "default_tenant",
        term_name: str = "Annual Recurring Revenue (ARR)",
        definition: str = "Normalized annualized recurring revenue run-rate derived from active paid subscriptions.",
        domain_name: str = "Finance",
        owner_email: str = "vp-finance@uzaii.com",
        synonyms: Optional[List[str]] = None,
        related_metrics: Optional[List[str]] = None,
    ) -> AttrDict:
        term_id = generate_data_id("term")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "term_id": term_id,
            "id": term_id,
            "tenant_id": tenant_id,
            "term_name": term_name,
            "definition": definition,
            "domain_name": domain_name,
            "owner_email": owner_email,
            "synonyms": synonyms or ["Annual Run Rate", "ARR"],
            "related_metrics": related_metrics or ["mrr", "net_revenue_retention"],
            "created_at": now,
        }
        self._glossary[term_id] = record
        return AttrDict(record)

    def define_semantic_metric(
        self,
        tenant_id: str = "default_tenant",
        name: str = "Customer Lifetime Value (LTV)",
        definition: str = "Gross margin-adjusted average revenue per account divided by account churn rate.",
        formula_sql: str = "(arpu_monthly * gross_margin_pct) / nullif(monthly_churn_rate, 0)",
        dimensions: Optional[List[str]] = None,
        source_table: str = "gold_customer_economics_mart",
        owner_team: str = "Revenue Growth & Finance",
    ) -> AttrDict:
        metric_id = generate_data_id("met")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "metric_id": metric_id,
            "id": metric_id,
            "tenant_id": tenant_id,
            "name": name,
            "definition": definition,
            "formula_sql": formula_sql,
            "dimensions": dimensions or ["tier", "geography", "cohort_month", "sales_channel"],
            "source_table": source_table,
            "owner_team": owner_team,
            "is_authoritative": True,
            "created_at": now,
        }
        self._semantic_metrics[metric_id] = record
        return AttrDict(record)
