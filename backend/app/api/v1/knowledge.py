"""
REST API Router for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

try:
    from app.api.deps import get_db, get_security_context
    from app.knowledge.base import (
        KnowledgeAuthority,
        KnowledgeDomain,
        KnowledgeProvenance,
        KnowledgeType,
    )
    from app.knowledge.service import KnowledgePlatformService
    from app.schemas.knowledge import (
        ConflictResolveRequest,
        ContextAssemblyRequest,
        ContextAssemblyResponse,
        DocumentProcessRequest,
        KnowledgeConflictResponse,
        KnowledgeDecisionCreateRequest,
        KnowledgeDecisionResponse,
        KnowledgeFactCreateRequest,
        KnowledgeFactResponse,
        KnowledgeItemCreateRequest,
        KnowledgeItemResponse,
        KnowledgeItemUpdateRequest,
        KnowledgeLessonCreateRequest,
        KnowledgeLessonResponse,
        KnowledgeOverviewResponse,
        KnowledgeSearchRequest,
        SearchResultResponse,
        SearchFeedbackRequest,
    )
except ImportError:
    from backend.app.api.deps import get_db, get_security_context
    from backend.app.knowledge.base import (
        KnowledgeAuthority,
        KnowledgeDomain,
        KnowledgeProvenance,
        KnowledgeType,
    )
    from backend.app.knowledge.service import KnowledgePlatformService
    from backend.app.schemas.knowledge import (
        ConflictResolveRequest,
        ContextAssemblyRequest,
        ContextAssemblyResponse,
        DocumentProcessRequest,
        KnowledgeConflictResponse,
        KnowledgeDecisionCreateRequest,
        KnowledgeDecisionResponse,
        KnowledgeFactCreateRequest,
        KnowledgeFactResponse,
        KnowledgeItemCreateRequest,
        KnowledgeItemResponse,
        KnowledgeItemUpdateRequest,
        KnowledgeLessonCreateRequest,
        KnowledgeLessonResponse,
        KnowledgeOverviewResponse,
        KnowledgeSearchRequest,
        SearchResultResponse,
        SearchFeedbackRequest,
    )

router = APIRouter(prefix="/knowledge", tags=["knowledge-platform"])

# Shared service instance
_knowledge_service = KnowledgePlatformService()


def get_knowledge_service() -> KnowledgePlatformService:
    return _knowledge_service


# =============================================================================
# 1. Overview & Health
# =============================================================================

@router.get("/overview", response_model=KnowledgeOverviewResponse)
def get_knowledge_overview(
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """Retrieves organizational memory health, domain breakdowns, and open conflicts."""
    overview = service.get_overview(tenant_id=tenant_id)
    return KnowledgeOverviewResponse(**overview)


# =============================================================================
# 2. Canonical Knowledge Items
# =============================================================================

@router.get("/items", response_model=List[KnowledgeItemResponse])
def list_knowledge_items(
    domain: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """Lists canonical items scoped to tenant and optional domain filter."""
    dom = KnowledgeDomain(domain) if domain else None
    items = service.list_knowledge_items(domain=dom, tenant_id=tenant_id)
    return [
        KnowledgeItemResponse(
            knowledge_code=i.knowledge_code,
            tenant_id=i.tenant_id,
            title=i.title,
            content=i.content,
            summary=i.summary,
            domain=i.domain.value,
            item_type=i.item_type.value,
            provenance=i.provenance.value,
            authority=i.authority.value,
            confidence=i.confidence,
            classification=i.classification,
            freshness_status=i.freshness_status.value,
            version=i.version,
            status=i.status.value,
            owner_id=i.owner_id,
            content_hash=i.content_hash,
            created_at=i.created_at,
            updated_at=i.updated_at,
        )
        for i in items
    ]


@router.post("/items", response_model=KnowledgeItemResponse, status_code=status.HTTP_201_CREATED)
def create_knowledge_item(
    req: KnowledgeItemCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """
    Creates a canonical knowledge item.
    Enforces Rule 1-3: AI-generated items cannot autonomously declare Authoritative or Confirmed status.
    """
    try:
        authority_enum = KnowledgeAuthority(req.authority)
        provenance_enum = KnowledgeProvenance(req.provenance)
        domain_enum = KnowledgeDomain(req.domain)
        item_type_enum = KnowledgeType(req.item_type)

        item = service.create_knowledge_item(
            knowledge_code=req.knowledge_code,
            title=req.title,
            content=req.content,
            domain=domain_enum,
            item_type=item_type_enum,
            authority=authority_enum,
            provenance=provenance_enum,
            confidence=req.confidence,
            classification=req.classification,
            tenant_id=tenant_id,
            is_ai_generated=req.is_ai_generated,
        )
        return KnowledgeItemResponse(
            knowledge_code=item.knowledge_code,
            tenant_id=item.tenant_id,
            title=item.title,
            content=item.content,
            summary=item.summary,
            domain=item.domain.value,
            item_type=item.item_type.value,
            provenance=item.provenance.value,
            authority=item.authority.value,
            confidence=item.confidence,
            classification=item.classification,
            freshness_status=item.freshness_status.value,
            version=item.version,
            status=item.status.value,
            owner_id=item.owner_id,
            content_hash=item.content_hash,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.get("/items/{knowledge_code}", response_model=KnowledgeItemResponse)
def get_knowledge_item(
    knowledge_code: str,
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    item = service.get_knowledge_item(knowledge_code=knowledge_code, tenant_id=tenant_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Knowledge item '{knowledge_code}' not found")
    return KnowledgeItemResponse(
        knowledge_code=item.knowledge_code,
        tenant_id=item.tenant_id,
        title=item.title,
        content=item.content,
        summary=item.summary,
        domain=item.domain.value,
        item_type=item.item_type.value,
        provenance=item.provenance.value,
        authority=item.authority.value,
        confidence=item.confidence,
        classification=item.classification,
        freshness_status=item.freshness_status.value,
        version=item.version,
        status=item.status.value,
        owner_id=item.owner_id,
        content_hash=item.content_hash,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.put("/items/{knowledge_code}", response_model=KnowledgeItemResponse)
def update_knowledge_item(
    knowledge_code: str,
    req: KnowledgeItemUpdateRequest,
    updated_by: str = Query("system_user"),
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    try:
        item = service.update_knowledge_item(
            knowledge_code=knowledge_code,
            new_content=req.new_content,
            change_reason=req.change_reason,
            updated_by=updated_by,
            new_title=req.new_title,
        )
        return KnowledgeItemResponse(
            knowledge_code=item.knowledge_code,
            tenant_id=item.tenant_id,
            title=item.title,
            content=item.content,
            summary=item.summary,
            domain=item.domain.value,
            item_type=item.item_type.value,
            provenance=item.provenance.value,
            authority=item.authority.value,
            confidence=item.confidence,
            classification=item.classification,
            freshness_status=item.freshness_status.value,
            version=item.version,
            status=item.status.value,
            owner_id=item.owner_id,
            content_hash=item.content_hash,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get("/items/{knowledge_code}/versions")
def get_item_version_history(
    knowledge_code: str,
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    versions = service.get_item_version_history(knowledge_code)
    return {"knowledge_code": knowledge_code, "versions": versions}


# =============================================================================
# 3. Enterprise & Hybrid Search
# =============================================================================

@router.post("/search", response_model=List[SearchResultResponse])
def search_knowledge(
    req: KnowledgeSearchRequest,
    tenant_id: str = Query("default_tenant"),
    user_role: str = Query("INTERNAL_USER"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """Permission-aware multi-factor hybrid enterprise search."""
    dom = KnowledgeDomain(req.domain) if req.domain else None
    results = service.search_knowledge(
        query=req.query,
        domain=dom,
        strategy=req.strategy,
        top_k=req.top_k,
        tenant_id=tenant_id,
        user_role=user_role,
    )
    return [
        SearchResultResponse(
            knowledge_code=r.knowledge_code,
            title=r.title,
            snippet=r.snippet,
            domain=r.domain,
            item_type=r.item_type,
            authority=r.authority,
            provenance=r.provenance,
            freshness=r.freshness,
            score=r.score,
            relevance_factors=r.relevance_factors,
        )
        for r in results
    ]


# =============================================================================
# 4. Context Engine & AI Grounding
# =============================================================================

@router.post("/context", response_model=ContextAssemblyResponse)
def assemble_ai_context(
    req: ContextAssemblyRequest,
    tenant_id: str = Query("default_tenant"),
    user_role: str = Query("INTERNAL_USER"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """
    Assembles authorized context bundle for AI agents bounded by token budget
    and protected with security injection defense boundaries.
    """
    dom = KnowledgeDomain(req.domain) if req.domain else None
    bundle = service.assemble_ai_context(
        task_intent=req.task_intent,
        agent_id=req.agent_id,
        budget_tokens=req.budget_tokens,
        domain=dom,
        tenant_id=tenant_id,
        user_role=user_role,
    )
    return ContextAssemblyResponse(
        request_code=bundle.request_code,
        agent_id=bundle.agent_id,
        task_intent=bundle.task_intent,
        budget_tokens=bundle.budget_tokens,
        consumed_tokens=bundle.consumed_tokens,
        items_count=len(bundle.items),
        citations=bundle.citations,
        encapsulated_context=bundle.encapsulated_context,
        uncertainty_disclosures=bundle.uncertainty_disclosures,
        assembled_at=bundle.assembled_at,
    )


# =============================================================================
# 5. Document Processing & Intelligence
# =============================================================================

@router.post("/documents/process")
def process_document(
    req: DocumentProcessRequest,
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """Chunks documents and extracts candidate entities/facts safely marked INFERRED."""
    return service.process_document(
        document_id=req.document_id,
        title=req.title,
        content=req.content,
        doc_type=req.doc_type,
        tenant_id=tenant_id,
    )


# =============================================================================
# 6. Knowledge Graph Explorer
# =============================================================================

@router.get("/graph")
def get_knowledge_graph(
    root_code: Optional[str] = None,
    max_hops: int = Query(2, ge=1, le=5),
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """Returns organizational entity graph nodes and relationship edges for visualization."""
    return service.get_knowledge_graph(
        tenant_id=tenant_id,
        root_code=root_code,
        max_hops=max_hops,
    )


# =============================================================================
# 7. Contradiction & Conflict Resolution
# =============================================================================

@router.get("/conflicts", response_model=List[KnowledgeConflictResponse])
def list_conflicts(
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """Lists open contradiction records requiring human resolution."""
    conflicts = service.list_conflicts(tenant_id=tenant_id)
    return [
        KnowledgeConflictResponse(
            conflict_code=c.conflict_code,
            tenant_id=c.tenant_id,
            source_a_code=c.source_a_code,
            source_b_code=c.source_b_code,
            description=c.description,
            status=c.status.value,
            detected_at=c.detected_at,
            resolved_by=c.resolved_by,
            resolved_at=c.resolved_at,
            resolution_notes=c.resolution_notes,
        )
        for c in conflicts
    ]


@router.post("/conflicts/{conflict_code}/resolve", response_model=KnowledgeConflictResponse)
def resolve_conflict(
    conflict_code: str,
    req: ConflictResolveRequest,
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    """Resolves an open conflict with required human provenance and rationale."""
    conflict = service.resolve_conflict(
        conflict_code=conflict_code,
        resolved_by=req.resolved_by,
        resolution_notes=req.resolution_notes,
    )
    if not conflict:
        raise HTTPException(status_code=404, detail=f"Conflict '{conflict_code}' not found")
    return KnowledgeConflictResponse(
        conflict_code=conflict.conflict_code,
        tenant_id=conflict.tenant_id,
        source_a_code=conflict.source_a_code,
        source_b_code=conflict.source_b_code,
        description=conflict.description,
        status=conflict.status.value,
        detected_at=conflict.detected_at,
        resolved_by=conflict.resolved_by,
        resolved_at=conflict.resolved_at,
        resolution_notes=conflict.resolution_notes,
    )


# =============================================================================
# 8. Decision Memory & Lessons Learned
# =============================================================================

@router.get("/decisions", response_model=List[KnowledgeDecisionResponse])
def list_decisions(
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    decisions = service.store.list_decisions(tenant_id=tenant_id)
    return [
        KnowledgeDecisionResponse(
            decision_code=d.decision_code,
            tenant_id=d.tenant_id,
            title=d.title,
            question=d.question,
            context_background=d.context_background,
            options_considered=d.options_considered,
            decision_outcome=d.decision_outcome,
            rationale=d.rationale,
            owner_id=d.owner_id,
            approver_ids=d.approver_ids,
            evidence_references=d.evidence_references,
            status=d.status,
            decided_at=d.decided_at,
        )
        for d in decisions
    ]


@router.get("/lessons", response_model=List[KnowledgeLessonResponse])
def list_lessons(
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    lessons = service.store.list_lessons(tenant_id=tenant_id)
    return [
        KnowledgeLessonResponse(
            lesson_code=l.lesson_code,
            tenant_id=l.tenant_id,
            title=l.title,
            context_scope=l.context_scope,
            problem=l.problem,
            root_cause=l.root_cause,
            what_worked=l.what_worked,
            what_failed=l.what_failed,
            recommendation=l.recommendation,
            applicability_domain=l.applicability_domain,
            owner_id=l.owner_id,
            confidence=l.confidence,
        )
        for l in lessons
    ]


# =============================================================================
# 9. Quality & Feedback
# =============================================================================

@router.get("/quality")
def get_knowledge_quality(
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    return service.evaluate_quality(tenant_id=tenant_id)


@router.post("/feedback")
def record_search_feedback(
    req: SearchFeedbackRequest,
    user_id: str = Query("current_user"),
    tenant_id: str = Query("default_tenant"),
    service: KnowledgePlatformService = Depends(get_knowledge_service),
):
    return service.record_search_feedback(
        query=req.query,
        result_code=req.result_code,
        is_helpful=req.is_helpful,
        feedback_text=req.feedback_text,
        user_id=user_id,
        tenant_id=tenant_id,
    )
