"""Repository layer for Phase 36: Unified Data Platform, Data Governance, Data Lineage & Knowledge Architecture."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import func, select, desc, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.data import (
    DataSource,
    DataCatalogItem,
    DataContract,
    DataQualityRun,
    DataConflict,
    DataDuplicate,
    DataProvenanceRecord,
    DataLineageEdge,
    DocumentRecord,
    DocumentVersionRecord,
    KnowledgeItemRecord,
    KnowledgeRelationshipRecord,
    DataRetentionPolicyRecord,
    LegalHoldRecord,
)
from app.data.base import (
    DataAuthority,
    DataClassification,
    KnowledgeLifecycle,
)



class DataRepository:
    """Database repository for Phase 36 Data Platform, Governance, Lineage, Documents, Knowledge & Retention."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # -------------------------------------------------------------
    # 1. Data Sources & Catalog Items
    # -------------------------------------------------------------
    async def list_data_sources(
        self,
        tenant_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[DataSource]:
        stmt = (
            select(DataSource)
            .where(DataSource.tenant_id == tenant_id)
            .order_by(desc(DataSource.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_data_source(self, source_id: str) -> Optional[DataSource]:
        stmt = select(DataSource).where(DataSource.id == source_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_data_source(self, source: DataSource) -> DataSource:
        self.db.add(source)
        await self.db.flush()
        return source

    async def list_catalog_items(
        self,
        tenant_id: str,
        domain: Optional[str] = None,
        authority_level: Optional[DataAuthority] = None,
        classification: Optional[DataClassification] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[DataCatalogItem]:
        stmt = (
            select(DataCatalogItem)
            .where(DataCatalogItem.tenant_id == tenant_id)
            .order_by(DataCatalogItem.name)
        )
        if domain:
            stmt = stmt.where(DataCatalogItem.domain == domain)
        if authority_level:
            stmt = stmt.where(DataCatalogItem.authority_level == authority_level)
        if classification:
            stmt = stmt.where(DataCatalogItem.classification == classification)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_catalog_item(self, item_id: str) -> Optional[DataCatalogItem]:
        stmt = (
            select(DataCatalogItem)
            .options(
                selectinload(DataCatalogItem.quality_runs),
                selectinload(DataCatalogItem.contracts),
            )
            .where(DataCatalogItem.id == item_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_catalog_item(self, item: DataCatalogItem) -> DataCatalogItem:
        self.db.add(item)
        await self.db.flush()
        return item

    # -------------------------------------------------------------
    # 2. Data Quality & Conflicts
    # -------------------------------------------------------------
    async def list_quality_runs(
        self,
        tenant_id: str,
        catalog_item_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[DataQualityRun]:
        stmt = (
            select(DataQualityRun)
            .where(DataQualityRun.tenant_id == tenant_id)
            .order_by(desc(DataQualityRun.executed_at))
        )
        if catalog_item_id:
            stmt = stmt.where(DataQualityRun.catalog_item_id == catalog_item_id)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def record_quality_run(self, run: DataQualityRun) -> DataQualityRun:
        self.db.add(run)
        await self.db.flush()
        return run

    async def list_conflicts(
        self,
        tenant_id: str,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[DataConflict]:
        stmt = (
            select(DataConflict)
            .where(DataConflict.tenant_id == tenant_id)
            .order_by(desc(DataConflict.detected_at))
        )
        if status:
            stmt = stmt.where(DataConflict.status == status)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_conflict(self, conflict_id: str) -> Optional[DataConflict]:
        stmt = select(DataConflict).where(DataConflict.id == conflict_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_conflict(self, conflict: DataConflict) -> DataConflict:
        self.db.add(conflict)
        await self.db.flush()
        return conflict

    # -------------------------------------------------------------
    # 3. Lineage & Provenance
    # -------------------------------------------------------------
    async def list_lineage_edges(
        self,
        tenant_id: str,
        source_type: Optional[str] = None,
        source_id: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
    ) -> List[DataLineageEdge]:
        stmt = select(DataLineageEdge).where(DataLineageEdge.tenant_id == tenant_id)
        if source_type and source_id:
            stmt = stmt.where(
                and_(
                    DataLineageEdge.source_type == source_type,
                    DataLineageEdge.source_id == source_id,
                )
            )
        if target_type and target_id:
            stmt = stmt.where(
                and_(
                    DataLineageEdge.target_type == target_type,
                    DataLineageEdge.target_id == target_id,
                )
            )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def add_lineage_edge(self, edge: DataLineageEdge) -> DataLineageEdge:
        self.db.add(edge)
        await self.db.flush()
        return edge

    async def list_provenance(
        self,
        tenant_id: str,
        entity_type: str,
        entity_id: str,
    ) -> List[DataProvenanceRecord]:
        stmt = (
            select(DataProvenanceRecord)
            .where(
                and_(
                    DataProvenanceRecord.tenant_id == tenant_id,
                    DataProvenanceRecord.entity_type == entity_type,
                    DataProvenanceRecord.entity_id == entity_id,
                )
            )
            .order_by(desc(DataProvenanceRecord.recorded_at))
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def add_provenance(self, prov: DataProvenanceRecord) -> DataProvenanceRecord:
        self.db.add(prov)
        await self.db.flush()
        return prov

    # -------------------------------------------------------------
    # 4. Documents & Versions
    # -------------------------------------------------------------
    async def list_documents(
        self,
        tenant_id: str,
        document_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[DocumentRecord]:
        stmt = (
            select(DocumentRecord)
            .where(DocumentRecord.tenant_id == tenant_id)
            .order_by(desc(DocumentRecord.created_at))
        )
        if document_type:
            stmt = stmt.where(DocumentRecord.document_type == document_type)
        if status:
            stmt = stmt.where(DocumentRecord.status == status)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_document(self, document_id: str) -> Optional[DocumentRecord]:
        stmt = (
            select(DocumentRecord)
            .options(
                selectinload(DocumentRecord.versions),
                selectinload(DocumentRecord.signatures),
                selectinload(DocumentRecord.retention_holds),
            )
            .where(DocumentRecord.id == document_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_document(self, doc: DocumentRecord) -> DocumentRecord:
        self.db.add(doc)
        await self.db.flush()
        return doc

    async def add_document_version(self, ver: DocumentVersionRecord) -> DocumentVersionRecord:
        self.db.add(ver)
        await self.db.flush()
        return ver

    # -------------------------------------------------------------
    # 5. Knowledge Architecture
    # -------------------------------------------------------------
    async def list_knowledge_items(
        self,
        tenant_id: str,
        domain: Optional[str] = None,
        lifecycle_state: Optional[KnowledgeLifecycle] = None,
        authority_level: Optional[DataAuthority] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[KnowledgeItemRecord]:
        stmt = (
            select(KnowledgeItemRecord)
            .where(KnowledgeItemRecord.tenant_id == tenant_id)
            .order_by(desc(KnowledgeItemRecord.updated_at))
        )
        if domain:
            stmt = stmt.where(KnowledgeItemRecord.domain == domain)
        if lifecycle_state:
            stmt = stmt.where(KnowledgeItemRecord.lifecycle_state == lifecycle_state)
        if authority_level:
            stmt = stmt.where(KnowledgeItemRecord.authority_level == authority_level)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_knowledge_item(self, item_id: str) -> Optional[KnowledgeItemRecord]:
        stmt = (
            select(KnowledgeItemRecord)
            .options(
                selectinload(KnowledgeItemRecord.relationships),
                selectinload(KnowledgeItemRecord.verifications),
            )
            .where(KnowledgeItemRecord.id == item_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_knowledge_item(self, item: KnowledgeItemRecord) -> KnowledgeItemRecord:
        self.db.add(item)
        await self.db.flush()
        return item

    async def add_knowledge_relationship(
        self, rel: KnowledgeRelationshipRecord
    ) -> KnowledgeRelationshipRecord:
        self.db.add(rel)
        await self.db.flush()
        return rel

    # -------------------------------------------------------------
    # 6. Retention Policies & Legal Holds
    # -------------------------------------------------------------
    async def list_retention_policies(
        self,
        tenant_id: str,
        domain: Optional[str] = None,
    ) -> List[DataRetentionPolicyRecord]:
        stmt = (
            select(DataRetentionPolicyRecord)
            .where(DataRetentionPolicyRecord.tenant_id == tenant_id)
            .order_by(DataRetentionPolicyRecord.domain)
        )
        if domain:
            stmt = stmt.where(DataRetentionPolicyRecord.domain == domain)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_retention_policy(
        self, policy: DataRetentionPolicyRecord
    ) -> DataRetentionPolicyRecord:
        self.db.add(policy)
        await self.db.flush()
        return policy

    async def list_legal_holds(
        self,
        tenant_id: str,
        active_only: bool = True,
    ) -> List[LegalHoldRecord]:
        stmt = (
            select(LegalHoldRecord)
            .where(LegalHoldRecord.tenant_id == tenant_id)
            .order_by(desc(LegalHoldRecord.placed_at))
        )
        if active_only:
            stmt = stmt.where(LegalHoldRecord.active == True)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_legal_hold(self, hold_id: str) -> Optional[LegalHoldRecord]:
        stmt = select(LegalHoldRecord).where(LegalHoldRecord.id == hold_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_legal_hold(self, hold: LegalHoldRecord) -> LegalHoldRecord:
        self.db.add(hold)
        await self.db.flush()
        return hold

    async def check_entity_legal_hold(
        self,
        tenant_id: str,
        entity_type: str,
        entity_id: str,
    ) -> bool:
        """Check if any active legal hold targets this specific entity or entire tenant."""
        stmt = select(LegalHoldRecord).where(
            and_(
                LegalHoldRecord.tenant_id == tenant_id,
                LegalHoldRecord.active == True,
            )
        )
        result = await self.db.execute(stmt)
        holds = result.scalars().all()
        for h in holds:
            if h.entity_type == entity_type and (h.entity_id == entity_id or h.entity_id == "*"):
                return True
            if h.entity_type == "*" or h.scope == "ALL":
                return True
        return False
