"""
ORM models for Phase 48: Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from app.models.base import BaseModel
except ImportError:
    from app.models.base import BaseModel


class KnowledgeItemModel(BaseModel):
    """Canonical, governed organizational knowledge item."""

    __tablename__ = "knowledge_items"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    knowledge_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    item_type: Mapped[str] = mapped_column(String(50), default="FACT", nullable=False, index=True)  # FACT, DECISION, LESSON, REQUIREMENT, POLICY, GUIDELINE, TECHNICAL_PATTERN, CLIENT_PREFERENCE
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    domain: Mapped[str] = mapped_column(String(100), default="BUSINESS", nullable=False, index=True)  # BUSINESS, TECHNICAL, SECURITY, PRIVACY, AI, FINANCE, OPERATIONS, RELIABILITY, CLIENT, GOVERNANCE
    source_type: Mapped[str] = mapped_column(String(50), default="SYSTEM", nullable=False)  # DOCUMENT, MESSAGE, MEETING, HUMAN_INPUT, SYSTEM, AI_EXTRACTION, AUDIT
    source_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provenance: Mapped[str] = mapped_column(String(50), default="SYSTEM_GENERATED", nullable=False)  # USER_PROVIDED, CLIENT_PROVIDED, OBSERVED, DOCUMENT, AI_INFERRED, HUMAN_CONFIRMED, DERIVED
    authority: Mapped[str] = mapped_column(String(50), default="OBSERVED", nullable=False, index=True)  # AUTHORITATIVE, VERIFIED, CONFIRMED, OBSERVED, DERIVED, INFERRED, UNVERIFIED
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    classification: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    freshness_status: Mapped[str] = mapped_column(String(50), default="FRESH", nullable=False, index=True)  # FRESH, AGING, STALE, EXPIRED, UNKNOWN
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)  # DRAFT, REVIEW, CONFIRMED, ACTIVE, SUPERSEDED, ARCHIVED, CONTRADICTED
    owner_id: Mapped[str] = mapped_column(String(100), default="system", nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # SHA-256
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class KnowledgeItemVersionModel(BaseModel):
    """Immutable version history of knowledge changes (no silent overwriting)."""

    __tablename__ = "knowledge_item_versions"

    knowledge_item_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("knowledge_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    change_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)


class KnowledgeFactModel(BaseModel):
    """Atomic factual claims extracted from documents, systems, or human statements."""

    __tablename__ = "knowledge_facts"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    fact_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    predicate: Mapped[str] = mapped_column(String(100), nullable=False)
    target_value: Mapped[str] = mapped_column(Text, nullable=False)
    authority: Mapped[str] = mapped_column(String(50), default="OBSERVED", nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verified_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)


class KnowledgeDecisionModel(BaseModel):
    """Persistent organizational memory for architectural, commercial, and technical decisions."""

    __tablename__ = "knowledge_decisions"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    decision_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    question: Mapped[Text] = mapped_column(Text, nullable=False)
    context_background: Mapped[Text] = mapped_column(Text, nullable=False)
    options_considered: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    decision_outcome: Mapped[Text] = mapped_column(Text, nullable=False)
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    approver_ids: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    evidence_references: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="APPROVED", nullable=False)  # PROPOSED, APPROVED, SUPERSEDED, REVOKED
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class KnowledgeLessonModel(BaseModel):
    """Structured retrospective lessons learned from past projects, incidents, or sales."""

    __tablename__ = "knowledge_lessons"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    lesson_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    context_scope: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g., "PostgreSQL Multi-tenant Migrations"
    problem: Mapped[Text] = mapped_column(Text, nullable=False)
    root_cause: Mapped[Text] = mapped_column(Text, nullable=False)
    what_worked: Mapped[Text] = mapped_column(Text, nullable=False)
    what_failed: Mapped[Text] = mapped_column(Text, nullable=False)
    recommendation: Mapped[Text] = mapped_column(Text, nullable=False)
    applicability_domain: Mapped[str] = mapped_column(String(100), default="TECHNICAL", nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.9, nullable=False)


class KnowledgeEntityModel(BaseModel):
    """Named entity nodes in the organizational knowledge graph."""

    __tablename__ = "knowledge_entities"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    entity_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # CLIENT, PROJECT, REQUIREMENT, FEATURE, POLICY, CONTROL, SERVICE, VENDOR, INCIDENT
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str] = mapped_column(String(100), default="BUSINESS", nullable=False)
    canonical_uri: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class KnowledgeRelationshipModel(BaseModel):
    """Typed relationship edges connecting knowledge graph entities."""

    __tablename__ = "knowledge_relationships"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    source_entity_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    target_entity_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # RELATED_TO, DEPENDS_ON, REQUIRES, IMPLEMENTS, DERIVED_FROM, CONTRADICTS, SUPERSEDES, RESOLVES, REFERENCES
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class KnowledgeCollectionModel(BaseModel):
    """Curated groupings of knowledge assets."""

    __tablename__ = "knowledge_collections"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    collection_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    classification: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class KnowledgeCollectionMemberModel(BaseModel):
    """Items enrolled in a knowledge collection."""

    __tablename__ = "knowledge_collection_members"

    collection_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("knowledge_collections.id", ondelete="CASCADE"), nullable=False, index=True
    )
    knowledge_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    added_by: Mapped[str] = mapped_column(String(100), nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class KnowledgeChunkModel(BaseModel):
    """Structurally chunked document sections optimized for vectorization and semantic search."""

    __tablename__ = "knowledge_chunks"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    chunk_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    document_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    section_heading: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    token_estimate: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    access_scope: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)


class KnowledgeEmbeddingModel(BaseModel):
    """Vector representations for semantic similarity retrieval."""

    __tablename__ = "knowledge_embeddings"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    chunk_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model_name: Mapped[str] = mapped_column(String(100), default="text-embedding-3-small", nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    dimensions: Mapped[int] = mapped_column(Integer, default=1536, nullable=False)
    vector_data: Mapped[List[float]] = mapped_column(JSON, nullable=False)  # Normalized vector representation
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)


class KnowledgeConflictModel(BaseModel):
    """Detected contradictions between knowledge items, requirements, or client statements."""

    __tablename__ = "knowledge_conflicts"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    conflict_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    source_a_code: Mapped[str] = mapped_column(String(100), nullable=False)
    source_b_code: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="OPEN", nullable=False)  # OPEN, RESOLVED, DISMISSED
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class KnowledgeContextRequestModel(BaseModel):
    """Telemetry log of AI agent context assembly requests, budgeting, and citations."""

    __tablename__ = "knowledge_context_requests"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    request_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    task_intent: Mapped[str] = mapped_column(String(255), nullable=False)
    budget_tokens: Mapped[int] = mapped_column(Integer, default=4000, nullable=False)
    consumed_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    item_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    context_bundle_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class KnowledgeEvaluationRunModel(BaseModel):
    """Search & semantic retrieval evaluation benchmark metrics."""

    __tablename__ = "knowledge_evaluation_runs"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    run_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    dataset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    precision_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    recall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    mrr_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    grounding_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    unauthorized_leakage_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # Must be 0.0
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class KnowledgeFeedbackModel(BaseModel):
    """User and agent feedback on search results and knowledge quality."""

    __tablename__ = "knowledge_search_feedback"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    query_text: Mapped[str] = mapped_column(String(500), nullable=False)
    result_knowledge_code: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[str] = mapped_column(String(50), nullable=False)  # HELPFUL, NOT_HELPFUL, INCORRECT, OUTDATED, WRONG_PERMISSION
    feedback_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submitted_by: Mapped[str] = mapped_column(String(100), nullable=False)
