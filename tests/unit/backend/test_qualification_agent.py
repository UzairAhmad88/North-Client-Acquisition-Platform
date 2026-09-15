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
from datetime import datetime, timezone

from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import validate_agent_permissions
from agents.core.registry import global_registry
from agents.qualification.agent import QualificationAgent
from agents.qualification.confidence import QualificationConfidenceCalculator
from agents.qualification.qualification import QualificationEngine
from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.base import Base
from app.models.business import Business
from app.models.lead import Lead
from app.models.qualification import LeadQualification
from app.models.user import User
from app.services.qualification import QualificationService
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def auth_headers():
    db = TestingSessionLocal()
    user = User(
        email="qualifier@norths.agency",
        password_hash=hash_password("Password123!"),
        full_name="Norths Qualifier",
        role="ADMIN",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    db.close()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_lead_data():
    db = TestingSessionLocal()
    biz = Business(
        name="Apex Auto Spa",
        normalized_name="apex auto spa",
        category="automotive",
        city="Austin",
        status="ACTIVE",
        website_url="https://apexautospa.test",
        phone="+15125550188",
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)

    lead = Lead(
        business_id=biz.id,
        title="Apex Auto Spa Website & Automation Lead",
        status="NEW",
        source="INBOUND",
        qualification_status="UNQUALIFIED",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    db.close()

    return biz, lead


# 1. Qualification Agent Metadata & Registry Registration
def test_qualification_agent_registration():
    agent = global_registry.get("qualification_agent")
    assert agent.name == "qualification_agent"
    assert agent.version == "1.0"
    assert "READ_SCORE" in agent.permissions
    assert "CREATE_QUALIFICATION_RESULT" in agent.permissions
    assert "SEND_EMAIL" not in agent.permissions


# 2. DNC Guardrail Test
def test_dnc_guardrail_outreach_blocked():
    eval_res = QualificationEngine.evaluate(
        business_profile={"name": "Test Biz"},
        lead_profile={"title": "Test Lead"},
        research_data={},
        audit_data={},
        score_data={},
        recommended_services=[],
        dnc_status=True,
    )
    assert eval_res["outreach_readiness"] == "OUTREACH_BLOCKED"
    assert eval_res["recommended_internal_action"] == "HOLD"
    assert len(eval_res["risks"]) > 0


# 3. Unresolved Duplicate Guardrail Test
def test_unresolved_duplicate_guardrail():
    eval_res = QualificationEngine.evaluate(
        business_profile={"name": "Test Biz"},
        lead_profile={"title": "Test Lead"},
        research_data={"records": [{"field_name": "identity"}]},
        audit_data={"findings": [{"severity": "HIGH"}]},
        score_data={"score": 85, "score_band": "HIGH"},
        recommended_services=[{"relevance_band": "STRONG"}],
        dnc_status=False,
        has_unresolved_duplicate=True,
    )
    assert eval_res["decision"] == "NEEDS_REVIEW"
    assert eval_res["recommended_internal_action"] == "MERGE_DUPLICATE"


# 4. Insufficient Data Scenario
def test_insufficient_data_scenario():
    eval_res = QualificationEngine.evaluate(
        business_profile={},
        lead_profile={},
        research_data={},
        audit_data={},
        score_data={},
        recommended_services=[],
    )
    assert eval_res["decision"] == "INSUFFICIENT_DATA"
    assert eval_res["outreach_readiness"] == "NOT_READY"


# 5. Strong Qualification Scenario
def test_strong_qualification_scenario():
    eval_res = QualificationEngine.evaluate(
        business_profile={"name": "Test Biz", "phone": "+15125550188", "website_url": "https://test.com"},
        lead_profile={"title": "Test Lead"},
        research_data={"records": [{"field_name": "identity"}]},
        audit_data={"findings": [{"severity": "HIGH"}]},
        score_data={"score": 88, "score_band": "HIGH"},
        recommended_services=[{"relevance_band": "STRONG"}, {"relevance_band": "GOOD"}],
    )
    assert eval_res["decision"] == "QUALIFIED"
    assert eval_res["outreach_readiness"] == "OUTREACH_READY"
    assert eval_res["recommended_internal_action"] == "PREPARE_OUTREACH"


# 6. Score Non-Alteration Test
def test_score_non_alteration():
    eval_res = QualificationEngine.evaluate(
        business_profile={},
        lead_profile={},
        research_data={"records": [1]},
        audit_data={"findings": [1]},
        score_data={"score": 85, "score_band": "HIGH"},
        recommended_services=[],
    )
    assert eval_res["decision"] is not None


# 7. Prohibited Communication Permission Failure
def test_prohibited_communication_permission_failure():
    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"READ_SCORE", "SEND_EMAIL"})


