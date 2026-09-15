"""FastAPI Router for Phase 36: Unified Data Platform, Data Governance, Data Lineage & Knowledge Architecture."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_security_context, require_permission
from app.data.base import DataAuthority, DataClassification, KnowledgeLifecycle
from app.models.user import User
from app.schemas.data import (
    AddLineageEdgeRequest,
    ConflictDetectionRequest,
    ConflictResponse,
    DataCatalogItemCreate,
    DataCatalogItemResponse,
    DataSourceCreate,
    DataSourceResponse,
    DocumentCreateRequest,
    DocumentIntegrityVerification,
    DocumentResponse,
    KnowledgeItemCreateRequest,
    KnowledgeItemResponse,
    KnowledgePromoteRequest,
    KnowledgeRetrievalRequest,
    KnowledgeRetrievalResponse,
    LegalHoldCreateRequest,
    LegalHoldResponse,
    LineageGraphResponse,
    ProvenanceRecordResponse,
    QualityRunResponse,
    RetentionPolicyCreateRequest,
    RetentionPolicyResponse,
    TriggerQualityCheckRequest,
)
from app.security.principals import SecurityContext
from app.services.data import DataPlatformService

router = APIRouter(prefix="/data", tags=["Data Platform & Governance"])


# ==============================================================================
# 1. Data Sources & Catalog
# ==============================================================================

@router.get("/sources", response_model=List[DataSourceResponse])
async def list_data_sources(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all registered authoritative and external data sources."""
    service = DataPlatformService(db)
    sources = await service.list_data_sources(tenant_id=str(current_user.id))
    return [DataSourceResponse.model_validate(s) for s in sources]


