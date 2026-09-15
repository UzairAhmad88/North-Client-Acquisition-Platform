import sys
from pathlib import Path

import pytest

root_dir = Path(__file__).resolve().parent.parent.parent.parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import uuid
from app.core.exceptions import NotFoundError
from app.models.base import Base
from app.models.business import Business
from app.models.lead import Lead
from app.models.service import Service
from app.models.user import User
from app.services.recommendations import RecommendationRepository, RecommendationService
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


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_recommendation_service_not_found_errors():
    db = TestingSessionLocal()
    rec_service = RecommendationService()

    fake_id = uuid.uuid4()

    with pytest.raises(NotFoundError):
        rec_service.build_context(db, fake_id)

    with pytest.raises(NotFoundError):
        rec_service.list_recommendations(db, fake_id)

    with pytest.raises(NotFoundError):
        rec_service.get_recommendation(db, fake_id)

    db.close()


def test_staleness_invalidation():
    db = TestingSessionLocal()
    biz = Business(name="Test Biz", normalized_name="test biz", status="ACTIVE")
    db.add(biz)
    db.commit()

    lead = Lead(business_id=biz.id, title="Test Lead", status="NEW")
    db.add(lead)
    db.commit()

    service = Service(name="Test Service", slug="test-service", status="ACTIVE", is_active=True)
    db.add(service)
    db.commit()

    rec_service = RecommendationService()
    recs = rec_service.calculate_lead_recommendations(db, lead.id)
    assert len(recs) == 1
    assert recs[0].status == "SUGGESTED"

    # Mark stale
    stale_count = RecommendationRepository.mark_lead_recommendations_stale(db, lead.id)
    assert stale_count == 1

    fetched = rec_service.get_recommendation(db, recs[0].id)
    assert fetched.status == "STALE"

    db.close()
