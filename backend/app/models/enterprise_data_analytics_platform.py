"""
Phase 79: Enterprise Data & Analytics Platform, Lakehouse, Real-Time Data Fabric, BI, Metrics Layer, Advanced Analytics & Decision-Grade Intelligence Models.
Zero-collision namespace and extend_existing=True for maximum compatibility with existing tables.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, Base


# --- DATA SOURCES & CONNECTIONS ---
class EdapDataSourceModel(BaseModel):
    """Governed Data Source Registry."""
    __tablename__ = "data_sources"
    __table_args__ = {"extend_existing": True}

    source_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    type = Column(String(64), nullable=False)  # POSTGRESQL, MYSQL, MONGO, S3, KAFKA, API, CSV, PARQUET, etc.
    owner = Column(String(255), nullable=False)
    domain = Column(String(64), nullable=False, index=True)
    connection_string_enc = Column(Text, nullable=True)
    refresh_frequency = Column(String(64), default="HOURLY", nullable=False)
    data_classification = Column(String(64), default="INTERNAL", nullable=False)
    reliability_score = Column(Float, default=99.9, nullable=False)
    sla_hours = Column(Float, default=24.0, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    metadata_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataSourceConnectionModel(BaseModel):
    """Connection credentials and state for data sources."""
    __tablename__ = "data_source_connections"
    __table_args__ = {"extend_existing": True}

    source_code = Column(String(64), nullable=False, index=True)
    endpoint = Column(String(255), nullable=False)
    auth_type = Column(String(64), default="OAUTH2", nullable=False)
    status = Column(String(32), default="CONNECTED", nullable=False)
    last_health_check = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataSourceSlaModel(BaseModel):
    """SLA metrics per data source."""
    __tablename__ = "data_source_slas"
    __table_args__ = {"extend_existing": True}

    source_code = Column(String(64), nullable=False, index=True)
    freshness_target_minutes = Column(Integer, default=60, nullable=False)
    uptime_target_pct = Column(Float, default=99.9, nullable=False)
    max_allowed_latency_ms = Column(Integer, default=5000, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- INGESTION & PIPELINES ---
class EdapDataIngestionJobModel(BaseModel):
    """Pipeline orchestration job definitions."""
    __tablename__ = "data_ingestion_jobs"
    __table_args__ = {"extend_existing": True}

    job_name = Column(String(128), unique=True, nullable=False, index=True)
    source_code = Column(String(64), nullable=False, index=True)
    mode = Column(String(32), default="BATCH", nullable=False)  # BATCH, STREAMING, CDC, MICRO_BATCH
    schedule = Column(String(64), default="0 * * * *", nullable=False)
    version = Column(String(32), default="1.0.0", nullable=False)
    owner = Column(String(255), nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    dependencies = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataIngestionRunModel(BaseModel):
    """Execution history of ingestion jobs."""
    __tablename__ = "data_ingestion_runs"
    __table_args__ = {"extend_existing": True}

    job_name = Column(String(128), nullable=False, index=True)
    status = Column(String(32), default="COMPLETED", nullable=False)  # RUNNING, COMPLETED, FAILED
    records_processed = Column(Integer, default=0, nullable=False)
    bytes_processed = Column(Integer, default=0, nullable=False)
    execution_time_ms = Column(Float, default=0.0, nullable=False)
    error_message = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataIngestionEventModel(BaseModel):
    """Real-time streaming ingestion events."""
    __tablename__ = "data_ingestion_events"
    __table_args__ = {"extend_existing": True}

    event_id_str = Column(String(128), nullable=False, index=True)
    source_code = Column(String(64), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- SCHEMAS & CONTRACTS ---
class EdapDataSchemaModel(BaseModel):
    """Versioned schema registry."""
    __tablename__ = "data_schemas"
    __table_args__ = {"extend_existing": True}

    schema_name = Column(String(128), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    current_version = Column(String(32), default="1.0.0", nullable=False)
    compatibility_mode = Column(String(32), default="BACKWARD", nullable=False)
    schema_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataSchemaVersionModel(BaseModel):
    """Version history of schemas."""
    __tablename__ = "data_schema_versions"
    __table_args__ = {"extend_existing": True}

    schema_name = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    change_type = Column(String(32), default="COMPATIBLE", nullable=False)  # COMPATIBLE, POTENTIALLY_BREAKING, BREAKING
    schema_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataContractModel(BaseModel):
    """Producer-consumer data quality and schema contracts."""
    __tablename__ = "data_contracts"
    __table_args__ = {"extend_existing": True}

    contract_name = Column(String(128), unique=True, nullable=False, index=True)
    producer = Column(String(255), nullable=False)
    consumer = Column(String(255), nullable=False)
    schema_name = Column(String(128), nullable=False)
    sla_terms = Column(JSON, default=dict, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- DATASETS & LAKEHOUSE ZONES ---
class EdapDataDatasetModel(BaseModel):
    """Governed Datasets Catalog."""
    __tablename__ = "data_datasets"
    __table_args__ = {"extend_existing": True}

    dataset_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    zone = Column(String(32), default="SILVER", nullable=False)  # BRONZE, SILVER, GOLD, SEMANTIC, SERVING
    domain = Column(String(64), nullable=False, index=True)
    owner = Column(String(255), nullable=False)
    quality_score = Column(Float, default=98.5, nullable=False)
    record_count = Column(Integer, default=0, nullable=False)
    storage_bytes = Column(Integer, default=0, nullable=False)
    schema_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataDatasetVersionModel(BaseModel):
    """Dataset version history."""
    __tablename__ = "data_dataset_versions"
    __table_args__ = {"extend_existing": True}

    dataset_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    row_count = Column(Integer, default=0, nullable=False)
    snapshot_path = Column(String(255), nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataDatasetSnapshotModel(BaseModel):
    """Reproducible snapshot references."""
    __tablename__ = "data_dataset_snapshots"
    __table_args__ = {"extend_existing": True}

    dataset_code = Column(String(128), nullable=False, index=True)
    snapshot_id_str = Column(String(128), nullable=False, index=True)
    created_by = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataZoneModel(BaseModel):
    """Lakehouse zones configuration."""
    __tablename__ = "data_zones"
    __table_args__ = {"extend_existing": True}

    zone_name = Column(String(32), primary_key=True)  # BRONZE, SILVER, GOLD, SEMANTIC, SERVING
    description = Column(Text, nullable=True)
    retention_days = Column(Integer, default=365, nullable=False)
    access_level = Column(String(32), default="RESTRICTED", nullable=False)


class EdapDataTransformationModel(BaseModel):
    """ETL/ELT transformation specs."""
    __tablename__ = "data_transformations"
    __table_args__ = {"extend_existing": True}

    transform_code = Column(String(128), unique=True, nullable=False, index=True)
    input_dataset = Column(String(128), nullable=False)
    output_dataset = Column(String(128), nullable=False)
    sql_logic = Column(Text, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataTransformationVersionModel(BaseModel):
    """Transformation logic versions."""
    __tablename__ = "data_transformation_versions"
    __table_args__ = {"extend_existing": True}

    transform_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    sql_logic = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- DATA QUALITY & OBSERVABILITY ---
class EdapDataQualityRuleModel(BaseModel):
    """Configurable quality validation rule."""
    __tablename__ = "data_quality_rules"
    __table_args__ = {"extend_existing": True}

    rule_name = Column(String(128), unique=True, nullable=False, index=True)
    dataset_code = Column(String(128), nullable=False, index=True)
    column_name = Column(String(128), nullable=True)
    rule_type = Column(String(64), nullable=False)  # NOT_NULL, UNIQUE, RANGE, REGEX, REFERENTIAL_INTEGRITY, FRESHNESS
    expression = Column(String(255), nullable=False)
    severity = Column(String(32), default="HIGH", nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataQualityResultModel(BaseModel):
    """Execution results for data quality checks."""
    __tablename__ = "data_quality_results"
    __table_args__ = {"extend_existing": True}

    rule_name = Column(String(128), nullable=False, index=True)
    dataset_code = Column(String(128), nullable=False, index=True)
    passed = Column(Boolean, default=True, nullable=False)
    failed_rows = Column(Integer, default=0, nullable=False)
    total_rows = Column(Integer, default=0, nullable=False)
    execution_time_ms = Column(Float, default=0.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataQualityIncidentModel(BaseModel):
    """Data quality incident records."""
    __tablename__ = "data_quality_incidents"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), unique=True, nullable=False, index=True)
    dataset_code = Column(String(128), nullable=False, index=True)
    rule_name = Column(String(128), nullable=False)
    severity = Column(String(32), default="CRITICAL", nullable=False)
    owner = Column(String(255), nullable=False)
    status = Column(String(32), default="OPEN", nullable=False)  # OPEN, INVESTIGATING, RESOLVED
    root_cause = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataObservabilityEventModel(BaseModel):
    """Observability events tracking dataset volume & freshness."""
    __tablename__ = "data_observability_events"
    __table_args__ = {"extend_existing": True}

    dataset_code = Column(String(128), nullable=False, index=True)
    metric_name = Column(String(64), nullable=False)  # VOLUME, FRESHNESS, NULL_RATE, DUPLICATE_RATE
    metric_value = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataSchemaDriftEventModel(BaseModel):
    """Events recorded when schema drift occurs."""
    __tablename__ = "data_schema_drift_events"
    __table_args__ = {"extend_existing": True}

    dataset_code = Column(String(128), nullable=False, index=True)
    drift_type = Column(String(64), nullable=False)  # COLUMN_ADDED, COLUMN_REMOVED, TYPE_CHANGED
    details_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- DATA PRODUCTS & MARKETPLACE ---
class EdapDataProductModel(BaseModel):
    """Governed enterprise data products."""
    __tablename__ = "data_products"
    __table_args__ = {"extend_existing": True}

    product_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(255), nullable=False)
    domain = Column(String(64), nullable=False, index=True)
    rating = Column(Float, default=4.8, nullable=False)
    subscriber_count = Column(Integer, default=0, nullable=False)
    status = Column(String(32), default="PUBLISHED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataProductVersionModel(BaseModel):
    """Data product versioning."""
    __tablename__ = "data_product_versions"
    __table_args__ = {"extend_existing": True}

    product_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    release_notes = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataProductSubscriptionModel(BaseModel):
    """User/Team subscriptions to data products."""
    __tablename__ = "data_product_subscriptions"
    __table_args__ = {"extend_existing": True}

    product_code = Column(String(128), nullable=False, index=True)
    subscriber_email = Column(String(255), nullable=False, index=True)
    access_role = Column(String(32), default="READ", nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- GOVERNANCE & MASKING ---
class EdapDataAccessRequestModel(BaseModel):
    """Dataset access request tracking."""
    __tablename__ = "data_access_requests"
    __table_args__ = {"extend_existing": True}

    request_code = Column(String(64), unique=True, nullable=False, index=True)
    dataset_code = Column(String(128), nullable=False, index=True)
    requester_email = Column(String(255), nullable=False)
    purpose = Column(Text, nullable=False)
    status = Column(String(32), default="PENDING", nullable=False)  # PENDING, APPROVED, REJECTED
    approved_by = Column(String(255), nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataAccessPolicyModel(BaseModel):
    """RBAC / ABAC policies for data access."""
    __tablename__ = "data_access_policies"
    __table_args__ = {"extend_existing": True}

    policy_name = Column(String(128), unique=True, nullable=False, index=True)
    dataset_code = Column(String(128), nullable=False, index=True)
    role = Column(String(64), nullable=False)
    row_filter_sql = Column(Text, nullable=True)
    column_permissions_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataMaskingPolicyModel(BaseModel):
    """Data masking & anonymization rules."""
    __tablename__ = "data_masking_policies"
    __table_args__ = {"extend_existing": True}

    policy_name = Column(String(128), unique=True, nullable=False, index=True)
    column_name = Column(String(128), nullable=False)
    masking_type = Column(String(32), default="FULL", nullable=False)  # FULL, PARTIAL, TOKENIZATION, ANONYMIZATION
    pattern = Column(String(128), nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- WAREHOUSE & MARTS ---
class EdapWarehouseDimensionModel(BaseModel):
    """Dimension tables modeling."""
    __tablename__ = "warehouse_dimensions"
    __table_args__ = {"extend_existing": True}

    dim_name = Column(String(128), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    scd_type = Column(String(16), default="SCD_TYPE_2", nullable=False)
    columns_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapWarehouseFactModel(BaseModel):
    """Fact tables modeling."""
    __tablename__ = "warehouse_facts"
    __table_args__ = {"extend_existing": True}

    fact_name = Column(String(128), unique=True, nullable=False, index=True)
    grain = Column(String(128), nullable=False)
    measures_json = Column(JSON, default=list, nullable=False)
    foreign_keys_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapWarehouseSnapshotModel(BaseModel):
    """Periodic dimensional snapshots."""
    __tablename__ = "warehouse_snapshots"
    __table_args__ = {"extend_existing": True}

    snapshot_code = Column(String(128), unique=True, nullable=False, index=True)
    fact_name = Column(String(128), nullable=False)
    snapshot_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDataMartModel(BaseModel):
    """Domain-specific analytical data marts."""
    __tablename__ = "data_marts"
    __table_args__ = {"extend_existing": True}

    mart_code = Column(String(64), unique=True, nullable=False, index=True)
    domain = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    dataset_codes = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- SEMANTIC LAYER & METRICS LAYER ---
class EdapSemanticEntityModel(BaseModel):
    """Business Entities in the semantic layer."""
    __tablename__ = "semantic_entities"
    __table_args__ = {"extend_existing": True}

    entity_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(64), nullable=False, index=True)
    primary_key_col = Column(String(128), nullable=False)
    attributes_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapSemanticAttributeModel(BaseModel):
    """Business attributes in semantic entity models."""
    __tablename__ = "semantic_attributes"
    __table_args__ = {"extend_existing": True}

    entity_code = Column(String(64), nullable=False, index=True)
    attribute_name = Column(String(128), nullable=False)
    data_type = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapSemanticRelationshipModel(BaseModel):
    """Relationships between semantic entities."""
    __tablename__ = "semantic_relationships"
    __table_args__ = {"extend_existing": True}

    from_entity = Column(String(64), nullable=False, index=True)
    to_entity = Column(String(64), nullable=False, index=True)
    relationship_type = Column(String(32), default="ONE_TO_MANY", nullable=False)
    join_keys = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMetricModel(BaseModel):
    """Governed Enterprise Metrics (Single Source of Truth for KPIs)."""
    __tablename__ = "metrics"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    definition = Column(Text, nullable=False)
    formula = Column(Text, nullable=False)
    dimensions = Column(JSON, default=list, nullable=False)
    filters = Column(JSON, default=dict, nullable=False)
    owner = Column(String(255), nullable=False)
    domain = Column(String(64), nullable=False, index=True)
    source_dataset = Column(String(128), nullable=False)
    version = Column(String(32), default="1.0.0", nullable=False)
    status = Column(String(32), default="APPROVED", nullable=False)
    quality_score = Column(Float, default=99.5, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMetricVersionModel(BaseModel):
    """Versioned changes to metric definitions."""
    __tablename__ = "metric_versions"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    formula = Column(Text, nullable=False)
    change_reason = Column(Text, nullable=False)
    approved_by = Column(String(255), nullable=True)
    effective_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMetricDimensionModel(BaseModel):
    """Supported slice-and-dice dimensions for metrics."""
    __tablename__ = "metric_dimensions"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), nullable=False, index=True)
    dimension_name = Column(String(128), nullable=False)
    data_type = Column(String(64), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMetricDependencyModel(BaseModel):
    """Upstream and downstream metric dependency graph."""
    __tablename__ = "metric_dependencies"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), nullable=False, index=True)
    depends_on_metric = Column(String(128), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMetricQualityScoreModel(BaseModel):
    """Quality and freshness scores per metric."""
    __tablename__ = "metric_quality_scores"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), nullable=False, index=True)
    quality_score = Column(Float, default=99.0, nullable=False)
    freshness_score = Column(Float, default=99.5, nullable=False)
    adoption_score = Column(Float, default=95.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- QUERIES & CACHE ---
class EdapAnalyticsQueryModel(BaseModel):
    """Saved and executed analytical queries."""
    __tablename__ = "analytics_queries"
    __table_args__ = {"extend_existing": True}

    query_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    sql_text = Column(Text, nullable=False)
    nl_prompt = Column(Text, nullable=True)
    created_by = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsQueryRunModel(BaseModel):
    """Execution history of analytical queries."""
    __tablename__ = "analytics_query_runs"
    __table_args__ = {"extend_existing": True}

    query_code = Column(String(64), nullable=False, index=True)
    executed_by = Column(String(255), nullable=False)
    execution_time_ms = Column(Float, default=0.0, nullable=False)
    row_count = Column(Integer, default=0, nullable=False)
    status = Column(String(32), default="SUCCESS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsQueryCacheModel(BaseModel):
    """Governed query response cache."""
    __tablename__ = "analytics_query_cache"
    __table_args__ = {"extend_existing": True}

    cache_key = Column(String(255), primary_key=True)
    result_json = Column(JSON, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- BI DASHBOARDS & ANNOTATIONS ---
class EdapDashboardModel(BaseModel):
    """BI Dashboards catalog."""
    __tablename__ = "dashboards"
    __table_args__ = {"extend_existing": True}

    dashboard_code = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(255), nullable=False)
    department = Column(String(128), nullable=False)
    status = Column(String(32), default="PUBLISHED", nullable=False)  # DRAFT, REVIEW, PUBLISHED, ARCHIVED
    current_version = Column(String(32), default="1.0.0", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDashboardVersionModel(BaseModel):
    """Dashboard layout and design versions."""
    __tablename__ = "dashboard_versions"
    __table_args__ = {"extend_existing": True}

    dashboard_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    layout_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDashboardWidgetModel(BaseModel):
    """Individual widget/chart components on dashboards."""
    __tablename__ = "dashboard_widgets"
    __table_args__ = {"extend_existing": True}

    widget_code = Column(String(128), unique=True, nullable=False, index=True)
    dashboard_code = Column(String(128), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    chart_type = Column(String(64), default="BAR", nullable=False)  # LINE, BAR, AREA, SCATTER, HISTOGRAM, HEATMAP, FUNNEL, COHORT, KPI_CARD, TABLE
    metric_code = Column(String(128), nullable=True)
    config_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapDashboardPermissionModel(BaseModel):
    """Dashboard access control."""
    __tablename__ = "dashboard_permissions"
    __table_args__ = {"extend_existing": True}

    dashboard_code = Column(String(128), nullable=False, index=True)
    accessor_type = Column(String(32), default="TEAM", nullable=False)  # PRIVATE, TEAM, DEPARTMENT, ORGANIZATION
    accessor_id = Column(String(128), nullable=False)
    permission_level = Column(String(32), default="VIEW", nullable=False)  # VIEW, EDIT, ADMIN
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsAnnotationModel(BaseModel):
    """User annotations and explanations on charts/metrics."""
    __tablename__ = "analytics_annotations"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    comment = Column(Text, nullable=False)
    event_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- INSIGHTS & ANOMALIES ---
class EdapAnalyticsInsightModel(BaseModel):
    """Automated AI/Statistical analytical insights."""
    __tablename__ = "analytics_insights"
    __table_args__ = {"extend_existing": True}

    insight_code = Column(String(64), unique=True, nullable=False, index=True)
    metric_code = Column(String(128), nullable=False, index=True)
    insight_type = Column(String(64), nullable=False)  # TREND, SPIKE, DROP, ANOMALY, SEASONALITY, CORRELATION
    summary = Column(Text, nullable=False)
    evidence_json = Column(JSON, default=dict, nullable=False)
    confidence = Column(Float, default=0.92, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsAnomalyModel(BaseModel):
    """Detected metric anomalies."""
    __tablename__ = "analytics_anomalies"
    __table_args__ = {"extend_existing": True}

    anomaly_code = Column(String(64), unique=True, nullable=False, index=True)
    metric_code = Column(String(128), nullable=False, index=True)
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expected_value = Column(Float, nullable=False)
    actual_value = Column(Float, nullable=False)
    deviation_pct = Column(Float, nullable=False)
    detection_method = Column(String(64), default="ISOLATION_FOREST", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsChangePointModel(BaseModel):
    """Detected regime shifts/change points in time series."""
    __tablename__ = "analytics_change_points"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), nullable=False, index=True)
    change_date = Column(DateTime(timezone=True), nullable=False)
    magnitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- FORECASTING & TIME SERIES ---
class EdapForecastModelModel(BaseModel):
    """Forecasting models registry."""
    __tablename__ = "forecast_models"
    __table_args__ = {"extend_existing": True}

    model_code = Column(String(128), unique=True, nullable=False, index=True)
    metric_code = Column(String(128), nullable=False, index=True)
    algorithm = Column(String(64), default="ARIMA_PROPHET", nullable=False)
    horizon_days = Column(Integer, default=30, nullable=False)
    mae = Column(Float, default=0.035, nullable=False)
    mape = Column(Float, default=0.024, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapForecastRunModel(BaseModel):
    """Forecasting execution runs."""
    __tablename__ = "forecast_runs"
    __table_args__ = {"extend_existing": True}

    model_code = Column(String(128), nullable=False, index=True)
    run_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    status = Column(String(32), default="COMPLETED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapForecastResultModel(BaseModel):
    """Generated forecast values with uncertainty intervals."""
    __tablename__ = "forecast_results"
    __table_args__ = {"extend_existing": True}

    model_code = Column(String(128), nullable=False, index=True)
    target_date = Column(DateTime(timezone=True), nullable=False)
    predicted_value = Column(Float, nullable=False)
    lower_bound = Column(Float, nullable=False)
    upper_bound = Column(Float, nullable=False)
    confidence_interval = Column(Float, default=0.95, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapTimeSeriesModel(BaseModel):
    """Time series metric points."""
    __tablename__ = "time_series"
    __table_args__ = {"extend_existing": True}

    metric_code = Column(String(128), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    value = Column(Float, nullable=False)
    dimensions_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapCohortDefinitionModel(BaseModel):
    """Cohort analysis definitions."""
    __tablename__ = "cohort_definitions"
    __table_args__ = {"extend_existing": True}

    cohort_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    cohort_type = Column(String(64), default="SIGNUP", nullable=False)  # SIGNUP, PURCHASE, CONTRACT, PROJECT_START
    granularity = Column(String(32), default="MONTHLY", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapFunnelDefinitionModel(BaseModel):
    """Funnel analysis stage definitions."""
    __tablename__ = "funnel_definitions"
    __table_args__ = {"extend_existing": True}

    funnel_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    stages_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- EXPERIMENTS & FEATURE STORE ---
class EdapExperimentModel(BaseModel):
    """A/B Testing and experiment registry."""
    __tablename__ = "experiments"
    __table_args__ = {"extend_existing": True}

    experiment_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=False)
    status = Column(String(32), default="RUNNING", nullable=False)  # DRAFT, RUNNING, CONCLUDED
    primary_metric = Column(String(128), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapExperimentRunModel(BaseModel):
    """Experiment execution tracking."""
    __tablename__ = "experiment_runs"
    __table_args__ = {"extend_existing": True}

    experiment_code = Column(String(128), nullable=False, index=True)
    control_count = Column(Integer, default=0, nullable=False)
    treatment_count = Column(Integer, default=0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapExperimentResultModel(BaseModel):
    """Statistical evaluation results of experiments."""
    __tablename__ = "experiment_results"
    __table_args__ = {"extend_existing": True}

    experiment_code = Column(String(128), nullable=False, index=True)
    p_value = Column(Float, default=0.01, nullable=False)
    effect_size = Column(Float, default=0.15, nullable=False)
    is_significant = Column(Boolean, default=True, nullable=False)
    winner = Column(String(32), default="TREATMENT", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMlFeatureModel(BaseModel):
    """ML Feature Store registry."""
    __tablename__ = "ml_features"
    __table_args__ = {"extend_existing": True}

    feature_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    definition = Column(Text, nullable=False)
    source_dataset = Column(String(128), nullable=False)
    data_type = Column(String(64), nullable=False)
    version = Column(String(32), default="1.0.0", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMlFeatureVersionModel(BaseModel):
    """Feature versioning."""
    __tablename__ = "ml_feature_versions"
    __table_args__ = {"extend_existing": True}

    feature_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    transformation_logic = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMlFeatureLineageModel(BaseModel):
    """Feature to source dataset lineage."""
    __tablename__ = "ml_feature_lineage"
    __table_args__ = {"extend_existing": True}

    feature_code = Column(String(128), nullable=False, index=True)
    dataset_code = Column(String(128), nullable=False, index=True)
    source_column = Column(String(128), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMlDatasetModel(BaseModel):
    """ML training and evaluation dataset registry."""
    __tablename__ = "ml_datasets"
    __table_args__ = {"extend_existing": True}

    dataset_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    feature_codes = Column(JSON, default=list, nullable=False)
    target_column = Column(String(128), nullable=False)
    row_count = Column(Integer, default=0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapMlDatasetVersionModel(BaseModel):
    """ML dataset version snapshots."""
    __tablename__ = "ml_dataset_versions"
    __table_args__ = {"extend_existing": True}

    dataset_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    snapshot_path = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- WORKSPACES, ALERTS, RECOMMENDATIONS & LINEAGE ---
class EdapAnalyticsWorkspaceModel(BaseModel):
    """Data Science / Analytics Workspaces."""
    __tablename__ = "analytics_workspaces"
    __table_args__ = {"extend_existing": True}

    workspace_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsNotebookModel(BaseModel):
    """Analytical notebooks."""
    __tablename__ = "analytics_notebooks"
    __table_args__ = {"extend_existing": True}

    notebook_code = Column(String(128), unique=True, nullable=False, index=True)
    workspace_code = Column(String(128), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsAlertModel(BaseModel):
    """Analytics alerts."""
    __tablename__ = "analytics_alerts"
    __table_args__ = {"extend_existing": True}

    alert_code = Column(String(64), unique=True, nullable=False, index=True)
    rule_name = Column(String(128), nullable=False)
    metric_code = Column(String(128), nullable=False, index=True)
    severity = Column(String(32), default="HIGH", nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)  # ACTIVE, ACKNOWLEDGED, RESOLVED
    message = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsAlertRuleModel(BaseModel):
    """Alert trigger rules."""
    __tablename__ = "analytics_alert_rules"
    __table_args__ = {"extend_existing": True}

    rule_name = Column(String(128), unique=True, nullable=False, index=True)
    metric_code = Column(String(128), nullable=False, index=True)
    condition = Column(String(255), nullable=False)
    threshold = Column(Float, nullable=False)
    severity = Column(String(32), default="HIGH", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsAlertEventModel(BaseModel):
    """Historical alert events."""
    __tablename__ = "analytics_alert_events"
    __table_args__ = {"extend_existing": True}

    alert_code = Column(String(64), nullable=False, index=True)
    event_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    details_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsRecommendationModel(BaseModel):
    """Cost & performance optimization recommendations."""
    __tablename__ = "analytics_recommendations"
    __table_args__ = {"extend_existing": True}

    rec_code = Column(String(64), unique=True, nullable=False, index=True)
    category = Column(String(64), nullable=False)  # COST_OPTIMIZATION, INDEXING, CACHING, MATERIALIZATION
    title = Column(String(255), nullable=False)
    impact_description = Column(Text, nullable=False)
    estimated_monthly_savings = Column(Float, default=0.0, nullable=False)
    status = Column(String(32), default="PROPOSED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsLineageModel(BaseModel):
    """Data-to-Decision Lineage links."""
    __tablename__ = "analytics_lineage"
    __table_args__ = {"extend_existing": True}

    source_node = Column(String(128), nullable=False, index=True)
    target_node = Column(String(128), nullable=False, index=True)
    link_type = Column(String(64), nullable=False)  # DATA_TO_METRIC, METRIC_TO_DASHBOARD, METRIC_TO_INSIGHT, INSIGHT_TO_DECISION
    metadata_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EdapAnalyticsAuditEventModel(BaseModel):
    """Audit events for data platform activities."""
    __tablename__ = "analytics_audit_events"
    __table_args__ = {"extend_existing": True}

    actor_email = Column(String(255), nullable=False, index=True)
    action = Column(String(128), nullable=False)
    resource_code = Column(String(128), nullable=False)
    details_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)
