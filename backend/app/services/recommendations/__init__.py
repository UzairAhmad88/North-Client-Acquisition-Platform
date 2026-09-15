"""Recommendation Engine Package."""

from app.services.recommendations.components import (
    CandidateRecommendation,
    ComponentScoreResult,
    RecommendationContext,
    RecommendationSignal,
)
from app.services.recommendations.engine import RecommendationEngine
from app.services.recommendations.repository import RecommendationRepository
from app.services.recommendations.service import RecommendationService
from app.services.recommendations.versions import RECOMMENDATION_VERSION

__all__ = [
    "RECOMMENDATION_VERSION",
    "RecommendationSignal",
    "ComponentScoreResult",
    "CandidateRecommendation",
    "RecommendationContext",
    "RecommendationEngine",
    "RecommendationRepository",
    "RecommendationService",
]
