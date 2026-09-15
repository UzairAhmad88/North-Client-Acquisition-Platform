"""Unit tests for Phase 28 — Change Request, Scope Change & Commercial Change Management."""

import hashlib
import uuid
import pytest
from datetime import datetime, timezone

from app.models.change import (
    ChangeApproval,
    ChangeBaselineLink,
    ChangeCommercial,
    ChangeEstimate,
    ChangeEvidence,
    ChangeEvent,
    ChangeImpact,
    ChangeRequest,
    ChangeRequestVersion,
)
from agents.change_management.agent import ChangeAgent
from agents.change_management.classifier import ChangeClassifier
from agents.change_management.impact_analyzer import ChangeImpactAnalyzer
from agents.change_management.scope_analyzer import ChangeScopeAnalyzer
from agents.change_management.effort_analyzer import ChangeEffortAnalyzer
from agents.change_management.commercial_analyzer import ChangeCommercialAnalyzer
from agents.change_management.contract_analyzer import ChangeContractAnalyzer
from agents.change_management.summary import ChangeSummaryEngine
from agents.core.context import AgentContext
from agents.core.permissions import PROHIBITED_PERMISSIONS


def test_change_agent_permission_guardrails():
    """Verify ChangeAgent has zero autonomous permissions to approve scope changes, alter baselines or modify pricing."""
    agent = ChangeAgent()
    perms = {p.value for p in agent.get_required_permissions()}

    # Assert allowed READ & CLASSIFY permissions
    assert "READ_CHANGE_REQUEST" in perms
    assert "READ_BASELINE" in perms
    assert "CREATE_CHANGE_DRAFT" in perms
    assert "CREATE_CHANGE_ANALYSIS" in perms
    assert "CREATE_IMPACT_ANALYSIS" in perms

    # Assert strictly prohibited side-effect permissions
    prohibited_actions = [
        "APPROVE_CHANGE",
        "APPROVE_SCOPE_CHANGE",
        "CHANGE_CONTRACT",
        "MODIFY_BASELINE",
        "SEND_EXTERNAL_MESSAGE",
        "CHANGE_PRICE",
        "PROMISE_DEADLINE",
    ]
    for prohibited in prohibited_actions:
        assert prohibited not in perms
        assert prohibited in PROHIBITED_PERMISSIONS


def test_change_classifier():
    """Test classification and triage of change requests."""
    classifier = ChangeClassifier()

    # Out of scope
    res_out = classifier.classify_change("cr-1", "Build Mobile App", "We need a new mobile app for iOS.")
    assert res_out.classification == "OUT_OF_SCOPE"
    assert res_out.is_out_of_scope is True

    # Defect
    res_bug = classifier.classify_change("cr-2", "Fix Login Crash", "There is a broken error on login page.")
    assert res_bug.classification == "DEFECT"
    assert res_bug.is_out_of_scope is False

    # In scope content update
    res_in = classifier.classify_change("cr-3", "Logo Update", "Update logo image asset on header.")
    assert res_in.classification == "IN_SCOPE"


def test_change_impact_analyzer():
    """Test multi-dimensional impact analysis."""
    analyzer = ChangeImpactAnalyzer()

    res = analyzer.analyze_impact("cr-101", "Stripe Payment Gateway Integration", "Integrate credit card payments.")
    assert res.change_request_id == "cr-101"
    assert res.overall_impact_level == "HIGH"
    assert res.requires_contract_amendment is True
    assert res.requires_commercial_adjustment is True
    assert len(res.impacts) >= 3


def test_pert_effort_analyzer():
    """Test PERT three-point effort re-estimation."""
    analyzer = ChangeEffortAnalyzer()

    res = analyzer.calculate_effort("cr-102", "Mobile Application", "Build iOS app.")
    assert res.optimistic_hours == 80.0
    assert res.most_likely_hours == 120.0
    assert res.pessimistic_hours == 180.0
    # Expected = (80 + 4*120 + 180) / 6 = 740 / 6 = 123.33
    assert res.expected_hours == 123.33
    assert len(res.assumptions) >= 1


def test_commercial_analyzer():
    """Test commercial delta calculation."""
    analyzer = ChangeCommercialAnalyzer()

    res = analyzer.calculate_commercial_delta("cr-103", expected_hours=20.0, hourly_rate=5000.0, original_contract_value=500000.0)
    assert res.original_value == 500000.0
    assert res.change_value == 100000.0
    assert res.revised_value == 600000.0
    assert res.commercial_recommendation == "ADDITIONAL_COST_REQUIRED"


def test_contract_analyzer():
    """Test contract amendment signal detection."""
    analyzer = ChangeContractAnalyzer()

    res = analyzer.evaluate_contract_impact("cr-104", is_out_of_scope=True, commercial_change_value=100000.0)
    assert res["requires_contract_amendment"] is True
    assert res["contract_impact_type"] == "CONTRACT_AMENDMENT_REQUIRED"


def test_change_summary_engine():
    """Test generation of executive and client proposal summaries."""
    engine = ChangeSummaryEngine()

    res = engine.summarize_change("cr-105", "CR-0005", "Payment Gateway", "Add Stripe payments.", expected_hours=24.0, change_value=120000.0)
    assert res.change_number == "CR-0005"
    assert "24.0 hours" in res.executive_summary
    assert "PKR 120,000.00" in res.commercial_impact_summary
    assert res.estimated_schedule_impact_days == 4


@pytest.mark.asyncio
async def test_change_agent_full_execution():
    """Test full execution of ChangeAgent for CLASSIFY_CHANGE action."""
    agent = ChangeAgent()
    context = AgentContext(
        workflow_id="wf-change-test",
        task_id="t-change-test",
        agent_run_id="run-change-test",
        metadata={
            "action": "CLASSIFY_CHANGE",
            "change_request_id": "cr-999",
            "title": "Add Native iOS App",
            "description": "Can we also build a native iOS mobile application?",
        },
    )

    result = await agent.execute(context)
    assert "classification" in result
    assert result["classification"] == "OUT_OF_SCOPE"
    assert result["is_out_of_scope"] is True


def test_content_hash_and_baseline_versioning_integrity():
    """Verify SHA-256 content hashing for change request payload integrity."""
    payload_text = "CR-0001:Add Payment Gateway Integration"
    expected_hash = hashlib.sha256(payload_text.encode('utf-8')).hexdigest()

    version = ChangeRequestVersion(
        id=str(uuid.uuid4()),
        change_request_id=str(uuid.uuid4()),
        version_number=1,
        description="Add Payment Gateway Integration",
        content_hash=expected_hash,
        created_by="Client Admin",
    )

    assert version.version_number == 1
    assert version.content_hash == expected_hash
    assert len(version.content_hash) == 64
