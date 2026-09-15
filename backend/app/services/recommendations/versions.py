"""Recommendation system versioning, score bands, and priority mapping."""

RECOMMENDATION_VERSION: str = "1.0"


def get_relevance_band(score: float) -> str:
    """Map numeric relevance score (0-100) to relevance band."""
    if score >= 80.0:
        return "STRONG"
    elif score >= 60.0:
        return "GOOD"
    elif score >= 40.0:
        return "POSSIBLE"
    else:
        return "WEAK"


def calculate_priority(relevance_score: float, confidence: str) -> str:
    """Calculate recommendation priority based on score and confidence."""
    confidence_upper = confidence.upper()

    if relevance_score >= 80.0:
        if confidence_upper in ("HIGH", "MEDIUM"):
            return "HIGH"
        else:
            return "MEDIUM"
    elif relevance_score >= 60.0:
        if confidence_upper in ("HIGH", "MEDIUM"):
            return "MEDIUM"
        else:
            return "LOW"
    else:
        return "LOW"
