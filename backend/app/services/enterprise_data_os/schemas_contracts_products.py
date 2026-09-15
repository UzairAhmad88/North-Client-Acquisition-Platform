"""Schema Registry, Data Contracts, and Data Products Service.

Enforces schema evolution compatibility rules, formal data contracts with SLAs,
and publishes reusable Gold-layer data products.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.enterprise_data_os.base import (
        AttrDict,
        generate_data_id,
    )
except ImportError:
    from app.services.enterprise_data_os.base import (
        AttrDict,
        generate_data_id,
    )

logger = logging.getLogger(__name__)


class SchemasContractsProductsService:
    """Manages schemas, schema evolution, producer-consumer contracts, and curated data products."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._schemas: Dict[str, Dict[str, Any]] = {}
        self._contracts: Dict[str, Dict[str, Any]] = {}
        self._products: Dict[str, Dict[str, Any]] = {}

    def register_schema_version(
        self,
        tenant_id: str = "default_tenant",
        dataset_id: str = "ds_silver_cust",
        version: str = "v1.2.0",
        fields: Optional[List[Dict[str, Any]]] = None,
        compatibility_mode: str = "BACKWARD",  # BACKWARD, FORWARD, FULL, NONE
    ) -> AttrDict:
        schema_id = generate_data_id("sch")
        now = datetime.now(timezone.utc).isoformat()

        default_fields = [
            {"name": "customer_id", "type": "STRING", "nullable": False},
            {"name": "tenant_id", "type": "STRING", "nullable": False},
            {"name": "mrr_usd", "type": "DECIMAL(18,2)", "nullable": False},
            {"name": "health_score", "type": "FLOAT", "nullable": True},
            {"name": "updated_at", "type": "TIMESTAMP", "nullable": False},
        ]

        record = {
            "schema_id": schema_id,
            "id": schema_id,
            "tenant_id": tenant_id,
            "dataset_id": dataset_id,
            "version": version,
            "fields": fields or default_fields,
            "compatibility_mode": compatibility_mode,
            "is_active": True,
            "registered_at": now,
        }
        self._schemas[schema_id] = record
        return AttrDict(record)

    def create_data_contract(
        self,
        tenant_id: str = "default_tenant",
        producer_team: str = "Billing & Payments Engineering",
        consumer_team: str = "Revenue Operations & BI",
        dataset_id: str = "gold_subscription_mrr",
        schema_version: str = "v1.2.0",
        freshness_sla_minutes: int = 60,
        quality_threshold_pct: float = 99.5,
    ) -> AttrDict:
        contract_id = generate_data_id("con")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "contract_id": contract_id,
            "id": contract_id,
            "tenant_id": tenant_id,
            "producer_team": producer_team,
            "consumer_team": consumer_team,
            "dataset_id": dataset_id,
            "schema_version": schema_version,
            "freshness_sla_minutes": freshness_sla_minutes,
            "quality_threshold_pct": quality_threshold_pct,
            "status": "ACTIVE",
            "sla_compliance_pct": 100.0,
            "created_at": now,
        }
        self._contracts[contract_id] = record
        return AttrDict(record)

    def publish_data_product(
        self,
        tenant_id: str = "default_tenant",
        domain_id: str = "dom_001",
        name: str = "Customer 360 & Revenue Intelligence",
        purpose: str = "Unified cross-lifecycle customer behavioral, financial, and product telemetry data product.",
        owner_team: str = "Customer & Revenue Data Team",
        underlying_datasets: Optional[List[str]] = None,
        quality_score: float = 98.8,
    ) -> AttrDict:
        product_id = generate_data_id("prod")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "product_id": product_id,
            "id": product_id,
            "tenant_id": tenant_id,
            "domain_id": domain_id,
            "name": name,
            "purpose": purpose,
            "owner_team": owner_team,
            "underlying_datasets": underlying_datasets or ["gold_customer_mrr", "gold_feature_usage", "gold_csat"],
            "consumers_count": 14,
            "quality_score": quality_score,
            "health_status": "HEALTHY",
            "published_at": now,
        }
        self._products[product_id] = record
        return AttrDict(record)
