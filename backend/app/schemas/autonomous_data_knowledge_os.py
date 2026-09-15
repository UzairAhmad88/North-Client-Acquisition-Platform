"""Pydantic Schemas for Phase 65: Autonomous Data & Knowledge Operating System."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# 1. SOURCES & CONNECTORS
class DataSourceCreateRequest(BaseModel):
    name: str
    source_type: str = "DATABASE"  # DATABASE, API, FILE, CLOUD, SAAS, STREAMING
    provider: str = "POSTGRES"
    owner: str = "data-platform@uzaii.com"
    team: str = "Data Platform"
    environment: str = "PRODUCTION"
    connection_config: Dict[str, Any] = Field(default_factory=dict)
    auth_ref: Optional[str] = None
    schema_definition: Dict[str, Any] = Field(default_factory=dict)
    refresh_rate: str = "HOURLY"
    sensitivity: str = "INTERNAL"
    classification: str = "CONFIDENTIAL"


class ConnectorRegisterRequest(BaseModel):
    connector_type: str  # database, api, files, cloud, etc.
    name: str
    version: str = "v1.0.0"
    config_schema: Dict[str, Any] = Field(default_factory=dict)
    capabilities: List[str] = Field(default_factory=list)


class IngestionJobTriggerRequest(BaseModel):
    source_id: str
    connector_id: str
    job_type: str = "BATCH"  # BATCH, STREAMING, CDC, ON_DEMAND
    watermark: Optional[str] = None


# 2. PIPELINES
class DataPipelineCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_type: str = "SCHEDULED"
    schedule_cron: Optional[str] = "0 * * * *"
    owner: str = "data-eng@uzaii.com"
    sla_minutes: int = 60
    dependencies: List[str] = Field(default_factory=list)
    steps: List[Dict[str, Any]] = Field(default_factory=list)


class PipelineRunTriggerRequest(BaseModel):
    pipeline_id: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


# 3. LAKEHOUSE & WAREHOUSE
class LakeAssetCreateRequest(BaseModel):
    name: str
    layer: str = "BRONZE"  # RAW, BRONZE, SILVER, GOLD
    format: str = "PARQUET"  # PARQUET, DELTA, ICEBERG
    storage_path: str
    partition_columns: List[str] = Field(default_factory=list)
    lineage_parent_id: Optional[str] = None


class WarehouseTableCreateRequest(BaseModel):
    table_name: str
    model_type: str = "FACT"  # FACT, DIMENSION, MEASURE, AGGREGATION, SCD2
    schema_fields: List[Dict[str, Any]] = Field(default_factory=list)
    primary_keys: List[str] = Field(default_factory=list)
    surrogate_key: Optional[str] = None
    is_scd: bool = False


# 4. PRODUCTS & CONTRACTS
class DataProductCreateRequest(BaseModel):
    name: str
    description: str
    owner: str = "analytics-team@uzaii.com"
    source_datasets: List[str] = Field(default_factory=list)
    schema_def: Dict[str, Any] = Field(default_factory=dict)
    quality_score: float = 99.0
    sla_freshness_minutes: int = 60
    security_classification: str = "INTERNAL"
    monthly_cost_usd: float = 120.0
    version: str = "v1.0.0"


class DataContractCreateRequest(BaseModel):
    dataset_name: str
    owner: str = "data-team@uzaii.com"
    schema_rules: Dict[str, Any] = Field(default_factory=dict)
    constraints: List[Dict[str, Any]] = Field(default_factory=list)
    freshness_sla_minutes: int = 60
    quality_threshold_pct: float = 98.0
    compatibility_mode: str = "BACKWARD"
    version: str = "v1.0.0"


class SchemaRegisterRequest(BaseModel):
    subject: str
    schema_type: str = "JSON"
    version: str = "v1.0.0"
    fields: List[Dict[str, Any]] = Field(default_factory=list)
    compatibility: str = "BACKWARD"
    producer: str = "event-stream@uzaii.com"


# 5. DATA QUALITY & INCIDENTS
class QualityRuleCreateRequest(BaseModel):
    dataset_name: str
    dimension: str = "COMPLETENESS"  # COMPLETENESS, ACCURACY, VALIDITY, FRESHNESS, INTEGRITY
    rule_type: str = "NOT_NULL"  # NOT_NULL, RANGE, REGEX, UNIQUE, ANOMALY
    target_column: Optional[str] = None
    expression: str
    severity: str = "HIGH"


class QualityRunRequest(BaseModel):
    dataset_name: str
    rules: Optional[List[Dict[str, Any]]] = None


class DataIncidentCreateRequest(BaseModel):
    title: str
    dataset_name: str
    pipeline_id: Optional[str] = None
    severity: str = "SEV2"
    impact_scope: Optional[str] = None
    owner: str = "data-oncall@uzaii.com"
    root_cause: Optional[str] = None


# 6. LINEAGE
class LineageEdgeCreateRequest(BaseModel):
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    transformation_logic: Optional[str] = None


class ColumnLineageCreateRequest(BaseModel):
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    transform_expression: Optional[str] = None


# 7. CATALOG & GLOSSARY
class CatalogAssetCreateRequest(BaseModel):
    name: str
    asset_type: str = "DATASET"
    description: Optional[str] = None
    owner: str = "steward@uzaii.com"
    domain: str = "Sales"
    tags: List[str] = Field(default_factory=list)
    sensitivity: str = "INTERNAL"
    quality_score: float = 95.0


class GlossaryTermCreateRequest(BaseModel):
    term_name: str
    definition: str
    domain: str = "Core Business"
    owner: str = "governance@uzaii.com"
    synonyms: List[str] = Field(default_factory=list)
    related_metrics: List[str] = Field(default_factory=list)


# 8. SEMANTIC LAYER & METRIC STORE
class SemanticModelCreateRequest(BaseModel):
    entity_name: str
    underlying_source: str
    attributes: List[Dict[str, Any]] = Field(default_factory=list)
    primary_key: str = "id"


class MetricCreateRequest(BaseModel):
    name: str
    definition: str
    formula_sql: str
    source_table: str
    dimensions: List[str] = Field(default_factory=list)
    owner: str = "bi-team@uzaii.com"
    certification_status: str = "CERTIFIED"
    version: str = "v1.0.0"


# 9. MASTER DATA & ENTITY RESOLUTION
class MasterEntityCreateRequest(BaseModel):
    entity_type: str = "CUSTOMER"
    canonical_name: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0


class EntityResolutionMatchRequest(BaseModel):
    candidate_name: str
    entity_type: str = "CUSTOMER"
    threshold: float = 0.85


# 10. KNOWLEDGE GRAPH
class KnowledgeNodeCreateRequest(BaseModel):
    label: str  # Customer, Project, Service, Dataset, Metric, etc.
    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0


class KnowledgeEdgeCreateRequest(BaseModel):
    from_node_id: str
    to_node_id: str
    relationship_type: str  # OWNS, USES, DEPENDS_ON, IMPLEMENTS, etc.
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0


class KnowledgeGraphQueryRequest(BaseModel):
    start_node_id: Optional[str] = None
    relationship_types: Optional[List[str]] = None
    depth: int = 2
    direction: str = "BOTH"  # OUT, IN, BOTH


# 11. DOCUMENTS & ENTERPRISE SEARCH
class DocumentIndexRequest(BaseModel):
    title: str
    file_type: str = "MARKDOWN"
    content: str
    storage_uri: str = "s3://uzaii-docs/sample.md"
    permissions: List[str] = Field(default_factory=lambda: ["*"])


class EnterpriseSearchRequest(BaseModel):
    query: str
    user_roles: List[str] = Field(default_factory=lambda: ["USER"])
    limit: int = 20
    mode: str = "HYBRID"  # KEYWORD, SEMANTIC, HYBRID, GRAPH


# 12. AI MEMORY
class MemoryStoreRequest(BaseModel):
    content: str
    memory_type: str = "SEMANTIC"  # WORKING, EPISODIC, SEMANTIC, PROCEDURAL, ORGANIZATIONAL
    source: str = "autonomous-agent"
    entity_ref: Optional[str] = None
    confidence: float = 0.95
    classification: str = "OBSERVED"
    permissions: List[str] = Field(default_factory=lambda: ["*"])
    sensitivity: str = "INTERNAL"


# 13. DATASETS & FEATURES
class AiDatasetCreateRequest(BaseModel):
    name: str
    purpose: str = "TRAINING"
    storage_uri: str
    row_count: int = 1000
    owner: str = "ml-eng@uzaii.com"


class FeatureRegisterRequest(BaseModel):
    name: str
    entity_name: str
    data_type: str = "FLOAT"
    transformation_sql: str
    freshness_minutes: int = 60
    owner: str = "ml-eng@uzaii.com"


# 14. PRIVACY, GOVERNANCE & ACCESS
class DataClassificationRequest(BaseModel):
    dataset_name: str
    column_name: str
    classification: str = "CONFIDENTIAL"
    pii_type: Optional[str] = None
    masking_strategy: str = "REDACT"


class DataAccessRequestCreate(BaseModel):
    user_id: str
    dataset_name: str
    justification: str


# 15. NATURAL LANGUAGE TO DATA QUERY
class NaturalLanguageQueryRequest(BaseModel):
    natural_language_prompt: str
    user_id: str = "user@uzaii.com"
    user_roles: List[str] = Field(default_factory=lambda: ["ANALYST"])
    tenant_id: str = "default_tenant"
    dialect: str = "POSTGRES"


# 16. FINOPS & RELIABILITY
class DataCostRecordRequest(BaseModel):
    category: str = "COMPUTE"  # STORAGE, COMPUTE, QUERIES, PIPELINES, AI_RETRIEVAL
    cost_usd: float


class DataSloSetRequest(BaseModel):
    data_product_name: str
    freshness_target_pct: float = 99.5
    availability_target_pct: float = 99.9
    quality_target_pct: float = 99.0


class DataRecommendationCreateRequest(BaseModel):
    category: str = "COST_OPTIMIZATION"
    title: str
    description: str
    potential_savings_usd: float = 0.0


# Convenience Aliases
DataSourceCreate = DataSourceCreateRequest
DataConnectorCreate = ConnectorRegisterRequest
DataIngestionJobCreate = IngestionJobTriggerRequest
DataPipelineCreate = DataPipelineCreateRequest
DataProductCreate = DataProductCreateRequest
DataContractCreate = DataContractCreateRequest
DataQualityRuleCreate = QualityRuleCreateRequest
DataQualityEvaluationRequest = QualityRunRequest
DataIncidentCreate = DataIncidentCreateRequest
DataLineageCreate = LineageEdgeCreateRequest
DataCatalogAssetCreate = CatalogAssetCreateRequest
BusinessTermCreate = GlossaryTermCreateRequest
SemanticModelCreate = SemanticModelCreateRequest
MetricCreate = MetricCreateRequest
MasterEntityCreate = MasterEntityCreateRequest
EntityResolutionRequest = EntityResolutionMatchRequest
KnowledgeNodeCreate = KnowledgeNodeCreateRequest
KnowledgeEdgeCreate = KnowledgeEdgeCreateRequest
DocumentCreate = DocumentIndexRequest
EnterpriseMemoryCreate = MemoryStoreRequest
KnowledgeRAGRequest = EnterpriseSearchRequest
AIDatasetCreate = AiDatasetCreateRequest
FeatureCreate = FeatureRegisterRequest
DataClassificationCreate = DataClassificationRequest
DataAccessPolicyCreate = DataClassificationRequest
DataRetentionPolicyCreate = DataClassificationRequest
LegalHoldCreate = DataClassificationRequest
DataDeletionRequestCreate = DataClassificationRequest
DataShareCreate = DataClassificationRequest
DataExportRequestCreate = DataClassificationRequest
DataAlertCreate = DataIncidentCreateRequest
DataForecastCreate = DataRecommendationCreateRequest
DataSimulationCreate = DataRecommendationCreateRequest
DataCostCreate = DataCostRecordRequest
DataBudgetCreate = DataCostRecordRequest
DataSLOCreate = DataSloSetRequest
