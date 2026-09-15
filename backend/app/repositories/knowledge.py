"""
Database Repository for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

try:
    from app.models.knowledge import (
        KnowledgeItemModel,
        KnowledgeItemVersionModel,
        KnowledgeFactModel,
        KnowledgeDecisionModel,
        KnowledgeLessonModel,
        KnowledgeEntityModel,
        KnowledgeRelationshipModel,
        KnowledgeConflictModel,
        KnowledgeContextRequestModel,
        KnowledgeFeedbackModel,
    )
except ImportError:
    from backend.app.models.knowledge import (
        KnowledgeItemModel,
        KnowledgeItemVersionModel,
        KnowledgeFactModel,
        KnowledgeDecisionModel,
        KnowledgeLessonModel,
        KnowledgeEntityModel,
        KnowledgeRelationshipModel,
        KnowledgeConflictModel,
        KnowledgeContextRequestModel,
        KnowledgeFeedbackModel,
    )


class KnowledgePlatformRepository:
    """Repository managing SQL persistence for Phase 48 Knowledge Platform."""

    def __init__(self, db: Session):
        self.db = db

    # --- Knowledge Items ---
    def save_item(self, item_data: Dict[str, Any]) -> KnowledgeItemModel:
        item = KnowledgeItemModel(
            tenant_id=item_data.get("tenant_id", "default_tenant"),
            organization_id=item_data.get("organization_id"),
            knowledge_code=item_data["knowledge_code"],
            item_type=item_data.get("item_type", "FACT"),
            title=item_data["title"],
            content=item_data["content"],
            summary=item_data.get("summary"),
            domain=item_data.get("domain", "BUSINESS"),
            source_type=item_data.get("source_type", "SYSTEM"),
            source_id=item_data.get("source_id"),
            provenance=item_data.get("provenance", "SYSTEM_GENERATED"),
            authority=item_data.get("authority", "OBSERVED"),
            confidence=item_data.get("confidence", 1.0),
            classification=item_data.get("classification", "INTERNAL"),
            freshness_status=item_data.get("freshness_status", "FRESH"),
            version=item_data.get("version", 1),
            status=item_data.get("status", "ACTIVE"),
            owner_id=item_data.get("owner_id", "system"),
            content_hash=item_data.get("content_hash", ""),
            metadata_payload=item_data.get("metadata_payload", {}),
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_item_by_code(self, knowledge_code: str, tenant_id: str = "default_tenant") -> Optional[KnowledgeItemModel]:
        stmt = select(KnowledgeItemModel).where(
            KnowledgeItemModel.knowledge_code == knowledge_code,
            KnowledgeItemModel.tenant_id == tenant_id,
        )
        return self.db.execute(stmt).scalars().first()

    def list_items(
        self,
        tenant_id: str = "default_tenant",
        domain: Optional[str] = None,
        limit: int = 100,
    ) -> List[KnowledgeItemModel]:
        stmt = select(KnowledgeItemModel).where(KnowledgeItemModel.tenant_id == tenant_id)
        if domain:
            stmt = stmt.where(KnowledgeItemModel.domain == domain)
        stmt = stmt.order_by(desc(KnowledgeItemModel.created_at)).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    # --- Item Versions ---
    def save_version(self, version_data: Dict[str, Any]) -> KnowledgeItemVersionModel:
        ver = KnowledgeItemVersionModel(
            knowledge_id=version_data["knowledge_id"],
            version_number=version_data["version_number"],
            content_hash=version_data["content_hash"],
            title=version_data.get("title", ""),
            content=version_data["content"],
            change_reason=version_data["change_reason"],
            created_by=version_data["created_by"],
        )
        self.db.add(ver)
        self.db.commit()
        self.db.refresh(ver)
        return ver

    # --- Facts ---
    def save_fact(self, fact_data: Dict[str, Any]) -> KnowledgeFactModel:
        fact = KnowledgeFactModel(
            tenant_id=fact_data.get("tenant_id", "default_tenant"),
            fact_code=fact_data["fact_code"],
            subject=fact_data["subject"],
            predicate=fact_data["predicate"],
            target_value=fact_data["target_value"],
            authority=fact_data.get("authority", "OBSERVED"),
            confidence=fact_data.get("confidence", 1.0),
            source_reference=fact_data.get("source_reference"),
        )
        self.db.add(fact)
        self.db.commit()
        self.db.refresh(fact)
        return fact

    def list_facts(self, tenant_id: str = "default_tenant") -> List[KnowledgeFactModel]:
        stmt = select(KnowledgeFactModel).where(KnowledgeFactModel.tenant_id == tenant_id)
        return list(self.db.execute(stmt).scalars().all())

    # --- Decisions ---
    def save_decision(self, decision_data: Dict[str, Any]) -> KnowledgeDecisionModel:
        decision = KnowledgeDecisionModel(
            tenant_id=decision_data.get("tenant_id", "default_tenant"),
            decision_code=decision_data["decision_code"],
            title=decision_data["title"],
            question=decision_data["question"],
            context_background=decision_data["context_background"],
            options_considered=decision_data.get("options_considered", []),
            decision_outcome=decision_data["decision_outcome"],
            rationale=decision_data["rationale"],
            owner_id=decision_data["owner_id"],
            approver_ids=decision_data.get("approver_ids", []),
            evidence_references=decision_data.get("evidence_references", []),
            status=decision_data.get("status", "APPROVED"),
        )
        self.db.add(decision)
        self.db.commit()
        self.db.refresh(decision)
        return decision

    def list_decisions(self, tenant_id: str = "default_tenant") -> List[KnowledgeDecisionModel]:
        stmt = select(KnowledgeDecisionModel).where(KnowledgeDecisionModel.tenant_id == tenant_id)
        return list(self.db.execute(stmt).scalars().all())

    # --- Lessons ---
    def save_lesson(self, lesson_data: Dict[str, Any]) -> KnowledgeLessonModel:
        lesson = KnowledgeLessonModel(
            tenant_id=lesson_data.get("tenant_id", "default_tenant"),
            lesson_code=lesson_data["lesson_code"],
            title=lesson_data["title"],
            context_scope=lesson_data["context_scope"],
            problem=lesson_data["problem"],
            root_cause=lesson_data["root_cause"],
            what_worked=lesson_data["what_worked"],
            what_failed=lesson_data["what_failed"],
            recommendation=lesson_data["recommendation"],
            applicability_domain=lesson_data.get("applicability_domain", "TECHNICAL"),
            owner_id=lesson_data["owner_id"],
            confidence=lesson_data.get("confidence", 0.9),
        )
        self.db.add(lesson)
        self.db.commit()
        self.db.refresh(lesson)
        return lesson

    def list_lessons(self, tenant_id: str = "default_tenant") -> List[KnowledgeLessonModel]:
        stmt = select(KnowledgeLessonModel).where(KnowledgeLessonModel.tenant_id == tenant_id)
        return list(self.db.execute(stmt).scalars().all())

    # --- Conflicts ---
    def save_conflict(self, conflict_data: Dict[str, Any]) -> KnowledgeConflictModel:
        conflict = KnowledgeConflictModel(
            tenant_id=conflict_data.get("tenant_id", "default_tenant"),
            conflict_code=conflict_data["conflict_code"],
            source_a_code=conflict_data["source_a_code"],
            source_b_code=conflict_data["source_b_code"],
            description=conflict_data["description"],
            status=conflict_data.get("status", "OPEN"),
        )
        self.db.add(conflict)
        self.db.commit()
        self.db.refresh(conflict)
        return conflict

    def list_conflicts(self, tenant_id: str = "default_tenant", status: Optional[str] = None) -> List[KnowledgeConflictModel]:
        stmt = select(KnowledgeConflictModel).where(KnowledgeConflictModel.tenant_id == tenant_id)
        if status:
            stmt = stmt.where(KnowledgeConflictModel.status == status)
        return list(self.db.execute(stmt).scalars().all())
