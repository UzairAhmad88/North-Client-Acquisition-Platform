"""
Phase 77: Unified Enterprise Knowledge Graph, Universal Enterprise Search,
Semantic Intelligence, Data Fabric & Organizational Memory Test Suite.
"""

import pytest
from fastapi.testclient import TestClient
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS,
    validate_agent_permissions,
    AgentPermissionDeniedError,
)
from app.services.knowledge.service import EnterpriseKnowledgeFabricService
from app.agents.knowledge import (
    KnowledgeOrchestrator,
    ResearchAgent,
    EntityResolutionAgent,
    ExtractionAgent,
    ClassificationAgent,
    OntologyAgent,
    SearchAgent,
    GraphAgent,
    EvidenceAgent,
    FactCheckerAgent,
    ConflictAgent,
    KnowledgeGapAgent,
    KnowledgeStewardAgent,
)
from app.api.v1.enterprise_knowledge import router as enterprise_knowledge_router


@pytest.fixture
def fabric_service():
    return EnterpriseKnowledgeFabricService()


@pytest.fixture
def test_client():
    from fastapi import FastAPI
    test_app = FastAPI()
    test_app.include_router(enterprise_knowledge_router)
    return TestClient(test_app)



def test_fabric_summary(fabric_service):
    """Test real-time telemetry metrics of the knowledge fabric."""
    summary = fabric_service.get_fabric_summary(tenant_id="tenant-corp-1")
    assert summary.total_canonical_entities == 4850
    assert summary.total_relationships == 24900
    assert summary.total_claims == 12400
    assert summary.total_documents == 1820
    assert summary.overall_quality_score >= 95.0
    assert summary.active_conflicts == 3
    assert summary.open_knowledge_gaps == 5
    assert summary.active_knowledge_agents == 13
    assert summary.fabric_status == "OPERATIONAL"


def test_universal_search_query_understanding(fabric_service):
    """Test natural language query intent parsing and entity extraction."""
    res = fabric_service.universal_search(
        query="Show delayed projects involving our largest customers this quarter",
        tenant_id="tenant-corp-1",
        user_role="operator"
    )
    assert res.query == "Show delayed projects involving our largest customers this quarter"
    assert res.interpreted_intent in ["PROJECT_HEALTH", "CUSTOMER_DISCOVERY"]
    assert len(res.extracted_entities) >= 1
    assert res.total_results >= 2
    assert res.latency_ms < 50.0
    for r in res.results:
        assert r.relevance_score > 0.8
        assert r.confidence > 0.9


def test_universal_search_security_trimming(fabric_service):
    """Test RBAC/ABAC access-aware security trimming."""
    # Standard operator query -> RESTRICTED items should be trimmed
    op_res = fabric_service.universal_search(
        query="Show revenue runway and strategic models",
        tenant_id="tenant-corp-1",
        user_role="operator"
    )
    assert op_res.security_trimmed_count >= 1
    for r in op_res.results:
        assert r.security_clearance != "RESTRICTED"

    # Executive query -> RESTRICTED items should be accessible
    exec_res = fabric_service.universal_search(
        query="Show revenue runway and strategic models",
        tenant_id="tenant-corp-1",
        user_role="executive"
    )
    assert exec_res.security_trimmed_count == 0
    clearances = [r.security_clearance for r in exec_res.results]
    assert "RESTRICTED" in clearances


def test_entity_360_view(fabric_service):
    """Test complete 360-degree canonical entity representation."""
    e360 = fabric_service.get_entity_360(entity_code="ENT-CUST-101", tenant_id="tenant-corp-1")
    assert e360.entity_code == "ENT-CUST-101"
    assert "Acme" in e360.canonical_name
    assert e360.entity_type == "CUSTOMER"
    assert len(e360.aliases) == 4
    assert len(e360.relationships) == 3
    assert len(e360.documents) == 2
    assert len(e360.claims) == 2
    assert len(e360.lineage) == 2
    assert len(e360.ai_insights) == 2


def test_entity_resolution_and_mastering(fabric_service):
    """Test clustering disparate aliases into a canonical master entity."""
    records = [
        {"name": "Acme Ltd", "source": "Salesforce"},
        {"name": "ACME Limited", "source": "NetSuite"},
        {"name": "Acme Inc.", "source": "ContractRepo"},
    ]
    res = fabric_service.resolve_entities(records=records, tenant_id="tenant-corp-1")
    assert res.canonical_entity_code == "ENT-CUST-101"
    assert res.canonical_name == "Acme Corporation"
    assert len(res.merged_sources) == 3
    assert res.confidence_score >= 0.95
    assert len(res.match_evidence) >= 2
    assert res.requires_human_review is False


