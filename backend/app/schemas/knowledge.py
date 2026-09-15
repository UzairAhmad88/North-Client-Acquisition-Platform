"""
Pydantic Schemas for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class KnowledgeItemCreateRequest(BaseModel):
    knowledge_code: str
    title: str
    content: str
    summary: Optional[str] = None
    domain: str = "BUSINESS"
    item_type: str = "FACT"
    authority: str = "OBSERVED"
    provenance: str = "SYSTEM_GENERATED"
    confidence: float = 1.0
    classification: str = "INTERNAL"
    is_ai_generated: bool = False


class KnowledgeItemUpdateRequest(BaseModel):
    new_content: str
    change_reason: str
    new_title: Optional[str] = None


class KnowledgeItemResponse(BaseModel):
    knowledge_code: str
    tenant_id: str
    title: str
    content: str
    summary: Optional[str] = None
    domain: str
    item_type: str
    provenance: str
    authority: str
    confidence: float
    classification: str
    freshness_status: str
    version: int
    status: str
    owner_id: str
    content_hash: str
    created_at: datetime
    updated_at: datetime


class KnowledgeFactCreateRequest(BaseModel):
    fact_code: str
    subject: str
    predicate: str
    target_value: str
    authority: str = "OBSERVED"
    confidence: float = 1.0
    source_reference: Optional[str] = None


class KnowledgeFactResponse(BaseModel):
    fact_code: str
    tenant_id: str
    subject: str
    predicate: str
    target_value: str
    authority: str
    confidence: float
    source_reference: Optional[str] = None


class KnowledgeDecisionCreateRequest(BaseModel):
    decision_code: str
    title: str
    question: str
    context_background: str
    options_considered: List[Dict[str, Any]] = Field(default_factory=list)
    decision_outcome: str
    rationale: str
    owner_id: str = "architect"
    approver_ids: List[str] = Field(default_factory=list)
    evidence_references: List[str] = Field(default_factory=list)


class KnowledgeDecisionResponse(BaseModel):
    decision_code: str
    tenant_id: str
    title: str
    question: str
    context_background: str
    options_considered: List[Dict[str, Any]]
    decision_outcome: str
    rationale: str
    owner_id: str
    approver_ids: List[str]
    evidence_references: List[str]
    status: str
    decided_at: datetime


class KnowledgeLessonCreateRequest(BaseModel):
    lesson_code: str
    title: str
    context_scope: str
    problem: str
    root_cause: str
    what_worked: str
    what_failed: str
    recommendation: str
    applicability_domain: str = "TECHNICAL"
    owner_id: str = "lead"
    confidence: float = 0.9


class KnowledgeLessonResponse(BaseModel):
    lesson_code: str
    tenant_id: str
    title: str
    context_scope: str
    problem: str
    root_cause: str
    what_worked: str
    what_failed: str
    recommendation: str
    applicability_domain: str
    owner_id: str
    confidence: float


class KnowledgeSearchRequest(BaseModel):
    query: str
    domain: Optional[str] = None
    strategy: str = "HYBRID"
    top_k: int = 10


class SearchResultResponse(BaseModel):
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


class ContextAssemblyRequest(BaseModel):
    task_intent: str
    agent_id: str = "default_agent"
    budget_tokens: int = 4000
    domain: Optional[str] = None


class ContextAssemblyResponse(BaseModel):
    request_code: str
    agent_id: str
    task_intent: str
    budget_tokens: int
    consumed_tokens: int
    items_count: int
    citations: List[str]
    encapsulated_context: str
    uncertainty_disclosures: List[str] = Field(default_factory=list)
    assembled_at: datetime


class DocumentProcessRequest(BaseModel):
    document_id: str
    title: str
    content: str
    doc_type: str = "TECHNICAL_DOCUMENT"


class KnowledgeConflictResponse(BaseModel):
    conflict_code: str
    tenant_id: str
    source_a_code: str
    source_b_code: str
    description: str
    status: str
    detected_at: datetime
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None


class ConflictResolveRequest(BaseModel):
    resolved_by: str
    resolution_notes: str


class SearchFeedbackRequest(BaseModel):
    query: str
    result_code: str
    is_helpful: bool
    feedback_text: Optional[str] = None


class KnowledgeOverviewResponse(BaseModel):
    tenant_id: str
    total_items: int
    total_facts: int
    total_decisions: int
    total_lessons: int
    open_conflicts_count: int
    quality_scorecard: Dict[str, Any]
    domain_breakdown: Dict[str, int]
    authority_breakdown: Dict[str, int]
    recent_context_assemblies_count: int
    status: str
    timestamp: str
