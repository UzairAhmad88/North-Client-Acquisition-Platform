"""Data Pipelines, DAG Orchestration, Lakehouse Layers (Bronze/Silver/Gold) and Storage Service.

Manages data engineering pipelines, DAG workflow dependencies, and Bronze/Silver/Gold
storage tiers with format abstractions (Parquet, Delta, Iceberg).
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.enterprise_data_os.base import (
        AttrDict,
        DataLayerType,
        DataClassification,
        generate_data_id,
    )
except ImportError:
    from app.services.enterprise_data_os.base import (
        AttrDict,
        DataLayerType,
        DataClassification,
        generate_data_id,
    )

logger = logging.getLogger(__name__)


class PipelinesLakehouseStorageService:
    """Manages transformation pipelines, Lakehouse tier datasets, and storage objects."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._pipelines: Dict[str, Dict[str, Any]] = {}
        self._datasets: Dict[str, Dict[str, Any]] = {}

    def create_data_pipeline(
        self,
        tenant_id: str = "default_tenant",
        name: str = "silver_customer_enrichment_pipeline",
        source_datasets: Optional[List[str]] = None,
        target_dataset: str = "silver_customers_cleansed",
        schedule_type: str = "CRON_HOURLY",
        sla_minutes: int = 45,
        owner_team: str = "Data Engineering",
    ) -> AttrDict:
        pipeline_id = generate_data_id("pipe")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "pipeline_id": pipeline_id,
            "id": pipeline_id,
            "tenant_id": tenant_id,
            "name": name,
            "source_datasets": source_datasets or ["bronze_raw_users", "bronze_crm_accounts"],
            "target_dataset": target_dataset,
            "schedule_type": schedule_type,
            "sla_minutes": sla_minutes,
            "status": "ACTIVE",
            "owner_team": owner_team,
            "last_run_status": "SUCCESS",
            "created_at": now,
        }
        self._pipelines[pipeline_id] = record
        return AttrDict(record)

    def register_lakehouse_dataset(
        self,
        tenant_id: str = "default_tenant",
        domain_id: str = "dom_001",
        name: str = "silver_customer_profiles",
        layer: str = DataLayerType.SILVER.value,
        format_type: str = "PARQUET",
        storage_uri: str = "s3://uzaii-lakehouse-silver/customer_profiles/",
        partition_keys: Optional[List[str]] = None,
        record_count: int = 84000,
        size_mb: float = 248.5,
        classification: str = DataClassification.INTERNAL.value,
    ) -> AttrDict:
        dataset_id = generate_data_id("ds")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "dataset_id": dataset_id,
            "id": dataset_id,
            "tenant_id": tenant_id,
            "domain_id": domain_id,
            "name": name,
            "layer": layer,
            "format": format_type,
            "storage_uri": storage_uri,
            "partition_keys": partition_keys or ["tenant_id", "year", "month"],
            "record_count": record_count,
            "size_mb": size_mb,
            "classification": classification,
            "quality_status": "VALIDATED",
            "created_at": now,
        }
        self._datasets[dataset_id] = record
        return AttrDict(record)