def test_graph_traversal_and_analytics(fabric_service):
    """Test multi-hop graph traversal and topology calculations."""
    graph = fabric_service.traverse_graph(
        start_entity_code="ENT-CUST-101",
        max_depth=2,
        tenant_id="tenant-corp-1"
    )
    assert len(graph.nodes) == 4
    assert len(graph.edges) == 3
    assert graph.shortest_path == ["ENT-CUST-101", "PRJ-APOLLO", "SUP-INTEL-01"]
    assert graph.analytics["centrality_score"] > 0.8
    assert graph.analytics["critical_dependencies_count"] == 1


def test_claims_and_evidence_verification(fabric_service):
    """Test claim verification against authoritative documentary evidence."""
    claim = fabric_service.verify_claim(claim_code="CLM-SLA-01", tenant_id="tenant-corp-1")
    assert claim.claim_code == "CLM-SLA-01"
    assert claim.subject == "Acme Corporation"
    assert claim.predicate == "has_sla_uptime_target"
    assert claim.object_value == "99.95%"
    assert claim.verification_status == "VERIFIED"
    assert claim.composite_confidence >= 0.98
    assert len(claim.evidence_trail) == 2


def test_conflict_resolution_workflow(fabric_service):
    """Test deterministic conflict reconciliation."""
    resolved = fabric_service.resolve_conflict(
        conflict_code="CNF-2026-01",
        resolution_strategy="AUTHORITY_TIER",
        resolved_value="NET-30 (Audited ERP)",
        resolver="EnterpriseSteward",
        tenant_id="tenant-corp-1"
    )
    assert resolved.conflict_code == "CNF-2026-01"
    assert resolved.status == "RESOLVED"
    assert "NET-30" in resolved.resolved_value
    assert resolved.resolution_strategy == "AUTHORITY_TIER"


def test_knowledge_quality_scores(fabric_service):
    """Test composite multi-factor quality scoring."""
    scores = fabric_service.get_quality_scores(tenant_id="tenant-corp-1")
    assert scores.overall_quality_score >= 95.0
    assert scores.completeness_score >= 90.0
    assert scores.accuracy_score >= 95.0
    assert scores.freshness_score >= 90.0
    assert scores.source_reliability_score >= 95.0
    assert "FINANCE" in scores.domains
    assert "OPERATIONS" in scores.domains


def test_ekg_permissions_and_prohibitions():
    """Verify Phase 77 permissions and prohibitions are registered and enforced."""
    perms = [
        AgentPermission.READ_KNOWLEDGE_FABRIC,
        AgentPermission.SEARCH_UNIVERSAL_ENTERPRISE,
        AgentPermission.MANAGE_ENTERPRISE_KNOWLEDGE_GRAPH,
        AgentPermission.EXECUTE_ENTITY_RESOLUTION,
        AgentPermission.MANAGE_BUSINESS_ONTOLOGY,
        AgentPermission.GOVERN_ORGANIZATIONAL_MEMORY,
        AgentPermission.RESOLVE_KNOWLEDGE_CONFLICTS,
        AgentPermission.MANAGE_KNOWLEDGE_RETENTION_DELETION,
    ]
    for p in perms:
        assert p.value in AgentPermission.__members__

    prohibitions = [
        "AUTONOMOUS_DELETE_AUTHORITATIVE_KNOWLEDGE",
        "UNAUDITED_ENTITY_MERGE_HIGH_RISK",
        "BYPASS_SEARCH_SECURITY_TRIMMING",
        "EXPOSE_CONFIDENTIAL_METADATA_UNTRIMMED",
        "SILENTLY_OVERWRITE_KNOWLEDGE_RECORD",
        "POISON_KNOWLEDGE_GRAPH_UNVERIFIED",
    ]
    for ph in prohibitions:
        assert ph in PROHIBITED_PERMISSIONS
        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({ph})


@pytest.mark.asyncio
async def test_all_13_knowledge_agents():
    """Verify instantiation, execution, and permissions across all 13 Knowledge Agents."""
    agents = [
        KnowledgeOrchestrator(),
        ResearchAgent(),
        EntityResolutionAgent(),
        ExtractionAgent(),
        ClassificationAgent(),
        OntologyAgent(),
        SearchAgent(),
        GraphAgent(),
        EvidenceAgent(),
        FactCheckerAgent(),
        ConflictAgent(),
        KnowledgeGapAgent(),
        KnowledgeStewardAgent(),
    ]
    assert len(agents) == 13

    ctx = AgentContext(
        workflow_id="wf-ekg-test",
        task_id="task-ekg-01",
        agent_run_id="run-ekg-01",
        metadata={"tenant_id": "tenant-corp-1"}
    )

    for agent in agents:
        perms = agent.get_required_permissions()
        assert AgentPermission.READ_KNOWLEDGE_FABRIC in perms
        for p in perms:
            assert p.value not in PROHIBITED_PERMISSIONS

        res = await agent.run(ctx)
        assert res.status == "COMPLETED"
        assert res.confidence == "HIGH"
        assert res.metadata["agent_id"] == agent.agent_id


