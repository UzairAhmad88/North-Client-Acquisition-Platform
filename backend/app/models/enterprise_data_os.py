"""SQLAlchemy ORM Models for Phase 62: Unified Enterprise Data Operating System.

Comprehensive data models covering Data Domains, Data Sources, Ingestion,
Pipelines, Lakehouse datasets (Bronze/Silver/Gold), Schemas, Data Contracts,
Data Products, Catalog, Business Glossary, Semantic Layer, Data Quality,
Lineage, Data Access/Security, Feature Store, FinOps, and Incidents.
"""

from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    Integer,
    DateTime,
    JSON,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.models.base import Base


class DataDomainModel(Base):
    """Business and operational data domain taxonomy."""

    __tablename__ = "data_domains"
    __table_args__ = {"extend_existing": True}

    domain_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    slug = Column(String(128), nullable=False)
    owner_team = Column(String(128), nullable=False)
    lead_steward_email = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataSourceCatalogModel(Base):
    """Catalog of operational, transactional, analytics, and SaaS data sources."""

    __tablename__ = "data_sources"
    __table_args__ = {"extend_existing": True}

    source_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    source_type = Column(String(64), nullable=False)  # POSTGRES, MYSQL, S3, KAFKA, SAAS, API
    provider = Column(String(64), nullable=False)
    domain_id = Column(String(64), nullable=True)
    connection_endpoint = Column(String(256), nullable=False)
    auth_type = Column(String(64), nullable=False)  # IAM_ROLE, VAULT_SECRET_REF, OAUTH2
    data_classification = Column(String(64), default="INTERNAL")
    status = Column(String(64), default="ACTIVE")
    reliability_score = Column(Float, default=99.9)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataIngestionJobModel(Base):
    """Batch, micro-batch, streaming, and CDC ingestion jobs."""

    __tablename__ = "data_ingestion_jobs"
    __table_args__ = {"extend_existing": True}

    job_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_id = Column(String(64), nullable=False)
    target_dataset_id = Column(String(64), nullable=False)
    ingestion_mode = Column(String(64), default="BATCH")  # BATCH, STREAMING, CDC
    schedule_cron = Column(String(64), nullable=True)
    watermark_offset = Column(String(128), nullable=True)
    records_processed_count = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    status = Column(String(64), default="RUNNING")
    last_run_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataPipelineModel(Base):
    """Transformation, ETL/ELT DAG pipelines."""

    __tablename__ = "data_pipelines"
    __table_args__ = {"extend_existing": True}

    pipeline_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    source_datasets = Column(JSON, default=list)
    target_dataset = Column(String(128), nullable=False)
    schedule_type = Column(String(64), default="SCHEDULED")
    sla_minutes = Column(Integer, default=60)
    status = Column(String(64), default="ACTIVE")
    owner_team = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataLakehouseDatasetModel(Base):
    """Lakehouse datasets organized into Bronze, Silver, and Gold architectural layers."""

    __tablename__ = "data_lakehouse_datasets"
    __table_args__ = {"extend_existing": True}

    dataset_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    domain_id = Column(String(64), nullable=False)
    name = Column(String(128), nullable=False)
    layer = Column(String(32), default="BRONZE")  # BRONZE, SILVER, GOLD
    format = Column(String(32), default="PARQUET")  # PARQUET, DELTA, ICEBERG
    storage_uri = Column(String(256), nullable=False)
    partition_keys = Column(JSON, default=list)
    record_count = Column(Integer, default=0)
    size_mb = Column(Float, default=0.0)
    classification = Column(String(32), default="INTERNAL")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataSchemaRegistryModel(Base):
    """Schema evolution, compatibility rules, and versioning."""

    __tablename__ = "data_schemas"
    __table_args__ = {"extend_existing": True}

    schema_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_id = Column(String(64), nullable=False)
    version = Column(String(32), default="v1.0.0")
    fields = Column(JSON, default=list)
    compatibility_mode = Column(String(32), default="BACKWARD")
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataContractModel(Base):
    """Formal interface contracts between data producers and consumers."""

    __tablename__ = "data_contracts"
    __table_args__ = {"extend_existing": True}

    contract_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    producer_team = Column(String(128), nullable=False)
    consumer_team = Column(String(128), nullable=False)
    dataset_id = Column(String(64), nullable=False)
    schema_version = Column(String(32), default="v1.0.0")
    freshness_sla_minutes = Column(Integer, default=120)
    quality_threshold_pct = Column(Float, default=99.0)
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataProductModel(Base):
    """Reusable, curated Gold-layer data products."""

    __tablename__ = "data_products"
    __table_args__ = {"extend_existing": True}

    product_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    domain_id = Column(String(64), nullable=False)
    name = Column(String(128), nullable=False)
    purpose = Column(Text, nullable=False)
    owner_team = Column(String(128), nullable=False)
    underlying_datasets = Column(JSON, default=list)
    consumers_count = Column(Integer, default=0)
    quality_score = Column(Float, default=98.5)
    health_status = Column(String(32), default="HEALTHY")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataCatalogAssetModel(Base):
    """Global data catalog search index with natural language semantics."""

    __tablename__ = "data_catalog_assets"
    __table_args__ = {"extend_existing": True}

    asset_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    asset_name = Column(String(128), nullable=False)
    asset_type = Column(String(64), nullable=False)  # DATASET, TABLE, COLUMN, METRIC, DASHBOARD
    domain_name = Column(String(64), nullable=False)
    owner_email = Column(String(128), nullable=False)
    classification = Column(String(32), default="INTERNAL")
    quality_score = Column(Float, default=95.0)
    tags = Column(JSON, default=list)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class BusinessGlossaryTermModel(Base):
    """Authoritative enterprise business glossary definitions."""

    __tablename__ = "business_glossary_terms"
    __table_args__ = {"extend_existing": True}

    term_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    term_name = Column(String(128), nullable=False)
    definition = Column(Text, nullable=False)
    domain_name = Column(String(64), nullable=False)
    owner_email = Column(String(128), nullable=False)
    synonyms = Column(JSON, default=list)
    related_metrics = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SemanticModelMetricModel(Base):
    """Centralized semantic metrics layer powering Dashboards, BI, and AI."""

    __tablename__ = "semantic_metrics"
    __table_args__ = {"extend_existing": True}

    metric_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    definition = Column(Text, nullable=False)
    formula_sql = Column(Text, nullable=False)
    dimensions = Column(JSON, default=list)
    source_table = Column(String(128), nullable=False)
    owner_team = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataQualityRuleModel(Base):
    """Multi-factor data quality test assertions and findings."""

    __tablename__ = "data_quality_rules"
    __table_args__ = {"extend_existing": True}

    rule_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dataset_id = Column(String(64), nullable=False)
    rule_type = Column(String(64), nullable=False)  # NOT_NULL, UNIQUE, RANGE, FORMAT, FRESHNESS
    dimension = Column(String(64), default="COMPLETENESS")
    severity = Column(String(32), default="HIGH")
    pass_rate_pct = Column(Float, default=100.0)
    is_active = Column(Boolean, default=True)
    last_evaluated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataLineageEdgeModel(Base):
    """End-to-end directed lineage graph edges."""

    __tablename__ = "data_lineage_edges"
    __table_args__ = {"extend_existing": True}

    edge_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_asset_id = Column(String(64), nullable=False)
    target_asset_id = Column(String(64), nullable=False)
    relationship_type = Column(String(64), default="TRANSFORMS_INTO")
    transformation_name = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataAccessGrantModel(Base):
    """Role-based, column-level, and row-level access control grants."""

    __tablename__ = "data_access_grants"
    __table_args__ = {"extend_existing": True}

    grant_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    principal_id = Column(String(64), nullable=False)
    dataset_id = Column(String(64), nullable=False)
    access_level = Column(String(32), default="READ")  # READ, WRITE, ADMIN
    row_filter_expression = Column(String(256), nullable=True)
    masked_columns = Column(JSON, default=list)
    approved_by = Column(String(128), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class FeatureStoreItemModel(Base):
    """Curated machine learning and AI feature store repository."""

    __tablename__ = "feature_store_items"
    __table_args__ = {"extend_existing": True}

    feature_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    entity_name = Column(String(64), nullable=False)  # CUSTOMER, PRODUCT, LEAD, PROJECT
    data_type = Column(String(32), default="FLOAT")
    source_dataset_id = Column(String(64), nullable=False)
    transformation_logic = Column(Text, nullable=False)
    freshness_minutes = Column(Integer, default=60)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataFinopsCostModel(Base):
    """Storage, compute, query, and AI data engineering cost tracking."""

    __tablename__ = "data_finops_costs"
    __table_args__ = {"extend_existing": True}

    cost_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    domain_name = Column(String(64), nullable=False)
    cost_category = Column(String(64), nullable=False)  # STORAGE, COMPUTE, QUERY, INGESTION, AI_RAG
    monthly_spend_usd = Column(Float, default=0.0)
    waste_estimate_usd = Column(Float, default=0.0)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataIncidentModel(Base):
    """Data quality breaches, schema breaking changes, and pipeline failures."""

    __tablename__ = "data_incidents"
    __table_args__ = {"extend_existing": True}

    incident_id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    severity = Column(String(32), default="SEV2")
    incident_type = Column(String(64), nullable=False)  # PIPELINE_FAIL, SCHEMA_BREAK, QUALITY_BREACH
    affected_datasets = Column(JSON, default=list)
    status = Column(String(32), default="ACTIVE")
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)
