"""Pydantic request and response schemas for Phase 36: Data Governance, Lineage, Documents, Knowledge & Retention."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.data.base import (
    DataAuthority,
    DataClassification,
    KnowledgeLifecycle,
    LineageRelationship,
    ProvenanceType,
)


# -------------------------------------------------------------
# 1. Data Sources & Catalog Items
# -------------------------------------------------------------
class DataSourceCreate(BaseModel):
    name: str
    source_type: str
    description: Optional[str] = None
    connection_uri: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_authoritative: bool = False
    authority_level: DataAuthority = DataAuthority.SYSTEM_INTEGRATION


class DataSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    source_type: str
    description: Optional[str] = None
    is_authoritative: bool
    authority_level: DataAuthority
    is_active: bool
    sync_schedule: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class DataCatalogItemCreate(BaseModel):
    name: str
    domain: str
    table_or_entity_name: str
    description: Optional[str] = None
    classification: DataClassification = DataClassification.INTERNAL
    authority_level: DataAuthority = DataAuthority.VERIFIED_DATA
    source_id: Optional[str] = None
    schema_definition: Optional[Dict[str, Any]] = None
    data_owner: Optional[str] = None
    data_steward: Optional[str] = None
    sla_freshness_hours: Optional[int] = 24
    sla_quality_threshold: Optional[float] = 0.95


class DataCatalogItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    domain: str
    table_or_entity_name: str
    description: Optional[str] = None
    classification: DataClassification
    authority_level: DataAuthority
    source_id: Optional[str] = None
    schema_definition: Dict[str, Any]
    data_owner: Optional[str] = None
    data_steward: Optional[str] = None
    is_active: bool
    sla_freshness_hours: Optional[int] = None
    sla_quality_threshold: Optional[float] = None
    created_at: datetime
    updated_at: datetime


# -------------------------------------------------------------
# 2. Quality & Conflict Schemas
# -------------------------------------------------------------
class TriggerQualityCheckRequest(BaseModel):
    catalog_item_id: Optional[str] = None
    domain: Optional[str] = None
    rules_to_evaluate: Optional[List[str]] = None


class QualityMetricResponse(BaseModel):
    metric_name: str
    dimension: str
    score: float
    status: str
    details: Optional[Dict[str, Any]] = None


class QualityRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    catalog_item_id: Optional[str] = None
    rule_id: Optional[str] = None
    overall_score: float
    status: str
    total_records_evaluated: int
    passed_records: int
    failed_records: int
    dimension_scores: Dict[str, Any]
    violations: List[Any]
    executed_at: datetime


class ConflictDetectionRequest(BaseModel):
    domain: str
    entity_type: str
    entity_id: str
    records: List[Dict[str, Any]]


class ConflictResolutionRequest(BaseModel):
    resolution_strategy: str
    winning_source_id: Optional[str] = None
    resolution_notes: Optional[str] = None


class ConflictResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    domain: str
    entity_type: str
    entity_id: str
    conflict_type: str
    conflicting_fields: List[str]
    source_records: List[Any]
    status: str
    resolution_strategy: Optional[str] = None
    detected_at: datetime
    resolved_at: Optional[datetime] = None


# -------------------------------------------------------------
# 3. Lineage & Provenance Schemas
# -------------------------------------------------------------
class LineageNode(BaseModel):
    id: str
    type: str
    name: Optional[str] = None
    authority_level: Optional[str] = None


class LineageEdgeSchema(BaseModel):
    source: str
    target: str
    relationship: LineageRelationship
    transformation: Optional[str] = None
    confidence_score: Optional[float] = 1.0


class LineageGraphResponse(BaseModel):
    entity_id: str
    entity_type: str
    upstream_nodes: List[Dict[str, Any]]
    downstream_nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


class AddLineageEdgeRequest(BaseModel):
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    relationship: LineageRelationship
    transformation_name: Optional[str] = None
    transformation_version: Optional[str] = None
    confidence_score: float = 1.0
    metadata_json: Optional[Dict[str, Any]] = None


class ProvenanceRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    entity_type: str
    entity_id: str
    provenance_type: ProvenanceType
    actor_id: Optional[str] = None
    actor_type: str
    source_system: Optional[str] = None
    authority_level: DataAuthority
    context_data: Dict[str, Any]
    recorded_at: datetime


# -------------------------------------------------------------
# 4. Document Management & Integrity
# -------------------------------------------------------------
class DocumentCreateRequest(BaseModel):
    title: str
    document_type: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    classification: DataClassification = DataClassification.INTERNAL
    authority_level: DataAuthority = DataAuthority.HUMAN_CONFIRMATION


class DocumentVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    document_id: str
    version_number: int
    storage_path: Optional[str] = None
    file_size_bytes: int
    content_sha256: str
    change_summary: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    tracking_id: str
    title: str
    document_type: str
    classification: DataClassification
    authority_level: DataAuthority
    status: str
    current_version: int
    latest_sha256: str
    domain: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    metadata_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class DocumentIntegrityVerification(BaseModel):
    document_id: str
    version_number: int
    expected_sha256: str
    calculated_sha256: str
    is_valid: bool
    verified_at: datetime


# -------------------------------------------------------------
# 5. Knowledge Base & Context Retrieval
# -------------------------------------------------------------
class KnowledgeItemCreateRequest(BaseModel):
    title: str
    topic: str
    domain: str
    content: str
    summary: Optional[str] = None
    canonical_key: Optional[str] = None
    authority_level: DataAuthority = DataAuthority.RAW_DATA
    lifecycle_state: KnowledgeLifecycle = KnowledgeLifecycle.INGESTED
    classification: DataClassification = DataClassification.INTERNAL
    provenance_source: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class KnowledgePromoteRequest(BaseModel):
    target_lifecycle: KnowledgeLifecycle
    notes: Optional[str] = None
    verification_evidence: Optional[Dict[str, Any]] = None


class KnowledgeItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    canonical_key: Optional[str] = None
    title: str
    topic: str
    domain: str
    content: str
    summary: Optional[str] = None
    authority_level: DataAuthority
    lifecycle_state: KnowledgeLifecycle
    classification: DataClassification
    confidence_score: float
    provenance_source: Optional[str] = None
    created_by: Optional[str] = None
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class KnowledgeRetrievalRequest(BaseModel):
    query: str
    domain: Optional[str] = None
    allowed_classifications: Optional[List[DataClassification]] = None
    min_authority: Optional[DataAuthority] = None
    min_lifecycle: Optional[KnowledgeLifecycle] = KnowledgeLifecycle.VERIFIED
    limit: int = 10


class KnowledgeRetrievalResult(BaseModel):
    id: str
    title: str
    topic: str
    domain: str
    content: str
    authority_level: str
    lifecycle_state: str
    classification: str
    confidence_score: float
    provenance_source: Optional[str] = None


class KnowledgeRetrievalResponse(BaseModel):
    query: str
    results_count: int
    items: List[KnowledgeRetrievalResult]
    retrieved_at: datetime


# -------------------------------------------------------------
# 6. Retention Policies & Legal Holds
# -------------------------------------------------------------
class RetentionPolicyCreateRequest(BaseModel):
    domain: str
    entity_type: str
    retention_period_days: int
    action_on_expiry: str = "ARCHIVE"
    classification: Optional[DataClassification] = None
    description: Optional[str] = None


class RetentionPolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    domain: str
    entity_type: str
    classification: Optional[DataClassification] = None
    retention_period_days: int
    action_on_expiry: str
    is_active: bool
    created_at: datetime


class LegalHoldCreateRequest(BaseModel):
    case_reference: str
    reason: str
    entity_type: str
    entity_id: str
    notes: Optional[str] = None


class LegalHoldResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    case_reference: str
    reason: str
    entity_type: str
    entity_id: str
    active: bool
    placed_by: str
    placed_at: datetime
    released_by: Optional[str] = None
    released_at: Optional[datetime] = None
    notes: Optional[str] = None
