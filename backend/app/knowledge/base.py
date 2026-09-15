"""
Base Enums, Canonical Schemas and Constants for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class KnowledgeDomain(str, Enum):
    BUSINESS = "BUSINESS"
    CRM = "CRM"
    SALES = "SALES"
    CLIENT = "CLIENT"
    COMMUNICATION = "COMMUNICATION"
    REQUIREMENTS = "REQUIREMENTS"
    SOLUTION = "SOLUTION"
    PROJECT = "PROJECT"
    DELIVERY = "DELIVERY"
    SUPPORT = "SUPPORT"
    FINANCE = "FINANCE"
    CONTRACT = "CONTRACT"
    LEGAL = "LEGAL"
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    COMPLIANCE = "COMPLIANCE"
    AI = "AI"
    TECHNICAL = "TECHNICAL"
    OPERATIONS = "OPERATIONS"
    RELIABILITY = "RELIABILITY"
    WORKFLOW = "WORKFLOW"
    POLICY = "POLICY"
    GOVERNANCE = "GOVERNANCE"
    DOCUMENTS = "DOCUMENTS"
    DECISIONS = "DECISIONS"
    ORGANIZATIONAL_MEMORY = "ORGANIZATIONAL_MEMORY"


class KnowledgeType(str, Enum):
    FACT = "FACT"
    CLAIM = "CLAIM"
    DECISION = "DECISION"
    LESSON = "LESSON"
    REQUIREMENT = "REQUIREMENT"
    POLICY = "POLICY"
    PROCEDURE = "PROCEDURE"
    GUIDELINE = "GUIDELINE"
    INSIGHT = "INSIGHT"
    ISSUE = "ISSUE"
    RESOLUTION = "RESOLUTION"
    FAQ = "FAQ"
    CLIENT_PREFERENCE = "CLIENT_PREFERENCE"
    PROJECT_DECISION = "PROJECT_DECISION"
    TECHNICAL_PATTERN = "TECHNICAL_PATTERN"
    BUSINESS_RULE = "BUSINESS_RULE"
    CONTROL = "CONTROL"
    EVIDENCE_REFERENCE = "EVIDENCE_REFERENCE"


class KnowledgeAuthority(str, Enum):
    AUTHORITATIVE = "AUTHORITATIVE"  # Signed contracts, statutory laws, primary source records
    VERIFIED = "VERIFIED"            # Formally verified by QA, auditor, or compliance officer
    CONFIRMED = "CONFIRMED"          # Client-confirmed requirement or approved decision
    OBSERVED = "OBSERVED"            # System event, log telemetry, or raw web crawl
    DERIVED = "DERIVED"              # Calculated aggregate metric, normalized data
    INFERRED = "INFERRED"            # AI extraction or probabilistic inference (never authoritative)
    UNVERIFIED = "UNVERIFIED"        # Raw unconfirmed claim
    UNKNOWN = "UNKNOWN"


class KnowledgeProvenance(str, Enum):
    USER_PROVIDED = "USER_PROVIDED"
    CLIENT_PROVIDED = "CLIENT_PROVIDED"
    OBSERVED = "OBSERVED"
    DOCUMENT = "DOCUMENT"
    MESSAGE = "MESSAGE"
    MEETING = "MEETING"
    SYSTEM_GENERATED = "SYSTEM_GENERATED"
    AI_INFERRED = "AI_INFERRED"
    HUMAN_CONFIRMED = "HUMAN_CONFIRMED"
    IMPORTED = "IMPORTED"
    DERIVED = "DERIVED"
    CALCULATED = "CALCULATED"
    EXTERNAL_SOURCE = "EXTERNAL_SOURCE"


class KnowledgeLifecycle(str, Enum):
    DRAFT = "DRAFT"
    EXTRACTED = "EXTRACTED"
    REVIEW = "REVIEW"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    UPDATED = "UPDATED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"
    DISPUTED = "DISPUTED"
    CONTRADICTED = "CONTRADICTED"
    EXPIRED = "EXPIRED"


class FreshnessStatus(str, Enum):
    FRESH = "FRESH"
    AGING = "AGING"
    STALE = "STALE"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


class GraphRelationshipType(str, Enum):
    RELATED_TO = "RELATED_TO"
    DEPENDS_ON = "DEPENDS_ON"
    REQUIRES = "REQUIRES"
    IMPLEMENTS = "IMPLEMENTS"
    DERIVED_FROM = "DERIVED_FROM"
    SUPPORTED_BY = "SUPPORTED_BY"
    CONTRADICTS = "CONTRADICTS"
    SUPERSEDES = "SUPERSEDES"
    CREATED_BY = "CREATED_BY"
    OWNED_BY = "OWNED_BY"
    APPROVED_BY = "APPROVED_BY"
    AFFECTS = "AFFECTS"
    BLOCKS = "BLOCKS"
    RESOLVES = "RESOLVES"
    REFERENCES = "REFERENCES"
    USES = "USES"
    PART_OF = "PART_OF"
    PRECEDES = "PRECEDES"
    FOLLOWS = "FOLLOWS"


class SearchStrategy(str, Enum):
    KEYWORD = "KEYWORD"
    EXACT = "EXACT"
    SEMANTIC = "SEMANTIC"
    HYBRID = "HYBRID"
    GRAPH = "GRAPH"


class ConflictStatus(str, Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"


# =============================================================================
# Canonical Pydantic Schemas
# =============================================================================

class KnowledgeItem(BaseModel):
    knowledge_code: str
    tenant_id: str = "default_tenant"
    organization_id: Optional[str] = None
    item_type: KnowledgeType = KnowledgeType.FACT
    title: str
    content: str
    summary: Optional[str] = None
    domain: KnowledgeDomain = KnowledgeDomain.BUSINESS
    source_type: str = "SYSTEM"
    source_id: Optional[str] = None
    provenance: KnowledgeProvenance = KnowledgeProvenance.SYSTEM_GENERATED
    authority: KnowledgeAuthority = KnowledgeAuthority.OBSERVED
    confidence: float = 1.0
    classification: str = "INTERNAL"
    valid_from: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    valid_until: Optional[datetime] = None
    freshness_status: FreshnessStatus = FreshnessStatus.FRESH
    version: int = 1
    status: KnowledgeLifecycle = KnowledgeLifecycle.ACTIVE
    owner_id: str = "system"
    content_hash: str = ""
    metadata_payload: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FactItem(BaseModel):
    fact_code: str
    tenant_id: str = "default_tenant"
    subject: str
    predicate: str
    target_value: str
    authority: KnowledgeAuthority = KnowledgeAuthority.OBSERVED
    confidence: float = 1.0
    source_reference: Optional[str] = None
    verified_by: Optional[str] = None


class DecisionRecord(BaseModel):
    decision_code: str
    tenant_id: str = "default_tenant"
    title: str
    question: str
    context_background: str
    options_considered: List[Dict[str, Any]] = Field(default_factory=list)
    decision_outcome: str
    rationale: str
    owner_id: str
    approver_ids: List[str] = Field(default_factory=list)
    evidence_references: List[str] = Field(default_factory=list)
    status: str = "APPROVED"
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LessonItem(BaseModel):
    lesson_code: str
    tenant_id: str = "default_tenant"
    title: str
    context_scope: str
    problem: str
    root_cause: str
    what_worked: str
    what_failed: str
    recommendation: str
    applicability_domain: str = "TECHNICAL"
    owner_id: str
    confidence: float = 0.9


class KnowledgeEntity(BaseModel):
    entity_code: str
    tenant_id: str = "default_tenant"
    entity_type: str
    name: str
    domain: str = "BUSINESS"
    canonical_uri: Optional[str] = None
    metadata_payload: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeRelationship(BaseModel):
    source_entity_code: str
    target_entity_code: str
    relationship_type: GraphRelationshipType = GraphRelationshipType.RELATED_TO
    confidence: float = 1.0
    tenant_id: str = "default_tenant"
    metadata_payload: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeChunk(BaseModel):
    chunk_code: str
    document_id: str
    chunk_index: int
    section_heading: Optional[str] = None
    content: str
    content_hash: str
    token_estimate: int = 0
    access_scope: str = "INTERNAL"
    tenant_id: str = "default_tenant"


class SearchResultItem(BaseModel):
    knowledge_code: str
    title: str
    snippet: str
    domain: str
    item_type: str
    authority: str
    provenance: str
    freshness: str
    score: float
    relevance_factors: Dict[str, float] = Field(default_factory=dict)


class ContextBundle(BaseModel):
    request_code: str
    agent_id: str
    task_intent: str
    budget_tokens: int
    consumed_tokens: int
    items: List[KnowledgeItem]
    citations: List[str]
    encapsulated_context: str
    uncertainty_disclosures: List[str] = Field(default_factory=list)
    assembled_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConflictRecord(BaseModel):
    conflict_code: str
    tenant_id: str = "default_tenant"
    source_a_code: str
    source_b_code: str
    description: str
    status: ConflictStatus = ConflictStatus.OPEN
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
