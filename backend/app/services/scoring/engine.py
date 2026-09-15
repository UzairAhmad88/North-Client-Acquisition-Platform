from typing import Any, Dict

from app.services.scoring.explanations import ExplanationGenerator
from app.services.scoring.models import ComponentScoreResult, LeadScoreResult, ScoringContext
from app.services.scoring.rules import ComponentRules
from app.services.scoring.versions import (
    CURRENT_SCORE_VERSION,
    WEIGHT_CONFIG_V1,
    get_band_for_score,
)


class ScoringEngine:
    @staticmethod
    def calculate_opportunity_score(ctx: ScoringContext) -> LeadScoreResult:
        weights = WEIGHT_CONFIG_V1

        c_website = ComponentRules.calculate_website_need(ctx, weights["website_need"])
        c_presence = ComponentRules.calculate_online_presence(ctx, weights["online_presence"])
        c_capture = ComponentRules.calculate_lead_capture(ctx, weights["lead_capture"])
        c_automation = ComponentRules.calculate_automation_potential(ctx, weights["automation_potential"])
        c_activity = ComponentRules.calculate_business_activity(ctx, weights["business_activity"])
        c_contactability = ComponentRules.calculate_contactability(ctx, weights["contactability"])
        c_service = ComponentRules.calculate_service_fit(ctx, weights["service_fit"])

        component_scores: Dict[str, ComponentScoreResult] = {
            "website_need": c_website,
            "online_presence": c_presence,
            "lead_capture": c_capture,
            "automation_potential": c_automation,
            "business_activity": c_activity,
            "contactability": c_contactability,
            "service_fit": c_service,
        }

        total_score = sum(c.weighted_contribution for c in component_scores.values())
        band = get_band_for_score(total_score)

        # Confidence calculation based on evidence availability
        evidence_sources_count = 0
        if ctx.business:
            evidence_sources_count += 1
        if ctx.audit and ctx.audit.status == "AVAILABLE":
            evidence_sources_count += 2
        if ctx.research_records and len(ctx.research_records) > 0:
            evidence_sources_count += 1

        if evidence_sources_count >= 3:
            confidence = "HIGH"
        elif evidence_sources_count >= 2:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        # Evidence references gathering
        evidence_dict: Dict[str, Any] = {
            "business_id": str(ctx.business.id),
            "has_website": bool(ctx.business.website_url or ctx.business.normalized_website),
            "audit_id": str(ctx.audit.id) if ctx.audit else None,
            "research_records_count": len(ctx.research_records),
            "components": {k: v.evidence for k, v in component_scores.items()},
        }

        explanation = ExplanationGenerator.generate_explanation(total_score, band, component_scores)

        return LeadScoreResult(
            score_version=CURRENT_SCORE_VERSION,
            total_score=total_score,
            band=band,
            component_scores=component_scores,
            explanation=explanation,
            evidence=evidence_dict,
            confidence=confidence,
        )
