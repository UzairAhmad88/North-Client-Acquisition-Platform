"""ORM models for Unified Data Platform, Data Governance, Lineage, Documents, and Knowledge."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


# 1. Data Sources & Catalog
class DataSource(BaseModel):
    """External or internal data provider source."""

    __tablename__ = "data_sources"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), default="PUBLIC_WEB", nullable=False)
    trust_level: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class DataCatalogItem(BaseModel):
    """Canonical dataset description in the data catalog."""

    __tablename__ = "data_catalog_items"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    owner_role: Mapped[str] = mapped_column(String(100), default="ADMIN", nullable=False)
    classification: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)
    retention_days: Mapped[int] = mapped_column(Integer, default=365, nullable=False)
    schema_definition: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class DataContract(BaseModel):
    """Data contract between producer and consumer domains."""

    __tablename__ = "data_contracts"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    producer_domain: Mapped[str] = mapped_column(String(100), nullable=False)
    consumer_domain: Mapped[str] = mapped_column(String(100), nullable=False)
    contract_name: Mapped[str] = mapped_column(String(150), nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    schema_spec: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


# 2. Quality & Conflicts
class DataQualityRun(BaseModel):
    """Execution record for data quality evaluation jobs."""

    __tablename__ = "data_quality_runs"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    records_evaluated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    composite_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    completeness_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    accuracy_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    consistency_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    freshness_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    validity_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    uniqueness_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    provenance_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    issues_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class DataConflict(BaseModel):
    """Contradiction record between different data sources or versions."""

    __tablename__ = "data_conflicts"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_a: Mapped[str] = mapped_column(String(150), nullable=False)
    value_a: Mapped[str] = mapped_column(Text, nullable=False)
    source_b: Mapped[str] = mapped_column(String(150), nullable=False)
    value_b: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="UNRESOLVED", nullable=False)  # UNRESOLVED, RESOLVED, IGNORED
    resolved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class DataDuplicate(BaseModel):
    """Identified candidate duplicate records."""

    __tablename__ = "data_duplicates"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    primary_id: Mapped[str] = mapped_column(String(100), nullable=False)
    duplicate_id: Mapped[str] = mapped_column(String(100), nullable=False)
    similarity_score: Mapped[float] = mapped_column(Float, default=0.9, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="CANDIDATE", nullable=False)  # CANDIDATE, MERGED, DISMISSED


# 3. Provenance & Lineage
class DataProvenanceRecord(BaseModel):
    """Authoritative source and observation envelope for a fact."""

    __tablename__ = "data_provenance_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(50), default="OBSERVED", nullable=False)
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    authority: Mapped[str] = mapped_column(String(50), default="OBSERVED", nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    actor_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    agent_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    workflow_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class DataLineageEdge(BaseModel):
    """Directed connection in the platform's lifecycle graph."""

    __tablename__ = "data_lineage_edges"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    relationship: Mapped[str] = mapped_column(String(50), default="DERIVED_FROM", nullable=False)
    transformation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    actor_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    agent_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    workflow_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


# 4. Documents & Integrity
class DocumentRecord(BaseModel):
    """Document entity with SHA-256 integrity hash."""

    __tablename__ = "document_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    project_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    doc_type: Mapped[str] = mapped_column(String(50), default="REQUIREMENTS", nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="application/pdf", nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False, index=True)  # SHA-256
    classification: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="AVAILABLE", nullable=False)


class DocumentVersionRecord(BaseModel):
    """Version snapshot of an updated document."""

    __tablename__ = "document_version_records"

    document_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("document_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    change_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


# 5. Knowledge Base & Semantic Context
class KnowledgeItemRecord(BaseModel):
    """Reusable organizational knowledge item."""

    __tablename__ = "knowledge_item_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    project_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="BUSINESS_FACT", nullable=False)
    authority: Mapped[str] = mapped_column(String(50), default="OBSERVED", nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.9, nullable=False)
    lifecycle: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)
    classification: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    confirmed_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class KnowledgeRelationshipRecord(BaseModel):
    """Graph connection between knowledge items."""

    __tablename__ = "knowledge_relationship_records"

    source_knowledge_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("knowledge_item_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_knowledge_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("knowledge_item_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relationship_type: Mapped[str] = mapped_column(String(50), default="IMPLEMENTS", nullable=False)


# 6. Retention & Legal Hold
class DataRetentionPolicyRecord(BaseModel):
    """Configured domain retention rule."""

    __tablename__ = "data_retention_policy_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    retention_days: Mapped[int] = mapped_column(Integer, default=365, nullable=False)
    archive_after_days: Mapped[Optional[int]] = mapped_column(Integer, default=180, nullable=True)
    auto_delete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class LegalHoldRecord(BaseModel):
    """Legal hold locking records against deletion."""

    __tablename__ = "legal_hold_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    applied_by: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    released_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    released_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
