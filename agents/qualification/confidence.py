"""Qualification Confidence Calculator evaluating factor certainty and data quality."""

from typing import List
from agents.qualification.schemas import QualificationFactorItem


class QualificationConfidenceCalculator:
    """Calculates overall qualification confidence rating."""

    @staticmethod
    def calculate_overall_confidence(
        factors: List[QualificationFactorItem],
        data_quality_score: float = 100.0,
    ) -> str:
        if data_quality_score < 40:
            return "LOW"

        if not factors:
            return "MEDIUM"

        low_count = sum(1 for f in factors if f.confidence == "LOW")
        if low_count >= len(factors) / 2:
            return "LOW"

        medium_count = sum(1 for f in factors if f.confidence == "MEDIUM")
        if (low_count + medium_count) >= len(factors) / 2 or data_quality_score < 70:
            return "MEDIUM"

        return "HIGH"
