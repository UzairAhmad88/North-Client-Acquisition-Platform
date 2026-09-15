"""Unit tests for Phase 29 — Quality Assurance, UAT, Delivery Acceptance & Handover System."""

import hashlib
import uuid
import pytest
from datetime import datetime, timezone

from app.models.qa import (
    AcceptanceCriteria,
    Defect,
    DeliveryPackage,
    HandoverChecklist,
    QAEvent,
    ReleaseVersion,
    TestCase,
    TestEvidence,
    TestPlan,
    TestResult,
    TestRun,
    UATFeedback,
    UATSession,
)
from agents.qa.agent import QAAgent
from agents.qa.defect_classifier import DefectClassifierEngine
from agents.qa.handover_engine import HandoverEngine
from agents.qa.readiness_evaluator import ReadinessEvaluatorEngine
from agents.qa.regression_analyzer import RegressionAnalyzerEngine
from agents.qa.test_generator import TestGeneratorEngine
from agents.core.context import AgentContext
from agents.core.permissions import PROHIBITED_PERMISSIONS


def test_qa_agent_permission_guardrails():
    """Verify QAAgent has ZERO autonomous permissions to approve UAT, accept deliverables, close critical defects, or complete handover."""
    agent = QAAgent()
    perms = {p.value for p in agent.get_required_permissions()}

    # Assert allowed READ & DRAFT permissions
    assert "READ_TEST_PLANS" in perms
    assert "READ_DEFECTS" in perms
    assert "READ_UAT" in perms
    assert "READ_RELEASES" in perms
    assert "CREATE_TEST_CASE_DRAFT" in perms
    assert "CREATE_QA_SUMMARY" in perms
    assert "CREATE_RELEASE_READINESS_DRAFT" in perms
    assert "CREATE_HANDOVER_CHECKLIST_DRAFT" in perms

    # Assert strictly prohibited permissions
    prohibited_actions = [
        "APPROVE_UAT",
        "APPROVE_RELEASE",
        "ACCEPT_DELIVERABLE",
        "CLOSE_DEFECT",
        "MARK_PROJECT_COMPLETE",
        "DEPLOY_PRODUCTION",
        "TRANSFER_CREDENTIALS",
    ]
    for prohibited in prohibited_actions:
        assert prohibited not in perms
        assert prohibited in PROHIBITED_PERMISSIONS


def test_test_generator_engine():
    """Test AI drafting of functional, edge case, and deliverable test cases."""
    generator = TestGeneratorEngine()

    reqs = [{"id": "req-1", "title": "Stripe Integration", "description": "Process credit card payments securely."}]
    delivs = [{"id": "del-1", "title": "Payment Microservice API"}]

    res = generator.generate_test_cases(test_plan_id="tp-101", requirements=reqs, deliverables=delivs)
    assert res.test_plan_id == "tp-101"
    assert res.total_count == 3
    assert len(res.generated_test_cases) == 3

    # Check test case codes and categories
    tc_req_functional = res.generated_test_cases[0]
    assert tc_req_functional.category == "FUNCTIONAL"
    assert tc_req_functional.requirement_id == "req-1"

    tc_req_security = res.generated_test_cases[1]
    assert tc_req_security.category == "SECURITY"

    tc_deliv = res.generated_test_cases[2]
    assert tc_deliv.category == "UAT"
    assert tc_deliv.deliverable_id == "del-1"


def test_defect_classifier_engine():
    """Test defect classification into Critical/High/Low severity and Defect vs Scope Change."""
    classifier = DefectClassifierEngine()

    # 1. Critical Security Vulnerability / Crash
    res_crit = classifier.classify_defect(
        defect_id=None,
        title="Fatal System Crash on Database Connection",
        description="Database connection crash leads to fatal server error and data loss.",
        is_against_baseline_spec=True,
    )
    assert res_crit.severity == "CRITICAL"
    assert res_crit.classification == "DEFECT"
    assert res_crit.is_blocking_release is True

    # 2. Scope Change Detection
    res_scope = classifier.classify_defect(
        defect_id=None,
        title="Add support for PayPal payments",
        description="We also need a new feature to accept PayPal payments.",
        is_against_baseline_spec=False,
    )
    assert res_scope.classification == "SCOPE_CHANGE"
    assert res_scope.is_blocking_release is False


