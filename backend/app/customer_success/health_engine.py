"""Deterministic multi-factor client health scoring, trend analysis, and explanation engine."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple

from app.customer_success.base import (
    HealthBand,
    HealthFactorScore,
    HealthCalculationResult,
)

TWO_PLACES = Decimal("0.01")


def quantize_dec(val: Decimal | str | int | float) -> Decimal:
    """Quantize to 2 decimal places using HALF_UP rounding."""
    if not isinstance(val, Decimal):
        val = Decimal(str(val))
    return val.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


class HealthScoringEngine:
    """Deterministic, evidence-grounded health scoring and explainability engine."""

    DEFAULT_WEIGHTS = {
        "engagement": Decimal("0.15"),
        "project_health": Decimal("0.20"),
        "support_health": Decimal("0.10"),
        "financial_health": Decimal("0.15"),
        "satisfaction": Decimal("0.20"),
        "relationship": Decimal("0.10"),
        "goal_progress": Decimal("0.10"),
    }

    @classmethod
    def calculate_health_score(
        cls,
        client_id: str,
        factors_input: Dict[str, Optional[Decimal]],
        custom_weights: Optional[Dict[str, Decimal]] = None,
        historical_scores: Optional[List[Decimal]] = None,
        evidence_notes: Optional[Dict[str, str]] = None,
    ) -> HealthCalculationResult:
        """Calculates multi-factor health with missing data protection and explainability."""
        weights = custom_weights or cls.DEFAULT_WEIGHTS
        notes = evidence_notes or {}

        available_factors: List[HealthFactorScore] = []
        total_available_weight = Decimal("0.00")

        # Evaluate each factor
        for factor_key, weight in weights.items():
            val = factors_input.get(factor_key)
            if val is not None:
                score_dec = quantize_dec(val)
                score_dec = max(Decimal("0.00"), min(Decimal("100.00"), score_dec))
                total_available_weight += weight
                available_factors.append(
                    HealthFactorScore(
                        factor_name=factor_key,
                        weight=weight,
                        score=score_dec,
                        confidence="HIGH",
                        evidence_summary=notes.get(factor_key),
                    )
                )
            else:
                available_factors.append(
                    HealthFactorScore(
                        factor_name=factor_key,
                        weight=weight,
                        score=None,
                        confidence="UNKNOWN",
                        evidence_summary="No data available for this factor.",
                    )
                )

        # Insufficient data check (less than 2 active factors or zero weight)
        valid_factors = [f for f in available_factors if f.score is not None]
        if len(valid_factors) < 2 or total_available_weight == Decimal("0.00"):
            return HealthCalculationResult(
                client_id=client_id,
                overall_score=Decimal("0.00"),
                health_band=HealthBand.INSUFFICIENT_DATA,
                confidence="LOW",
                trend="UNKNOWN",
                factors=available_factors,
                positive_factors=[],
                risk_factors=["Insufficient historical or operational data to compute reliable health."],
                explanation="Client health could not be determined due to insufficient operational data.",
            )

        # Normalized weighted sum
        weighted_sum = Decimal("0.00")
        for f in valid_factors:
            normalized_weight = f.weight / total_available_weight
            weighted_sum += f.score * normalized_weight

        overall_score = quantize_dec(weighted_sum)

        # Band Assignment
        if overall_score >= Decimal("80.00"):
            band = HealthBand.HEALTHY
        elif overall_score >= Decimal("60.00"):
            band = HealthBand.STABLE
        elif overall_score >= Decimal("40.00"):
            band = HealthBand.WATCH
        elif overall_score >= Decimal("20.00"):
            band = HealthBand.AT_RISK
        else:
            band = HealthBand.CRITICAL

        # Confidence based on available factor coverage
        coverage_pct = (Decimal(len(valid_factors)) / Decimal(len(weights))) * Decimal("100.00")
        if coverage_pct >= Decimal("80.00"):
            confidence = "HIGH"
        elif coverage_pct >= Decimal("50.00"):
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        # Trend analysis
        trend = cls.evaluate_trend(overall_score, historical_scores or [])

        # Positives and Risks
        positives = []
        risks = []
        for f in valid_factors:
            name_display = f.factor_name.replace("_", " ").title()
            if f.score >= Decimal("75.00"):
                positives.append(f"{name_display} is strong ({f.score}/100)")
            elif f.score < Decimal("60.00"):
                risks.append(f"{name_display} requires attention ({f.score}/100)")

        # Explanation sentence
        explanation_parts = [
            f"Overall health is {band.value} with a score of {overall_score}/100 ({trend.lower()} trend, {confidence.lower()} confidence)."
        ]
        if positives:
            explanation_parts.append(f"Key strengths: {', '.join(positives[:2])}.")
        if risks:
            explanation_parts.append(f"Identified risks: {', '.join(risks[:2])}.")

        return HealthCalculationResult(
            client_id=client_id,
            overall_score=overall_score,
            health_band=band,
            confidence=confidence,
            trend=trend,
            factors=available_factors,
            positive_factors=positives,
            risk_factors=risks,
            explanation=" ".join(explanation_parts),
        )

    @staticmethod
    def evaluate_trend(current_score: Decimal, historical_scores: List[Decimal]) -> str:
        """Determines health velocity: IMPROVING, DECLINING, or STABLE."""
        if not historical_scores or len(historical_scores) < 2:
            return "STABLE"

        recent = historical_scores[-3:] + [current_score]
        diffs = [recent[i] - recent[i - 1] for i in range(1, len(recent))]

        if all(d < Decimal("-2.00") for d in diffs):
            return "DECLINING"
        elif all(d > Decimal("2.00") for d in diffs):
            return "IMPROVING"
        return "STABLE"
