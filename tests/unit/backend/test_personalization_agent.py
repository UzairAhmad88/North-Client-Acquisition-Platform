"""Unit tests for Phase 18 — Personalization Agent, claim validation, risk classification, and draft persistence."""

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

from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import validate_agent_permissions
from agents.core.registry import global_registry
from agents.personalization.agent import PersonalizationAgent
from agents.personalization.angles import AngleSelector
from agents.personalization.draft import DraftGenerator
from agents.personalization.planner import PersonalizationPlanner
from agents.personalization.profile import PersonalizationProfileGenerator
from agents.personalization.schemas import OutreachDraftPayload, VerifiedSignal
from agents.personalization.validation import ClaimValidator
from app.models.base import Base
from app.models.business import Business
from app.models.lead import Lead
from app.models.outreach import OutreachDraft
from app.repositories.outreach import OutreachDraftRepository
from app.services.outreach import OutreachDraftService


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


def test_personalization_agent_registration():
    """Verify PersonalizationAgent is registered in AgentRegistry with required permissions."""
    agent = global_registry.get("personalization_agent")
    assert agent is not None
    assert agent.name == "personalization_agent"
    assert "READ_QUALIFICATION" in agent.permissions
    assert "CREATE_OUTREACH_DRAFT" in agent.permissions


def test_prohibited_communication_permissions():
    """Verify prohibited communication permissions raise AgentPermissionDeniedError."""
    prohibited_set = {"READ_BUSINESS", "SEND_EMAIL", "SEND_WHATSAPP"}
    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions(prohibited_set)


def test_qualification_gate_not_qualified():
    """Verify NOT_QUALIFIED status prevents sendable outreach generation."""
    is_eligible, readiness, reason = PersonalizationPlanner.evaluate_eligibility(
        qualification_data={"decision": "NOT_QUALIFIED"},
        is_dnc=False,
    )
    assert is_eligible is False
    assert readiness == "NOT_RECOMMENDED"


def test_dnc_guardrail():
    """Verify DNC status enforces OUTREACH_BLOCKED readiness."""
    is_eligible, readiness, reason = PersonalizationPlanner.evaluate_eligibility(
        qualification_data={"decision": "QUALIFIED"},
        is_dnc=True,
    )
    assert is_eligible is False
    assert readiness == "OUTREACH_BLOCKED"


def test_signal_extraction_and_angle_selection():
    """Verify signal extraction and angle selection logic."""
    signals = PersonalizationProfileGenerator.extract_signals(
        business_profile={"name": "Alpha Gym", "website_url": "https://alphagym.com", "phone": "555-0199"},
        research_data={"records": [{"fact_summary": "Personal training offered"}]},
        audit_data={"findings": [{"code": "NO_ONLINE_BOOKING", "description": "Lacks online booking", "severity": "HIGH"}]},
        score_data={"score": 85, "band": "HIGH"},
        recommendations_data=[{"service_title": "Booking System", "relevance_band": "STRONG"}],
        qualification_data={"decision": "QUALIFIED"},
    )
    assert len(signals) >= 3

    needs = PersonalizationProfileGenerator.map_business_needs(signals)
    primary_angle, supporting = AngleSelector.select_angles(signals, needs)
    assert primary_angle is not None
    assert primary_angle.angle_type in ("BOOKING", "WEBSITE_IMPROVEMENT", "LEAD_CAPTURE", "DIGITAL_PRESENCE")


def test_prohibited_claim_detection():
    """Verify prohibited claims (guarantees, false urgency) flag risk as HIGH/BLOCKED."""
    draft = OutreachDraftPayload(
        channel="EMAIL",
        subject="Guaranteed 50% increase in customers!",
        body="We guarantee your competitors are taking your customers if you do not act today.",
        outreach_readiness="READY",
    )
    claims, risk_level, warnings = ClaimValidator.validate_claims_and_risk(
        draft=draft,
        verified_evidence_count=1,
    )
    assert risk_level in ("HIGH", "BLOCKED")
    assert len(warnings) > 0


def test_draft_versioning_and_approval_reset(db_session: Session):
    """Verify updating draft body increments version and resets approval to PENDING_APPROVAL."""
    biz = Business(name="Beta Corp", normalized_name="beta corp", legal_name="Beta Corp", country="US")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Beta Lead", business_id=biz.id, qualification_status="QUALIFIED")
    db_session.add(lead)
    db_session.commit()

    draft = OutreachDraftRepository.create_draft(
        db_session,
        {
            "lead_id": lead.id,
            "business_id": biz.id,
            "channel": "EMAIL",
            "subject": "Initial Subject",
            "body": "Initial Body content.",
            "version": 1,
            "approval_status": "APPROVED",
        },
    )
    assert draft.version == 1
    assert draft.approval_status == "APPROVED"

    updated = OutreachDraftRepository.update_draft(
        db_session, draft, {"body": "Modified Body content requiring re-approval."}
    )
    assert updated.version == 2
    assert updated.approval_status == "PENDING_APPROVAL"


@pytest.mark.asyncio
async def test_personalization_agent_execution(db_session: Session):
    """Verify full PersonalizationAgent execution workflow."""
    biz = Business(name="Gamma Fitness", normalized_name="gamma fitness", website_url="https://gammafit.com", phone="555 border")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Gamma Lead", business_id=biz.id, qualification_status="QUALIFIED")
    db_session.add(lead)
    db_session.commit()

    draft = await OutreachDraftService.run_personalization(
        db=db_session,
        lead_id=lead.id,
        channel="EMAIL",
        tone="PROFESSIONAL",
    )
    assert draft is not None
    assert draft.lead_id == lead.id
    assert draft.approval_status == "PENDING_APPROVAL"
    assert draft.version == 1
    assert draft.body != ""
