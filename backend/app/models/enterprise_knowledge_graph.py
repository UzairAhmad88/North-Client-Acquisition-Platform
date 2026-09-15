"""
Phase 77: Enterprise Knowledge Graph, Organizational Memory, Semantic Intelligence & Universal Enterprise Search.
Table Prefix: ekg_*
Zero-collision namespace with Phases 0-76.
"""

from datetime import datetime
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
    Text
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class EkgEntityModel(BaseModel):
    """Canonical enterprise entity resolved across all source systems."""
    __tablename__ = "ekg_entities"

    entity_code = Column(String(64), unique=True, nullable=False, index=True)
    canonical_name = Column(String(255), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False, index=True)  # CUSTOMER, SUPPLIER, PRODUCT, PROJECT, CONTRACT, INVOICE, PERSON, SYSTEM
    description = Column(Text, nullable=True)
    confidence_score = Column(Float, default=1.0, nullable=False)
    source_count = Column(Integer, default=1, nullable=False)
    aliases = Column(JSON, default=list, nullable=False)
    attributes = Column(JSON, default=dict, nullable=False)
    provenance = Column(JSON, default=dict, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)  # ACTIVE, MERGED, ARCHIVED, PROPOSED
    owner = Column(String(255), default="EnterpriseSteward", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgEntityAliasModel(BaseModel):
    """Alternative names and representations mapped to canonical entity."""
    __tablename__ = "ekg_entity_aliases"

    alias_name = Column(String(255), nullable=False, index=True)
    entity_code = Column(String(64), nullable=False, index=True)
    source_system = Column(String(64), nullable=False)
    confidence = Column(Float, default=0.9, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgRelationshipModel(BaseModel):
    """Temporal directed graph edge connecting two canonical entities."""
    __tablename__ = "ekg_relationships"

    rel_code = Column(String(64), unique=True, nullable=False, index=True)
    source_entity_code = Column(String(64), nullable=False, index=True)
    target_entity_code = Column(String(64), nullable=False, index=True)
    relationship_type = Column(String(64), nullable=False, index=True)  # OWNS, SUPPLIES, WORKS_ON, DEPENDS_ON, GOVERNS, REFERENCES
    confidence = Column(Float, default=1.0, nullable=False)
    valid_from = Column(DateTime, default=datetime.utcnow, nullable=False)
    valid_to = Column(DateTime, nullable=True)
    properties = Column(JSON, default=dict, nullable=False)
    provenance = Column(JSON, default=dict, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgClaimModel(BaseModel):
    """Knowledge claim asserting Subject-Predicate-Object with evidence strength."""
    __tablename__ = "ekg_claims"

    claim_code = Column(String(64), unique=True, nullable=False, index=True)
    subject = Column(String(255), nullable=False, index=True)
    predicate = Column(String(128), nullable=False, index=True)
    object_value = Column(Text, nullable=False)
    claim_type = Column(String(32), default="FACT", nullable=False)  # FACT, OBSERVATION, INFERENCE, HYPOTHESIS, PREDICTION, POLICY
    confidence = Column(Float, default=0.95, nullable=False)
    verification_status = Column(String(32), default="VERIFIED", nullable=False)
    evidence_summary = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgClaimEvidenceModel(BaseModel):
    """Specific document, audit record, or telemetry supporting a claim."""
    __tablename__ = "ekg_claim_evidence"

    evidence_code = Column(String(64), unique=True, nullable=False, index=True)
    claim_code = Column(String(64), nullable=False, index=True)
    source_document_code = Column(String(64), nullable=True)
    evidence_text = Column(Text, nullable=False)
    relevance_score = Column(Float, default=0.9, nullable=False)
    source_reliability = Column(Float, default=0.95, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgDocumentModel(BaseModel):
    """Ingested enterprise document metadata and extraction state."""
    __tablename__ = "ekg_documents"

    document_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    file_type = Column(String(32), nullable=False)  # PDF, DOCX, XLSX, CSV, PPTX, HTML, TXT
    classification = Column(String(32), default="INTERNAL", nullable=False)  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    author = Column(String(255), default="Unknown", nullable=False)
    version = Column(String(32), default="1.0.0", nullable=False)
    source_system = Column(String(64), default="ECM", nullable=False)
    content_hash = Column(String(64), nullable=False)
    chunk_count = Column(Integer, default=0, nullable=False)
    entity_count = Column(Integer, default=0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgDocumentChunkModel(BaseModel):
    """Text chunk extracted from ingested documents for vector/keyword retrieval."""
    __tablename__ = "ekg_document_chunks"

    chunk_code = Column(String(64), unique=True, nullable=False, index=True)
    document_code = Column(String(64), nullable=False, index=True)
    chunk_index = Column(Integer, default=0, nullable=False)
    content = Column(Text, nullable=False)
    embedding_id = Column(String(64), nullable=True)
    metadata_payload = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgSourceModel(BaseModel):
    """Authoritative enterprise data sources with configured reliability rankings."""
    __tablename__ = "ekg_sources"

    source_code = Column(String(64), unique=True, nullable=False, index=True)
    source_name = Column(String(128), nullable=False)
    source_type = Column(String(64), nullable=False)  # ERP, CRM, FINANCIAL_LEDGER, CONTRACT_REPO, HRIS, TELEMETRY
    reliability_tier = Column(Integer, default=1, nullable=False)  # 1 (Highest) to 5 (Unverified)
    reliability_weight = Column(Float, default=1.0, nullable=False)
    is_authoritative = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgOntologyModel(BaseModel):
    """Formal business ontology definitions for entity classes, predicates and axioms."""
    __tablename__ = "ekg_ontologies"

    ontology_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    domain = Column(String(64), nullable=False)  # FINANCE, OPERATIONS, SALES, LEGAL, COMPLIANCE
    version = Column(String(32), default="1.0.0", nullable=False)
    entity_types = Column(JSON, default=list, nullable=False)
    relationship_types = Column(JSON, default=list, nullable=False)
    axioms = Column(JSON, default=list, nullable=False)
    status = Column(String(32), default="PUBLISHED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgTaxonomyModel(BaseModel):
    """Hierarchical classification taxonomy for enterprise concepts."""
    __tablename__ = "ekg_taxonomies"

    taxonomy_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    domain = Column(String(64), nullable=False)
    tree_hierarchy = Column(JSON, default=dict, nullable=False)
    node_count = Column(Integer, default=0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgGlossaryTermModel(BaseModel):
    """Governed enterprise business glossary term with canonical definition."""
    __tablename__ = "ekg_glossary_terms"

    term_code = Column(String(64), unique=True, nullable=False, index=True)
    term = Column(String(128), nullable=False, index=True)
    definition = Column(Text, nullable=False)
    domain = Column(String(64), nullable=False)
    owner = Column(String(255), nullable=False)
    aliases = Column(JSON, default=list, nullable=False)
    related_terms = Column(JSON, default=list, nullable=False)
    status = Column(String(32), default="APPROVED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgMetadataAssetModel(BaseModel):
    """Metadata catalog asset representing a table, API, model or document stream."""
    __tablename__ = "ekg_metadata_assets"

    asset_code = Column(String(64), unique=True, nullable=False, index=True)
    asset_name = Column(String(255), nullable=False, index=True)
    asset_type = Column(String(64), nullable=False)  # TABLE, COLUMN, API, DATASET, AI_MODEL
    source_system = Column(String(64), nullable=False)
    schema_definition = Column(JSON, default=dict, nullable=False)
    sensitivity = Column(String(32), default="INTERNAL", nullable=False)
    owner = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgDataLineageModel(BaseModel):
    """Data lineage tracking provenance from upstream ingestion to downstream AI decisions."""
    __tablename__ = "ekg_data_lineage"

    lineage_code = Column(String(64), unique=True, nullable=False, index=True)
    upstream_asset_code = Column(String(64), nullable=False, index=True)
    downstream_asset_code = Column(String(64), nullable=False, index=True)
    transformation_step = Column(String(128), nullable=False)
    run_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    impact_weight = Column(Float, default=1.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgDataClassificationModel(BaseModel):
    """Information security tagging: Public, Internal, Confidential, Restricted."""
    __tablename__ = "ekg_data_classifications"

    classification_code = Column(String(64), unique=True, nullable=False, index=True)
    target_entity_code = Column(String(64), nullable=False, index=True)
    classification_level = Column(String(32), nullable=False)  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
    tags = Column(JSON, default=list, nullable=False)  # PII, FINANCIAL, CREDENTIAL, LEGAL
    justification = Column(String(255), nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgConflictModel(BaseModel):
    """Discrepancy detected between two conflicting authoritative facts or sources."""
    __tablename__ = "ekg_conflicts"

    conflict_code = Column(String(64), unique=True, nullable=False, index=True)
    entity_code = Column(String(64), nullable=False, index=True)
    attribute_name = Column(String(128), nullable=False)
    fact_a_value = Column(Text, nullable=False)
    fact_a_source = Column(String(128), nullable=False)
    fact_b_value = Column(Text, nullable=False)
    fact_b_source = Column(String(128), nullable=False)
    resolution_status = Column(String(32), default="DETECTED", nullable=False)  # DETECTED, RESOLVED, ESCALATED
    resolution_strategy = Column(String(64), nullable=True)  # RECENCY, AUTHORITY_TIER, MANUAL_OVERRIDE
    resolved_value = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgGapModel(BaseModel):
    """Detected knowledge gap such as missing definitions, unlinked entities, or stale data."""
    __tablename__ = "ekg_gaps"

    gap_code = Column(String(64), unique=True, nullable=False, index=True)
    gap_type = Column(String(64), nullable=False)  # MISSING_ENTITY, UNLINKED_RELATION, STALE_RECORD, NO_OWNER
    domain = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(32), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    recommended_action = Column(Text, nullable=False)
    status = Column(String(32), default="OPEN", nullable=False)  # OPEN, IN_PROGRESS, RESOLVED
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgQualityScoreModel(BaseModel):
    """Aggregate domain knowledge quality metric."""
    __tablename__ = "ekg_quality_scores"

    domain = Column(String(64), nullable=False, index=True)
    overall_quality = Column(Float, default=95.0, nullable=False)
    completeness_score = Column(Float, default=94.0, nullable=False)
    accuracy_score = Column(Float, default=97.0, nullable=False)
    freshness_score = Column(Float, default=92.0, nullable=False)
    source_reliability_score = Column(Float, default=98.0, nullable=False)
    uniqueness_score = Column(Float, default=96.0, nullable=False)
    evaluated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgLessonModel(BaseModel):
    """Organizational memory record documenting historical lessons learned."""
    __tablename__ = "ekg_lessons"

    lesson_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    problem_statement = Column(Text, nullable=False)
    action_taken = Column(Text, nullable=False)
    outcome = Column(Text, nullable=False)
    applicability_domain = Column(String(64), nullable=False)
    related_entity_codes = Column(JSON, default=list, nullable=False)
    owner = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgSearchQueryModel(BaseModel):
    """Search log tracking query understanding, security trimming, and latency."""
    __tablename__ = "ekg_search_queries"

    query_code = Column(String(64), unique=True, nullable=False, index=True)
    query_text = Column(String(512), nullable=False)
    intent = Column(String(64), nullable=False)
    extracted_entities = Column(JSON, default=list, nullable=False)
    results_count = Column(Integer, default=0, nullable=False)
    latency_ms = Column(Float, default=12.5, nullable=False)
    user_role = Column(String(64), default="operator", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgStewardModel(BaseModel):
    """Designated knowledge and data stewards overseeing domain integrity."""
    __tablename__ = "ekg_stewards"

    steward_code = Column(String(64), unique=True, nullable=False, index=True)
    steward_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    domain = Column(String(64), nullable=False)  # FINANCE, OPERATIONS, LEGAL, SECURITY
    role = Column(String(64), default="DOMAIN_STEWARD", nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgRetentionPolicyModel(BaseModel):
    """Configurable lifecycle retention and deletion rules."""
    __tablename__ = "ekg_retention_policies"

    policy_code = Column(String(64), unique=True, nullable=False, index=True)
    domain = Column(String(64), nullable=False)
    entity_type = Column(String(64), nullable=False)
    retention_days = Column(Integer, default=365, nullable=False)
    deletion_propagation = Column(Boolean, default=True, nullable=False)  # Propagate to indexes, vectors, graph
    legal_hold_enabled = Column(Boolean, default=False, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EkgIngestionJobModel(BaseModel):
    """Background ingestion and normalization pipeline run."""
    __tablename__ = "ekg_ingestion_jobs"

    job_code = Column(String(64), unique=True, nullable=False, index=True)
    source_name = Column(String(128), nullable=False)
    documents_processed = Column(Integer, default=0, nullable=False)
    entities_extracted = Column(Integer, default=0, nullable=False)
    relationships_created = Column(Integer, default=0, nullable=False)
    status = Column(String(32), default="COMPLETED", nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)
