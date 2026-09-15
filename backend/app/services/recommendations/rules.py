"""Calculators for the 6 recommendation score dimensions:
1. Business Fit (25%)
2. Problem / Gap Fit (30%)
3. Audit Evidence (20%)
4. Research Evidence (10%)
5. Service Category Fit (10%)
6. Existing Lead Context (5%)
"""

from typing import Any, List

from app.models.service import Service
from app.services.recommendations.components import (
    ComponentScoreResult,
    RecommendationContext,
    RecommendationSignal,
)
from app.services.recommendations.mappings import (
    AUDIT_FINDING_SERVICE_MAPPINGS,
    BUSINESS_TYPE_SERVICE_FIT,
    RESEARCH_SIGNAL_SERVICE_MAPPINGS,
)


def _match_keyword(service: Service, keyword: str) -> bool:
    """Check if service slug, name, subcategory, or features contain keyword."""
    kw = keyword.lower().replace("_", "")
    target = f"{service.slug} {service.name} {service.category} {service.subcategory or ''}".lower().replace("_", "").replace("-", "")
    if kw in target:
        return True
    if service.target_business_types:
        types_str = " ".join([str(t).lower() for t in service.target_business_types]).replace("_", "")
        if kw in types_str:
            return True
    return False


def calculate_business_fit(service: Service, context: RecommendationContext) -> ComponentScoreResult:
    """Evaluate Business Fit (25%) based on business category & target business types."""
    score = 40.0  # baseline fit score
    signals: List[RecommendationSignal] = []
    reasons: List[str] = []

    cat = (context.business.category or "").lower().strip()
    business_name = context.business.name or "Business"

    fit_dict = BUSINESS_TYPE_SERVICE_FIT.get(cat, BUSINESS_TYPE_SERVICE_FIT["general_business"])

    matched_weight = 0.0
    for keyword, weight in fit_dict.items():
        if _match_keyword(service, keyword):
            if weight > matched_weight:
                matched_weight = weight

    if matched_weight > 0:
        score = matched_weight
        sig = RecommendationSignal(
            signal=f"BUSINESS_CATEGORY_MATCH_{cat.upper()}",
            source="business",
            source_id=str(context.business.id),
            strength=score,
            confidence="HIGH",
            description=f"Service aligns with {cat.replace('_', ' ')} business operational needs.",
        )
        signals.append(sig)
        reasons.append(f"Service matches operational model for category '{cat.title() or 'General'}'.")
    else:
        # Check target business types in service model
        if service.target_business_types:
            for bt in service.target_business_types:
                if str(bt).lower() in cat or cat in str(bt).lower():
                    score = 80.0
                    signals.append(
                        RecommendationSignal(
                            signal="TARGET_BUSINESS_TYPE_MATCH",
                            source="service_catalog",
                            source_id=str(service.id),
                            strength=80.0,
                            confidence="MEDIUM",
                            description=f"Service targets '{bt}' businesses directly.",
                        )
                    )
                    reasons.append(f"Catalog explicitly targets {bt} business models.")
                    break

    weighted_contrib = (score * 0.25)
    return ComponentScoreResult(
        component_name="business_fit",
        weight=0.25,
        raw_score=score,
        weighted_contribution=weighted_contrib,
        signals=signals,
        reasons=reasons,
    )


def calculate_problem_gap_fit(service: Service, context: RecommendationContext) -> ComponentScoreResult:
    """Evaluate Problem / Gap Fit (30%) based on identified digital gaps."""
    score = 30.0  # baseline if no gaps detected
    signals: List[RecommendationSignal] = []
    reasons: List[str] = []

    # Check website existence gap
    has_no_website = False
    if context.audit:
        if context.audit.status in ("NO_WEBSITE", "UNAVAILABLE"):
            has_no_website = True

    if not context.business.website_url and not has_no_website:
        has_no_website = True

    if has_no_website:
        if _match_keyword(service, "website") or service.category in ("WEB_DEVELOPMENT", "LANDING_PAGE"):
            score = 95.0
            sig = RecommendationSignal(
                signal="NO_WEBSITE_OBSERVED",
                source="audit" if context.audit else "business",
                source_id=str(context.audit.id) if context.audit else str(context.business.id),
                strength=95.0,
                confidence="HIGH",
                description="No functional website was observed.",
            )
            signals.append(sig)
            reasons.append("No active web presence was detected for the business.")

    # Check lead score gaps if present
    if context.lead_score:
        if context.lead_score.website_need_score > 70.0 and (_match_keyword(service, "website") or service.category == "WEB_DEVELOPMENT"):
            score = max(score, context.lead_score.website_need_score)
            reasons.append(f"High website need score of {context.lead_score.website_need_score:.0f} detected.")
        if context.lead_score.lead_capture_score > 70.0 and (_match_keyword(service, "lead") or _match_keyword(service, "crm") or service.category == "CRM"):
            score = max(score, context.lead_score.lead_capture_score)
            reasons.append(f"Lead capture opportunity score of {context.lead_score.lead_capture_score:.0f} observed.")
        if context.lead_score.automation_potential_score > 70.0 and (service.category == "AUTOMATION" or _match_keyword(service, "automation")):
            score = max(score, context.lead_score.automation_potential_score)
            reasons.append(f"Process automation opportunity score of {context.lead_score.automation_potential_score:.0f} observed.")

    weighted_contrib = (score * 0.30)
    return ComponentScoreResult(
        component_name="problem_gap_fit",
        weight=0.30,
        raw_score=score,
        weighted_contribution=weighted_contrib,
        signals=signals,
        reasons=reasons,
    )


