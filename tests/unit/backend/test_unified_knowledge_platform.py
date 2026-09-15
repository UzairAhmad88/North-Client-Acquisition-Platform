"""
Comprehensive Unit Test Suite for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.

Validates all 20 Non-Negotiable Rules, lifecycle transitions, hybrid search, AI context assembly,
injection boundary encapsulation, conflict detection, quality scoring, retrieval benchmarks, and agents.
"""

import pytest
from datetime import datetime, timezone, timedelta
from typing import List

from backend.app.knowledge.base import (
    ConflictRecord,
    ConflictStatus,
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
from backend.app.knowledge.service import KnowledgePlatformService

from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS,
    validate_agent_permissions,
    AgentPermissionDeniedError,
)
from agents.knowledge.extraction import KnowledgeExtractionAgent
from agents.knowledge.retrieval import KnowledgeRetrievalAgent
from agents.knowledge.context_assembly import ContextAssemblyAgent
from agents.knowledge.learning import OrganizationalLearningAgent


# =============================================================================
# 1. Knowledge Store & Versioning Tests (Section 6, 7, 8, 10)
# =============================================================================

def test_knowledge_store_create_and_versioning():
    store = KnowledgeStore()
    item = store.create_item(
        knowledge_code="KNW-TEST-001",
        title="PostgreSQL Concurrency Policy",
        content="Read committed is default transactional isolation level.",
        domain=KnowledgeDomain.TECHNICAL,
        authority=KnowledgeAuthority.AUTHORITATIVE,
        owner_id="architect",
    )

    assert item.knowledge_code == "KNW-TEST-001"
    assert item.version == 1
    assert item.content_hash != ""

    # Update item with required change reason
    updated = store.update_item(
        knowledge_code="KNW-TEST-001",
        new_content="Serializable isolation is required for financial ledger debit balances.",
        change_reason="Audit requirement for financial ledger consistency",
        updated_by="security_officer",
    )

    assert updated.version == 2
    assert "Serializable isolation" in updated.content

    history = store.get_version_history("KNW-TEST-001")
    assert len(history) == 2
    assert history[0]["version_number"] == 1
    assert history[1]["version_number"] == 2
    assert history[1]["change_reason"] == "Audit requirement for financial ledger consistency"


def test_ai_cannot_declare_authoritative_status():
    """Non-Negotiable Rule 1-3: AI generation cannot autonomously declare Authoritative or Confirmed status."""
    store = KnowledgeStore()

    with pytest.raises(PermissionError, match="Safety violation: AI-generated knowledge cannot be created as AUTHORITATIVE"):
        store.create_item(
            knowledge_code="KNW-AI-FAIL",
            title="Unchecked AI Claim",
            content="All clients receive a 50% discount on annual subscriptions.",
            authority=KnowledgeAuthority.AUTHORITATIVE,
            is_ai_generated=True,
        )

    with pytest.raises(PermissionError, match="Safety violation: AI-generated knowledge cannot be created as AUTHORITATIVE"):
        store.create_item(
            knowledge_code="KNW-AI-FAIL2",
            title="Unchecked AI Claim 2",
            content="Unchecked claim.",
            authority=KnowledgeAuthority.CONFIRMED,
            is_ai_generated=True,
        )


# =============================================================================
# 2. Document Extraction & Structural Chunking Tests (Section 20-22)
# =============================================================================

def test_document_intelligence_extraction():
    engine = DocumentIntelligenceEngine()
    content = """
# Enterprise Deployment Guide

## Architecture Overview
The platform requires PostgreSQL 16 and Redis 7.2.

## Security Controls
All dispatchers require MFA step-up verification.
    """

    chunks = engine.chunk_document("DOC-101", content)
    assert len(chunks) >= 2
    assert any("Architecture Overview" in (c.section_heading or "") for c in chunks)
    assert any("Security Controls" in (c.section_heading or "") for c in chunks)

    entities = engine.extract_entities("DOC-101", content)
    assert len(entities) > 0

    candidate_facts = engine.extract_candidate_facts("DOC-101", content)
    # Rule 1 & 2: Candidate facts MUST be INFERRED authority
    for f in candidate_facts:
        assert f.authority == KnowledgeAuthority.INFERRED


# =============================================================================
# 3. Knowledge Graph Engine Tests (Section 23, 24)
# =============================================================================

def test_knowledge_graph_multi_hop_traversal():
    graph = KnowledgeGraphEngine()
    # Baseline seed connects:
    # ENT-CLI-ACME -> ENT-PRJ-PORTAL -> ENT-REQ-MFA -> ENT-DEC-POSTGRES
    path = graph.find_path("ENT-CLI-ACME", "ENT-DEC-POSTGRES", max_hops=4)
    assert path is not None
    assert path[0] == "ENT-CLI-ACME"
    assert path[-1] == "ENT-DEC-POSTGRES"

    neighbors = graph.get_neighbors("ENT-PRJ-PORTAL")
    assert len(neighbors) >= 1

    vis_data = graph.get_graph_visualization_data()
    assert len(vis_data["nodes"]) >= 5
    assert len(vis_data["edges"]) >= 4