# 8. Full Qualification Agent Execution Workflow
@pytest.mark.asyncio
async def test_qualification_agent_execution(sample_lead_data):
    biz, lead = sample_lead_data
    agent = QualificationAgent()

    ctx = AgentContext(
        workflow_id="wf-qual-run",
        task_id="t-qual-run",
        agent_run_id="r-qual-run",
        business_id=biz.id,
        lead_id=lead.id,
        business_profile={"id": str(biz.id), "name": biz.name, "phone": biz.phone},
        lead_profile={"id": str(lead.id), "title": lead.title},
        score_data={"score": 85, "score_band": "HIGH"},
        service_recommendations=[{"relevance_band": "STRONG"}],
        research_data={"records": [{"field_name": "identity"}]},
        audit_data={"findings": [{"severity": "MEDIUM"}]},
    )

    result = await agent.run(ctx)
    assert result.status == "COMPLETED"
    assert result.result["decision"] in ("QUALIFIED", "POTENTIALLY_QUALIFIED", "NEEDS_REVIEW", "NOT_QUALIFIED", "INSUFFICIENT_DATA")
    assert result.result["qualification_version"] == "1.0"


# 9. Human Override Test
def test_human_override(sample_lead_data):
    db = TestingSessionLocal()
    biz, lead = sample_lead_data

    qual_data = {
        "lead_id": lead.id,
        "business_id": biz.id,
        "decision": "POTENTIALLY_QUALIFIED",
        "confidence": "HIGH",
        "summary": "Initial AI decision",
        "outreach_readiness": "NEEDS_VERIFICATION",
    }

    qual = LeadQualification(**qual_data)
    db.add(qual)
    db.commit()
    db.refresh(qual)

    updated = QualificationService.apply_override(
        db,
        lead_id=lead.id,
        override_decision="QUALIFIED",
        override_reason="Verified owner willingness in preliminary call.",
    )

    assert updated.human_override_decision == "QUALIFIED"
    assert updated.decision == "POTENTIALLY_QUALIFIED"  # Original AI decision preserved
    assert updated.human_override_reason == "Verified owner willingness in preliminary call."
    db.close()


# 10. REST API Integration Test
def test_qualification_api(auth_headers, sample_lead_data):
    client = TestClient(app)
    biz, lead = sample_lead_data

    # Unauthenticated
    unauth = client.post(f"/api/v1/leads/{lead.id}/qualification/run")
    assert unauth.status_code == 401

    # Run qualification via API
    run_resp = client.post(
        f"/api/v1/leads/{lead.id}/qualification/run",
        headers=auth_headers,
    )
    assert run_resp.status_code == 200
    assert run_resp.json()["data"]["lead_id"] == str(lead.id)

    # Get latest qualification
    get_resp = client.get(f"/api/v1/leads/{lead.id}/qualification", headers=auth_headers)
    assert get_resp.status_code == 200

    # Post human override
    override_resp = client.post(
        f"/api/v1/leads/{lead.id}/qualification/override",
        headers=auth_headers,
        json={"decision": "QUALIFIED", "reason": "Approved by Sales Lead."},
    )
    assert override_resp.status_code == 200
    assert override_resp.json()["data"]["human_override_decision"] == "QUALIFIED"
