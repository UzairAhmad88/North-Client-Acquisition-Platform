from app.services.scoring import ScoringService


def test_scoring_service_available():
    assert hasattr(ScoringService, "calculate_lead_score")
