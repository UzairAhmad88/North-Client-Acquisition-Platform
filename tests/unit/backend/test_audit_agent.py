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
from datetime import datetime, timedelta, timezone

from agents.audit.agent import AuditAgent
from agents.audit.confidence import AuditConfidenceCalculator
from agents.audit.findings import AuditFindingCollector
from agents.audit.planner import AuditPlanner
from agents.audit.tools import FetchAuditPageTool
from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import validate_agent_permissions
from agents.core.registry import global_registry
from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.base import Base
from app.models.business import Business
from app.models.user import User
from app.services.audit import AuditService
from fastapi.testclient import TestClient
from integrations.web.security import SecurityValidationError, validate_url_security
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
        email="auditor@norths.agency",
        password_hash=hash_password("Password123!"),
        full_name="Norths Auditor",
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
        name="Starlight Fitness",
        normalized_name="starlight fitness",
        category="gym",
        city="Austin",
        status="ACTIVE",
        website_url="https://starlightfitness.test",
        phone="+15125550199",
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)
    db.close()
    return biz


# 1. Audit Agent Metadata & Registry Registration
def test_audit_agent_registration():
    agent = global_registry.get("audit_agent")
    assert agent.name == "audit_agent"
    assert agent.version == "1.0"
    assert "READ_AUDIT" in agent.permissions
    assert "RUN_AUDIT" in agent.permissions
    assert "SEND_EMAIL" not in agent.permissions


# 2. Audit Target Selection Hierarchy
def test_audit_planner_target_selection():
    # Official website preferred
    biz_prof = {"website_url": "https://official.com"}
    res_data = {"records": [{"field_name": "website", "source_url": "https://researched.com"}]}
    target, src = AuditPlanner.select_target_url(biz_prof, res_data)
    assert target == "https://official.com"
    assert src == "OFFICIAL_WEBSITE"

    # Researched website fallback
    target_res, src_res = AuditPlanner.select_target_url({}, res_data)
    assert target_res == "https://researched.com"
    assert src_res == "RESEARCHED_WEBSITE"

    # No website scenario
    target_none, src_none = AuditPlanner.select_target_url({}, {})
    assert target_none is None
    assert src_none == "NO_WEBSITE"


# 3. Existing Audit Freshness Reuse (<= 7 days)
def test_audit_planner_freshness_reuse():
    now = datetime.now(timezone.utc)
    fresh_audit = {"completed_at": (now - timedelta(days=3)).isoformat(), "overall_health": "HEALTHY"}
    assert AuditPlanner.check_audit_freshness(fresh_audit, max_age_days=7) is True

    stale_audit = {"completed_at": (now - timedelta(days=10)).isoformat(), "overall_health": "HEALTHY"}
    assert AuditPlanner.check_audit_freshness(stale_audit, max_age_days=7) is False


# 4. Finding Collector Severity Assignment
def test_finding_collector_severity():
    f_https = AuditFindingCollector.create_finding(
        code="NO_HTTPS",
        category="security",
        title="No HTTPS Available",
        description="Website plain HTTP without TLS.",
        evidence_url="http://example.com",
    )
    assert f_https.severity == "HIGH"

    f_meta = AuditFindingCollector.create_finding(
        code="MISSING_META_DESC",
        category="seo",
        title="Missing Meta Description",
        description="Page lacks meta description.",
        evidence_url="https://example.com",
    )
    assert f_meta.severity == "LOW"


# 5. SSRF Security Guard Test
def test_ssrf_security_guard():
    with pytest.raises(SecurityValidationError) as exc_local:
        validate_url_security("http://127.0.0.1/admin")
    assert "SSRF" in str(exc_local.value) or "blocked" in str(exc_local.value).lower() or "private" in str(exc_local.value).lower()

    with pytest.raises(SecurityValidationError) as exc_meta:
        validate_url_security("http://169.254.169.254/latest/meta-data")
    assert "SSRF" in str(exc_meta.value) or "blocked" in str(exc_meta.value).lower() or "private" in str(exc_meta.value).lower()


# 6. Prompt Injection Defense Test Fixture
@pytest.mark.asyncio
async def test_prompt_injection_defense():
    tool = FetchAuditPageTool(db=None)
    ctx = AgentContext(workflow_id="wf-inj", task_id="t-inj", agent_run_id="r-inj")

    res = await tool.execute(
        {"url": "https://example.com"}, ctx, agent_permissions={"FETCH_WEB"}
    )
    assert "<UNTRUSTED_EXTERNAL_DATA>" in res["content"]


# 7. Prohibited Communication Permission Failure
def test_prohibited_communication_permission_failure():
    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"READ_AUDIT", "SEND_EMAIL"})


# 8. Full Audit Agent Execution Workflow
@pytest.mark.asyncio
async def test_audit_agent_execution(sample_business):
    biz = sample_business
    agent = AuditAgent()

    ctx = AgentContext(
        workflow_id="wf-audit-run",
        task_id="t-audit-run",
        agent_run_id="r-audit-run",
        business_id=biz.id,
        business_profile={
            "id": str(biz.id),
            "name": biz.name,
            "category": biz.category,
            "website_url": biz.website_url,
            "phone": biz.phone,
        },
    )

    result = await agent.run(ctx)
    assert result.status in ("COMPLETED", "PARTIAL")
    assert result.confidence in ("HIGH", "MEDIUM", "LOW")
    assert "overall_health" in result.result
    assert "findings" in result.result


# 9. REST API Endpoint Integration Test
def test_audit_agent_api(auth_headers, sample_business):
    client = TestClient(app)
    biz = sample_business

    db = TestingSessionLocal()
    job = AuditService.create_job(db, business_id=biz.id)
    db.close()

    # Unauthenticated
    unauth = client.post(f"/api/v1/audits/jobs/{job.id}/run-agent")
    assert unauth.status_code == 401

    # Run agent via API
    run_resp = client.post(
        f"/api/v1/audits/jobs/{job.id}/run-agent",
        headers=auth_headers,
    )
    assert run_resp.status_code == 200
    assert run_resp.json()["data"]["id"] == str(job.id)
