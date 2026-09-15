"""Unit and Integration Tests for Phase 36: Unified Data Platform, Data Governance, Data Lineage & Knowledge Architecture."""

import pytest
from datetime import datetime, timezone, timedelta

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
from app.data.quality import ConflictDetector, DataQualityScorer, SourceRecord
from app.data.retention import RetentionEngine


# =============================================================================
# 1. Data Quality & Multi-Dimensional Scoring Tests
# =============================================================================

def test_data_quality_scorer_completeness_and_validity():
    """Verify DataQualityScorer evaluates completeness and validity across sample records."""
    scorer = DataQualityScorer()

    records = [
        {"id": "1", "name": "Company A", "email": "a@company.com", "revenue": 100000},
        {"id": "2", "name": "Company B", "email": "b@company.com", "revenue": 250000},
        {"id": "3", "name": "", "email": None, "revenue": None},
    ]

    result = scorer.evaluate_dataset(records)
    assert result["total_records"] == 3
    assert result["dimensions"]["completeness"] < 1.0
    assert result["dimensions"]["validity"] > 0.5
    assert len(result["violations"]) > 0


def test_data_quality_scorer_uniqueness_detection():
    """Verify duplicate records lower uniqueness score and flag violations."""
    scorer = DataQualityScorer()

    records = [
        {"id": "rec-1", "email": "lead@target.com"},
        {"id": "rec-2", "email": "lead@target.com"}, # duplicate email
        {"id": "rec-3", "email": "unique@target.com"},
    ]

    result = scorer.evaluate_dataset(records)
    assert result["dimensions"]["uniqueness"] < 1.0
    assert any(v.get("dimension") == "uniqueness" for v in result["violations"])


# =============================================================================
# 2. Conflict & Contradiction Detection Tests
# =============================================================================

def test_conflict_detector_identifies_contradictory_field_values():
    """Verify ConflictDetector flags conflicting source statements for the same entity."""
    detector = ConflictDetector()

    records = [
        {
            "source_id": "CRM",
            "source_name": "Hubspot",
            "authority_level": DataAuthority.SYSTEM_INTEGRATION,
            "data": {"company_name": "Acme Corp", "employee_count": 50, "budget": 100000},
        },
        {
            "source_id": "AI_DISCOVERY",
            "source_name": "DiscoveryAgent",
            "authority_level": DataAuthority.AI_INFERENCE,
            "data": {"company_name": "Acme Corp", "employee_count": 250, "budget": 500000},
        },
    ]

    conflicts = detector.detect_conflicts(records)
    assert len(conflicts) > 0
    conflict = conflicts[0]
    assert "employee_count" in conflict.conflicting_fields
    assert "budget" in conflict.conflicting_fields


def test_conflict_detector_no_conflict_on_congruent_records():
    """Verify ConflictDetector passes clean when data fields agree."""
    detector = ConflictDetector()

    records = [
        {
            "source_id": "S1",
            "source_name": "Source1",
            "authority_level": DataAuthority.RAW_DATA,
            "data": {"name": "Identical Name", "tier": "ENTERPRISE"},
        },
        {
            "source_id": "S2",
            "source_name": "Source2",
            "authority_level": DataAuthority.VERIFIED_DATA,
            "data": {"name": "Identical Name", "tier": "ENTERPRISE"},
        },
    ]

    conflicts = detector.detect_conflicts(records)
    assert len(conflicts) == 0


# =============================================================================
# 3. Lineage Graph Engine Tests
# =============================================================================

def test_lineage_graph_trace_upstream_and_downstream():
    """Verify LineageGraphEngine correctly traverses multi-hop dependency networks."""
    engine = LineageGraphEngine()

    edges = [
        # Lead -> Audit
        {
            "source_type": "LEAD",
            "source_id": "lead-001",
            "target_type": "AUDIT",
            "target_id": "audit-001",
            "relationship": LineageRelationship.TRANSFORMED_FROM.value,
            "transformation_name": "DigitalAuditRunner",
            "confidence_score": 0.98,
        },
        # Audit -> Requirement
        {
            "source_type": "AUDIT",
            "source_id": "audit-001",
            "target_type": "REQUIREMENT",
            "target_id": "req-001",
            "relationship": LineageRelationship.DERIVED_FROM.value,
            "transformation_name": "RequirementExtractor",
            "confidence_score": 0.95,
        },
        # Requirement -> Proposal
        {
            "source_type": "REQUIREMENT",
            "source_id": "req-001",
            "target_type": "PROPOSAL",
            "target_id": "prop-001",
            "relationship": LineageRelationship.COMPOSED_OF.value,
            "transformation_name": "ProposalBuilder",
            "confidence_score": 1.0,
        },
        # Proposal -> Contract
        {
            "source_type": "PROPOSAL",
            "source_id": "prop-001",
            "target_type": "CONTRACT",
            "target_id": "contract-001",
            "relationship": LineageRelationship.TRANSFORMED_FROM.value,
            "transformation_name": "ContractGenerator",
            "confidence_score": 1.0,
        },
    ]

    # Trace upstream of proposal
    upstream = engine.trace_upstream(edges, "prop-001")
    upstream_ids = [u["id"] for u in upstream]
    assert "req-001" in upstream_ids
    assert "audit-001" in upstream_ids
    assert "lead-001" in upstream_ids

    # Trace downstream of audit
    downstream = engine.trace_downstream(edges, "audit-001")
    downstream_ids = [d["id"] for d in downstream]
    assert "req-001" in downstream_ids
    assert "prop-001" in downstream_ids
    assert "contract-001" in downstream_ids


