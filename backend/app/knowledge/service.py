"""
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Service Facade.
Phase 48 Architecture: Connects CRM, Projects, Contracts, Incidents, Policies, Telemetry, and AI Decisions.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.knowledge.base import (
        ConflictRecord,
        ContextBundle,
        DecisionRecord,
        FactItem,
        FreshnessStatus,
        GraphRelationshipType,
        KnowledgeAuthority,
        KnowledgeChunk,
        KnowledgeDomain,
        KnowledgeEntity,
        KnowledgeItem,
        KnowledgeLifecycle,
        KnowledgeProvenance,
        KnowledgeRelationship,
        KnowledgeType,
        LessonItem,
        SearchResultItem,
    )
    from backend.app.knowledge.conflicts.detector import ConflictDetector
    from backend.app.knowledge.context.engine import KnowledgeContextEngine
    from backend.app.knowledge.evaluation.benchmarks import RetrievalEvaluator
    from backend.app.knowledge.extraction.engine import DocumentIntelligenceEngine
    from backend.app.knowledge.freshness.monitor import FreshnessMonitor
    from backend.app.knowledge.graph.engine import KnowledgeGraphEngine
    from backend.app.knowledge.items.store import KnowledgeStore
    from backend.app.knowledge.quality.evaluator import KnowledgeQualityEvaluator
    from backend.app.knowledge.search.hybrid import HybridSearchEngine
    from backend.app.knowledge.semantic.engine import SemanticIntelligenceEngine
except ImportError:
    from app.knowledge.base import (
        ConflictRecord,
        ContextBundle,
        DecisionRecord,
        FactItem,
        FreshnessStatus,
        GraphRelationshipType,
        KnowledgeAuthority,
        KnowledgeChunk,
        KnowledgeDomain,
        KnowledgeEntity,
        KnowledgeItem,
        KnowledgeLifecycle,
        KnowledgeProvenance,
        KnowledgeRelationship,
        KnowledgeType,
        LessonItem,
        SearchResultItem,
    )
    from app.knowledge.conflicts.detector import ConflictDetector
    from app.knowledge.context.engine import KnowledgeContextEngine
    from app.knowledge.evaluation.benchmarks import RetrievalEvaluator
    from app.knowledge.extraction.engine import DocumentIntelligenceEngine
    from app.knowledge.freshness.monitor import FreshnessMonitor
    from app.knowledge.graph.engine import KnowledgeGraphEngine
    from app.knowledge.items.store import KnowledgeStore
    from app.knowledge.quality.evaluator import KnowledgeQualityEvaluator
    from app.knowledge.search.hybrid import HybridSearchEngine
    from app.knowledge.semantic.engine import SemanticIntelligenceEngine


class KnowledgePlatformService:
    """
    Central orchestration service for Phase 48:
    Governs knowledge ingestion, storage, graph relationships, semantic indexing,
    hybrid search, AI context assembly, freshness, and quality assurance.
    """

    def __init__(self):
        self.store = KnowledgeStore()
        self.semantic_engine = SemanticIntelligenceEngine()
        self.search_engine = HybridSearchEngine(self.store, self.semantic_engine)
        self.context_engine = KnowledgeContextEngine(self.search_engine)
        self.extraction_engine = DocumentIntelligenceEngine()
        self.graph_engine = KnowledgeGraphEngine()
        self.conflict_detector = ConflictDetector()
        self.freshness_monitor = FreshnessMonitor()
        self.quality_evaluator = KnowledgeQualityEvaluator()
        self.retrieval_evaluator = RetrievalEvaluator()

        self._feedbacks: List[Dict[str, Any]] = []
        self._seed_memory()

    def _seed_memory(self) -> None:
        """Seeds canonical facts, decisions, and organizational lessons."""
        # 1. Canonical Facts
        self.store.create_fact(FactItem(
            fact_code="FACT-SEC-001",
            subject="Privileged Dispatcher",
            predicate="requires_mfa",
            target_value="true",
            authority=KnowledgeAuthority.AUTHORITATIVE,
            source_reference="POL-SEC-001",
        ))
        self.store.create_fact(FactItem(
            fact_code="FACT-DB-001",
            subject="Multi-Tenant Database",
            predicate="isolation_strategy",
            target_value="row_level_with_tenant_id",
            authority=KnowledgeAuthority.AUTHORITATIVE,
            source_reference="ARCH-DB-001",
        ))

        # 2. Decision Memory (Section 26)
        self.store.create_decision(DecisionRecord(
            decision_code="DEC-2026-001",
            title="Adopt Hybrid Semantic & Lexical Search Architecture",
            question="How should enterprise enterprise search rank multi-modal technical and business records?",
            context_background="Keyword search alone misses semantic intent; vector search alone suffers lexical precision on code identifiers.",
            options_considered=[
                {"option": "Keyword Only", "pros": "Deterministic, exact matching", "cons": "Zero conceptual generalization"},
                {"option": "Vector Only", "pros": "Handles natural language variations", "cons": "Hallucinates on exact identifiers and acronyms"},
                {"option": "Hybrid with Authority & Freshness Reranking", "pros": "High precision, semantic understanding, authority-weighted", "cons": "Requires multi-stage pipeline"},
            ],
            decision_outcome="Selected Hybrid with Authority & Freshness Reranking",
            rationale="Balances exact technical matching with semantic generalization, while preventing unverified AI assertions from outranking authoritative signed contracts.",
            owner_id="platform_architect",
            approvers=["cto", "ciso"],
            evidence_references=["BENCHMARK-SEARCH-2026-01"],
            status="APPROVED",
        ))

        # 3. Lesson Library (Section 30)
        self.store.create_lesson(LessonItem(
            lesson_code="LES-2026-001",
            title="Integration Scope Discovery Before Estimation",
            context_scope="Enterprise CRM & WhatsApp Automation Integrations",
            problem="Project carrier portal experienced +25% delivery variance due to unannounced third-party webhook rate-limits.",
            root_cause="Third-party vendor documentation was taken as authoritative without empirical sandbox load testing.",
            what_worked="Formal integration spike testing before fixed-price quote approval.",
            what_failed="Assuming third-party sandbox quotas match production tier throughput.",
            recommendation="Mandate 2-day technical sandbox verification spike on all external API dependencies prior to final estimate lock.",
            applicability_domain="TECHNICAL",
            owner_id="lead_solution_architect",
            confidence=0.95,
        ))

    # =========================================================================
    # Knowledge Overview & Analytics (Section 46, 76)
    # =========================================================================

    def get_overview(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        """Provides executive telemetry and overview metrics across all knowledge domains."""
        items = self.store.list_items(tenant_id=tenant_id)
        open_conflicts = self.conflict_detector.list_open_conflicts(tenant_id=tenant_id)
        quality_scorecard = self.quality_evaluator.evaluate_quality_scorecard(items, len(open_conflicts))

        domain_counts: Dict[str, int] = {}
        authority_counts: Dict[str, int] = {}
        for it in items:
            domain_counts[it.domain.value] = domain_counts.get(it.domain.value, 0) + 1
            authority_counts[it.authority.value] = authority_counts.get(it.authority.value, 0) + 1

        recent_contexts = self.context_engine.get_recent_requests()

        return {
            "tenant_id": tenant_id,
            "total_items": len(items),
            "total_facts": len(self.store.list_facts(tenant_id=tenant_id)),
            "total_decisions": len(self.store.list_decisions(tenant_id=tenant_id)),
            "total_lessons": len(self.store.list_lessons(tenant_id=tenant_id)),
            "open_conflicts_count": len(open_conflicts),
            "quality_scorecard": quality_scorecard,
            "domain_breakdown": domain_counts,
            "authority_breakdown": authority_counts,
            "recent_context_assemblies_count": len(recent_contexts),
            "status": "OPERATIONAL",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # =========================================================================
    # Canonical Knowledge Item Management (Section 6, 7, 8, 10)
    # =========================================================================

    def create_knowledge_item(
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
        is_ai_generated: bool = False,
    ) -> KnowledgeItem:
        """
        Creates knowledge item enforcing Rule 1-3 (AI cannot autonomously declare Authoritative status).
        """
        item = self.store.create_item(
            knowledge_code=knowledge_code,
            title=title,
            content=content,
            domain=domain,
            item_type=item_type,
            authority=authority,
            provenance=provenance,
            confidence=confidence,
            owner_id=owner_id,
            classification=classification,
            tenant_id=tenant_id,
            is_ai_generated=is_ai_generated,
        )
        return item

    def update_knowledge_item(
        self,
        knowledge_code: str,
        new_content: str,
        change_reason: str,
        updated_by: str,
        new_title: Optional[str] = None,
    ) -> KnowledgeItem:
        """Updates knowledge item with immutable SHA-256 version lineage."""
        return self.store.update_item(
            knowledge_code=knowledge_code,
            new_content=new_content,
            change_reason=change_reason,
            updated_by=updated_by,
            new_title=new_title,
        )

    def list_knowledge_items(
        self,
        domain: Optional[KnowledgeDomain] = None,
        item_type: Optional[KnowledgeType] = None,
        tenant_id: str = "default_tenant",
    ) -> List[KnowledgeItem]:
        return self.store.list_items(domain=domain, item_type=item_type, tenant_id=tenant_id)

    def get_knowledge_item(self, knowledge_code: str, tenant_id: str = "default_tenant") -> Optional[KnowledgeItem]:
        return self.store.get_item(knowledge_code=knowledge_code, tenant_id=tenant_id)

    def get_item_version_history(self, knowledge_code: str) -> List[Dict[str, Any]]:
        return self.store.get_version_history(knowledge_code)

    # =========================================================================
    # Search & Retrieval (Section 14-18, 43)
    # =========================================================================

    def search_knowledge(
        self,
        query: str,
        domain: Optional[KnowledgeDomain] = None,
        strategy: str = "HYBRID",
        top_k: int = 10,
        tenant_id: str = "default_tenant",
        user_role: str = "INTERNAL_USER",
    ) -> List[SearchResultItem]:
        """Permission-aware enterprise search strictly scoped to tenant and user role."""
        return self.search_engine.search(
            query=query,
            domain=domain,
            strategy=strategy,
            top_k=top_k,
            tenant_id=tenant_id,
            user_role=user_role,
        )

    # =========================================================================
    # AI Context Assembly & Grounding Engine (Section 31-35, 70)
    # =========================================================================

    def assemble_ai_context(
        self,
        task_intent: str,
        agent_id: str,
        budget_tokens: int = 4000,
        domain: Optional[KnowledgeDomain] = None,
        tenant_id: str = "default_tenant",
        user_role: str = "INTERNAL_USER",
    ) -> ContextBundle:
        """
        Assembles a bounded, verified AI context bundle wrapped in security injection defenses.
        """
        return self.context_engine.assemble_context(
            task_intent=task_intent,
            agent_id=agent_id,
            budget_tokens=budget_tokens,
            domain=domain,
            tenant_id=tenant_id,
            user_role=user_role,
        )

    # =========================================================================
    # Document Intelligence & Extraction (Section 20-22)
    # =========================================================================

    def process_document(
        self,
        document_id: str,
        title: str,
        content: str,
        doc_type: str = "TECHNICAL_DOCUMENT",
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """
        Processes document into chunks, extracts candidate entities and facts,
        ensuring candidate facts are safely marked INFERRED (Rule 1 & 2).
        """
        chunks = self.extraction_engine.chunk_document(
            document_id=document_id,
            content=content,
            tenant_id=tenant_id,
        )
        entities = self.extraction_engine.extract_entities(
            document_id=document_id,
            content=content,
            tenant_id=tenant_id,
        )
        facts = self.extraction_engine.extract_candidate_facts(
            document_id=document_id,
            content=content,
            tenant_id=tenant_id,
        )

        return {
            "document_id": document_id,
            "title": title,
            "doc_type": doc_type,
            "chunks_count": len(chunks),
            "chunks": [c.model_dump() for c in chunks],
            "extracted_entities": [e.model_dump() for e in entities],
            "candidate_facts": [f.model_dump() for f in facts],
        }

    # =========================================================================
    # Knowledge Graph Explorer (Section 23, 24, 48)
    # =========================================================================

    def get_knowledge_graph(
        self,
        tenant_id: str = "default_tenant",
        root_code: Optional[str] = None,
        max_hops: int = 2,
    ) -> Dict[str, Any]:
        return self.graph_engine.get_graph_visualization_data(
            root_code=root_code,
            max_hops=max_hops,
            tenant_id=tenant_id,
        )

    def query_graph_path(
        self,
        source_code: str,
        target_code: str,
        max_hops: int = 4,
    ) -> Optional[List[str]]:
        return self.graph_engine.find_path(
            source_code=source_code,
            target_code=target_code,
            max_hops=max_hops,
        )

    # =========================================================================
    # Conflicts & Resolution (Section 12, 42)
    # =========================================================================

    def detect_conflicts(self, tenant_id: str = "default_tenant") -> List[ConflictRecord]:
        facts = self.store.list_facts(tenant_id=tenant_id)
        return self.conflict_detector.scan_fact_conflicts(facts)

    def list_conflicts(self, tenant_id: str = "default_tenant") -> List[ConflictRecord]:
        return self.conflict_detector.list_open_conflicts(tenant_id=tenant_id)

    def resolve_conflict(
        self,
        conflict_code: str,
        resolved_by: str,
        resolution_notes: str,
    ) -> Optional[ConflictRecord]:
        return self.conflict_detector.resolve_conflict(
            conflict_code=conflict_code,
            resolved_by=resolved_by,
            resolution_notes=resolution_notes,
        )

    # =========================================================================
    # Quality & Freshness (Section 11, 39, 72)
    # =========================================================================

    def evaluate_quality(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        items = self.store.list_items(tenant_id=tenant_id)
        open_conflicts = self.conflict_detector.list_open_conflicts(tenant_id=tenant_id)
        return self.quality_evaluator.evaluate_quality_scorecard(items, len(open_conflicts))

    def evaluate_item_freshness(self, item: KnowledgeItem) -> FreshnessStatus:
        return self.freshness_monitor.update_item_freshness(item).freshness_status

    # =========================================================================
    # Evaluations & Benchmarks (Section 40, 41, 78, 79)
    # =========================================================================

    def evaluate_retrieval_benchmarks(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.retrieval_evaluator.evaluate_retrieval_metrics(test_cases)

    def evaluate_ai_grounding(
        self,
        question: str,
        retrieved_evidence: List[str],
        ai_response_claims: List[str],
    ) -> Dict[str, Any]:
        return self.retrieval_evaluator.evaluate_grounding_case(
            question=question,
            retrieved_evidence=retrieved_evidence,
            ai_response_claims=ai_response_claims,
        )

    # =========================================================================
    # Search Feedback (Section 74, 75)
    # =========================================================================

    def record_search_feedback(
        self,
        query: str,
        result_code: str,
        is_helpful: bool,
        feedback_text: Optional[str] = None,
        user_id: str = "system_user",
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        record = {
            "feedback_id": f"FBK-{uuid.uuid4().hex[:8].upper()}",
            "query": query,
            "result_code": result_code,
            "is_helpful": is_helpful,
            "feedback_text": feedback_text,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._feedbacks.append(record)
        return record
