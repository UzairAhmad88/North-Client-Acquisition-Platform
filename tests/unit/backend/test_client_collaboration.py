"""Unit tests for Phase 27 — Client Collaboration, Communication & Delivery Workspace."""

import hashlib
import uuid
import pytest
from datetime import datetime, timezone, timedelta

from app.models.client import (
    ClientAccount,
    ClientMember,
    ClientInvitation,
    ClientProjectAccess,
    DiscussionThread,
    ThreadMessage,
    ClientQuestion,
    ClientRequest,
    ClientFeedback,
    DeliverableReview,
    DeliverableApproval,
    ProjectFile,
    ClientActionItem,
    ProjectAnnouncement,
    ClientActivity,
)
from agents.client_collaboration.agent import ClientCollaborationAgent
from agents.client_collaboration.classifier import ClientRequestClassifier
from agents.client_collaboration.summarizer import ClientFeedbackSummarizer
from agents.client_collaboration.action_extractor import ClientActionExtractor
from agents.client_collaboration.scope_detector import ClientScopeDetector
from agents.core.context import AgentContext
from agents.core.permissions import PROHIBITED_PERMISSIONS


def test_client_collaboration_agent_permission_guardrails():
    """Verify ClientCollaborationAgent has zero autonomous permissions to approve deliverables, alter scope/pricing or promise deadlines."""
    agent = ClientCollaborationAgent()
    perms = {p.value for p in agent.get_required_permissions()}

    # Assert allowed READ & CLASSIFY permissions
    assert "READ_CLIENT_FEEDBACK" in perms
    assert "READ_CLIENT_MESSAGES" in perms
    assert "CREATE_CLASSIFICATION" in perms
    assert "CREATE_SUMMARY" in perms
    assert "CREATE_ACTION_DRAFT" in perms
    assert "CREATE_SCOPE_SIGNAL" in perms

    # Assert strictly prohibited side-effect permissions
    prohibited_actions = [
        "APPROVE_DELIVERABLE",
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


def test_client_request_classifier():
    """Test classification of incoming client messages into structured request types."""
    classifier = ClientRequestClassifier()

    # Scope change classification
    res_scope = classifier.classify_request("req-101", "Mobile App Feature", "Can we also build a new mobile app for iOS?")
    assert res_scope.classification == "POTENTIAL_SCOPE_CHANGE"
    assert res_scope.confidence_score >= 0.8
    assert res_scope.is_potential_scope_change is True

    # Bug classification
    res_bug = classifier.classify_request("req-102", "Login Failure", "There is a broken error on login page.")
    assert res_bug.classification == "BUG"
    assert res_bug.is_potential_scope_change is False

    # In scope feedback classification
    res_in_scope = classifier.classify_request("req-103", "UI Colors", "The general layout looks good.")
    assert res_in_scope.classification == "IN_SCOPE"


def test_client_feedback_summarizer():
    """Test aggregation and summarization of client feedback items."""
    summarizer = ClientFeedbackSummarizer()

    feedback_items = [
        {"content": "The header logo looks small.", "category": "DESIGN"},
        {"content": "Please fix the drop-down selector alignment.", "category": "BUG"},
    ]

    summary = summarizer.summarize_feedback(
        deliverable_id="del-101",
        deliverable_name="Frontend UI",
        feedback_items=feedback_items,
    )
    assert summary.deliverable_id == "del-101"
    assert summary.deliverable_name == "Frontend UI"
    assert summary.overall_sentiment == "REVISION_REQUIRED"
    assert len(summary.key_feedback_points) == 2
    assert summary.is_revision_requested is True


def test_client_action_extractor():
    """Test extraction of client action items and dependencies from conversation text."""
    extractor = ClientActionExtractor()

    messages = [
        {"id": "msg-1", "content": "Please provide production Stripe API keys by Friday."},
        {"id": "msg-2", "content": "We have updated the design document."},
    ]
    actions = extractor.extract_action_items(messages=messages)

    assert len(actions) == 1
    assert "Client input required" in actions[0].title
    assert actions[0].priority == "HIGH"


def test_client_scope_detector():
    """Test evaluation of scope expansion signals in client inquiries."""
    detector = ClientScopeDetector()

    baseline_scope = ["Web Dashboard UI", "REST API Layer"]
    text = "Can we also build a new mobile app for iOS?"

    result = detector.evaluate_scope(text=text, baseline_scope_items=baseline_scope)
    assert result.classification == "POTENTIAL_SCOPE_CHANGE"
    assert result.is_potential_scope_change is True
    assert result.confidence_score >= 0.8


@pytest.mark.asyncio
async def test_client_collaboration_agent_full_execution():
    """Test full execution of ClientCollaborationAgent for CLASSIFY_REQUEST action."""
    agent = ClientCollaborationAgent()
    context = AgentContext(
        workflow_id="wf-client-test",
        task_id="t-client-test",
        agent_run_id="run-client-test",
        metadata={
            "action": "CLASSIFY_REQUEST",
            "request_id": "req-99",
            "title": "Add Excel Export",
            "description": "Can we also build export to Excel for all reports?",
        },
    )

    result = await agent.execute(context)
    assert "classification" in result
    assert result["classification"] == "POTENTIAL_SCOPE_CHANGE"
    assert result["is_potential_scope_change"] is True


def test_deliverable_approval_hash_integrity():
    """Verify SHA-256 hashing logic for client deliverable approvals."""
    content_payload = "Version 1.0 Architecture Specification Payload"
    expected_hash = hashlib.sha256(content_payload.encode('utf-8')).hexdigest()

    approval = DeliverableApproval(
        id=str(uuid.uuid4()),
        deliverable_id=str(uuid.uuid4()),
        version_number=1,
        content_hash=expected_hash,
        approval_statement="I explicitly confirm and approve this deliverable version.",
        signer_name="Client Executive",
        signer_email="client@acme.com",
        approved_at=datetime.now(timezone.utc),
    )

    assert approval.version_number == 1
    assert approval.content_hash == expected_hash
    assert len(approval.content_hash) == 64
    assert "confirm and approve" in approval.approval_statement


def test_invitation_token_hash_and_expiry():
    """Verify single-use invitation token SHA-256 hash generation and 48-hour expiration calculation."""
    raw_token = str(uuid.uuid4())
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(hours=48)

    invitation = ClientInvitation(
        id=str(uuid.uuid4()),
        client_account_id=str(uuid.uuid4()),
        email="newuser@client.com",
        role="CLIENT_MEMBER",
        token_hash=token_hash,
        expires_at=expires_at,
        is_used=False,
    )

    assert invitation.token_hash == token_hash
    assert invitation.is_used is False
    assert (invitation.expires_at - created_at).total_seconds() == 48 * 3600
