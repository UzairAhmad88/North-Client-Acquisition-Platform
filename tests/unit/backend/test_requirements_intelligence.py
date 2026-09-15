"""Unit test suite for Phase 22 — Client Requirements & Discovery Intelligence System."""

import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.base import Base
from app.models.business import Business
from app.models.lead import Lead
from app.models.user import User
from app.models.requirements import DiscoverySession, ClientRequirement
from app.services.requirements import RequirementsService
from agents.requirements.agent import requirements_agent
from agents.requirements.contradictions import ContradictionDetector
from agents.requirements.extractor import RequirementExtractor
from agents.requirements.questions import DiscoveryQuestionGenerator
from agents.requirements.readiness import ReadinessEvaluator
from agents.requirements.scope import ScopeManager, ScopeItemSchema

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


def test_requirements_agent_permissions():
    """Verify RequirementsAgent does NOT possess external send or contract permissions."""
    perms = [p.value if hasattr(p, "value") else str(p) for p in requirements_agent.get_permissions()]
    assert "SEND_EMAIL" not in perms
    assert "SEND_MESSAGE" not in perms
    assert "SEND_WHATSAPP" not in perms
    assert "SIGN_CONTRACT" not in perms
    assert "CREATE_PAYMENT" not in perms


def test_explicit_vs_inferred_requirements():
    """Verify explicit client requests vs inferred requirements distinction."""
    text = "I need online appointment booking for our website."
    reqs, goal, problem, users = RequirementExtractor.extract(text, "msg-001")
    
    categories = [r.category for r in reqs]
    assert "BOOKING" in categories
    assert "AUTHENTICATION" in categories

    booking_req = next(r for r in reqs if r.category == "BOOKING")
    assert booking_req.explicit is True
    assert booking_req.source_type == "CLIENT_MESSAGE"

    auth_req = next(r for r in reqs if r.category == "AUTHENTICATION")
    assert auth_req.explicit is False
    assert auth_req.source_type == "AI_INFERENCE"
    assert auth_req.status == "PROPOSED"


def test_contradiction_detection():
    """Verify contradiction engine flags conflicting requirements."""
    text = "Only staff should manage bookings, but customers can book appointments online directly."
    reqs, _, _, _ = RequirementExtractor.extract(text, "msg-002")
    contradictions = ContradictionDetector.detect(text, reqs)
    
    assert len(contradictions) > 0
    assert "Staff-only booking restriction" in contradictions[0].requirement_a


def test_discovery_questions_generator():
    """Verify prioritized discovery question generation."""
    text = "We want a website with online booking and payment processing."
    reqs, _, _, _ = RequirementExtractor.extract(text, "msg-003")
    questions = DiscoveryQuestionGenerator.generate(reqs, text)

    assert len(questions) > 0
    categories = [q.category for q in questions]
    assert "WORKFLOW" in categories or "INTEGRATION" in categories or "BUDGET" in categories


def test_scope_expansion_detection():
    """Verify scope expansion detector when unexpected high-complexity requirements appear."""
    reqs, _, _, _ = RequirementExtractor.extract("We need a custom mobile app and CRM system.", "msg-004")
    existing_scope = [ScopeItemSchema(description="Business Website", scope_status="IN_SCOPE")]
    
    scope_items, expansion_detected = ScopeManager.process_scope(reqs, existing_scope)
    assert expansion_detected is True


def test_readiness_evaluation():
    """Verify readiness stage, completeness score, and complexity calculation."""
    text = "We want a business website with online booking and payment gateway."
    reqs, _, _, _ = RequirementExtractor.extract(text, "msg-005")
    scope_items, _ = ScopeManager.process_scope(reqs)

    evaluation = ReadinessEvaluator.evaluate(reqs, scope_items, questions_count=2, message_body=text)
    assert evaluation.completeness_score > 0.0
    assert evaluation.scope_complexity in ("MEDIUM", "HIGH")


@pytest.mark.asyncio
async def test_full_discovery_session_workflow(db_session: Session):
    """Verify end-to-end discovery session creation, analysis, confirmation, and question answering."""
    biz = Business(name="Lambda Corp", normalized_name="lambda corp", email="contact@lambdacorp.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Lambda Opportunity", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    user = User(email="architect@norths.com", password_hash="hashed_pwd", full_name="Architect User", is_active=True)
    db_session.add(user)
    db_session.commit()

    # 1. Create Discovery Session
    session_obj = RequirementsService.create_discovery_session(
        db_session, business_id=biz.id, lead_id=lead.id, user_id=user.id, notes="Initial intake session"
    )
    assert session_obj.status == "OPEN"
    assert session_obj.version == 1

    # 2. Analyze Discovery Session
    analyzed_session = await RequirementsService.analyze_discovery_session(db_session, session_obj.id)
    assert analyzed_session.status == "IN_PROGRESS"
    assert len(analyzed_session.requirements) > 0

    # 3. Confirm Requirement (Human Operator Action)
    target_req = analyzed_session.requirements[0]
    confirmed_req = RequirementsService.confirm_requirement(db_session, target_req.id, user.id)
    assert confirmed_req.status == "CONFIRMED"
    assert confirmed_req.confirmed_by_id == user.id

    # 4. Answer Discovery Question
    if analyzed_session.questions:
        target_q = analyzed_session.questions[0]
        answered_q = RequirementsService.answer_question(db_session, target_q.id, "Stripe Payment Gateway")
        assert answered_q.status == "ANSWERED"
        assert answered_q.answer_text == "Stripe Payment Gateway"
