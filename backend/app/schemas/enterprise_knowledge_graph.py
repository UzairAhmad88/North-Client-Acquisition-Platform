"""
Phase 77: Enterprise Knowledge Graph, Semantic Intelligence & Universal Enterprise Search Schemas.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# Universal Search Schemas
class UniversalSearchRequest(BaseModel):
    query: str = Field(..., description="Natural language or keyword search query")
    tenant_id: str = Field("tenant-default", description="Tenant isolation context")
    user_role: str = Field("operator", description="RBAC/ABAC role for security trimming")
    domains: Optional[List[str]] = Field(default=None, description="Optional domain filters (FINANCE, OPERATIONS, etc.)")
    limit: int = Field(20, ge=1, le=100)


class SearchResultItem(BaseModel):
    id: str
    title: str
    entity_type: str
    snippet: str
    relevance_score: float
    domain: str
    source_system: str
    confidence: float
    security_clearance: str
    explanation: Dict[str, Any]


class UniversalSearchResponse(BaseModel):
    query: str
    interpreted_intent: str
    extracted_entities: List[str]
    total_results: int
    security_trimmed_count: int
    latency_ms: float
    results: List[SearchResultItem]


# Entity & Entity 360 Schemas
class EntityResolveRequest(BaseModel):
    records: List[Dict[str, Any]]
    tenant_id: str = Field("tenant-default")


class EntityResolveResponse(BaseModel):
    canonical_entity_code: str
    canonical_name: str
    merged_sources: List[str]
    confidence_score: float
    match_evidence: List[str]
    requires_human_review: bool


class Entity360Response(BaseModel):
    entity_code: str
    canonical_name: str
    entity_type: str
    confidence: float
    status: str
    attributes: Dict[str, Any]
    aliases: List[str]
    relationships: List[Dict[str, Any]]
    documents: List[Dict[str, Any]]
    claims: List[Dict[str, Any]]
    lineage: List[Dict[str, Any]]
    ai_insights: List[str]


# Graph Traversal Schemas
class GraphQueryRequest(BaseModel):
    start_entity_code: str
    max_depth: int = Field(2, ge=1, le=5)
    relationship_types: Optional[List[str]] = None
    tenant_id: str = Field("tenant-default")


class GraphQueryResponse(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    shortest_path: Optional[List[str]] = None
    analytics: Dict[str, Any]


# Claims & Evidence Schemas
class ClaimVerificationRequest(BaseModel):
    claim_code: str
    tenant_id: str = Field("tenant-default")


class ClaimVerificationResponse(BaseModel):
    claim_code: str
    subject: str
    predicate: str
    object_value: str
    verification_status: str  # VERIFIED, CONTRADICTED, UNCERTAIN
    evidence_count: int
    composite_confidence: float
    evidence_trail: List[Dict[str, Any]]


# Conflict & Quality Schemas
class ConflictResolutionRequest(BaseModel):
    conflict_code: str
    resolution_strategy: str  # RECENCY, AUTHORITY_TIER, MANUAL_OVERRIDE
    resolved_value: Optional[str] = None
    resolver: str = "EnterpriseSteward"
    tenant_id: str = Field("tenant-default")


class ConflictResolutionResponse(BaseModel):
    conflict_code: str
    status: str
    resolved_value: str
    resolution_strategy: str


class KnowledgeQualityResponse(BaseModel):
    overall_quality_score: float
    completeness_score: float
    accuracy_score: float
    freshness_score: float
    source_reliability_score: float
    uniqueness_score: float
    domains: Dict[str, float]
    active_conflicts_count: int
    open_gaps_count: int


# Ingestion Schemas
class IngestionTriggerRequest(BaseModel):
    source_name: str
    document_payloads: List[Dict[str, Any]]
    tenant_id: str = Field("tenant-default")


class IngestionTriggerResponse(BaseModel):
    job_code: str
    status: str
    documents_queued: int
    estimated_duration_sec: float


# Summary Dashboard Schemas
class KnowledgeFabricSummaryResponse(BaseModel):
    total_canonical_entities: int
    total_relationships: int
    total_claims: int
    total_documents: int
    overall_quality_score: float
    active_conflicts: int
    open_knowledge_gaps: int
    search_queries_today: int
    active_knowledge_agents: int
    fabric_status: str