def calculate_audit_evidence_fit(service: Service, context: RecommendationContext) -> ComponentScoreResult:
    """Evaluate Audit Evidence (20%) using technical audit findings."""
    score = 20.0  # baseline
    signals: List[RecommendationSignal] = []
    reasons: List[str] = []

    if not context.findings:
        return ComponentScoreResult(
            component_name="audit_evidence",
            weight=0.20,
            raw_score=30.0,  # neutral default
            weighted_contribution=30.0 * 0.20,
            signals=[],
            reasons=["No audit findings available to increase or decrease audit score."],
        )

    matched_scores: List[float] = []
    for f in context.findings:
        flag = f.code
        if flag in AUDIT_FINDING_SERVICE_MAPPINGS:
            mapping = AUDIT_FINDING_SERVICE_MAPPINGS[flag]
            for kw, weight in mapping.items():
                if _match_keyword(service, kw):
                    matched_scores.append(weight)
                    sig = RecommendationSignal(
                        signal=f"AUDIT_FINDING_{flag}",
                        source="audit_finding",
                        source_id=str(f.id),
                        strength=weight,
                        confidence="HIGH",
                        description=str(f.title or f.description or flag),
                    )
                    signals.append(sig)
                    reasons.append(f"Audit finding '{f.title or flag}' indicates need for this service.")

    if matched_scores:
        score = min(100.0, max(matched_scores))

    weighted_contrib = (score * 0.20)
    return ComponentScoreResult(
        component_name="audit_evidence",
        weight=0.20,
        raw_score=score,
        weighted_contribution=weighted_contrib,
        signals=signals,
        reasons=reasons,
    )


def calculate_research_evidence_fit(service: Service, context: RecommendationContext) -> ComponentScoreResult:
    """Evaluate Research Evidence (10%) from research records."""
    score = 30.0  # baseline
    signals: List[RecommendationSignal] = []
    reasons: List[str] = []

    if not context.research_records:
        return ComponentScoreResult(
            component_name="research_evidence",
            weight=0.10,
            raw_score=30.0,
            weighted_contribution=30.0 * 0.10,
            signals=[],
            reasons=["No research records available."],
        )

    # Search in research record key values
    combined_text = ""
    for r in context.research_records:
        combined_text += f" {r.field_name} {r.normalized_value} {r.evidence_text or ''}"

    text_lower = combined_text.lower()

    for kw, mapping in RESEARCH_SIGNAL_SERVICE_MAPPINGS.items():
        clean_kw = kw.replace("_", " ")
        if clean_kw in text_lower:
            for s_kw, weight in mapping.items():
                if _match_keyword(service, s_kw):
                    score = max(score, weight)
                    sig = RecommendationSignal(
                        signal=f"RESEARCH_SIGNAL_{kw.upper()}",
                        source="research",
                        source_id=str(context.research_records[0].id),
                        strength=weight,
                        confidence="HIGH",
                        description=f"Public research indicated signal '{clean_kw}'.",
                    )
                    signals.append(sig)
                    reasons.append(f"Research signal '{clean_kw}' supports service requirement.")

    weighted_contrib = (score * 0.10)
    return ComponentScoreResult(
        component_name="research_evidence",
        weight=0.10,
        raw_score=score,
        weighted_contribution=weighted_contrib,
        signals=signals,
        reasons=reasons,
    )


def calculate_service_category_fit(service: Service, context: RecommendationContext) -> ComponentScoreResult:
    """Evaluate Service Category Fit (10%) using service catalog hierarchy."""
    score = 50.0  # baseline neutral category score
    signals: List[RecommendationSignal] = []
    reasons: List[str] = []

    cat = (context.business.category or "").lower()
    service_cat = (service.category or "").lower()

    if "web" in service_cat and ("restaurant" in cat or "gym" in cat or "hotel" in cat or "school" in cat or "retail" in cat):
        score = 85.0
        reasons.append("Web service category directly aligns with consumer-facing business model.")
    elif "automation" in service_cat or "ai" in service_cat:
        score = 75.0
        reasons.append("Automation/AI category fits operational efficiency goals.")
    elif "software" in service_cat or "management" in service.name.lower():
        score = 80.0
        reasons.append("Software system category fits business management structure.")

    weighted_contrib = (score * 0.10)
    return ComponentScoreResult(
        component_name="service_category_fit",
        weight=0.10,
        raw_score=score,
        weighted_contribution=weighted_contrib,
        signals=signals,
        reasons=reasons,
    )


def calculate_lead_context_fit(service: Service, context: RecommendationContext) -> ComponentScoreResult:
    """Evaluate Existing Lead Context (5%) from lead notes & lead services."""
    score = 40.0  # baseline
    signals: List[RecommendationSignal] = []
    reasons: List[str] = []

    # Check if existing LeadService relationship exists
    for ls in context.existing_lead_services:
        if ls.service_id == service.id:
            score = 90.0
            sig = RecommendationSignal(
                signal=f"LEAD_SERVICE_EXISTING_{ls.relationship_type}",
                source="lead_services",
                source_id=str(ls.id),
                strength=90.0,
                confidence="HIGH",
                description=f"Existing lead service association '{ls.relationship_type}'.",
            )
            signals.append(sig)
            reasons.append(f"Service was previously recorded in lead services as '{ls.relationship_type}'.")
            break

    # Check lead notes if present
    if context.lead.notes:
        notes_lower = context.lead.notes.lower()
        if service.name.lower() in notes_lower or service.slug.replace("-", " ") in notes_lower:
            score = max(score, 85.0)
            reasons.append("Lead notes explicitly reference this service or requirement.")

    weighted_contrib = (score * 0.05)
    return ComponentScoreResult(
        component_name="lead_context_fit",
        weight=0.05,
        raw_score=score,
        weighted_contribution=weighted_contrib,
        signals=signals,
        reasons=reasons,
    )
