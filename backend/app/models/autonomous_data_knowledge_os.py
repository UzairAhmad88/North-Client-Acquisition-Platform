"""Phase 65 — Autonomous Data & Knowledge Operating System SQLAlchemy Models.

Comprehensive enterprise data layer linking sources, connectors, ingestion,
lakehouse, warehouse, marts, contracts, schemas, quality, lineage, catalog,
glossary, semantic metrics, master data & entity resolution, knowledge graph,
document intelligence, hybrid enterprise search, AI memory, datasets & features,
governance, privacy & masking, finops costs, security, SLOs, and autonomous agents.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

try:
    from app.models.base import Base
except ImportError:
    from app.models.base import Base


# ----------------------------------------------------------------------
# 1. DATA SOURCES & CONNECTORS
# ----------------------------------------------------------------------
class AdkosDataSourceModel(Base):
    """Enterprise Data Source definition."""
    __tablename__ = "adkos_sources"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    source_type = Column(String(64), nullable=False)  # DATABASE, API, FILE, CLOUD, SAAS, STREAMING
    provider = Column(String(64), nullable=False)
    owner = Column(String(128), nullable=False)
    team = Column(String(128), nullable=False)
    environment = Column(String(64), default="PRODUCTION")
    connection_config = Column(JSON, default=dict)
    auth_ref = Column(String(128), nullable=True)  # Vault reference, zero plaintext
    schema_definition = Column(JSON, default=dict)
    refresh_rate = Column(String(64), default="HOURLY")
    sensitivity = Column(String(64), default="INTERNAL")
    classification = Column(String(64), default="CONFIDENTIAL")
    status = Column(String(64), default="ACTIVE")
    last_sync_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataConnectorModel(Base):
    """Standardized connector implementation metadata."""
    __tablename__ = "adkos_connectors"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    connector_type = Column(String(64), nullable=False)  # database, api, files, cloud, etc.
    name = Column(String(128), nullable=False)
    version = Column(String(32), default="v1.0.0")
    config_schema = Column(JSON, default=dict)
    capabilities = Column(JSON, default=list)  # batch, streaming, cdc, schema_discovery
    is_enabled = Column(Boolean, default=True)
    health_status = Column(String(64), default="HEALTHY")
    last_health_check = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataSourceCredentialModel(Base):
    """Vault-isolated credential mapping."""
    __tablename__ = "adkos_source_credentials"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_id = Column(String(64), nullable=False, index=True)
    vault_key_ref = Column(String(256), nullable=False)
    auth_type = Column(String(64), nullable=False)  # IAM, OAUTH2, MTLS, TOKEN
    rotated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)


class AdkosDataIngestionJobModel(Base):
    """Ingestion execution job."""
    __tablename__ = "adkos_ingestion_jobs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_id = Column(String(64), nullable=False, index=True)
    connector_id = Column(String(64), nullable=False)
    job_type = Column(String(64), default="BATCH")  # BATCH, STREAMING, CDC, ON_DEMAND
    status = Column(String(64), default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    records_ingested = Column(Integer, default=0)
    bytes_processed = Column(Float, default=0.0)
    duration_ms = Column(Float, default=0.0)
    watermark = Column(String(128), nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)


# ----------------------------------------------------------------------
# 2. PIPELINES & ORCHESTRATION
# ----------------------------------------------------------------------
class AdkosDataPipelineModel(Base):
    """ETL/ELT Transformation Pipeline DAG."""
    __tablename__ = "adkos_pipelines"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    trigger_type = Column(String(64), default="SCHEDULED")  # SCHEDULED, DEPENDENCY, EVENT, AI_TRIGGERED
    schedule_cron = Column(String(64), nullable=True)
    owner = Column(String(128), nullable=False)
    sla_minutes = Column(Integer, default=60)
    dependencies = Column(JSON, default=list)  # Pipeline IDs
    status = Column(String(64), default="ACTIVE")
    version = Column(String(32), default="v1.0.0")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosPipelineStepModel(Base):
    """Individual transform/validation step within a pipeline."""
    __tablename__ = "adkos_pipeline_steps"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    pipeline_id = Column(String(64), nullable=False, index=True)
    step_order = Column(Integer, default=1)
    name = Column(String(128), nullable=False)
    step_type = Column(String(64), nullable=False)  # EXTRACT, TRANSFORM, VALIDATE, LOAD, ENRICH
    config = Column(JSON, default=dict)
    retry_count = Column(Integer, default=3)


class AdkosPipelineRunModel(Base):
    """Pipeline run execution record."""
    __tablename__ = "adkos_pipeline_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    pipeline_id = Column(String(64), nullable=False, index=True)
    run_status = Column(String(64), default="RUNNING")
    records_transformed = Column(Integer, default=0)
    latency_seconds = Column(Float, default=0.0)
    logs = Column(JSON, default=list)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    finished_at = Column(DateTime, nullable=True)


class AdkosPipelineDependencyModel(Base):
    """Pipeline DAG edge dependencies."""
    __tablename__ = "adkos_pipeline_dependencies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    upstream_pipeline_id = Column(String(64), nullable=False)
    downstream_pipeline_id = Column(String(64), nullable=False)
    dependency_condition = Column(String(64), default="SUCCESS")


# ----------------------------------------------------------------------
# 3. LAKEHOUSE, WAREHOUSE & MARTS
# ----------------------------------------------------------------------
class AdkosDataLakeAssetModel(Base):
    """Bronze, Silver, Gold Layer assets in Data Lake."""
    __tablename__ = "adkos_lake_assets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    layer = Column(String(32), default="BRONZE")  # RAW, BRONZE, SILVER, GOLD
    format = Column(String(32), default="PARQUET")  # PARQUET, DELTA, ICEBERG
    storage_path = Column(String(256), nullable=False)
    partition_columns = Column(JSON, default=list)
    record_count = Column(Integer, default=0)
    size_mb = Column(Float, default=0.0)
    lineage_parent_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataWarehouseAssetModel(Base):
    """Dimensional modeling entities (Facts, Dimensions, Aggregations)."""
    __tablename__ = "adkos_warehouse_assets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    table_name = Column(String(128), nullable=False)
    model_type = Column(String(64), default="FACT")  # FACT, DIMENSION, MEASURE, AGGREGATION, SCD2
    schema_fields = Column(JSON, default=list)
    primary_keys = Column(JSON, default=list)
    surrogate_key = Column(String(64), nullable=True)
    is_scd = Column(Boolean, default=False)
    row_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataMartModel(Base):
    """Domain-specific Data Marts."""
    __tablename__ = "adkos_marts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    domain = Column(String(64), nullable=False)  # Sales, Finance, Customers, Operations, Engineering, AI, etc.
    description = Column(Text, nullable=True)
    underlying_tables = Column(JSON, default=list)
    target_audiences = Column(JSON, default=list)
    status = Column(String(64), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 4. DATA PRODUCTS, CONTRACTS & SCHEMAS
# ----------------------------------------------------------------------
class AdkosDataProductModel(Base):
    """Curated, Governed Data Product."""
    __tablename__ = "adkos_products"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(String(128), nullable=False)
    source_datasets = Column(JSON, default=list)
    contract_id = Column(String(64), nullable=True)
    schema_def = Column(JSON, default=dict)
    quality_score = Column(Float, default=99.0)
    sla_freshness_minutes = Column(Integer, default=60)
    security_classification = Column(String(64), default="INTERNAL")
    monthly_cost_usd = Column(Float, default=0.0)
    version = Column(String(32), default="v1.0.0")
    status = Column(String(64), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataProductVersionModel(Base):
    """Version history of Data Products."""
    __tablename__ = "adkos_product_versions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    product_id = Column(String(64), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    change_summary = Column(Text, nullable=True)
    schema_snapshot = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataProductConsumerModel(Base):
    """Consumers authorized for a Data Product."""
    __tablename__ = "adkos_product_consumers"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    product_id = Column(String(64), nullable=False, index=True)
    consumer_name = Column(String(128), nullable=False)
    consumer_type = Column(String(64), default="APPLICATION")  # APPLICATION, AGENT, DASHBOARD, TEAM
    sla_tier = Column(String(64), default="STANDARD")
    registered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataContractModel(Base):
    """Producer-Consumer Data Contract."""
    __tablename__ = "adkos_contracts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_name = Column(String(128), nullable=False)
    owner = Column(String(128), nullable=False)
    schema_rules = Column(JSON, default=dict)
    constraints = Column(JSON, default=list)
    freshness_sla_minutes = Column(Integer, default=60)
    quality_threshold_pct = Column(Float, default=98.0)
    compatibility_mode = Column(String(32), default="BACKWARD")
    version = Column(String(32), default="v1.0.0")
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataContractVersionModel(Base):
    """Contract version log."""
    __tablename__ = "adkos_contract_versions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    contract_id = Column(String(64), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    spec_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosSchemaRegistryModel(Base):
    """Schema Registry tracking schema evolution."""
    __tablename__ = "adkos_schema_registry"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    subject = Column(String(128), nullable=False, index=True)
    schema_type = Column(String(32), default="JSON")  # JSON, AVRO, PROTOBUF
    current_version = Column(String(32), default="v1.0.0")
    fields = Column(JSON, default=list)
    compatibility = Column(String(32), default="BACKWARD")
    producer = Column(String(128), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosSchemaVersionModel(Base):
    """Schema version detail."""
    __tablename__ = "adkos_schema_versions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    registry_id = Column(String(64), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    fields = Column(JSON, default=list)
    breaking_change = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 5. DATA QUALITY, OBSERVABILITY & INCIDENTS
# ----------------------------------------------------------------------
class AdkosDataQualityRuleModel(Base):
    """Quality rules (Completeness, Validity, Freshness, Accuracy, etc.)."""
    __tablename__ = "adkos_quality_rules"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_name = Column(String(128), nullable=False)
    dimension = Column(String(64), nullable=False)  # COMPLETENESS, ACCURACY, VALIDITY, FRESHNESS, INTEGRITY
    rule_type = Column(String(64), nullable=False)  # NOT_NULL, RANGE, REGEX, UNIQUE, ANOMALY
    target_column = Column(String(128), nullable=True)
    expression = Column(String(256), nullable=False)
    severity = Column(String(32), default="HIGH")
    is_active = Column(Boolean, default=True)


class AdkosDataQualityRunModel(Base):
    """Execution of quality rule set."""
    __tablename__ = "adkos_quality_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_name = Column(String(128), nullable=False)
    overall_score = Column(Float, default=100.0)
    completeness_score = Column(Float, default=100.0)
    validity_score = Column(Float, default=100.0)
    freshness_score = Column(Float, default=100.0)
    accuracy_score = Column(Float, default=100.0)
    rules_passed = Column(Integer, default=0)
    rules_failed = Column(Integer, default=0)
    executed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataQualityResultModel(Base):
    """Specific rule finding."""
    __tablename__ = "adkos_quality_results"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    run_id = Column(String(64), nullable=False, index=True)
    rule_id = Column(String(64), nullable=False)
    status = Column(String(32), default="PASSED")  # PASSED, FAILED
    failed_records_count = Column(Integer, default=0)
    failure_details = Column(JSON, default=dict)


class AdkosDataIncidentModel(Base):
    """Data Incident (Pipeline timeout, Drift, Quality breach)."""
    __tablename__ = "adkos_incidents"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    dataset_name = Column(String(128), nullable=False)
    pipeline_id = Column(String(64), nullable=True)
    severity = Column(String(32), default="SEV2")
    impact_scope = Column(Text, nullable=True)
    owner = Column(String(128), nullable=False)
    root_cause = Column(Text, nullable=True)
    status = Column(String(32), default="OPEN")  # OPEN, INVESTIGATING, MITIGATED, RESOLVED
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)


class AdkosDataIncidentEventModel(Base):
    """Timeline event in incident resolution."""
    __tablename__ = "adkos_incident_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    incident_id = Column(String(64), nullable=False, index=True)
    event_text = Column(Text, nullable=False)
    actor = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataIncidentPostmortemModel(Base):
    """Incident postmortem report."""
    __tablename__ = "adkos_incident_postmortems"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    incident_id = Column(String(64), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    preventative_actions = Column(JSON, default=list)
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 6. LINEAGE & COLUMN LINEAGE
# ----------------------------------------------------------------------
class AdkosDataLineageModel(Base):
    """Dataset-level end-to-end directed lineage graph edge."""
    __tablename__ = "adkos_lineage"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_type = Column(String(64), nullable=False)  # SOURCE, TABLE, DATASET, METRIC, DASHBOARD, MODEL
    source_id = Column(String(128), nullable=False)
    target_type = Column(String(64), nullable=False)
    target_id = Column(String(128), nullable=False)
    transformation_logic = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosColumnLineageModel(Base):
    """Column-level lineage edge."""
    __tablename__ = "adkos_column_lineage"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_table = Column(String(128), nullable=False)
    source_column = Column(String(128), nullable=False)
    target_table = Column(String(128), nullable=False)
    target_column = Column(String(128), nullable=False)
    transform_expression = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 7. CATALOG, METADATA & BUSINESS GLOSSARY
# ----------------------------------------------------------------------
class AdkosDataCatalogModel(Base):
    """Searchable Enterprise Data Catalog item."""
    __tablename__ = "adkos_catalog"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    asset_type = Column(String(64), nullable=False)  # TABLE, DATASET, FILE, API, METRIC, MODEL, REPORT, DOCUMENT, PRODUCT
    description = Column(Text, nullable=True)
    owner = Column(String(128), nullable=False)
    domain = Column(String(64), nullable=False)
    tags = Column(JSON, default=list)
    sensitivity = Column(String(32), default="INTERNAL")
    quality_score = Column(Float, default=95.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataMetadataModel(Base):
    """Technical, Business, Operational, Security, AI metadata."""
    __tablename__ = "adkos_metadata"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    asset_id = Column(String(64), nullable=False, index=True)
    category = Column(String(64), default="TECHNICAL")  # TECHNICAL, BUSINESS, OPERATIONAL, SECURITY, AI
    properties = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosBusinessGlossaryModel(Base):
    """Authoritative Business Terms & Glossary."""
    __tablename__ = "adkos_glossary"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    term_name = Column(String(128), nullable=False)
    definition = Column(Text, nullable=False)
    domain = Column(String(64), nullable=False)
    owner = Column(String(128), nullable=False)
    synonyms = Column(JSON, default=list)
    related_metrics = Column(JSON, default=list)
    status = Column(String(32), default="CERTIFIED")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosBusinessTermRelationshipModel(Base):
    """Relationships between glossary business terms."""
    __tablename__ = "adkos_business_term_relationships"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    term_id_a = Column(String(64), nullable=False)
    term_id_b = Column(String(64), nullable=False)
    relation = Column(String(64), default="SYNONYM")  # SYNONYM, BROADER, NARROWER, RELATED


# ----------------------------------------------------------------------
# 8. SEMANTIC LAYER & METRIC STORE
# ----------------------------------------------------------------------
class AdkosSemanticModel(Base):
    """Semantic abstraction modeling real-world business entities."""
    __tablename__ = "adkos_semantic_models"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    entity_name = Column(String(128), nullable=False)
    underlying_source = Column(String(128), nullable=False)
    attributes = Column(JSON, default=list)
    primary_key = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosSemanticRelationshipModel(Base):
    """Semantic joins and associations."""
    __tablename__ = "adkos_semantic_relationships"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    entity_a = Column(String(128), nullable=False)
    entity_b = Column(String(128), nullable=False)
    join_type = Column(String(32), default="ONE_TO_MANY")
    join_condition = Column(String(256), nullable=False)


class AdkosMetricModel(Base):
    """Governed single-source-of-truth business metric."""
    __tablename__ = "adkos_metrics"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    definition = Column(Text, nullable=False)
    formula_sql = Column(Text, nullable=False)
    source_table = Column(String(128), nullable=False)
    dimensions = Column(JSON, default=list)
    owner = Column(String(128), nullable=False)
    certification_status = Column(String(32), default="CERTIFIED")  # DRAFT, VERIFIED, CERTIFIED, DEPRECATED
    version = Column(String(32), default="v1.0.0")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosMetricDimensionModel(Base):
    """Dimensions for metric aggregation."""
    __tablename__ = "adkos_metric_dimensions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    metric_id = Column(String(64), nullable=False, index=True)
    dimension_name = Column(String(128), nullable=False)
    dimension_type = Column(String(32), default="STRING")


class AdkosMetricVersionModel(Base):
    """Version history of metric formulas."""
    __tablename__ = "adkos_metric_versions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    metric_id = Column(String(64), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    formula_sql = Column(Text, nullable=False)
    changed_by = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 9. MASTER DATA MANAGEMENT & ENTITY RESOLUTION
# ----------------------------------------------------------------------
class AdkosMasterEntityModel(Base):
    """Canonical golden master entity (Customer, Company, Product, etc.)."""
    __tablename__ = "adkos_master_entities"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False)  # CUSTOMER, COMPANY, EMPLOYEE, PRODUCT, VENDOR
    canonical_name = Column(String(128), nullable=False)
    attributes = Column(JSON, default=dict)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosEntityAliasModel(Base):
    """Synonyms and matched names for canonical entity."""
    __tablename__ = "adkos_entity_aliases"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    master_entity_id = Column(String(64), nullable=False, index=True)
    alias_name = Column(String(128), nullable=False)
    source_system = Column(String(64), nullable=False)


class AdkosEntityMatchModel(Base):
    """Fuzzy entity resolution pair."""
    __tablename__ = "adkos_entity_matches"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    master_entity_id = Column(String(64), nullable=False)
    matched_candidate_name = Column(String(128), nullable=False)
    match_score = Column(Float, default=0.95)
    evidence = Column(JSON, default=dict)
    status = Column(String(32), default="RESOLVED")  # RESOLVED, PENDING_REVIEW, REJECTED


class AdkosEntityMergeHistoryModel(Base):
    """Audit of merged master entities."""
    __tablename__ = "adkos_entity_merge_history"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    surviving_entity_id = Column(String(64), nullable=False)
    merged_entity_id = Column(String(64), nullable=False)
    merged_by = Column(String(128), nullable=False)
    merged_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 10. KNOWLEDGE GRAPH
# ----------------------------------------------------------------------
class AdkosKnowledgeNodeModel(Base):
    """Knowledge Graph Entity Node."""
    __tablename__ = "adkos_knowledge_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    label = Column(String(64), nullable=False)  # Person, Company, Customer, Product, Project, Requirement, Service, Dataset, etc.
    name = Column(String(128), nullable=False)
    properties = Column(JSON, default=dict)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosKnowledgeEdgeModel(Base):
    """Knowledge Graph Relationship Edge."""
    __tablename__ = "adkos_knowledge_edges"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    from_node_id = Column(String(64), nullable=False, index=True)
    to_node_id = Column(String(64), nullable=False, index=True)
    relationship_type = Column(String(64), nullable=False)  # OWNS, USES, DEPENDS_ON, IMPLEMENTS, PRODUCES, CONSUMES, etc.
    properties = Column(JSON, default=dict)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosKnowledgeSourceModel(Base):
    """Provenance citation for knowledge facts."""
    __tablename__ = "adkos_knowledge_sources"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    node_or_edge_id = Column(String(64), nullable=False)
    source_uri = Column(String(256), nullable=False)
    source_type = Column(String(64), default="DOCUMENT")
    extracted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosKnowledgeConflictModel(Base):
    """Contradictions surfaced between conflicting knowledge sources."""
    __tablename__ = "adkos_knowledge_conflicts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    node_id = Column(String(64), nullable=False)
    property_name = Column(String(128), nullable=False)
    value_a = Column(Text, nullable=False)
    source_a = Column(String(256), nullable=False)
    value_b = Column(Text, nullable=False)
    source_b = Column(String(256), nullable=False)
    status = Column(String(32), default="SURFACED")  # SURFACED, RESOLVED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 11. DOCUMENTS & ENTERPRISE SEARCH
# ----------------------------------------------------------------------
class AdkosDocumentModel(Base):
    """Document knowledge system entity."""
    __tablename__ = "adkos_documents"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    file_type = Column(String(32), nullable=False)  # PDF, DOCX, PPTX, TXT, MARKDOWN, HTML
    storage_uri = Column(String(256), nullable=False)
    summary = Column(Text, nullable=True)
    extracted_topics = Column(JSON, default=list)
    permissions = Column(JSON, default=list)
    version = Column(String(32), default="v1.0.0")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDocumentChunkModel(Base):
    """Chunked passages with embeddings for semantic RAG."""
    __tablename__ = "adkos_document_chunks"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    document_id = Column(String(64), nullable=False, index=True)
    chunk_index = Column(Integer, default=0)
    content = Column(Text, nullable=False)
    embedding_vector_id = Column(String(128), nullable=True)
    extracted_entities = Column(JSON, default=list)


class AdkosSearchIndexModel(Base):
    """Unified hybrid enterprise search index."""
    __tablename__ = "adkos_search_indexes"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    index_name = Column(String(128), nullable=False)
    doc_count = Column(Integer, default=0)
    last_indexed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosSearchQueryModel(Base):
    """Search query analytics and audit."""
    __tablename__ = "adkos_search_queries"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    query_text = Column(String(256), nullable=False)
    user_id = Column(String(128), nullable=False)
    results_count = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 12. AI MEMORY (WORKING, EPISODIC, SEMANTIC, ORGANIZATIONAL)
# ----------------------------------------------------------------------
class AdkosMemoryModel(Base):
    """Governed AI Enterprise Memory Object."""
    __tablename__ = "adkos_memories"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    content = Column(Text, nullable=False)
    memory_type = Column(String(64), default="SEMANTIC")  # WORKING, EPISODIC, SEMANTIC, PROCEDURAL, ORGANIZATIONAL
    source = Column(String(128), nullable=False)
    entity_ref = Column(String(128), nullable=True)
    confidence = Column(Float, default=0.9)
    classification = Column(String(64), default="OBSERVED")  # OBSERVED, DERIVED, INFERRED, HYPOTHESIS, USER_PROVIDED
    permissions = Column(JSON, default=list)
    sensitivity = Column(String(32), default="INTERNAL")
    version = Column(String(32), default="v1.0.0")
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosMemoryConflictModel(Base):
    """Memory contradiction log."""
    __tablename__ = "adkos_memory_conflicts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    memory_id_a = Column(String(64), nullable=False)
    memory_id_b = Column(String(64), nullable=False)
    conflict_reason = Column(Text, nullable=False)
    status = Column(String(32), default="UNRESOLVED")


# ----------------------------------------------------------------------
# 13. AI-READY DATASETS & FEATURE STORE
# ----------------------------------------------------------------------
class AdkosDatasetModel(Base):
    """Curated AI training/evaluation dataset."""
    __tablename__ = "adkos_datasets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    purpose = Column(String(64), default="TRAINING")  # TRAINING, EVALUATION, SYNTHETIC, INFERENCE
    version = Column(String(32), default="v1.0.0")
    row_count = Column(Integer, default=0)
    pii_cleansed = Column(Boolean, default=True)
    owner = Column(String(128), nullable=False)
    storage_uri = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosFeatureModel(Base):
    """Online/Offline ML Feature."""
    __tablename__ = "adkos_features"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    entity_name = Column(String(64), nullable=False)  # CUSTOMER, LEAD, PROJECT, ORDER
    data_type = Column(String(32), default="FLOAT")
    transformation_sql = Column(Text, nullable=False)
    freshness_minutes = Column(Integer, default=60)
    owner = Column(String(128), nullable=False)
    version = Column(String(32), default="v1.0.0")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 14. PRIVACY, ACCESS CONTROL & RETENTION
# ----------------------------------------------------------------------
class AdkosDataClassificationModel(Base):
    """Data sensitivity classification rules."""
    __tablename__ = "adkos_classifications"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_name = Column(String(128), nullable=False)
    column_name = Column(String(128), nullable=False)
    classification = Column(String(64), default="INTERNAL")  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, HIGHLY_RESTRICTED
    pii_type = Column(String(64), nullable=True)  # EMAIL, PHONE, SSN, NAME, FINANCIAL
    masking_strategy = Column(String(64), default="REDACT")  # REDACT, HASH, TOKENIZE, PARTIAL_MASK
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosPiiFindingModel(Base):
    """Discovered PII instances."""
    __tablename__ = "adkos_pii_findings"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_name = Column(String(128), nullable=False)
    column_name = Column(String(128), nullable=False)
    sample_masked_value = Column(String(128), nullable=False)
    confidence = Column(Float, default=0.95)
    reviewed = Column(Boolean, default=False)
    discovered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataAccessPolicyModel(Base):
    """RBAC / ABAC / Row-Level policy."""
    __tablename__ = "adkos_access_policies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    policy_name = Column(String(128), nullable=False)
    dataset_name = Column(String(128), nullable=False)
    allowed_roles = Column(JSON, default=list)
    row_filter_sql = Column(String(256), nullable=True)
    masked_columns = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)


class AdkosDataAccessRequestModel(Base):
    """Workflow access requests."""
    __tablename__ = "adkos_access_requests"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    user_id = Column(String(128), nullable=False)
    dataset_name = Column(String(128), nullable=False)
    justification = Column(Text, nullable=False)
    status = Column(String(32), default="PENDING")  # PENDING, APPROVED, REJECTED, EXPIRED
    approver_id = Column(String(128), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataRetentionPolicyModel(Base):
    """Retention & Legal Hold schedules."""
    __tablename__ = "adkos_retention_policies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_name = Column(String(128), nullable=False)
    retention_days = Column(Integer, default=365)
    archive_after_days = Column(Integer, default=90)
    has_legal_hold = Column(Boolean, default=False)
    auto_delete = Column(Boolean, default=False)


class AdkosDataDeletionRequestModel(Base):
    """Right-to-be-forgotten & dataset deletion requests."""
    __tablename__ = "adkos_deletion_requests"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    target_entity = Column(String(128), nullable=False)  # DATASET, RECORD, ENTITY, DOCUMENT, MEMORY
    target_id = Column(String(128), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(32), default="SCHEDULED")  # SCHEDULED, COMPLETED, BLOCKED_LEGAL_HOLD
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------
# 15. FINOPS, SECURITY & RELIABILITY (SLOs)
# ----------------------------------------------------------------------
class AdkosDataCostModel(Base):
    """Data infrastructure cost tracking (FinOps)."""
    __tablename__ = "adkos_costs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    category = Column(String(64), nullable=False)  # STORAGE, COMPUTE, QUERIES, PIPELINES, AI_RETRIEVAL
    cost_usd = Column(Float, default=0.0)
    recorded_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataSecurityEventModel(Base):
    """Data access and anomaly security audit trail."""
    __tablename__ = "adkos_security_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    user_or_agent = Column(String(128), nullable=False)
    action = Column(String(64), nullable=False)  # QUERY, EXPORT, BULK_READ, PERMISSION_CHANGE
    dataset_name = Column(String(128), nullable=False)
    result = Column(String(32), default="ALLOWED")  # ALLOWED, BLOCKED
    risk_score = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataAuditEventModel(Base):
    """Data Audit Record."""
    __tablename__ = "adkos_audit_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, default=lambda: f"audit_{uuid.uuid4().hex[:12]}", index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    actor_id = Column(String(128), nullable=False)
    actor_type = Column(String(64), default="USER")
    action = Column(String(64), nullable=False)
    target_resource = Column(String(256), nullable=False)
    query_text = Column(Text, nullable=True)
    purpose = Column(String(256), nullable=True)
    result_status = Column(String(32), default="SUCCESS")
    metadata_context = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataSloModel(Base):
    """Data Reliability SLOs."""
    __tablename__ = "adkos_slos"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    data_product_name = Column(String(128), nullable=False)
    freshness_target_pct = Column(Float, default=99.5)
    availability_target_pct = Column(Float, default=99.9)
    quality_target_pct = Column(Float, default=99.0)
    current_health = Column(String(32), default="HEALTHY")
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AdkosDataRecommendationModel(Base):
    """AI recommendations for partitioning, indexing, caching, and cost."""
    __tablename__ = "adkos_recommendations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    category = Column(String(64), default="COST_OPTIMIZATION")  # COST_OPTIMIZATION, PERFORMANCE, QUALITY, SECURITY
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    potential_savings_usd = Column(Float, default=0.0)
    confidence = Column(Float, default=0.9)
    status = Column(String(32), default="OPEN")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Convenience Aliases & Exports
# ----------------------------------------------------------------------
DataSourceModel = AdkosDataSourceModel
DataConnectorModel = AdkosDataConnectorModel
DataSourceCredentialModel = AdkosDataSourceCredentialModel
DataIngestionJobModel = AdkosDataIngestionJobModel
DataPipelineModel = AdkosDataPipelineModel
PipelineStepModel = AdkosPipelineStepModel
PipelineRunModel = AdkosPipelineRunModel
PipelineDependencyModel = AdkosPipelineDependencyModel
DataLakeAssetModel = AdkosDataLakeAssetModel
DataWarehouseAssetModel = AdkosDataWarehouseAssetModel
DataMartModel = AdkosDataMartModel
DataProductModel = AdkosDataProductModel
DataProductVersionModel = AdkosDataProductVersionModel
DataProductConsumerModel = AdkosDataProductConsumerModel
DataContractModel = AdkosDataContractModel
DataContractVersionModel = AdkosDataContractVersionModel
SchemaRegistryModel = AdkosSchemaRegistryModel
SchemaVersionModel = AdkosSchemaVersionModel
DataQualityRuleModel = AdkosDataQualityRuleModel
DataQualityRunModel = AdkosDataQualityRunModel
DataQualityResultModel = AdkosDataQualityResultModel
DataIncidentModel = AdkosDataIncidentModel
DataIncidentEventModel = AdkosDataIncidentEventModel
DataIncidentPostmortemModel = AdkosDataIncidentPostmortemModel
DataLineageModel = AdkosDataLineageModel
ColumnLineageModel = AdkosColumnLineageModel
DataCatalogModel = AdkosDataCatalogModel
DataMetadataModel = AdkosDataMetadataModel
BusinessGlossaryModel = AdkosBusinessGlossaryModel
BusinessTermRelationshipModel = AdkosBusinessTermRelationshipModel
SemanticModel = AdkosSemanticModel
SemanticRelationshipModel = AdkosSemanticRelationshipModel
MetricModel = AdkosMetricModel
MetricDimensionModel = AdkosMetricDimensionModel
MetricVersionModel = AdkosMetricVersionModel
MasterEntityModel = AdkosMasterEntityModel
EntityAliasModel = AdkosEntityAliasModel
EntityMatchModel = AdkosEntityMatchModel
EntityMergeHistoryModel = AdkosEntityMergeHistoryModel
KnowledgeNodeModel = AdkosKnowledgeNodeModel
KnowledgeEdgeModel = AdkosKnowledgeEdgeModel
KnowledgeSourceModel = AdkosKnowledgeSourceModel
KnowledgeConflictModel = AdkosKnowledgeConflictModel
DocumentModel = AdkosDocumentModel
DocumentChunkModel = AdkosDocumentChunkModel
SearchIndexModel = AdkosSearchIndexModel
SearchQueryModel = AdkosSearchQueryModel
MemoryModel = AdkosMemoryModel
MemoryConflictModel = AdkosMemoryConflictModel
DatasetModel = AdkosDatasetModel
FeatureModel = AdkosFeatureModel
DataClassificationModel = AdkosDataClassificationModel
PiiFindingModel = AdkosPiiFindingModel
DataAccessPolicyModel = AdkosDataAccessPolicyModel
DataAccessRequestModel = AdkosDataAccessRequestModel
DataRetentionPolicyModel = AdkosDataRetentionPolicyModel
DataDeletionRequestModel = AdkosDataDeletionRequestModel
DataCostModel = AdkosDataCostModel
DataSecurityEventModel = AdkosDataSecurityEventModel
DataSloModel = AdkosDataSloModel
DataRecommendationModel = AdkosDataRecommendationModel
DataAlertModel = AdkosDataIncidentModel
DataSensitivityRuleModel = AdkosDataClassificationModel
DataQualityRunModel = AdkosDataQualityRunModel
DataQualityResultModel = AdkosDataQualityResultModel
DataIncidentEventModel = AdkosDataIncidentEventModel
DataIncidentPostmortemModel = AdkosDataIncidentPostmortemModel
BusinessTermModel = AdkosBusinessGlossaryModel
BusinessTermRelationshipModel = AdkosBusinessTermRelationshipModel
MetricDimensionModel = AdkosMetricDimensionModel
MetricVersionModel = AdkosMetricVersionModel
EntityAliasModel = AdkosEntityAliasModel
EntityMatchModel = AdkosEntityMatchModel
EntityMergeHistoryModel = AdkosEntityMergeHistoryModel
KnowledgeVersionModel = AdkosKnowledgeConflictModel
DocumentChunkModel = AdkosDocumentChunkModel
MemoryVersionModel = AdkosMemoryConflictModel
DatasetVersionModel = AdkosDatasetModel
FeatureVersionModel = AdkosFeatureModel
DataAccessGrantModel = AdkosDataAccessRequestModel
LegalHoldModel = AdkosDataRetentionPolicyModel
DataShareModel = AdkosDataAccessPolicyModel
DataExportModel = AdkosDataAccessRequestModel
DataAnomalyModel = AdkosDataQualityResultModel
DataForecastModel = AdkosDataRecommendationModel
DataSimulationModel = AdkosDataRecommendationModel
DataBudgetModel = AdkosDataCostModel
DataAuditEventModel = AdkosDataAuditEventModel
DataSLOModel = AdkosDataSloModel
DataSLOHistoryModel = AdkosDataSloModel

__all__ = ['AdkosDataSourceModel', 'AdkosDataConnectorModel', 'AdkosDataSourceCredentialModel', 'AdkosDataIngestionJobModel', 'AdkosDataPipelineModel', 'AdkosPipelineStepModel', 'AdkosPipelineRunModel', 'AdkosPipelineDependencyModel', 'AdkosDataLakeAssetModel', 'AdkosDataWarehouseAssetModel', 'AdkosDataMartModel', 'AdkosDataProductModel', 'AdkosDataProductVersionModel', 'AdkosDataProductConsumerModel', 'AdkosDataContractModel', 'AdkosDataContractVersionModel', 'AdkosSchemaRegistryModel', 'AdkosSchemaVersionModel', 'AdkosDataQualityRuleModel', 'AdkosDataQualityRunModel', 'AdkosDataQualityResultModel', 'AdkosDataIncidentModel', 'AdkosDataIncidentEventModel', 'AdkosDataIncidentPostmortemModel', 'AdkosDataLineageModel', 'AdkosColumnLineageModel', 'AdkosDataCatalogModel', 'AdkosDataMetadataModel', 'AdkosBusinessGlossaryModel', 'AdkosBusinessTermRelationshipModel', 'AdkosSemanticModel', 'AdkosSemanticRelationshipModel', 'AdkosMetricModel', 'AdkosMetricDimensionModel', 'AdkosMetricVersionModel', 'AdkosMasterEntityModel', 'AdkosEntityAliasModel', 'AdkosEntityMatchModel', 'AdkosEntityMergeHistoryModel', 'AdkosKnowledgeNodeModel', 'AdkosKnowledgeEdgeModel', 'AdkosKnowledgeSourceModel', 'AdkosKnowledgeConflictModel', 'AdkosDocumentModel', 'AdkosDocumentChunkModel', 'AdkosSearchIndexModel', 'AdkosSearchQueryModel', 'AdkosMemoryModel', 'AdkosMemoryConflictModel', 'AdkosDatasetModel', 'AdkosFeatureModel', 'AdkosDataClassificationModel', 'AdkosPiiFindingModel', 'AdkosDataAccessPolicyModel', 'AdkosDataAccessRequestModel', 'AdkosDataRetentionPolicyModel', 'AdkosDataDeletionRequestModel', 'AdkosDataCostModel', 'AdkosDataSecurityEventModel', 'AdkosDataSloModel', 'AdkosDataRecommendationModel', 'DataSourceModel', 'DataConnectorModel', 'DataSourceCredentialModel', 'DataIngestionJobModel', 'DataPipelineModel', 'PipelineStepModel', 'PipelineRunModel', 'PipelineDependencyModel', 'DataLakeAssetModel', 'DataWarehouseAssetModel', 'DataMartModel', 'DataProductModel', 'DataProductVersionModel', 'DataProductConsumerModel', 'DataContractModel', 'DataContractVersionModel', 'SchemaRegistryModel', 'SchemaVersionModel', 'DataQualityRuleModel', 'DataQualityRunModel', 'DataQualityResultModel', 'DataIncidentModel', 'DataIncidentEventModel', 'DataIncidentPostmortemModel', 'DataLineageModel', 'ColumnLineageModel', 'DataCatalogModel', 'DataMetadataModel', 'BusinessGlossaryModel', 'BusinessTermRelationshipModel', 'SemanticModel', 'SemanticRelationshipModel', 'MetricModel', 'MetricDimensionModel', 'MetricVersionModel', 'MasterEntityModel', 'EntityAliasModel', 'EntityMatchModel', 'EntityMergeHistoryModel', 'KnowledgeNodeModel', 'KnowledgeEdgeModel', 'KnowledgeSourceModel', 'KnowledgeConflictModel', 'DocumentModel', 'DocumentChunkModel', 'SearchIndexModel', 'SearchQueryModel', 'MemoryModel', 'MemoryConflictModel', 'DatasetModel', 'FeatureModel', 'DataClassificationModel', 'PiiFindingModel', 'DataAccessPolicyModel', 'DataAccessRequestModel', 'DataRetentionPolicyModel', 'DataDeletionRequestModel', 'DataCostModel', 'DataSecurityEventModel', 'DataSloModel', 'DataRecommendationModel', 'DataAlertModel', 'DataSensitivityRuleModel', 'DataQualityRunModel', 'DataQualityResultModel', 'DataIncidentEventModel', 'DataIncidentPostmortemModel', 'BusinessTermModel', 'BusinessTermRelationshipModel', 'MetricDimensionModel', 'MetricVersionModel', 'EntityAliasModel', 'EntityMatchModel', 'EntityMergeHistoryModel', 'KnowledgeVersionModel', 'DocumentChunkModel', 'MemoryVersionModel', 'DatasetVersionModel', 'FeatureVersionModel', 'DataAccessGrantModel', 'LegalHoldModel', 'DataShareModel', 'DataExportModel', 'DataAnomalyModel', 'DataForecastModel', 'DataSimulationModel', 'DataBudgetModel', 'DataAuditEventModel', 'DataSLOModel', 'DataSLOHistoryModel']