# =============================================================================
# 4. Document Management & SHA-256 Integrity Tests
# =============================================================================

def test_document_engine_sha256_computation_and_tamper_detection():
    """Verify DocumentEngine computes deterministic SHA-256 and detects unauthorized alterations."""
    engine = DocumentEngine()

    original_text = "Master Services Agreement between North and Client XYZ with baseline value $50,000."
    tampered_text = "Master Services Agreement between North and Client XYZ with baseline value $10,000."

    checksum = engine.compute_sha256(original_text)
    assert len(checksum) == 64

    # Verification on original must pass
    assert engine.verify_integrity(original_text, checksum) is True

    # Verification on altered text must fail
    assert engine.verify_integrity(tampered_text, checksum) is False


# =============================================================================
# 5. Knowledge Architecture & Lifecycle Promotion Tests
# =============================================================================

def test_knowledge_engine_lifecycle_promotion_permissions():
    """Verify KnowledgeEngine permits authorized promotions and enforces lifecycle order."""
    engine = KnowledgeEngine()

    # Ingested -> Verified by Lead/Admin
    assert engine.promote_item(
        current_state=KnowledgeLifecycle.INGESTED,
        target_state=KnowledgeLifecycle.VERIFIED,
        actor_role="LEAD",
    ) is True

    # Verified -> Canonical by Admin/Owner
    assert engine.promote_item(
        current_state=KnowledgeLifecycle.VERIFIED,
        target_state=KnowledgeLifecycle.CANONICAL,
        actor_role="ADMIN",
    ) is True

    # Unauthorized role attempting canonical promotion should fail
    with pytest.raises(ValueError):
        engine.promote_item(
            current_state=KnowledgeLifecycle.VERIFIED,
            target_state=KnowledgeLifecycle.CANONICAL,
            actor_role="VIEWER",
        )


def test_knowledge_context_retrieval_respects_clearance():
    """Verify KnowledgeEngine filters out items above user clearance level."""
    engine = KnowledgeEngine()

    items = [
        {
            "id": "1",
            "title": "Public Guide",
            "content": "Public information",
            "classification": DataClassification.PUBLIC,
        },
        {
            "id": "2",
            "title": "Internal SOP",
            "content": "Internal procedures",
            "classification": DataClassification.INTERNAL,
        },
        {
            "id": "3",
            "title": "Restricted Keys",
            "content": "Top secret architectural keys",
            "classification": DataClassification.RESTRICTED,
        },
    ]

    # User with only PUBLIC and INTERNAL clearance
    user_clearance = [DataClassification.PUBLIC, DataClassification.INTERNAL]
    filtered = engine.filter_authorized_items(items, user_clearance)

    filtered_ids = [f["id"] for f in filtered]
    assert "1" in filtered_ids
    assert "2" in filtered_ids
    assert "3" not in filtered_ids


# =============================================================================
# 6. Retention Policy & Legal Hold Tests
# =============================================================================

def test_retention_engine_blocks_deletion_under_legal_hold():
    """Verify active legal holds strictly prevent entity deletion."""
    engine = RetentionEngine()

    active_holds = [
        {
            "case_reference": "SEC-2026-99",
            "entity_type": "CONTRACT",
            "entity_id": "CTR-1001",
            "active": True,
        }
    ]

    # Trying to delete held contract must be blocked
    result = engine.check_deletion_eligibility(
        entity_type="CONTRACT",
        entity_id="CTR-1001",
        created_at=datetime.now(timezone.utc) - timedelta(days=500),
        retention_days=365,
        active_holds=active_holds,
    )
    assert result["allowed"] is False
    assert result["reason"] == "ACTIVE_LEGAL_HOLD"

    # Different contract not under hold can be deleted if expired
    result_free = engine.check_deletion_eligibility(
        entity_type="CONTRACT",
        entity_id="CTR-9999",
        created_at=datetime.now(timezone.utc) - timedelta(days=500),
        retention_days=365,
        active_holds=active_holds,
    )
    assert result_free["allowed"] is True
