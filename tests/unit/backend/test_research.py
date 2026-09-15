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
from app.services.research import ResearchService
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from integrations.web.parser import WebParser
from integrations.web.security import SecurityValidationError, validate_url_security
from integrations.web.validator import URLValidator

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
        full_name="Uzair Researcher",
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
        name="Apex Digital Solutions",
        normalized_name="apex digital solutions",
        industry="Technology",
        city="Austin",
        status="ACTIVE",
        website_url="https://apexdigital.test",
        normalized_website="apexdigital.test",
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)
    db.close()
    return biz


# 1. SSRF & Security Tests
def test_ssrf_security_blocks_private_and_loopback_ips():
    with pytest.raises(SecurityValidationError):
        validate_url_security("http://127.0.0.1/admin")

    with pytest.raises(SecurityValidationError):
        validate_url_security("http://169.254.169.254/latest/meta-data")

    with pytest.raises(SecurityValidationError):
        validate_url_security("http://localhost:8000")

    with pytest.raises(SecurityValidationError):
        validate_url_security("file:///etc/passwd")

    with pytest.raises(SecurityValidationError):
        validate_url_security("ftp://example.com/file")


def test_url_validator_accepts_safe_url():
    url = "https://example.com/about"
    assert URLValidator.is_safe_url(url) is True
    assert URLValidator.sanitize_and_validate(url) == "https://example.com/about"


# 2. Web Parser Tests
def test_web_parser_extracts_facts_cleanly():
    sample_html = """
    <html>
      <head>
        <title>Apex Digital Solutions - Leading Software & AI Agency</title>
        <meta name="description" content="Custom software development and AI automation systems in Austin.">
      </head>
      <body>
        <h1>Apex Digital Solutions</h1>
        <p>Contact us at contact@apexdigital.test or call +1-512-555-0199.</p>
        <a href="https://linkedin.com/company/apex-digital">LinkedIn Profile</a>
      </body>
    </html>
    """
    facts = WebParser.extract_facts(sample_html)
    assert facts.title == "Apex Digital Solutions - Leading Software & AI Agency"
    assert facts.meta_description == "Custom software development and AI automation systems in Austin."
    assert "contact@apexdigital.test" in facts.emails
    assert len(facts.phones) > 0
    assert facts.social_links.get("linkedin") == "https://linkedin.com/company/apex-digital"


# 3. Research Service & Workflow Tests
@pytest.mark.asyncio
async def test_mock_research_job_execution(sample_business):
    db = TestingSessionLocal()
    job = ResearchService.create_job(db, sample_business.id, sections=["ALL"])
    assert job.status == "PENDING"

    completed_job = await ResearchService.run_job(db, job.id, provider_type="MOCK")
    assert completed_job.status == "COMPLETED"
    assert completed_job.records_validated > 0

    profile = ResearchService.get_business_research_profile(db, sample_business.id)
    assert profile.total_records > 0
    assert profile.confidence_score > 0
    db.close()


# 4. REST API Endpoint Tests
def test_research_api_endpoints(auth_headers, sample_business):
    client = TestClient(app)

    # Require auth check
    unauth_resp = client.get(f"/api/v1/research/businesses/{sample_business.id}")
    assert unauth_resp.status_code == 401

    # Create job via API
    create_resp = client.post(
        "/api/v1/research/jobs",
        json={"business_id": str(sample_business.id), "sections": ["IDENTITY", "CONTACT"]},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    job_id = create_resp.json()["data"]["id"]

    # Run job via API
    run_resp = client.post(
        f"/api/v1/research/jobs/{job_id}/run?provider_type=MOCK",
        headers=auth_headers,
    )
    assert run_resp.status_code == 200
    assert run_resp.json()["data"]["status"] == "COMPLETED"

    # Get Business Research Profile via API
    profile_resp = client.get(
        f"/api/v1/research/businesses/{sample_business.id}",
        headers=auth_headers,
    )
    assert profile_resp.status_code == 200
    assert profile_resp.json()["data"]["total_records"] > 0
