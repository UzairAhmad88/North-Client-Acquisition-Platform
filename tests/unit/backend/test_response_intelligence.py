"""Unit test suite for Phase 21 — Response & Conversation Intelligence System."""

import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.base import Base
from app.models.business import Business
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.dnc import DoNotContact
from app.models.lead import Lead
from app.models.message import Message
from app.models.user import User
from app.services.response import ResponseService
from agents.response.agent import response_agent
from agents.response.buying_signals import BuyingSignalDetector
from agents.response.extraction import RequirementExtractor
from agents.response.intent import IntentClassifier
from agents.response.next_action import NextActionRecommender
from agents.response.objections import ObjectionClassifier
from integrations.inbound.models import InboundMessagePayload
from integrations.inbound.opt_out import DeterministicOptOutDetector
from integrations.inbound.security import WebhookSecurityGuard

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
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


def test_response_agent_permissions():
    """Verify ResponseAgent does NOT possess external send permissions."""
    perms = [p.value for p in response_agent.get_permissions()]
    assert "SEND_EMAIL" not in perms
    assert "SEND_MESSAGE" not in perms
    assert "SEND_WHATSAPP" not in perms
    assert "SEND_SMS" not in perms


def test_intent_classification():
    """Verify intent classifier pattern matching for price, meeting, and interested intents."""
    p1, intents1, _ = IntentClassifier.classify("How much would a new website cost?")
    assert p1 == "REQUEST_FOR_PRICE"

    p2, intents2, _ = IntentClassifier.classify("Can we schedule a call tomorrow at 10 AM?")
    assert p2 == "REQUEST_FOR_MEETING"

    p3, intents3, _ = IntentClassifier.classify("Yes, I am interested in your services.")
    assert p3 == "INTERESTED"


def test_buying_signals_and_objections():
    """Verify buying signal detection and objection classification."""
    signal = BuyingSignalDetector.detect("Can you send us a proposal and pricing options?")
    assert signal.level == "STRONG"

    obj = ObjectionClassifier.detect("Your service sounds great, but it is outside our budget.")
    assert obj is not None
    assert obj.type == "PRICE"


def test_requirement_extraction():
    """Verify explicit requirement extraction and missing info identification."""
    reqs, missing = RequirementExtractor.extract("We need a new website with online booking capability.")
    categories = [r.category for r in reqs]
    assert "WEBSITE" in categories
    assert "BOOKING" in categories
    assert "Budget Range" in missing


def test_deterministic_opt_out_and_dnc_trigger(db_session: Session):
    """Verify opt-out keyword triggers immediate DNC entry."""
    text = "Please stop sending me messages and unsubscribe my email."
    assert DeterministicOptOutDetector.is_opt_out_request(text) is True

    is_opt, reason = DeterministicOptOutDetector.process_opt_out_if_present(
        db_session, text=text, sender_email="optout@client.com"
    )
    assert is_opt is True

    dnc = db_session.query(DoNotContact).filter(DoNotContact.target_value == "optout@client.com").first()
    assert dnc is not None
    assert dnc.is_active is True


@pytest.mark.asyncio
async def test_full_inbound_response_processing(db_session: Session):
    """Verify end-to-end inbound message resolution, persistence, analysis, and draft generation."""
    biz = Business(name="Kappa Inc", normalized_name="kappa inc", email="contact@kappainc.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Kappa Lead", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    contact = Contact(business_id=biz.id, lead_id=lead.id, email="contact@kappainc.com", name="Kappa User")
    db_session.add(contact)
    db_session.commit()

    user = User(email="operator@norths.com", password_hash="hashed_pwd", full_name="Operator", is_active=True)
    db_session.add(user)
    db_session.commit()

    payload = InboundMessagePayload(
        provider="Mock",
        provider_event_id="evt-kappa-001",
        channel="EMAIL",
        sender_email="contact@kappainc.com",
        recipient_address="outreach@norths.com",
        subject="Re: Proposal",
        body="We are interested in your service. Can we schedule a meeting next week?",
    )

    msg, conv, analysis = await ResponseService.process_inbound_message(db_session, payload)

    assert msg.direction == "INBOUND"
    assert conv.lead_id == lead.id
    assert analysis is not None
    assert analysis.primary_intent == "REQUEST_FOR_MEETING"
    assert analysis.recommended_next_action == "SCHEDULE_MEETING"
    assert conv.current_intent == "REQUEST_FOR_MEETING"

    # Human Correction Recording
    updated_analysis = ResponseService.record_human_correction(
        db_session,
        conv.id,
        user.id,
        {"corrected_intent": "REQUEST_FOR_MEETING", "corrected_next_action": "SCHEDULE_MEETING", "reason": "Verified"},
    )
    assert updated_analysis.human_correction is not None
    assert updated_analysis.human_correction_by_id == user.id