# =============================================================================
# 4. Semantic Intelligence & Vector Cosine Similarity Tests (Section 18, 19)
# =============================================================================

def test_semantic_intelligence_engine():
    engine = SemanticIntelligenceEngine()
    emb1 = engine.generate_embedding("KNW-1", "Multi-tenant PostgreSQL database isolation with tenant_id")
    emb2 = engine.generate_embedding("KNW-2", "PostgreSQL database tenant partitioning schema")
    emb3 = engine.generate_embedding("KNW-3", "Baking banana bread culinary cake chocolate dessert recipe")

    sim_related = engine.cosine_similarity(emb1.vector, emb2.vector)
    sim_unrelated = engine.cosine_similarity(emb1.vector, emb3.vector)

    assert sim_related > sim_unrelated
    assert sim_related > 0.3


# =============================================================================
# 5. Hybrid Search & Multi-Factor Relevance Tests (Section 14-17, 43)
# =============================================================================

def test_hybrid_search_ranking():
    store = KnowledgeStore()
    semantic = SemanticIntelligenceEngine()
    search_engine = HybridSearchEngine(store, semantic)

    results = search_engine.search(
        query="PostgreSQL tenant isolation",
        domain=KnowledgeDomain.TECHNICAL,
        strategy="HYBRID",
        top_k=5,
    )

    assert len(results) > 0
    top_result = results[0]
    assert "KNW-ARCH-POSTGRES" in top_result.knowledge_code or "Postgres" in top_result.title
    assert top_result.score > 0.0
    assert "authority" in top_result.relevance_factors
    assert "freshness" in top_result.relevance_factors


def test_search_tenant_isolation_boundary():
    """Non-Negotiable Rule 4 & 5: Search strictly enforces tenant boundaries."""
    store = KnowledgeStore()
    store.create_item(
        knowledge_code="KNW-TENANT-SECRET-001",
        title="Tenant B Secret Strategic Deal",
        content="Confidential acquisition terms for Tenant B.",
        tenant_id="tenant_b",
        classification="INTERNAL",
    )

    semantic = SemanticIntelligenceEngine()
    search_engine = HybridSearchEngine(store, semantic)

    # Search as default_tenant
    results_a = search_engine.search(
        query="Secret Strategic Deal",
        tenant_id="default_tenant",
    )
    assert not any(r.knowledge_code == "KNW-TENANT-SECRET-001" for r in results_a)

    # Search as tenant_b
    results_b = search_engine.search(
        query="Secret Strategic Deal",
        tenant_id="tenant_b",
    )
    assert any(r.knowledge_code == "KNW-TENANT-SECRET-001" for r in results_b)


# =============================================================================
# 6. Context Engine, Injection Defense & Uncertainty Tests (Section 31-35, 70)
# =============================================================================

def test_context_engine_injection_encapsulation_and_uncertainty():
    store = KnowledgeStore()
    semantic = SemanticIntelligenceEngine()
    search_engine = HybridSearchEngine(store, semantic)
    context_engine = KnowledgeContextEngine(search_engine)

    # 1. Normal task intent with available knowledge
    bundle = context_engine.assemble_context(
        task_intent="Step-up authentication MFA policy for administrative state changes",
        agent_id="security_agent",
        budget_tokens=2000,
    )

    assert bundle.consumed_tokens > 0
    assert bundle.consumed_tokens <= bundle.budget_tokens
    assert len(bundle.citations) > 0

    # Rule 7 & 8: Untrusted content boundary encapsulation
    assert "<UNTRUSTED_RETRIEVED_KNOWLEDGE" in bundle.encapsulated_context
    assert "</UNTRUSTED_RETRIEVED_KNOWLEDGE>" in bundle.encapsulated_context
    assert "KNW-SEC-MFA-STEPUP" in bundle.citations

    # 2. Query with zero known knowledge -> Must disclose uncertainty
    empty_bundle = context_engine.assemble_context(
        task_intent="Quantum teleportation mechanics in ancient Mesopotamian pottery",
        agent_id="research_agent",
        budget_tokens=2000,
    )
    assert any("INSUFFICIENT_INFORMATION" in d for d in empty_bundle.uncertainty_disclosures)


# =============================================================================
# 7. Contradiction & Conflict Detection Tests (Section 12, 42)
# =============================================================================

