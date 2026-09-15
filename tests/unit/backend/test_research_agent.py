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
from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import validate_agent_permissions
from agents.core.registry import global_registry
from agents.research.agent import ResearchAgent
from agents.research.confidence import ResearchConfidenceCalculator
from agents.research.evidence import ResearchEvidenceCollector
from agents.research.planner import ResearchPlanner
from agents.research.tools import FetchWebTool, SearchWebTool
from integrations.web.security import SecurityValidationError, validate_url_security
from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.base import Base
from app.models.business import Business
from app.models.user import User
from app.services.research import ResearchService
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
        email="researcher@norths.agency",
        password_hash=hash_password("Password123!"),
        full_name="Norths Researcher",
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
def sample_business():
    db = TestingSessionLocal()
    biz = Business(
        name="Starlight Fitness & Wellness",
        normalized_name="starlight fitness & wellness",
        category="gym",
        city="Austin",
        status="ACTIVE",
        website_url="https://starlightfitness.test",
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)
    db.close()
    return biz


# 1. Research Agent Metadata & Registry Registration
def test_research_agent_registration():
    agent = global_registry.get("research_agent")
    assert agent.name == "research_agent"
    assert agent.version == "1.0"
    assert "READ_BUSINESS" in agent.permissions
    assert "SEARCH_WEB" in agent.permissions
    assert "SEND_EMAIL" not in agent.permissions


# 2. Research Planning & Data Reuse
def test_research_planner_data_reuse():
    requested = ["identity", "services"]
    existing = [{"field_name": "identity"}, {"field_name": "services"}]
    plan = ResearchPlanner.plan_research(requested, existing, max_age_days=30)

    assert plan["existing_fields_count"] == 2
    assert len(plan["target_fields"]) == 0
    assert plan["should_search_web"] is False


# 3. Source Trust & Evidence Collector
def test_evidence_collector_trust_hierarchy():
    trust_official = ResearchEvidenceCollector.classify_source_trust(
        "https://starlightfitness.test/about", "https://starlightfitness.test"
    )
    assert trust_official == "OFFICIAL"

    trust_google = ResearchEvidenceCollector.classify_source_trust(
        "https://google.com/search?q=gym", "https://starlightfitness.test"
    )
    assert trust_google == "HIGH_TRUST"


# 4. Confidence Calculator Logic
def test_confidence_calculator():
    high_conf = ResearchConfidenceCalculator.calculate_finding_confidence(
        source_trust="OFFICIAL", is_fresh=True, has_conflict=False
    )
    assert high_conf == "HIGH"

    conflict_conf = ResearchConfidenceCalculator.calculate_finding_confidence(
        source_trust="OFFICIAL", is_fresh=True, has_conflict=True
    )
    assert conflict_conf == "LOW"


# 5. Prompt Injection Defense Test Fixture
@pytest.mark.asyncio
async def test_prompt_injection_defense():
    tool = FetchWebTool()
    ctx = AgentContext(workflow_id="wf-inj", task_id="t-inj", agent_run_id="r-inj")

    # Untrusted external fetch content using a realResolvable URL
    res = await tool.execute(
        {"url": "https://example.com"}, ctx, agent_permissions={"FETCH_WEB"}
    )
    assert "<UNTRUSTED_EXTERNAL_DATA>" in res["content"]


# 6. SSRF Security Guard Test
def test_ssrf_security_guard():
    with pytest.raises(SecurityValidationError) as exc_local:
        validate_url_security("http://127.0.0.1/admin")
    assert "SSRF" in str(exc_local.value) or "blocked" in str(exc_local.value).lower() or "private" in str(exc_local.value).lower()

    with pytest.raises(SecurityValidationError) as exc_meta:
        validate_url_security("http://169.254.169.254/latest/meta-data")
    assert "SSRF" in str(exc_meta.value) or "blocked" in str(exc_meta.value).lower() or "private" in str(exc_meta.value).lower()


# 7. Prohibited Communication Permission Failure
def test_prohibited_communication_permission_failure():
    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"READ_BUSINESS", "SEND_EMAIL"})


# 8. Full Research Agent Execution Workflow
@pytest.mark.asyncio
async def test_research_agent_execution(sample_business):
    biz = sample_business
    agent = ResearchAgent()

    ctx = AgentContext(
        workflow_id="wf-test-run",
        task_id="t-test-run",
        agent_run_id="r-test-run",
        business_id=biz.id,
        business_profile={
            "id": str(biz.id),
            "name": biz.name,
            "category": biz.category,
            "website_url": biz.website_url,
        },
    )

    result = await agent.run(ctx)
    assert result.status in ("COMPLETED", "PARTIAL")
    assert result.confidence in ("HIGH", "MEDIUM", "LOW")
    assert "business_summary" in result.result
    assert len(result.result["findings"]) > 0


# 9. REST API Endpoint Integration Test
def test_research_agent_api(auth_headers, sample_business):
    client = TestClient(app)
    biz = sample_business

    db = TestingSessionLocal()
    job = ResearchService.create_job(db, business_id=biz.id, sections=["identity"])
    db.close()

    # Unauthenticated
    unauth = client.post(f"/api/v1/research/jobs/{job.id}/run-agent")
    assert unauth.status_code == 401

    # Run agent via API
    run_resp = client.post(
        f"/api/v1/research/jobs/{job.id}/run-agent",
        headers=auth_headers,
    )
    assert run_resp.status_code == 200
    assert run_resp.json()["data"]["id"] == str(job.id)
