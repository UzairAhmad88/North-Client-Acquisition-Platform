"""Core Recommendation Engine evaluating candidate services for a Lead."""

from typing import List

from app.models.service import Service
from app.services.recommendations.components import (
    CandidateRecommendation,
    RecommendationContext,
)
from app.services.recommendations.explanations import ExplanationGenerator
from app.services.recommendations.rules import (
    calculate_audit_evidence_fit,
    calculate_business_fit,
    calculate_lead_context_fit,
    calculate_problem_gap_fit,
    calculate_research_evidence_fit,
    calculate_service_category_fit,
)
from app.services.recommendations.versions import (
    RECOMMENDATION_VERSION,
    calculate_priority,
    get_relevance_band,
)


class RecommendationEngine:
    """Deterministic recommendation engine for North's Service Catalog."""

    def calculate_recommendations(
        self, context: RecommendationContext
    ) -> List[CandidateRecommendation]:
        """Evaluate all available active services against the context and return candidate recommendations."""
        candidates: List[CandidateRecommendation] = []

        for service in context.available_services:
            if not service.is_active:
                continue

            # Calculate 6 components
            comp_business = calculate_business_fit(service, context)
            comp_gap = calculate_problem_gap_fit(service, context)
            comp_audit = calculate_audit_evidence_fit(service, context)
            comp_research = calculate_research_evidence_fit(service, context)
            comp_category = calculate_service_category_fit(service, context)
            comp_lead = calculate_lead_context_fit(service, context)

            component_scores = {
                "business_fit": comp_business,
                "problem_gap_fit": comp_gap,
                "audit_evidence": comp_audit,
                "research_evidence": comp_research,
                "service_category_fit": comp_category,
                "lead_context_fit": comp_lead,
            }

            # Formula:
            # Business Fit (25%) + Problem/Gap (30%) + Audit (20%) + Research (10%) + Category (10%) + Lead Context (5%)
            total_relevance_score = round(
                sum(c.weighted_contribution for c in component_scores.values()), 2
            )

            # Cap total relevance score between 0.0 and 100.0
            total_relevance_score = max(0.0, min(100.0, total_relevance_score))

            band = get_relevance_band(total_relevance_score)

            reasons, evidence, limitations, confidence = (
                ExplanationGenerator.generate_explanations_evidence_limitations(
                    component_scores, context
                )
            )

            priority = calculate_priority(total_relevance_score, confidence)

            candidate = CandidateRecommendation(
                service_id=service.id,
                service_name=service.name,
                service_slug=service.slug,
                category=service.category,
                recommendation_version=RECOMMENDATION_VERSION,
                relevance_score=total_relevance_score,
                band=band,
                priority=priority,
                confidence=confidence,
                reasons=reasons,
                evidence=evidence,
                limitations=limitations,
                component_scores=component_scores,
            )

            candidates.append(candidate)

        # Sort candidates descending by relevance score
        candidates.sort(key=lambda c: c.relevance_score, reverse=True)
        return candidates