def test_conflict_detector_blocks_silent_resolution():
    detector = ConflictDetector()

    facts = [
        FactItem(
            fact_code="F-1",
            subject="Carrier Portal UI",
            predicate="supported_languages",
            target_value="English_Only",
            authority=KnowledgeAuthority.CONFIRMED,
        ),
        FactItem(
            fact_code="F-2",
            subject="Carrier Portal UI",
            predicate="supported_languages",
            target_value="English_and_Urdu",
            authority=KnowledgeAuthority.AUTHORITATIVE,
        ),
    ]

    conflicts = detector.scan_fact_conflicts(facts)
    assert len(conflicts) == 1
    conflict = conflicts[0]
    assert conflict.status == ConflictStatus.OPEN
    assert "Contradiction on subject 'Carrier Portal UI'" in conflict.description

    # Rule 42: Authority comparison provides human recommendation without auto-resolving
    rec = detector.evaluate_authority_resolution_recommendation(
        KnowledgeItem(knowledge_code="K1", title="Title 1", content="Text 1", authority=KnowledgeAuthority.CONFIRMED),
        KnowledgeItem(knowledge_code="K2", title="Title 2", content="Text 2", authority=KnowledgeAuthority.AUTHORITATIVE),
    )
    assert rec["auto_resolve_permitted"] is False
    assert rec["favored_item"] == "K2"

    # Human sign-off resolution
    resolved = detector.resolve_conflict(
        conflict_code=conflict.conflict_code,
        resolved_by="client_success_vp",
        resolution_notes="Client confirmed multilingual support in signed Addendum #2.",
    )
    assert resolved is not None
    assert resolved.status == ConflictStatus.RESOLVED
    assert resolved.resolved_by == "client_success_vp"


# =============================================================================
# 8. Freshness Monitor Tests (Section 11, 52)
# =============================================================================

def test_freshness_monitor_decay():
    monitor = FreshnessMonitor()
    now = datetime.now(timezone.utc)

    # Fresh item
    fresh_item = KnowledgeItem(
        knowledge_code="K-FRESH",
        title="Fresh Item",
        content="Content",
        domain=KnowledgeDomain.SECURITY,
        created_at=now,
        updated_at=now,
    )
    status_fresh, score_fresh = monitor.evaluate_freshness(fresh_item, current_time=now)
    assert status_fresh == FreshnessStatus.FRESH
    assert score_fresh == 1.0

    # Stale item (older than 60 days for SECURITY)
    old_time = now - timedelta(days=75)
    stale_item = KnowledgeItem(
        knowledge_code="K-STALE",
        title="Stale Item",
        content="Content",
        domain=KnowledgeDomain.SECURITY,
        created_at=old_time,
        updated_at=old_time,
    )
    status_stale, score_stale = monitor.evaluate_freshness(stale_item, current_time=now)
    assert status_stale in (FreshnessStatus.STALE, FreshnessStatus.AGING)
    assert score_stale < 1.0


# =============================================================================
# 9. Knowledge Quality & Retrieval Evaluation Benchmarks (Section 39, 40, 72, 78)
# =============================================================================

def test_knowledge_quality_scorecard():
    evaluator = KnowledgeQualityEvaluator()
    items = [
        KnowledgeItem(
            knowledge_code="K1",
            title="Title 1",
            content="Authoritative validated policy with extensive content and clear rules.",
            domain=KnowledgeDomain.TECHNICAL,
            authority=KnowledgeAuthority.AUTHORITATIVE,
            provenance=KnowledgeProvenance.HUMAN_CONFIRMED,
            content_hash="hash1",
        ),
        KnowledgeItem(
            knowledge_code="K2",
            title="Title 2",
            content="Inferred draft rule requiring additional verification.",
            domain=KnowledgeDomain.AI,
            authority=KnowledgeAuthority.INFERRED,
            provenance=KnowledgeProvenance.AI_INFERRED,
            content_hash="hash2",
        ),
    ]

    card = evaluator.evaluate_quality_scorecard(items, open_conflict_count=0)
    assert card["total_items"] == 2
    assert card["overall_quality_score"] > 80.0
    assert card["metrics"]["verified_count"] == 1
    assert card["metrics"]["inferred_count"] == 1


