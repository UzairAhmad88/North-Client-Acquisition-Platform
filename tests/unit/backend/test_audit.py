import sys
from pathlib import Path

import pytest

root_dir = Path(__file__).resolve().parent.parent.parent.parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.base import Base
from app.models.business import Business
from app.models.user import User
from app.services.audit import AuditService
from app.services.audit.analyzers import AuditAnalyzers
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from integrations.web.audit_parser import AuditParser
from integrations.web.security import SecurityValidationError, validate_url_security

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
        name="Lumina Tech Agency",
        normalized_name="lumina tech agency",
        industry="Technology",
        city="San Francisco",
        status="ACTIVE",
        website_url="https://luminatech.test",
        normalized_website="luminatech.test",
        phone="+1-415-555-0188",
        email="info@luminatech.test",
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)
    db.close()
    return biz


# 1. Target Validation & SSRF Security Tests
def test_audit_ssrf_security_boundary():
    with pytest.raises(SecurityValidationError):
        validate_url_security("http://127.0.0.1/internal")

    with pytest.raises(SecurityValidationError):
        validate_url_security("http://169.254.169.254/latest/meta-data")

    with pytest.raises(SecurityValidationError):
        validate_url_security("http://localhost:3000")

    with pytest.raises(SecurityValidationError):
        validate_url_security("file:///etc/passwd")


# 2. HTML Audit Parser Tests
def test_audit_parser_extracts_page_features():
    html_sample = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lumina Tech Agency - Web & AI Solutions</title>
        <meta name="description" content="Leading web performance and digital presence engineering.">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="canonical" href="https://luminatech.test">
    </head>
    <body>
        <h1>Lumina Tech Agency</h1>
        <p>Contact our team for a free consultation or estimate.</p>
        <form action="/contact" method="post">
            <input type="text" name="name">
            <input type="email" name="email">
            <button type="submit">Contact Us</button>
        </form>
        <a href="/about">About Us</a>
        <a href="/services">Services</a>
        <a href="https://facebook.com/luminatech">Facebook</a>
        <a href="https://linkedin.com/company/luminatech">LinkedIn</a>
        <img src="/logo.png" alt="Lumina Tech Logo">
        <img src="/banner.png">
    </body>
    </html>
    """
    parsed = AuditParser.parse_page("https://luminatech.test", html_sample)

    assert parsed.title == "Lumina Tech Agency - Web & AI Solutions"
    assert parsed.meta_description == "Leading web performance and digital presence engineering."
    assert parsed.viewport == "width=device-width, initial-scale=1.0"
    assert parsed.contact_forms_count == 1
    assert parsed.image_count == 2
    assert parsed.images_missing_alt == 1
    assert "https://facebook.com/luminatech" in parsed.social_links.values()
    assert "https://linkedin.com/company/luminatech" in parsed.social_links.values()
    assert len(parsed.internal_links) >= 2


# 3. Category Analyzers & Health Calculation
def test_audit_analyzers_produce_structured_findings():
    html_sample = """
    <html>
    <head><title>Test Title</title></head>
    <body><p>Short snippet</p></body>
    </html>
    """
    parsed = AuditParser.parse_page("http://example.test", html_sample)
    findings = AuditAnalyzers.analyze_all(
        homepage_data=parsed,
        all_pages=[parsed],
        headers_dict={},
        is_https=False,
        redirect_to_https=False,
        response_time_ms=120,
    )

    finding_codes = [f.code for f in findings]
    assert "MISSING_HTTPS" in finding_codes
    assert "MISSING_CONTACT_FORM" in finding_codes
    assert "MISSING_META_DESCRIPTION" in finding_codes


# 4. Service & Workflow Tests
@pytest.mark.asyncio
async def test_audit_service_workflow(sample_business):
    db = TestingSessionLocal()
    job = AuditService.create_job(db, sample_business.id)
    assert job.status == "PENDING"

    completed_job = await AuditService.run_job(db, job.id, runner_type="MOCK")
    assert completed_job.status == "COMPLETED"
    assert completed_job.findings_count > 0

    latest_audit = AuditService.get_runner("MOCK")
    assert latest_audit is not None
    db.close()


# 5. REST API Endpoint Tests
def test_audit_api_endpoints(auth_headers, sample_business):
    client = TestClient(app)

    # Require auth
    unauth_resp = client.get(f"/api/v1/audits/businesses/{sample_business.id}")
    assert unauth_resp.status_code == 401

    # Create job via API
    create_resp = client.post(
        "/api/v1/audits/jobs",
        json={"business_id": str(sample_business.id)},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    job_id = create_resp.json()["data"]["id"]

    # Run job via API
    run_resp = client.post(
        f"/api/v1/audits/jobs/{job_id}/run?runner_type=MOCK",
        headers=auth_headers,
    )
    assert run_resp.status_code == 200
    assert run_resp.json()["data"]["status"] == "COMPLETED"

    # Get latest business audit via API
    audit_resp = client.get(
        f"/api/v1/audits/businesses/{sample_business.id}",
        headers=auth_headers,
    )
    assert audit_resp.status_code == 200
    assert audit_resp.json()["data"]["overall_health"] in ("HEALTHY", "FAIR", "NEEDS_ATTENTION", "LIMITED_DATA")

    # Get business audit history via API
    hist_resp = client.get(
        f"/api/v1/audits/businesses/{sample_business.id}/history",
        headers=auth_headers,
    )
    assert hist_resp.status_code == 200
    assert hist_resp.json()["data"]["total_audits"] == 1