@router.post("/sources", response_model=DataSourceResponse, status_code=status.HTTP_201_CREATED)
async def create_data_source(
    payload: DataSourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Register a new data source with authority classification."""
    service = DataPlatformService(db)
    source = await service.create_data_source(tenant_id=str(current_user.id), payload=payload)
    return DataSourceResponse.model_validate(source)


@router.get("/catalog", response_model=List[DataCatalogItemResponse])
async def list_catalog_items(
    domain: Optional[str] = None,
    authority_level: Optional[DataAuthority] = None,
    classification: Optional[DataClassification] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Browse the unified enterprise data catalog."""
    service = DataPlatformService(db)
    items = await service.list_catalog_items(
        tenant_id=str(current_user.id),
        domain=domain,
        authority_level=authority_level,
        classification=classification,
    )
    return [DataCatalogItemResponse.model_validate(item) for item in items]


@router.post("/catalog", response_model=DataCatalogItemResponse, status_code=status.HTTP_201_CREATED)
async def create_catalog_item(
    payload: DataCatalogItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Register a data entity or schema definition into the catalog."""
    service = DataPlatformService(db)
    item = await service.create_catalog_item(tenant_id=str(current_user.id), payload=payload)
    return DataCatalogItemResponse.model_validate(item)


@router.get("/catalog/{item_id}", response_model=DataCatalogItemResponse)
async def get_catalog_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve catalog item details, SLA requirements, and contracts."""
    service = DataPlatformService(db)
    item = await service.get_catalog_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Catalog item not found")
    return DataCatalogItemResponse.model_validate(item)


# ==============================================================================
# 2. Data Quality & Conflicts
# ==============================================================================

@router.post("/quality/evaluate", response_model=QualityRunResponse)
async def evaluate_quality(
    payload: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Evaluate completeness, accuracy, consistency, freshness, validity, and uniqueness."""
    service = DataPlatformService(db)
    records = payload.get("records", [])
    schema_def = payload.get("schema_definition")
    catalog_item_id = payload.get("catalog_item_id")

    run = await service.evaluate_dataset_quality(
        tenant_id=str(current_user.id),
        catalog_item_id=catalog_item_id,
        records=records,
        schema_def=schema_def,
    )
    return QualityRunResponse.model_validate(run)


@router.get("/quality/runs", response_model=List[QualityRunResponse])
async def list_quality_runs(
    catalog_item_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List historical data quality evaluation runs."""
    service = DataPlatformService(db)
    runs = await service.repo.list_quality_runs(
        tenant_id=str(current_user.id),
        catalog_item_id=catalog_item_id,
        limit=limit,
    )
    return [QualityRunResponse.model_validate(r) for r in runs]


@router.get("/conflicts", response_model=List[ConflictResponse])
async def list_conflicts(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List detected data contradictions and version conflicts."""
    service = DataPlatformService(db)
    conflicts = await service.list_conflicts(
        tenant_id=str(current_user.id),
        status=status_filter,
    )
    return [ConflictResponse.model_validate(c) for c in conflicts]


@router.post("/conflicts/detect", response_model=List[ConflictResponse])
async def detect_conflicts(
    payload: ConflictDetectionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Perform deterministic contradiction detection across multi-source payloads."""
    service = DataPlatformService(db)
    conflicts = await service.detect_conflicts(
        tenant_id=str(current_user.id),
        domain=payload.domain,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        records=payload.records,
    )
    return [ConflictResponse.model_validate(c) for c in conflicts]


# ==============================================================================
# 3. Lineage & Provenance
# ==============================================================================

@router.get("/lineage/{entity_type}/{entity_id}", response_model=LineageGraphResponse)
async def get_lineage_graph(
    entity_type: str,
    entity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trace end-to-end upstream origins and downstream dependencies."""
    service = DataPlatformService(db)
    graph = await service.get_lineage_graph(
        tenant_id=str(current_user.id),
        entity_type=entity_type,
        entity_id=entity_id,
    )
    return graph


@router.post("/lineage/edges", status_code=status.HTTP_201_CREATED)
async def add_lineage_edge(
    payload: AddLineageEdgeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Explicitly record a lineage transformation or derivation link."""
    service = DataPlatformService(db)
    edge = await service.add_lineage_link(
        tenant_id=str(current_user.id),
        source_type=payload.source_type,
        source_id=payload.source_id,
        target_type=payload.target_type,
        target_id=payload.target_id,
        relationship=payload.relationship,
        transformation_name=payload.transformation_name,
        confidence_score=payload.confidence_score,
        metadata_json=payload.metadata_json,
    )
    return {"id": edge.id, "status": "RECORDED"}


@router.get("/provenance/{entity_type}/{entity_id}", response_model=List[ProvenanceRecordResponse])
async def list_provenance(
    entity_type: str,
    entity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve immutable audit and provenance log for a specific entity."""
    service = DataPlatformService(db)
    records = await service.repo.list_provenance(
        tenant_id=str(current_user.id),
        entity_type=entity_type,
        entity_id=entity_id,
    )
    return [ProvenanceRecordResponse.model_validate(r) for r in records]


# ==============================================================================
# 4. Documents & Integrity Verification
# ==============================================================================

@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(
    document_type: Optional[str] = None,
    doc_status: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List managed immutable business documents."""
    service = DataPlatformService(db)
    docs = await service.list_documents(
        tenant_id=str(current_user.id),
        document_type=document_type,
        status=doc_status,
    )
    return [DocumentResponse.model_validate(d) for d in docs]


@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    payload: DocumentCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Store an authoritative business document with SHA-256 integrity checksum."""
    service = DataPlatformService(db)
    doc = await service.create_document(
        tenant_id=str(current_user.id),
        payload=payload,
        created_by=str(current_user.id),
    )
    return DocumentResponse.model_validate(doc)


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get document details and current version metadata."""
    service = DataPlatformService(db)
    doc = await service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse.model_validate(doc)


@router.post("/documents/{document_id}/verify", response_model=DocumentIntegrityVerification)
async def verify_document(
    document_id: str,
    payload: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cryptographically verify that document content matches SHA-256 checksum."""
    content = payload.get("content", "")
    version_number = payload.get("version_number", 1)
    service = DataPlatformService(db)
    result = await service.verify_document_integrity(
        doc_id=document_id,
        version_number=version_number,
        content=content,
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return DocumentIntegrityVerification(**result)


# ==============================================================================
# 5. Knowledge Base & AI Context Retrieval
# ==============================================================================

@router.get("/knowledge", response_model=List[KnowledgeItemResponse])
async def list_knowledge_items(
    domain: Optional[str] = None,
    lifecycle_state: Optional[KnowledgeLifecycle] = None,
    authority_level: Optional[DataAuthority] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List curated knowledge items with lifecycle states."""
    service = DataPlatformService(db)
    items = await service.list_knowledge_items(
        tenant_id=str(current_user.id),
        domain=domain,
        lifecycle_state=lifecycle_state,
        authority_level=authority_level,
    )
    return [KnowledgeItemResponse.model_validate(i) for i in items]


@router.post("/knowledge", response_model=KnowledgeItemResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge_item(
    payload: KnowledgeItemCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Ingest a new knowledge item into the enterprise knowledge graph."""
    service = DataPlatformService(db)
    item = await service.create_knowledge_item(
        tenant_id=str(current_user.id),
        payload=payload,
        created_by=str(current_user.id),
    )
    return KnowledgeItemResponse.model_validate(item)


@router.post("/knowledge/{item_id}/promote", response_model=KnowledgeItemResponse)
async def promote_knowledge_item(
    item_id: str,
    payload: KnowledgePromoteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Promote knowledge lifecycle (e.g. INGESTED -> VERIFIED -> CANONICAL)."""
    service = DataPlatformService(db)
    try:
        updated = await service.promote_knowledge_item(
            item_id=item_id,
            target_lifecycle=payload.target_lifecycle,
            actor_id=str(current_user.id),
            actor_role=current_user.role,
            notes=payload.notes,
        )
        return KnowledgeItemResponse.model_validate(updated)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/knowledge/retrieve", response_model=KnowledgeRetrievalResponse)
async def retrieve_knowledge(
    payload: KnowledgeRetrievalRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Authorized semantic and keyword retrieval for LLM context assembly."""
    service = DataPlatformService(db)
    # Default clearance based on user role
    clearances = [DataClassification.PUBLIC, DataClassification.INTERNAL]
    if current_user.role in ["ADMIN", "OWNER", "LEAD"]:
        clearances.extend([DataClassification.CONFIDENTIAL, DataClassification.RESTRICTED])

    result = await service.retrieve_knowledge_for_context(
        tenant_id=str(current_user.id),
        user_classification_clearance=clearances,
        request=payload,
    )
    return result


# ==============================================================================
# 6. Retention Policies & Legal Holds
# ==============================================================================

@router.get("/retention/policies", response_model=List[RetentionPolicyResponse])
async def list_retention_policies(
    domain: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List data lifecycle and retention policies."""
    service = DataPlatformService(db)
    policies = await service.list_retention_policies(
        tenant_id=str(current_user.id),
        domain=domain,
    )
    return [RetentionPolicyResponse.model_validate(p) for p in policies]


@router.post("/retention/policies", response_model=RetentionPolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_retention_policy(
    payload: RetentionPolicyCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Define a domain-specific data retention and expiry policy."""
    service = DataPlatformService(db)
    policy = await service.create_retention_policy(
        tenant_id=str(current_user.id),
        payload=payload,
    )
    return RetentionPolicyResponse.model_validate(policy)


@router.get("/retention/legal-holds", response_model=List[LegalHoldResponse])
async def list_legal_holds(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List active and historical legal holds."""
    service = DataPlatformService(db)
    holds = await service.list_legal_holds(
        tenant_id=str(current_user.id),
        active_only=active_only,
    )
    return [LegalHoldResponse.model_validate(h) for h in holds]


@router.post("/retention/legal-holds", response_model=LegalHoldResponse, status_code=status.HTTP_201_CREATED)
async def place_legal_hold(
    payload: LegalHoldCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Place a binding legal hold locking data deletion across entities."""
    service = DataPlatformService(db)
    hold = await service.place_legal_hold(
        tenant_id=str(current_user.id),
        payload=payload,
        placed_by=str(current_user.id),
    )
    return LegalHoldResponse.model_validate(hold)


@router.post("/retention/legal-holds/{hold_id}/release", response_model=LegalHoldResponse)
async def release_legal_hold(
    hold_id: str,
    payload: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Release an active legal hold."""
    service = DataPlatformService(db)
    released = await service.release_legal_hold(
        hold_id=hold_id,
        released_by=str(current_user.id),
        notes=payload.get("notes"),
    )
    if not released:
        raise HTTPException(status_code=404, detail="Legal hold not found")
    return LegalHoldResponse.model_validate(released)


@router.get("/retention/check-delete/{entity_type}/{entity_id}")
async def check_delete_allowed(
    entity_type: str,
    entity_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Verify if entity deletion is blocked by legal holds or active retention locks."""
    service = DataPlatformService(db)
    return await service.can_safely_delete_entity(
        tenant_id=str(current_user.id),
        entity_type=entity_type,
        entity_id=entity_id,
    )