def test_retrieval_benchmarks_and_zero_leakage_assertion():
    """Non-Negotiable: Unauthorized Retrieval Leakage Rate must be EXACTLY 0.0."""
    evaluator = RetrievalEvaluator()
    test_cases = [
        {
            "query": "PostgreSQL Tenant Isolation",
            "expected_codes": ["KNW-ARCH-POSTGRES-TENANT"],
            "retrieved_codes": ["KNW-ARCH-POSTGRES-TENANT", "KNW-SEC-MFA-STEPUP"],
            "unauthorized_retrieved_count": 0,
            "is_grounded": True,
            "citations_accurate": True,
        },
        {
            "query": "Redis Connection Pool",
            "expected_codes": ["KNW-REL-REDIS-CONN-POOL"],
            "retrieved_codes": ["KNW-REL-REDIS-CONN-POOL"],
            "unauthorized_retrieved_count": 0,
            "is_grounded": True,
            "citations_accurate": True,
        },
    ]

    metrics = evaluator.evaluate_retrieval_metrics(test_cases)
    assert metrics["precision_at_k"] > 0.5
    assert metrics["recall_at_k"] == 1.0
    assert metrics["mrr"] == 1.0
    assert metrics["unauthorized_retrieval_rate"] == 0.0
    assert metrics["zero_leakage_verified"] is True


# =============================================================================
# 10. Agent Permissions & Knowledge Agents Tests (Section 37, 63)
# =============================================================================

def test_knowledge_agent_permissions_and_prohibitions():
    # Valid Phase 48 permissions
    valid_perms = {
        AgentPermission.READ_KNOWLEDGE.value,
        AgentPermission.SEARCH_KNOWLEDGE.value,
        AgentPermission.REQUEST_CONTEXT.value,
        AgentPermission.CREATE_KNOWLEDGE_DRAFT.value,
    }
    validated = validate_agent_permissions(valid_perms)
    assert len(validated) == 4

    # Prohibited actions
    prohibited_candidates = [
        "PROMOTE_TO_AUTHORITATIVE",
        "AUTONOMOUS_POLICY_CHANGE",
        "BYPASS_KNOWLEDGE_AUTHORIZATION",
        "FORCE_RESOLVE_CONFLICT",
        "DELETE_KNOWLEDGE",
    ]
    for p in prohibited_candidates:
        assert p in PROHIBITED_PERMISSIONS
        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({p})


@pytest.mark.asyncio
async def test_knowledge_agents_execution():
    service = KnowledgePlatformService()

    # 1. KnowledgeExtractionAgent
    extract_agent = KnowledgeExtractionAgent()
    doc_content = "# Project Brief\nClient requires PostgreSQL and Redis with MFA."
    ctx_extract = AgentContext(
        workflow_id="wf-test-1",
        task_id="task-test-1",
        agent_run_id="run-test-1",
        metadata={"tenant_id": "default_tenant", "parameters": {"document_id": "DOC-EX-1", "content": doc_content}},
    )
    res_extract = await extract_agent.execute(ctx_extract)
    assert res_extract["status"] == "SUCCESS"
    assert res_extract["chunks_count"] >= 1

    # 2. KnowledgeRetrievalAgent
    retrieval_agent = KnowledgeRetrievalAgent(service)
    ctx_retrieval = AgentContext(
        workflow_id="wf-test-2",
        task_id="task-test-2",
        agent_run_id="run-test-2",
        metadata={"tenant_id": "default_tenant", "parameters": {"query": "PostgreSQL", "strategy": "HYBRID"}},
    )
    res_retrieval = await retrieval_agent.execute(ctx_retrieval)
    assert res_retrieval["status"] == "SUCCESS"
    assert res_retrieval["results_count"] > 0

    # 3. ContextAssemblyAgent
    context_agent = ContextAssemblyAgent(service)
    ctx_bundle = AgentContext(
        workflow_id="wf-test-3",
        task_id="task-test-3",
        agent_run_id="run-test-3",
        metadata={"tenant_id": "default_tenant", "parameters": {"task_intent": "Implement Redis pool", "agent_id": "sre_agent"}},
    )
    res_bundle = await context_agent.execute(ctx_bundle)
    assert res_bundle["status"] == "SUCCESS"
    assert "<UNTRUSTED_RETRIEVED_KNOWLEDGE" in res_bundle["encapsulated_context"]

    # 4. OrganizationalLearningAgent
    learning_agent = OrganizationalLearningAgent(service)
    ctx_learning = AgentContext(
        workflow_id="wf-test-4",
        task_id="task-test-4",
        agent_run_id="run-test-4",
        metadata={
            "tenant_id": "default_tenant",
            "parameters": {
                "title": "Third-Party Rate Limit Buffer Lesson",
                "problem": "Unannounced upstream rate-limits caused 429 errors.",
                "root_cause": "No exponential backoff with jitter on outgoing requests.",
                "what_worked": "Token-bucket client middleware with jittered retry.",
                "what_failed": "Immediate fixed 1s retry loops.",
                "recommendation": "Implement token-bucket client middleware with jitter on all third-party integrations.",
            }
        },
    )
    res_learning = await learning_agent.execute(ctx_learning)
    assert res_learning["status"] == "SUCCESS"
    assert "LES-" in res_learning["lesson_code"]
