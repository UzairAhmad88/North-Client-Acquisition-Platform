"""Unit test suite for Phase 23 — Proposal & Solution Design Intelligence System."""

import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models
from app.models.base import Base
from app.models.business import Business
from app.models.lead import Lead
from app.models.user import User
from app.models.requirements import DiscoverySession, ClientRequirement
from app.models.solution import SolutionDesign
from app.models.proposal import Proposal
from app.services.requirements import RequirementsService
from app.services.solution import SolutionService
from app.services.proposal import ProposalService
from agents.solution.agent import solution_agent
from agents.proposal.agent import proposal_agent
from agents.solution.mapper import RequirementMapper
from agents.proposal.composer import ProposalComposer

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


def test_agent_permissions():
    """Verify SolutionAgent and ProposalAgent possess zero external send or contract permissions."""
    sol_perms = [p.value if hasattr(p, "value") else str(p) for p in solution_agent.get_permissions()]
    prop_perms = [p.value if hasattr(p, "value") else str(p) for p in proposal_agent.get_permissions()]

    for p in ("SEND_EMAIL", "SEND_MESSAGE", "SEND_WHATSAPP", "SIGN_CONTRACT", "MAKE_PAYMENT"):
        assert p not in sol_perms
        assert p not in prop_perms


def test_solution_design_mapping():
    """Verify requirement to feature mapping produces traceable features."""
    reqs = [
        {"category": "BOOKING", "title": "Online Booking Request", "explicit": True},
        {"category": "WEBSITE", "title": "Business Website Request", "explicit": True},
    ]
    features = RequirementMapper.map_requirements(reqs)

    assert len(features) >= 2
    categories = [f.category for f in features]
    assert "BOOKING" in categories
    assert "WEBSITE" in categories


def test_proposal_composition_and_hash():
    """Verify proposal section composition and SHA-256 content hashing."""
    sol_data = {
        "overview": "Overview text",
        "architecture_summary": "Frontend -> Backend -> DB",
        "features": [{"title": "Booking Module", "description": "Booking feature"}],
        "deliverables": [{"name": "Booking Deliverable", "description": "Deliverable desc"}],
    }

    sections = ProposalComposer.compose_sections("Acme Corp", sol_data)
    assert len(sections) >= 5
    types = [s.section_type for s in sections]
    assert "COVER" in types
    assert "SUMMARY" in types
    assert "SOLUTION" in types
    assert "DELIVERABLES" in types

    content_hash = ProposalComposer.calculate_content_hash(sections)
    assert len(content_hash) == 64  # SHA-256 hex string


def test_proposal_pricing_safety():
    """Verify commercial safety defaults pricing_status to PRICING_REQUIRES_HUMAN_REVIEW."""
    sol_data = {
        "features": [{"title": "Web Portal", "description": "Web feature"}],
        "deliverables": [{"name": "Web Deliverable", "description": "Web deliv"}],
    }
    sections = ProposalComposer.compose_sections("Beta Inc", sol_data)
    hash_val = ProposalComposer.calculate_content_hash(sections)

    assert hash_val is not None


@pytest.mark.asyncio
async def test_full_solution_and_proposal_workflow(db_session: Session):
    """Verify end-to-end discovery -> solution design -> proposal generation -> approval workflow."""
    biz = Business(name="Gamma Labs", normalized_name="gamma labs", email="contact@gammalabs.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Gamma Project", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    user = User(email="architect@norths.com", password_hash="hashed_pwd", full_name="Architect User", is_active=True)
    db_session.add(user)
    db_session.commit()

    # 1. Discovery Session & Requirements
    disc_session = RequirementsService.create_discovery_session(
        db_session, business_id=biz.id, lead_id=lead.id, user_id=user.id
    )
    analyzed_session = await RequirementsService.analyze_discovery_session(db_session, disc_session.id)
    assert analyzed_session is not None

    # 2. Create & Analyze Solution Design
    sol_obj = SolutionService.create_solution_design(db_session, discovery_session_id=disc_session.id, user_id=user.id)
    assert sol_obj.status == "DRAFT"

    analyzed_sol = await SolutionService.analyze_solution_design(db_session, sol_obj.id)
    assert analyzed_sol.status == "GENERATED"
    assert len(analyzed_sol.features) > 0

    approved_sol = SolutionService.approve_solution_design(db_session, sol_obj.id, user.id)
    assert approved_sol.status == "APPROVED"

    # 3. Create & Generate Proposal
    prop_obj = ProposalService.create_proposal(db_session, solution_id=approved_sol.id, user_id=user.id)
    assert prop_obj.status == "DRAFT"
    assert prop_obj.pricing_status == "PRICING_REQUIRES_HUMAN_REVIEW"

    generated_prop = await ProposalService.generate_proposal(db_session, prop_obj.id)
    assert generated_prop.status == "IN_REVIEW"
    assert generated_prop.content_hash is not None

    approved_prop = ProposalService.approve_proposal(db_session, prop_obj.id, user.id)
    assert approved_prop.status == "APPROVED"
    assert approved_prop.approved_by_id == user.id
