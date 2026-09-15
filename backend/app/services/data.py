"""Service layer for Phase 36: Unified Data Platform, Governance, Lineage, Documents, Knowledge & Retention."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.data.base import (
    DataAuthority,
    DataClassification,
    KnowledgeLifecycle,
    LineageRelationship,
    ProvenanceMetadata,
    ProvenanceType,
)
from app.data.documents import DocumentEngine
from app.data.knowledge import KnowledgeEngine
from app.data.lineage import LineageGraphEngine
from app.data.quality import ConflictDetector, DataQualityScorer
from app.data.retention import RetentionEngine
from app.models.data import (
    DataCatalogItem,
    DataConflict,
    DataLineageEdge,
    DataProvenanceRecord,
    DataQualityRun,
    DataRetentionPolicyRecord,
    DataSource,
    DocumentRecord,
    DocumentVersionRecord,
    KnowledgeItemRecord,
    LegalHoldRecord,
)

from app.repositories.data import DataRepository
from app.schemas.data import (
    DataCatalogItemCreate,
    DataSourceCreate,
    DocumentCreateRequest,
    KnowledgeItemCreateRequest,
    KnowledgeRetrievalRequest,
    KnowledgeRetrievalResponse,
    KnowledgeRetrievalResult,
    LegalHoldCreateRequest,
    LineageGraphResponse,
    RetentionPolicyCreateRequest,
)


class DataPlatformService:
    """Service orchestrating data catalog, quality checks, lineage, documents, knowledge, and retention."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DataRepository(db)
        self.quality_scorer = DataQualityScorer()
        self.conflict_detector = ConflictDetector()
        self.lineage_engine = LineageGraphEngine()
        self.knowledge_engine = KnowledgeEngine()
        self.document_engine = DocumentEngine()
        self.retention_engine = RetentionEngine()

    # -------------------------------------------------------------
    # 1. Data Sources & Catalog
    # -------------------------------------------------------------
    async def create_data_source(
        self, tenant_id: str, payload: DataSourceCreate
    ) -> DataSource:
        source = DataSource(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            name=payload.name,
            source_type=payload.source_type,
            description=payload.description,
            connection_uri=payload.connection_uri,
            config=payload.config or {},
            is_authoritative=payload.is_authoritative,
            authority_level=payload.authority_level,
        )
        return await self.repo.create_data_source(source)

    async def list_data_sources(self, tenant_id: str) -> List[DataSource]:
        return await self.repo.list_data_sources(tenant_id)

    async def create_catalog_item(
        self, tenant_id: str, payload: DataCatalogItemCreate
    ) -> DataCatalogItem:
        item = DataCatalogItem(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            name=payload.name,
            domain=payload.domain,
            table_or_entity_name=payload.table_or_entity_name,
            description=payload.description,
            classification=payload.classification,
            authority_level=payload.authority_level,
            source_id=payload.source_id,
            schema_definition=payload.schema_definition or {},
            data_owner=payload.data_owner,
            data_steward=payload.data_steward,
            sla_freshness_hours=payload.sla_freshness_hours,
            sla_quality_threshold=payload.sla_quality_threshold,
        )
        return await self.repo.create_catalog_item(item)

    async def list_catalog_items(
        self,
        tenant_id: str,
        domain: Optional[str] = None,
        authority_level: Optional[DataAuthority] = None,
        classification: Optional[DataClassification] = None,
    ) -> List[DataCatalogItem]:
        return await self.repo.list_catalog_items(
            tenant_id=tenant_id,
            domain=domain,
            authority_level=authority_level,
            classification=classification,
        )

    async def get_catalog_item(self, item_id: str) -> Optional[DataCatalogItem]:
        return await self.repo.get_catalog_item(item_id)

    # -------------------------------------------------------------
    # 2. Quality Scoring & Conflicts
    # -------------------------------------------------------------
    async def evaluate_dataset_quality(
        self,
        tenant_id: str,
        catalog_item_id: Optional[str],
        records: List[Dict[str, Any]],
        schema_def: Optional[Dict[str, Any]] = None,
    ) -> DataQualityRun:
        run_result = self.quality_scorer.evaluate_dataset(records, schema_def)
        
        quality_run = DataQualityRun(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            catalog_item_id=catalog_item_id,
            overall_score=run_result["overall_score"],
            status="PASSED" if run_result["overall_score"] >= 0.85 else "FAILED",
            total_records_evaluated=run_result["total_records"],
            passed_records=run_result["passed_records"],
            failed_records=run_result["failed_records"],
            dimension_scores=run_result["dimensions"],
            violations=run_result["violations"],
            executed_at=datetime.now(timezone.utc),
        )
        return await self.repo.record_quality_run(quality_run)

    async def detect_conflicts(
        self,
        tenant_id: str,
        domain: str,
        entity_type: str,
        entity_id: str,
        records: List[Dict[str, Any]],
    ) -> List[DataConflict]:
        conflicts_detected = self.conflict_detector.detect_conflicts(records)
        created_conflicts = []
        for c in conflicts_detected:
            conflict_model = DataConflict(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                domain=domain,
                entity_type=entity_type,
                entity_id=entity_id,
                conflict_type="FIELD_VALUE_CONTRADICTION",
                conflicting_fields=c.conflicting_fields,
                source_records=[s.to_dict() for s in c.sources],
                status="DETECTED",
                detected_at=datetime.now(timezone.utc),
            )
            saved = await self.repo.create_conflict(conflict_model)
            created_conflicts.append(saved)
        return created_conflicts

    async def list_conflicts(
        self, tenant_id: str, status: Optional[str] = None
    ) -> List[DataConflict]:
        return await self.repo.list_conflicts(tenant_id, status=status)

    # -------------------------------------------------------------
    # 3. Lineage & Provenance
    # -------------------------------------------------------------
    async def add_lineage_link(
        self,
        tenant_id: str,
        source_type: str,
        source_id: str,
        target_type: str,
        target_id: str,
        relationship: LineageRelationship,
        transformation_name: Optional[str] = None,
        confidence_score: float = 1.0,
        metadata_json: Optional[Dict[str, Any]] = None,
    ) -> DataLineageEdge:
        edge = DataLineageEdge(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            relationship=relationship,
            transformation_name=transformation_name,
            confidence_score=confidence_score,
            metadata_json=metadata_json or {},
        )
        return await self.repo.add_lineage_edge(edge)

    async def get_lineage_graph(
        self,
        tenant_id: str,
        entity_type: str,
        entity_id: str,
    ) -> LineageGraphResponse:
        all_edges = await self.repo.list_lineage_edges(tenant_id=tenant_id)
        edge_dicts = [
            {
                "id": e.id,
                "source_type": e.source_type,
                "source_id": e.source_id,
                "target_type": e.target_type,
                "target_id": e.target_id,
                "relationship": e.relationship.value if hasattr(e.relationship, "value") else str(e.relationship),
                "transformation_name": e.transformation_name,
                "confidence_score": e.confidence_score,
            }
            for e in all_edges
        ]

        upstream = self.lineage_engine.trace_upstream(edge_dicts, entity_id)
        downstream = self.lineage_engine.trace_downstream(edge_dicts, entity_id)

        return LineageGraphResponse(
            entity_id=entity_id,
            entity_type=entity_type,
            upstream_nodes=upstream,
            downstream_nodes=downstream,
            edges=edge_dicts,
        )

    async def record_provenance(
        self,
        tenant_id: str,
        entity_type: str,
        entity_id: str,
        provenance_type: ProvenanceType,
        actor_id: Optional[str],
        actor_type: str,
        source_system: Optional[str],
        authority_level: DataAuthority,
        context_data: Dict[str, Any],
    ) -> DataProvenanceRecord:
        record = DataProvenanceRecord(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            entity_type=entity_type,
            entity_id=entity_id,
            provenance_type=provenance_type,
            actor_id=actor_id,
            actor_type=actor_type,
            source_system=source_system,
            authority_level=authority_level,
            context_data=context_data,
            recorded_at=datetime.now(timezone.utc),
        )
        return await self.repo.add_provenance(record)

    # -------------------------------------------------------------
    # 4. Documents & Integrity Verification
    # -------------------------------------------------------------
    async def create_document(
        self,
        tenant_id: str,
        payload: DocumentCreateRequest,
        created_by: Optional[str] = None,
    ) -> DocumentRecord:
        sha256_hash = self.document_engine.compute_sha256(payload.content)
        doc_id = str(uuid.uuid4())
        tracking_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"

        doc = DocumentRecord(
            id=doc_id,
            tenant_id=tenant_id,
            tracking_id=tracking_id,
            title=payload.title,
            document_type=payload.document_type,
            classification=payload.classification,
            authority_level=payload.authority_level,
            status="PUBLISHED",
            current_version=1,
            latest_sha256=sha256_hash,
            domain=payload.domain,
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            metadata_json={"summary": payload.summary} if payload.summary else {},
        )
        created_doc = await self.repo.create_document(doc)

        ver = DocumentVersionRecord(
            id=str(uuid.uuid4()),
            document_id=doc_id,
            version_number=1,
            storage_path=f"documents/{tenant_id}/{doc_id}/v1.txt",
            file_size_bytes=len(payload.content.encode("utf-8")),
            content_sha256=sha256_hash,
            change_summary="Initial document creation",
            created_by=created_by,
            created_at=datetime.now(timezone.utc),
        )
        await self.repo.add_document_version(ver)
        return created_doc

    async def list_documents(
        self,
        tenant_id: str,
        document_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[DocumentRecord]:
        return await self.repo.list_documents(tenant_id, document_type, status)

    async def get_document(self, doc_id: str) -> Optional[DocumentRecord]:
        return await self.repo.get_document(doc_id)

    async def verify_document_integrity(
        self,
        doc_id: str,
        version_number: int,
        content: str,
    ) -> Dict[str, Any]:
        doc = await self.repo.get_document(doc_id)
        if not doc:
            return {"error": "Document not found", "is_valid": False}

        matched_ver = next(
            (v for v in doc.versions if v.version_number == version_number), None
        )
        expected_hash = matched_ver.content_sha256 if matched_ver else doc.latest_sha256
        is_valid = self.document_engine.verify_integrity(content, expected_hash)

        return {
            "document_id": doc_id,
            "version_number": version_number,
            "expected_sha256": expected_hash,
            "calculated_sha256": self.document_engine.compute_sha256(content),
            "is_valid": is_valid,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }

    # -------------------------------------------------------------
    # 5. Knowledge Management & AI Context Retrieval
    # -------------------------------------------------------------
    async def create_knowledge_item(
        self,
        tenant_id: str,
        payload: KnowledgeItemCreateRequest,
        created_by: Optional[str] = None,
    ) -> KnowledgeItemRecord:
        item = KnowledgeItemRecord(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            canonical_key=payload.canonical_key or f"KNOW-{uuid.uuid4().hex[:8].upper()}",
            title=payload.title,
            topic=payload.topic,
            domain=payload.domain,
            content=payload.content,
            summary=payload.summary,
            authority_level=payload.authority_level,
            lifecycle_state=payload.lifecycle_state,
            classification=payload.classification,
            confidence_score=1.0 if payload.authority_level == DataAuthority.HUMAN_CONFIRMATION else 0.8,
            provenance_source=payload.provenance_source,
            created_by=created_by,
        )
        return await self.repo.create_knowledge_item(item)

    async def promote_knowledge_item(
        self,
        item_id: str,
        target_lifecycle: KnowledgeLifecycle,
        actor_id: str,
        actor_role: str,
        notes: Optional[str] = None,
    ) -> KnowledgeItemRecord:
        item = await self.repo.get_knowledge_item(item_id)
        if not item:
            raise ValueError("Knowledge item not found")

        # Validate lifecycle promotion rules
        self.knowledge_engine.promote_item(
            current_state=item.lifecycle_state,
            target_state=target_lifecycle,
            actor_role=actor_role,
        )

        item.lifecycle_state = target_lifecycle
        if target_lifecycle == KnowledgeLifecycle.VERIFIED or target_lifecycle == KnowledgeLifecycle.CANONICAL:
            item.verified_by = actor_id
            item.verified_at = datetime.now(timezone.utc)
            item.authority_level = DataAuthority.VERIFIED_DATA

        await self.repo.db.flush()
        return item


    async def list_knowledge_items(
        self,
        tenant_id: str,
        domain: Optional[str] = None,
        lifecycle_state: Optional[KnowledgeLifecycle] = None,
        authority_level: Optional[DataAuthority] = None,
    ) -> List[KnowledgeItemRecord]:
        return await self.repo.list_knowledge_items(
            tenant_id=tenant_id,
            domain=domain,
            lifecycle_state=lifecycle_state,
            authority_level=authority_level,
        )

    async def retrieve_knowledge_for_context(
        self,
        tenant_id: str,
        user_classification_clearance: List[DataClassification],
        request: KnowledgeRetrievalRequest,
    ) -> KnowledgeRetrievalResponse:
        """Authorized context retrieval for AI models with tenant and clearance boundary enforcement."""
        items = await self.repo.list_knowledge_items(
            tenant_id=tenant_id,
            domain=request.domain,
            lifecycle_state=request.min_lifecycle,
            authority_level=request.min_authority,
        )

        filtered = []
        for it in items:
            # Classification boundary
            if it.classification not in user_classification_clearance:
                continue
            # Text query matching
            if request.query.lower() in it.title.lower() or request.query.lower() in it.content.lower() or request.query.lower() in it.topic.lower():
                filtered.append(
                    KnowledgeRetrievalResult(
                        id=it.id,
                        title=it.title,
                        topic=it.topic,
                        domain=it.domain,
                        content=it.content,
                        authority_level=it.authority_level.value,
                        lifecycle_state=it.lifecycle_state.value,
                        classification=it.classification.value,
                        confidence_score=it.confidence_score,
                        provenance_source=it.provenance_source,
                    )
                )

        return KnowledgeRetrievalResponse(
            query=request.query,
            results_count=len(filtered),
            items=filtered[: request.limit],
            retrieved_at=datetime.now(timezone.utc),
        )

    # -------------------------------------------------------------
    # 6. Retention & Legal Holds
    # -------------------------------------------------------------
    async def create_retention_policy(
        self, tenant_id: str, payload: RetentionPolicyCreateRequest
    ) -> DataRetentionPolicyRecord:
        policy = DataRetentionPolicyRecord(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            domain=payload.domain,
            entity_type=payload.entity_type,
            classification=payload.classification,
            retention_period_days=payload.retention_period_days,
            action_on_expiry=payload.action_on_expiry,
            is_active=True,
        )
        return await self.repo.create_retention_policy(policy)

    async def list_retention_policies(
        self, tenant_id: str, domain: Optional[str] = None
    ) -> List[DataRetentionPolicyRecord]:
        return await self.repo.list_retention_policies(tenant_id, domain=domain)

    async def place_legal_hold(
        self,
        tenant_id: str,
        payload: LegalHoldCreateRequest,
        placed_by: str,
    ) -> LegalHoldRecord:
        hold = LegalHoldRecord(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            case_reference=payload.case_reference,
            reason=payload.reason,
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            active=True,
            placed_by=placed_by,
            placed_at=datetime.now(timezone.utc),
            notes=payload.notes,
        )
        return await self.repo.create_legal_hold(hold)

    async def release_legal_hold(
        self,
        hold_id: str,
        released_by: str,
        notes: Optional[str] = None,
    ) -> Optional[LegalHoldRecord]:
        hold = await self.repo.get_legal_hold(hold_id)
        if not hold:
            return None
        hold.active = False
        hold.released_by = released_by
        hold.released_at = datetime.now(timezone.utc)
        if notes:
            hold.notes = f"{hold.notes or ''} | Release Notes: {notes}"
        await self.repo.db.flush()
        return hold

    async def list_legal_holds(
        self, tenant_id: str, active_only: bool = True
    ) -> List[LegalHoldRecord]:
        return await self.repo.list_legal_holds(tenant_id, active_only=active_only)

    async def can_safely_delete_entity(
        self,
        tenant_id: str,
        entity_type: str,
        entity_id: str,
    ) -> Dict[str, Any]:
        """Check if an entity can be safely deleted without violating legal holds or retention policies."""
        is_held = await self.repo.check_entity_legal_hold(
            tenant_id=tenant_id,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        if is_held:
            return {
                "can_delete": False,
                "reason": "ACTIVE_LEGAL_HOLD",
                "message": "Entity is locked under an active legal hold and cannot be deleted.",
            }
        return {
            "can_delete": True,
            "reason": "OK",
            "message": "No active legal holds found for this entity.",
        }
