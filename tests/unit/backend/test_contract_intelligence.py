"""Unit test suite for Phase 25 — Contract, Scope Commitment & Client Approval Workflow."""

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
from app.services.requirements import RequirementsService
from app.services.solution import SolutionService
from app.services.estimate import EstimateService
from app.services.proposal import ProposalService
from app.services.contract import ContractService
from agents.contracts.agent import contract_agent
from agents.contracts.generator import ContractGenerator
from agents.contracts.validator import ContractValidator
from agents.contracts.discrepancies import DiscrepancyDetector
from agents.contracts.models import ContractSectionSchema
from integrations.signature.service import SignatureService
from integrations.signature.models import SignatureRequest

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


def test_contract_agent_permissions():
    """Verify ContractAgent holds zero send, approval, acceptance, or signature permissions."""
    perms = [p.value if hasattr(p, "value") else str(p) for p in contract_agent.get_permissions()]

    for p in ("SEND_EMAIL", "SEND_MESSAGE", "SEND_WHATSAPP", "APPROVE_CONTRACT", "ACCEPT_CONTRACT", "SIGN_CONTRACT", "SEND_CONTRACT", "EXECUTE_CONTRACT"):
        assert p not in perms


def test_contract_generator_and_hash():
    """Verify controlled contract section generation and content hash calculation."""
    sections = ContractGenerator.generate_sections(
        contract_number="CTR-2026-TEST",
        business_name="Epsilon Corp",
        proposal_data={"summary": "Epsilon proposal summary"},
        estimate_data={"recommended_min": 1000.0, "recommended_max": 1500.0},
        solution_data={"features": [{"title": "CRM Module", "description": "CRM feature"}]},
    )
    assert len(sections) >= 7
    types = [s.section_type for s in sections]
    assert "PARTIES" in types
    assert "SCOPE" in types
    assert "COMMERCIAL" in types

    content_hash = ContractGenerator.calculate_content_hash(sections)
    assert len(content_hash) == 64  # SHA-256 hex string


def test_contract_completeness_validator():
    """Verify completeness scoring evaluates mandatory sections."""
    sections = [
        ContractSectionSchema(title="Parties", section_type="PARTIES", content="Parties text"),
        ContractSectionSchema(title="Scope", section_type="SCOPE", content="Scope text"),
        ContractSectionSchema(title="Signatures", section_type="SIGNATURES", content="Sig text"),
    ]
    res = ContractValidator.evaluate_completeness(sections)
    assert res.completeness_score < 100.0
    assert len(res.missing_sections) > 0


def test_discrepancy_detector():
    """Verify discrepancy detector flags missing features or price mismatches."""
    sections = ContractGenerator.generate_sections(
        contract_number="CTR-DISC",
        business_name="Zeta Inc",
        proposal_data={"summary": "Zeta proposal"},
        estimate_data={"recommended_min": 5000.0},
        solution_data={"features": [{"title": "Web Application"}, {"title": "Mobile App"}]},
    )

    discrepancies = DiscrepancyDetector.detect_discrepancies(
        sections, proposal_data={}, estimate_data={"recommended_min": 9999.0}, solution_data={"features": [{"title": "Web Application"}, {"title": "Mobile App"}, {"title": "AI Bot"}]}
    )
    assert len(discrepancies) > 0


@pytest.mark.asyncio
async def test_mock_signature_provider():
    """Verify MockSignatureProvider workflow."""
    req = SignatureRequest(
        contract_id="test-contract-id",
        signer_email="client@test.com",
        signer_name="Client Signer",
        document_title="Test Agreement",
        content_hash="hash-123",
    )
    init_res = await SignatureService.request_signature(req)
    assert init_res.status == "PENDING"

    done_res = await SignatureService.complete_signature(init_res.provider_request_id)
    assert done_res.status == "SIGNED"


@pytest.mark.asyncio
async def test_full_contract_commitment_workflow(db_session: Session):
    """Verify end-to-end requirement -> solution -> estimate -> proposal -> contract -> explicit acceptance -> signature -> baseline locking workflow."""
    biz = Business(name="Epsilon Enterprises", normalized_name="epsilon enterprises", email="contact@epsilon.com")
    db_session.add(biz)
    db_session.commit()

    lead = Lead(title="Epsilon Project", business_id=biz.id)
    db_session.add(lead)
    db_session.commit()

    user = User(email="legal@norths.com", password_hash="hashed_pwd", full_name="Legal Operator", is_active=True)
    db_session.add(user)
    db_session.commit()

    # 1. Discovery, Solution & Estimate
    disc_session = RequirementsService.create_discovery_session(db_session, business_id=biz.id, lead_id=lead.id, user_id=user.id)
    await RequirementsService.analyze_discovery_session(db_session, disc_session.id)

    sol_obj = SolutionService.create_solution_design(db_session, discovery_session_id=disc_session.id, user_id=user.id)
    await SolutionService.analyze_solution_design(db_session, sol_obj.id)
    SolutionService.approve_solution_design(db_session, sol_obj.id, user.id)

    est_obj = EstimateService.create_estimate(db_session, solution_id=sol_obj.id, user_id=user.id)
    await EstimateService.calculate_estimate(db_session, est_obj.id)
    EstimateService.approve_estimate(db_session, est_obj.id, user.id)

    # 2. Proposal
    prop_obj = ProposalService.create_proposal(db_session, solution_id=sol_obj.id, user_id=user.id)
    await ProposalService.generate_proposal(db_session, prop_obj.id)
    ProposalService.approve_proposal(db_session, prop_obj.id, user.id)

    # 3. Create & Generate Contract
    contract_obj = ContractService.create_contract(db_session, proposal_id=prop_obj.id, estimate_id=est_obj.id, user_id=user.id)
    assert contract_obj.status == "DRAFT"

    generated_contract = await ContractService.generate_contract(db_session, contract_obj.id)
    assert generated_contract.status == "IN_REVIEW"
    assert len(generated_contract.sections) > 0

    # 4. Operator Internal Approval
    approved_contract = ContractService.approve_contract_internally(db_session, contract_obj.id, user.id)
    assert approved_contract.status == "READY_FOR_CLIENT"

    # 5. Client Explicit Acceptance
    accepted_contract = ContractService.client_accept_contract(
        db_session, contract_id=contract_obj.id, client_email="contact@epsilon.com", acceptance_statement="I explicitly accept all contract terms."
    )
    assert accepted_contract.status == "CLIENT_APPROVED"

    # 6. Execute Mock Signature
    signed_contract = await ContractService.complete_contract_signature(db_session, contract_obj.id)
    assert signed_contract.status == "SIGNED"

    # 7. Lock Committed Project Baseline
    baseline = ContractService.lock_contract_baseline(db_session, contract_obj.id)
    assert baseline.is_locked is True
    assert signed_contract.status == "ACTIVE"