def test_api_endpoints_knowledge_fabric(test_client):
    """Test FastAPI REST endpoints mounted at /knowledge-fabric."""
    # 1. Summary
    summary_resp = test_client.get("/knowledge-fabric/summary?tenant_id=tenant-corp-1")
    assert summary_resp.status_code == 200
    assert summary_resp.json()["overall_quality_score"] >= 95.0

    # 2. Universal Search
    search_resp = test_client.post(
        "/knowledge-fabric/search/universal",
        json={
            "query": "Find delayed projects and contracts for customer Acme",
            "tenant_id": "tenant-corp-1",
            "user_role": "operator"
        }
    )
    assert search_resp.status_code == 200
    assert len(search_resp.json()["results"]) >= 2

    # 3. Entity 360
    e360_resp = test_client.get("/knowledge-fabric/entities/ENT-CUST-101/360?tenant_id=tenant-corp-1")
    assert e360_resp.status_code == 200
    assert e360_resp.json()["entity_code"] == "ENT-CUST-101"

    # 4. Resolve Entities
    resolve_resp = test_client.post(
        "/knowledge-fabric/entities/resolve",
        json={
            "records": [{"name": "Acme Ltd"}, {"name": "ACME Limited"}],
            "tenant_id": "tenant-corp-1"
        }
    )
    assert resolve_resp.status_code == 200
    assert resolve_resp.json()["canonical_name"] == "Acme Corporation"

    # 5. Graph Query
    graph_resp = test_client.post(
        "/knowledge-fabric/graph/query",
        json={
            "start_entity_code": "ENT-CUST-101",
            "max_depth": 2,
            "tenant_id": "tenant-corp-1"
        }
    )
    assert graph_resp.status_code == 200
    assert len(graph_resp.json()["nodes"]) == 4

    # 6. Verify Claim
    claim_resp = test_client.post(
        "/knowledge-fabric/claims/verify",
        json={"claim_code": "CLM-SLA-01", "tenant_id": "tenant-corp-1"}
    )
    assert claim_resp.status_code == 200
    assert claim_resp.json()["verification_status"] == "VERIFIED"

    # 7. Quality Scores
    quality_resp = test_client.get("/knowledge-fabric/quality/scores?tenant_id=tenant-corp-1")
    assert quality_resp.status_code == 200
    assert quality_resp.json()["overall_quality_score"] >= 95.0

    # 8. Resolve Conflict
    conflict_resp = test_client.post(
        "/knowledge-fabric/conflicts/resolve",
        json={
            "conflict_code": "CNF-2026-01",
            "resolution_strategy": "AUTHORITY_TIER",
            "resolved_value": "NET-30",
            "resolver": "Steward",
            "tenant_id": "tenant-corp-1"
        }
    )
    assert conflict_resp.status_code == 200
    assert conflict_resp.json()["status"] == "RESOLVED"

    # 9. Trigger Ingestion
    ingest_resp = test_client.post(
        "/knowledge-fabric/ingestion/trigger",
        json={
            "source_name": "ContractRepo",
            "document_payloads": [{"title": "MSA 2026", "type": "PDF"}],
            "tenant_id": "tenant-corp-1"
        }
    )
    assert ingest_resp.status_code == 200
    assert ingest_resp.json()["status"] == "QUEUED"

    # 10. Lessons
    lessons_resp = test_client.get("/knowledge-fabric/lessons?domain=OPERATIONS&tenant_id=tenant-corp-1")
    assert lessons_resp.status_code == 200
    assert len(lessons_resp.json()) >= 1

    # 11. Agents List
    agents_resp = test_client.get("/knowledge-fabric/agents")
    assert agents_resp.status_code == 200
    assert agents_resp.json()["total_agents"] == 13

    # 12. Gaps & Stewards
    gaps_resp = test_client.get("/knowledge-fabric/gaps?tenant_id=tenant-corp-1")
    assert gaps_resp.status_code == 200
    assert gaps_resp.json()["open_gaps_count"] == 2

    stewards_resp = test_client.get("/knowledge-fabric/stewards?tenant_id=tenant-corp-1")
    assert stewards_resp.status_code == 200
    assert stewards_resp.json()["total_stewards"] == 4
