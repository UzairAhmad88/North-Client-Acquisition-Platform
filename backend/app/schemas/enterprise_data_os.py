"""Pydantic Schemas for Phase 62: Unified Enterprise Data Operating System."""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime


class DataDomainCreateRequest(BaseModel):
    tenant_id: str = "default_tenant"
    name: str
    slug: str
    owner_team: str
    lead_steward_email: str
    description: Optional[str] = None


class DataSourceCreateRequest(BaseModel):
    tenant_id: str = "default_tenant"
    name: str
    source_type: str
    provider: str
    domain_id: Optional[str] = None
    connection_endpoint: str
    auth_type: str = "VAULT_SECRET_REF"
    data_classification: str = "INTERNAL"


class DataPipelineCreateRequest(BaseModel):
    tenant_id: str = "default_tenant"
    name: str
    source_datasets: List[str]
    target_dataset: str
    schedule_type: str = "SCHEDULED"
    sla_minutes: int = 60
    owner_team: str


class DataLakehouseDatasetCreateRequest(BaseModel):
    tenant_id: str = "default_tenant"
    domain_id: str
    name: str
    layer: str = "BRONZE"
    format_type: str = "PARQUET"
    storage_uri: str
    partition_keys: Optional[List[str]] = None
    record_count: int = 0
    size_mb: float = 0.0


class DataContractCreateRequest(BaseModel):
    tenant_id: str = "default_tenant"
    producer_team: str
    consumer_team: str
    dataset_id: str
    schema_version: str = "v1.0.0"
    freshness_sla_minutes: int = 120
    quality_threshold_pct: float = 99.0


class DataProductCreateRequest(BaseModel):
    tenant_id: str = "default_tenant"
    domain_id: str
    name: str
    purpose: str
    owner_team: str
    underlying_datasets: Optional[List[str]] = None


class SemanticMetricCreateRequest(BaseModel):
    tenant_id: str = "default_tenant"
    name: str
    definition: str
    formula_sql: str
    dimensions: Optional[List[str]] = None
    source_table: str
    owner_team: str


class DataAccessGrantRequest(BaseModel):
    tenant_id: str = "default_tenant"
    principal_id: str
    dataset_id: str
    access_level: str = "READ"
    row_filter_expression: Optional[str] = None
    masked_columns: Optional[List[str]] = None
    approved_by: str


class DataCopilotQueryRequest(BaseModel):
    query: str
    tenant_id: str = "default_tenant"


class SandboxedSqlQueryRequest(BaseModel):
    sql_query: str
    tenant_id: str = "default_tenant"
    read_only: bool = True
