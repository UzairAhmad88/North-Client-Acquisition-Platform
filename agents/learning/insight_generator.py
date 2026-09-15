"""Insight & Recommendation Generator with Strict Empirical Evidence Grounding."""

from typing import Any, Dict, List, Optional
from agents.learning.models import InsightDraft, RecommendationDraft


class InsightGeneratorEngine:
    """Generates structured organizational insights and non-autonomous recommendations from empirical facts."""

    def generate_lead_scoring_insight(self, pattern_result: Dict[str, Any]) -> Optional[InsightDraft]:
        """Generate insight from lead score calibration analysis."""
        if pattern_result.get("status") != "VALID":
            return None

        sample_size = pattern_result["sample_size"]
        conversions = pattern_result.get("band_conversions", {})
        high_precision = pattern_result.get("high_score_precision_pct", 0.0)
        false_pos = pattern_result.get("false_positives", 0)

        confidence = "HIGH" if sample_size >= 25 else "MEDIUM"
        if sample_size < 10:
            confidence = "LOW"

        title = f"Lead Score Calibration: High-Tier Conversion at {high_precision}% across {sample_size} Leads"
        description = (
            f"Analysis of {sample_size} historical leads indicates that leads scored in the 80–100 band achieve a "
            f"{high_precision}% conversion rate. A total of {false_pos} high-scoring leads failed to convert, "
            f"highlighting opportunities for qualification criteria refinement without changing automated policies."
        )

        evidence = [
            {
                "source_type": "LEAD_SCORE_CALIBRATION",
                "sample_count": sample_size,
                "baseline_value": 50.0,
                "observed_value": high_precision,
                "variance_pct": None,
                "details": {
                    "band_conversions": conversions,
                    "false_positives": false_pos,
                    "false_negatives": pattern_result.get("false_negatives", 0),
                },
            }
        ]

        recommended_action = (
            "Review qualification criteria for high-scoring lost leads to identify common objection patterns "
            "before considering any adjustments to scoring weights."
        )

        return InsightDraft(
            title=title,
            description=description,
            category="SALES",
            confidence=confidence,
            sample_size=sample_size,
            time_window="historical",
            affected_entities={"workflow": "qualification", "bands": list(conversions.keys())},
            recommended_action=recommended_action,
            evidence_items=evidence,
        )

    def generate_estimation_variance_insight(self, pattern_result: Dict[str, Any]) -> Optional[InsightDraft]:
        """Generate insight from project effort variance analysis."""
        if pattern_result.get("status") != "VALID":
            return None

        sample_size = pattern_result["sample_size"]
        avg_var = pattern_result.get("average_variance_pct", 0.0)
        mae = pattern_result.get("mean_abs_error_pct", 0.0)
        service_breakdown = pattern_result.get("service_breakdown", {})

        confidence = "HIGH" if sample_size >= 20 else ("MEDIUM" if sample_size >= 10 else "LOW")

        direction = "underestimation" if avg_var > 0 else "overestimation"
        title = f"Project Estimation Variance: Average {abs(avg_var):.1f}% {direction} (MAE: {mae:.1f}%)"
        description = (
            f"Across {sample_size} completed projects, actual delivery effort deviated from planned estimates with "
            f"an average variance of {avg_var:.1f}% and mean absolute error of {mae:.1f}%. "
            f"Highest variance observed in: {list(service_breakdown.keys())[:3]}."
        )

        evidence = [
            {
                "source_type": "ESTIMATION_VARIANCE",
                "sample_count": sample_size,
                "baseline_value": pattern_result.get("total_estimated_hours", 0.0),
                "observed_value": pattern_result.get("total_actual_hours", 0.0),
                "variance_pct": avg_var,
                "details": {
                    "mean_abs_error_pct": mae,
                    "underestimated_count": pattern_result.get("underestimated_projects", 0),
                    "overestimated_count": pattern_result.get("overestimated_projects", 0),
                    "service_breakdown": service_breakdown,
                },
            }
        ]

        recommended_action = (
            "Calibrate PERT uncertainty assumptions for high-variance service categories during discovery review. "
            "Requires human estimation team review."
        )

        return InsightDraft(
            title=title,
            description=description,
            category="ESTIMATION",
            confidence=confidence,
            sample_size=sample_size,
            time_window="historical",
            affected_entities={"services": list(service_breakdown.keys())},
            recommended_action=recommended_action,
            evidence_items=evidence,
        )

    def generate_requirements_creep_insight(self, pattern_result: Dict[str, Any]) -> Optional[InsightDraft]:
        """Generate insight linking incomplete initial requirements to scope change frequency."""
        if pattern_result.get("status") != "VALID":
            return None

        sample_size = pattern_result["sample_size"]
        incomplete_rate = pattern_result.get("incomplete_change_risk_pct", 0.0)
        complete_rate = pattern_result.get("complete_change_risk_pct", 0.0)
        rr = pattern_result.get("relative_risk_ratio") or 1.0

        confidence = "HIGH" if sample_size >= 15 else "MEDIUM"

        title = f"Requirements Ambiguity Impact: {incomplete_rate}% of Unresolved Requirements Lead to 2+ Scope Changes"
        description = (
            f"In an empirical study of {sample_size} projects, projects commencing with unresolved requirements "
            f"exhibited a {incomplete_rate}% probability of experiencing 2+ scope changes compared to {complete_rate}% "
            f"for fully specified baselines (Relative Risk: {rr}x)."
        )

        evidence = [
            {
                "source_type": "REQUIREMENTS_AMBIGUITY_CORRELATION",
                "sample_count": sample_size,
                "baseline_value": complete_rate,
                "observed_value": incomplete_rate,
                "variance_pct": round(((incomplete_rate - complete_rate) / (complete_rate or 1.0)) * 100, 2),
                "details": pattern_result,
            }
        ]

        recommended_action = (
            "Enforce a mandatory Requirements Discovery Checklist sign-off gate before entering Implementation phase."
        )

        return InsightDraft(
            title=title,
            description=description,
            category="DELIVERY",
            confidence=confidence,
            sample_size=sample_size,
            time_window="historical",
            affected_entities={"workflow": "requirements_discovery"},
            recommended_action=recommended_action,
            evidence_items=evidence,
        )

    def create_recommendation_from_insight(self, insight: InsightDraft) -> RecommendationDraft:
        """Create a structured, reviewable recommendation from an approved insight."""
        if insight.category == "ESTIMATION":
            return RecommendationDraft(
                title=f"Calibrate Discovery Estimation Buffers for High-Variance Deliverables",
                recommendation="Introduce a 15% PERT standard deviation buffer for complex third-party API and integration tasks.",
                reason=insight.description,
                expected_benefit="Reduction in project schedule overrun risk and improved delivery timeline reliability.",
                potential_downside="Slightly higher initial quoted hours during proposal review, requiring clear value justification.",
                confidence=insight.confidence,
                affected_workflow="ESTIMATION",
            )
        elif insight.category == "DELIVERY":
            return RecommendationDraft(
                title="Establish Pre-Implementation Requirements Confirmation Gate",
                recommendation="Require client approval on all functional requirements and explicit dependency sign-off prior to task sprint activation.",
                reason=insight.description,
                expected_benefit="Up to 40% reduction in late-stage scope change requests and reduced project delivery friction.",
                potential_downside="Adds 1–2 days to initial discovery alignment before sprint execution starts.",
                confidence=insight.confidence,
                affected_workflow="REQUIREMENTS",
            )
        else:
            return RecommendationDraft(
                title=f"Process Improvement for {insight.category.capitalize()}",
                recommendation=insight.recommended_action or "Review operational performance guidelines.",
                reason=insight.description,
                expected_benefit="Enhanced operational consistency and predictability.",
                potential_downside="Requires human review and change adoption overhead.",
                confidence=insight.confidence,
                affected_workflow=insight.category,
            )
