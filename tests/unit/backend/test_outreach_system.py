"""Comprehensive unit test suite for Phase 19 — Outreach System, CommunicationGuard, and Mock Provider."""

import sys
from pathlib import Path
import pytest

root_dir = Path(__file__).resolve().parent.parent.parent.parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.exceptions import AppError
from app.models.base import Base
from app.models.business import Business
from app.models.conversation import Conversation
from app.models.lead import Lead
from app.models.message import Message
from app.models.outreach import OutreachDraft
from app.models.outreach_event import OutreachEvent
from app.models.user import User
from app.repositories.outreach import OutreachDraftRepository
from app.services.outreach.approval import ApprovalEngine
from app.services.outreach.communication_guard import CommunicationGuard
from app.services.outreach.communication_service import CommunicationService
from app.services.outreach.dnc import DncService
from app.services.outreach.duplicate import DuplicateDetector
from app.services.outreach.frequency import FrequencyController
from app.services.outreach.idempotency import IdempotencyManager
from integrations.email.models import EmailMessagePayload
from integrations.email.providers.mock import MockEmailProvider


TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_approval_engine_hash_binding(db_session: Session):
    """Verify approval computes SHA-256 hash and binds APPROVED status."""
    biz = Business(name="Delta Corp", normalized_name="delta corp", email="contact@deltacorp.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Delta Lead", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    draft = OutreachDraftRepository.create_draft(
        db_session,
        {
            "lead_id": lead.id,
            "business_id": biz.id,
            "channel": "EMAIL",
            "subject": "Proposal for Delta",
            "body": "Hello Delta Corp team, here is our proposal.",
            "version": 1,
            "approval_status": "PENDING_APPROVAL",
        },
    )

    approved = ApprovalEngine.approve_draft(db_session, draft, user_id=None, recipient_email="contact@deltacorp.com")
    assert approved.approval_status == "APPROVED"
    assert approved.content_hash is not None

    is_valid, err = ApprovalEngine.verify_approval(approved, "contact@deltacorp.com")
    assert is_valid is True


def test_approval_invalidation_on_edit(db_session: Session):
    """Verify editing draft body invalidates approval and resets status to PENDING_APPROVAL."""
    biz = Business(name="Epsilon Inc", normalized_name="epsilon inc", email="contact@epsilon.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Epsilon Lead", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    draft = OutreachDraftRepository.create_draft(
        db_session,
        {
            "lead_id": lead.id,
            "business_id": biz.id,
            "channel": "EMAIL",
            "subject": "Original Subject",
            "body": "Original body text.",
            "version": 1,
            "approval_status": "APPROVED",
        },
    )
    ApprovalEngine.approve_draft(db_session, draft, user_id=None, recipient_email="contact@epsilon.com")

    # Edit body
    updated = OutreachDraftRepository.update_draft(
        db_session, draft, {"body": "Tampered body text requiring new approval."}
    )
    assert updated.version == 2
    assert updated.approval_status == "PENDING_APPROVAL"

    is_valid, err = ApprovalEngine.verify_approval(updated, "contact@epsilon.com")
    assert is_valid is False
    assert "PENDING_APPROVAL" in err


def test_communication_guard_dnc_race_condition(db_session: Session):
    """Verify DNC entry added after approval blocks send at send time."""
    biz = Business(name="Zeta Ltd", normalized_name="zeta ltd", email="contact@zetaltd.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Zeta Lead", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    user = User(email="operator@norths.com", password_hash="hashed_pwd", full_name="Test Operator", is_active=True)
    db_session.add(user)
    db_session.commit()

    draft = OutreachDraftRepository.create_draft(
        db_session,
        {
            "lead_id": lead.id,
            "business_id": biz.id,
            "channel": "EMAIL",
            "subject": "Hello Zeta",
            "body": "Zeta body.",
            "version": 1,
            "approval_status": "APPROVED",
        },
    )
    ApprovalEngine.approve_draft(db_session, draft, user_id=user.id, recipient_email="contact@zetaltd.com")

    # Add to DNC AFTER approval
    DncService.add_dnc_entry(db_session, scope="EMAIL", target_value="contact@zetaltd.com", reason="User opted out")

    is_valid, err_code, reason = CommunicationGuard.validate_send(db_session, draft, user.id)
    assert is_valid is False
    assert err_code == "DNC_BLOCKED"


def test_idempotency_lock_and_release():
    """Verify IdempotencyManager prevents concurrent sending on same idempotency key."""
    key = IdempotencyManager.get_idempotency_key(uuid.uuid4(), version=1)

    acquired1, err1 = IdempotencyManager.acquire_lock(key)
    assert acquired1 is True

    acquired2, err2 = IdempotencyManager.acquire_lock(key)
    assert acquired2 is False
    assert "lock conflict" in err2.lower()

    IdempotencyManager.release_lock(key)
    acquired3, err3 = IdempotencyManager.acquire_lock(key)
    assert acquired3 is True
    IdempotencyManager.release_lock(key)


@pytest.mark.asyncio
async def test_mock_email_provider_execution():
    """Verify MockEmailProvider handles success, bounce, and failure modes without network access."""
    provider_success = MockEmailProvider(mode="success")
    payload = EmailMessagePayload(recipient_email="test@example.com", subject="Test", body="Hello World")

    res_succ = await provider_success.send(payload)
    assert res_succ.status == "ACCEPTED"
    assert res_succ.provider_message_id.startswith("mock-msg-")

    provider_bounce = MockEmailProvider(mode="bounce")
    res_bounce = await provider_bounce.send(payload)
    assert res_bounce.status == "BOUNCED"

    provider_fail = MockEmailProvider(mode="failure")
    res_fail = await provider_fail.send(payload)
    assert res_fail.status == "FAILED"


@pytest.mark.asyncio
async def test_full_guarded_send_workflow(db_session: Session):
    """Verify end-to-end guarded send workflow: Draft -> Approve -> Send -> Event + Conversation + Message."""
    biz = Business(name="Eta Tech", normalized_name="eta tech", email="info@etatech.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Eta Lead", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    user = User(email="admin@norths.com", password_hash="hashed_pwd", full_name="Admin User", is_active=True)
    db_session.add(user)
    db_session.commit()

    # 1. Create Draft
    draft = OutreachDraftRepository.create_draft(
        db_session,
        {
            "lead_id": lead.id,
            "business_id": biz.id,
            "channel": "EMAIL",
            "subject": "Introductory Proposal for Eta Tech",
            "body": "Hi Eta Tech team, we would love to connect.",
            "version": 1,
            "approval_status": "PENDING_APPROVAL",
        },
    )

    # 2. Approve Draft
    ApprovalEngine.approve_draft(db_session, draft, user_id=user.id, recipient_email="info@etatech.com")

    # 3. Guarded Send
    sent_draft = await CommunicationService.send_outreach(db_session, draft.id, user_id=user.id)
    assert sent_draft.approval_status in ("ACCEPTED", "DELIVERED", "SENT")

    # 4. Verify Conversation & Message created
    conv = db_session.query(Conversation).filter(Conversation.lead_id == lead.id).first()
    assert conv is not None

    msg = db_session.query(Message).filter(Message.conversation_id == conv.id).first()
    assert msg is not None
    assert msg.subject == "Introductory Proposal for Eta Tech"
    assert msg.direction == "OUTBOUND"

    # 5. Verify Timeline Events logged
    events = db_session.query(OutreachEvent).filter(OutreachEvent.outreach_id == draft.id).all()
    assert len(events) >= 2