def test_regression_analyzer_engine():
    """Test targeted regression test suite selection."""
    analyzer = RegressionAnalyzerEngine()

    all_cases = [
        {"id": "tc-1", "is_regression": True, "priority": "CRITICAL", "requirement_id": "req-1"},
        {"id": "tc-2", "is_regression": True, "priority": "LOW", "requirement_id": "req-2"},
        {"id": "tc-3", "is_regression": False, "priority": "HIGH", "deliverable_id": "del-1"},
    ]

    res = analyzer.select_regression_suite(
        project_id="p-1",
        all_test_cases=all_cases,
        changed_requirement_ids=["req-1"],
        changed_deliverable_ids=[],
    )
    assert res.project_id == "p-1"
    assert "tc-1" in res.selected_test_case_ids


def test_readiness_evaluator_engine_gate_rules():
    """Test release readiness score calculation and deterministic quality gate blocking rules."""
    evaluator = ReadinessEvaluatorEngine()

    # 1. Ready Release (100% tests passed, 0 critical defects, UAT approved)
    res_ready = evaluator.evaluate_readiness(
        project_id="p-1",
        version_tag="v1.0.0",
        total_test_count=10,
        passed_test_count=10,
        failed_test_count=0,
        open_critical_defects=0,
        open_high_defects=0,
        uat_approved=True,
    )
    assert res_ready.is_ready_for_release is True
    assert res_ready.readiness_score == 100.0
    assert len(res_ready.blocking_conditions) == 0

    # 2. Blocked Release (Failing tests and open critical defects override score)
    res_blocked = evaluator.evaluate_readiness(
        project_id="p-1",
        version_tag="v1.0.0",
        total_test_count=10,
        passed_test_count=8,
        failed_test_count=2,
        open_critical_defects=1,
        open_high_defects=0,
        uat_approved=False,
    )
    assert res_blocked.is_ready_for_release is False
    assert len(res_blocked.blocking_conditions) == 3
    assert "2 failing test(s) detected in execution run." in res_blocked.blocking_conditions[0]
    assert "1 open CRITICAL defect(s) unresolved." in res_blocked.blocking_conditions[1]


def test_handover_engine():
    """Test handover checklist drafting."""
    engine = HandoverEngine()
    res = engine.build_handover_checklist(
        project_id="p-1",
        code_repo_url="https://github.com/org/repo",
        docs_url="https://docs.org",
        staging_url="https://app.org",
    )
    assert res.project_id == "p-1"
    assert len(res.verification_notes) == 5
    assert res.code_repository_transferred is False


@pytest.mark.asyncio
async def test_qa_agent_full_execution():
    """Test full execution of QAAgent for GENERATE_TEST_CASES action."""
    agent = QAAgent()
    context = AgentContext(
        workflow_id="wf-qa-test",
        task_id="t-qa-test",
        agent_run_id="run-qa-test",
        metadata={
            "action": "GENERATE_TEST_CASES",
            "test_plan_id": "tp-999",
            "requirements": [{"id": "req-10", "title": "User Authentication"}],
        },
    )

    result = await agent.execute(context)
    assert "generated_test_cases" in result
    assert result["total_count"] >= 2
    assert result["confidence"] == 0.95


def test_sha256_client_signoff_verification_hash():
    """Verify SHA-256 content hash generation for client acceptance and handover signoff."""
    project_id = "proj-101"
    client_signer_id = "Client CEO"
    signoff_statement = "I approve final delivery and handover of the software package."

    payload = f"{project_id}:{client_signer_id}:{signoff_statement}"
    sha256_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    checklist = HandoverChecklist(
        id=str(uuid.uuid4()),
        project_id=project_id,
        title="Final Handover",
        signed_off_by_client=True,
        client_signoff_hash=sha256_hash,
        signed_off_at=datetime.now(timezone.utc),
    )

    assert checklist.signed_off_by_client is True
    assert checklist.client_signoff_hash == sha256_hash
    assert len(checklist.client_signoff_hash) == 64
