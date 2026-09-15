"""
Knowledge Store & Versioning Engine (Section 6, 7, 8, 10).
Manages canonical knowledge items, version lineage, authority levels, and tenant isolation.
"""

from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.knowledge.base import (
        DecisionRecord,
        FactItem,
        FreshnessStatus,
        KnowledgeAuthority,
        KnowledgeDomain,
        KnowledgeItem,
        KnowledgeLifecycle,
        KnowledgeProvenance,
        KnowledgeType,
        LessonItem,
    )
except ImportError:
    from app.knowledge.base import (
        DecisionRecord,
        FactItem,
        FreshnessStatus,
        KnowledgeAuthority,
        KnowledgeDomain,
        KnowledgeItem,
        KnowledgeLifecycle,
        KnowledgeProvenance,
        KnowledgeType,
        LessonItem,
    )


class KnowledgeStore:
    """Governed knowledge store enforcing provenance, authority boundaries, and immutable versioning."""

    def __init__(self):
        self._items: Dict[str, KnowledgeItem] = {}
        self._versions: Dict[str, List[Dict[str, Any]]] = {}  # knowledge_code -> version history
        self._seed_default_knowledge()

    def _seed_default_knowledge(self) -> None:
        """Seeds baseline architectural patterns, technical knowledge, and client success memory."""
        # 1. Architecture Pattern
        self.create_item(
            knowledge_code="KNW-ARCH-POSTGRES-TENANT",
            title="Multi-Tenant PostgreSQL Row-Level Isolation Architecture",
            content="All relational PostgreSQL entities must enforce mandatory tenant_id constraints with foreign keys and index scoping to prevent IDOR and cross-tenant leakage.",
            domain=KnowledgeDomain.TECHNICAL,
            item_type=KnowledgeType.TECHNICAL_PATTERN,
            authority=KnowledgeAuthority.AUTHORITATIVE,
            provenance=KnowledgeProvenance.HUMAN_CONFIRMED,
            owner_id="platform_architect",
            classification="INTERNAL",
        )

        # 2. Security Runbook
        self.create_item(
            knowledge_code="KNW-SEC-MFA-STEPUP",
            title="Step-Up Authentication Policy for High-Risk State Changes",
            content="Administrative role promotions, API key generation, and financial ledger adjustments require active step-up MFA verification within a 15-minute validity window.",
            domain=KnowledgeDomain.SECURITY,
            item_type=KnowledgeType.POLICY,
            authority=KnowledgeAuthority.AUTHORITATIVE,
            provenance=KnowledgeProvenance.HUMAN_CONFIRMED,
            owner_id="ciso",
            classification="CONFIDENTIAL",
        )

        # 3. AI Governance Rule
        self.create_item(
            knowledge_code="KNW-AI-HUMAN-OVERSIGHT",
            title="NIST AI RMF Human-in-the-Loop Oversight for High-Impact Actions",
            content="Autonomous agents are strictly prohibited from signing commercial contracts, declaring compliance, or executing unilateral data erasures without human approval.",
            domain=KnowledgeDomain.AI,
            item_type=KnowledgeType.BUSINESS_RULE,
            authority=KnowledgeAuthority.AUTHORITATIVE,
            provenance=KnowledgeProvenance.HUMAN_CONFIRMED,
            owner_id="ai_governance_lead",
            classification="INTERNAL",
        )

        # 4. Reliability Lesson
        self.create_item(
            knowledge_code="KNW-REL-REDIS-CONN-POOL",
            title="Redis Connection Pooling & Timeout Protection",
            content="Always configure bounded max_connections (default 50) and aggressive socket_timeout (2.0s) on Celery Redis broker to prevent worker starvation during network partitions.",
            domain=KnowledgeDomain.RELIABILITY,
            item_type=KnowledgeType.LESSON,
            authority=KnowledgeAuthority.CONFIRMED,
            provenance=KnowledgeProvenance.OBSERVED,
            owner_id="sre_lead",
            classification="INTERNAL",
        )

        # 5. Client Success Playbook
        self.create_item(
            knowledge_code="KNW-CS-COMM-CADENCE",
            title="Executive Client Communication Cadence & Survey Triggers",
            content="Enterprise clients require bi-weekly progress synchronization and automated CSAT surveys immediately following Phase UAT acceptance milestones.",
            domain=KnowledgeDomain.CLIENT,
            item_type=KnowledgeType.GUIDELINE,
            authority=KnowledgeAuthority.CONFIRMED,
            provenance=KnowledgeProvenance.HUMAN_CONFIRMED,
            owner_id="customer_success_lead",
            classification="INTERNAL",
        )

    @staticmethod
    def calculate_hash(content: str) -> str:
        return hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    def create_item(
        self,
        knowledge_code: str,
        title: str,
        content: str,
        domain: KnowledgeDomain = KnowledgeDomain.BUSINESS,
        item_type: KnowledgeType = KnowledgeType.FACT,
        authority: KnowledgeAuthority = KnowledgeAuthority.OBSERVED,
        provenance: KnowledgeProvenance = KnowledgeProvenance.SYSTEM_GENERATED,
        confidence: float = 1.0,
        owner_id: str = "system",
        classification: str = "INTERNAL",
        tenant_id: str = "default_tenant",
        validity_days: int = 365,
        is_ai_generated: bool = False,
    ) -> KnowledgeItem:
        """Creates a new canonical knowledge item, strictly guarding against unauthorized authority elevation."""
        if not title or not content:
            raise ValueError("Knowledge title and content are strictly required.")

        # Non-negotiable Rule 1-3: AI generation cannot autonomously declare Authoritative or Confirmed status
        if is_ai_generated and authority in [KnowledgeAuthority.AUTHORITATIVE, KnowledgeAuthority.CONFIRMED]:
            raise PermissionError("Safety violation: AI-generated knowledge cannot be created as AUTHORITATIVE or CONFIRMED without human review.")

        c_hash = self.calculate_hash(content)
        now = datetime.now(timezone.utc)

        item = KnowledgeItem(
            knowledge_code=knowledge_code,
            tenant_id=tenant_id,
            item_type=item_type,
            title=title,
            content=content,
            domain=domain,
            provenance=KnowledgeProvenance.AI_INFERRED if is_ai_generated else provenance,
            authority=KnowledgeAuthority.INFERRED if is_ai_generated else authority,
            confidence=min(confidence, 0.85) if is_ai_generated else confidence,
            classification=classification,
            valid_from=now,
            freshness_status=FreshnessStatus.FRESH,
            version=1,
            status=KnowledgeLifecycle.DRAFT if is_ai_generated else KnowledgeLifecycle.ACTIVE,
            owner_id=owner_id,
            content_hash=c_hash,
            created_at=now,
            updated_at=now,
        )

        self._items[knowledge_code] = item
        self._versions[knowledge_code] = [
            {
                "version_number": 1,
                "content_hash": c_hash,
                "content": content,
                "change_reason": "Initial creation",
                "created_by": owner_id,
                "created_at": now.isoformat(),
            }
        ]
        return item

    def update_item(
        self,
        knowledge_code: str,
        new_content: str,
        change_reason: str,
        updated_by: str,
        new_title: Optional[str] = None,
    ) -> KnowledgeItem:
        """Updates knowledge item with immutable version history tracking (Rule 10: No silent overwrites)."""
        item = self._items.get(knowledge_code)
        if not item:
            raise KeyError(f"Knowledge item '{knowledge_code}' not found.")
        if not change_reason:
            raise ValueError("Version change_reason is required for knowledge auditability.")

        new_hash = self.calculate_hash(new_content)
        now = datetime.now(timezone.utc)

        item.version += 1
        item.content = new_content
        if new_title:
            item.title = new_title
        item.content_hash = new_hash
        item.updated_at = now
        item.freshness_status = FreshnessStatus.FRESH

        self._versions[knowledge_code].append(
            {
                "version_number": item.version,
                "content_hash": new_hash,
                "content": new_content,
                "change_reason": change_reason,
                "created_by": updated_by,
                "created_at": now.isoformat(),
            }
        )
        return item

    def get_item(self, knowledge_code: str, tenant_id: str = "default_tenant") -> Optional[KnowledgeItem]:
        item = self._items.get(knowledge_code)
        if item and item.tenant_id == tenant_id:
            return item
        return None

    def list_items(
        self,
        domain: Optional[KnowledgeDomain] = None,
        item_type: Optional[KnowledgeType] = None,
        tenant_id: str = "default_tenant",
    ) -> List[KnowledgeItem]:
        results = [i for i in self._items.values() if i.tenant_id == tenant_id]
        if domain:
            results = [i for i in results if i.domain == domain]
        if item_type:
            results = [i for i in results if i.item_type == item_type]
        return results

    def get_version_history(self, knowledge_code: str) -> List[Dict[str, Any]]:
        return self._versions.get(knowledge_code, [])

    # --- Facts, Decisions, and Lessons Memory (Section 26, 27, 30) ---

    def create_fact(self, fact: FactItem) -> FactItem:
        if not hasattr(self, "_facts"):
            self._facts: Dict[str, FactItem] = {}
        self._facts[fact.fact_code] = fact
        return fact

    def list_facts(self, tenant_id: str = "default_tenant") -> List[FactItem]:
        if not hasattr(self, "_facts"):
            self._facts = {}
        return [f for f in self._facts.values() if f.tenant_id == tenant_id]

    def create_decision(self, decision: DecisionRecord) -> DecisionRecord:
        if not hasattr(self, "_decisions"):
            self._decisions: Dict[str, DecisionRecord] = {}
        self._decisions[decision.decision_code] = decision
        return decision

    def list_decisions(self, tenant_id: str = "default_tenant") -> List[DecisionRecord]:
        if not hasattr(self, "_decisions"):
            self._decisions = {}
        return [d for d in self._decisions.values() if d.tenant_id == tenant_id]

    def create_lesson(self, lesson: LessonItem) -> LessonItem:
        if not hasattr(self, "_lessons"):
            self._lessons: Dict[str, LessonItem] = {}
        self._lessons[lesson.lesson_code] = lesson
        return lesson

    def list_lessons(self, tenant_id: str = "default_tenant") -> List[LessonItem]:
        if not hasattr(self, "_lessons"):
            self._lessons = {}
        return [l for l in self._lessons.values() if l.tenant_id == tenant_id]
