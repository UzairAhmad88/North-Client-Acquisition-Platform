from typing import List

from app.services.scoring.models import ComponentScoreResult, ScoringContext


class ComponentRules:
    @staticmethod
    def calculate_website_need(ctx: ScoringContext, weight: float) -> ComponentScoreResult:
        reasons: List[str] = []
        evidence: List[str] = []
        score = 0.0

        website_url = ctx.business.website_url or ctx.business.normalized_website

        if not website_url:
            score = 100.0
            reasons.append("No official website recorded for business")
            evidence.append("crm:business:website_url=None")
            return ComponentScoreResult("website_need", score, weight, reasons, evidence)

        if ctx.audit:
            evidence.append(f"audit:{ctx.audit.id}")
            if ctx.audit.status in ("NO_WEBSITE", "UNAVAILABLE"):
                score = 95.0
                reasons.append("Target website is unreachable or unavailable")
            else:
                base_need = 15.0
                metrics = ctx.audit.metrics or {}
                findings = ctx.audit.findings or []

                if not metrics.get("https_enabled", True):
                    base_need += 20.0
                    reasons.append("HTTPS security not enforced")
                if not metrics.get("viewport_present", True):
                    base_need += 25.0
                    reasons.append("Mobile viewport metadata missing")
                if not metrics.get("title_present", True):
                    base_need += 15.0
                    reasons.append("Missing page title tag")
                if not metrics.get("meta_description_present", True):
                    base_need += 15.0
                    reasons.append("Missing meta description tag")
                if not metrics.get("contact_form_detected", False):
                    base_need += 10.0
                    reasons.append("No contact form detected on website")

                score = min(100.0, base_need)
                if score < 30.0:
                    reasons.append("Website is functional with baseline signals")
        else:
            score = 50.0
            reasons.append("Website exists but audit has not been executed yet")
            evidence.append("crm:business:website_url=Present")

        return ComponentScoreResult("website_need", score, weight, reasons, evidence)

    @staticmethod
    def calculate_online_presence(ctx: ScoringContext, weight: float) -> ComponentScoreResult:
        reasons: List[str] = []
        evidence: List[str] = []
        score = 0.0

        if ctx.audit:
            evidence.append(f"audit:{ctx.audit.id}")
            metrics = ctx.audit.metrics or {}
            social_count = metrics.get("social_links_count", 0)

            if social_count == 0:
                score += 50.0
                reasons.append("No public social profiles detected on website")
            elif social_count <= 2:
                score += 30.0
                reasons.append(f"Limited social presence ({social_count} profiles detected)")
            else:
                score += 10.0
                reasons.append(f"Active social presence ({social_count} profiles detected)")
        else:
            score += 40.0
            reasons.append("Online presence audit pending")

        if len(ctx.research_records) > 0:
            evidence.append(f"research:records_count={len(ctx.research_records)}")
            score += 10.0
            reasons.append(f"Research evidence includes {len(ctx.research_records)} records")

        return ComponentScoreResult("online_presence", score, weight, reasons, evidence)

    @staticmethod
    def calculate_lead_capture(ctx: ScoringContext, weight: float) -> ComponentScoreResult:
        reasons: List[str] = []
        evidence: List[str] = []
        score = 0.0

        if ctx.audit:
            evidence.append(f"audit:{ctx.audit.id}")
            metrics = ctx.audit.metrics or {}
            has_form = metrics.get("contact_form_detected", False)
            cta_count = metrics.get("cta_count", 0)

            if not has_form:
                score += 50.0
                reasons.append("No visible contact form detected")
            if cta_count == 0:
                score += 40.0
                reasons.append("No obvious call-to-action buttons detected")
            elif cta_count <= 2:
                score += 20.0
                reasons.append(f"Limited call-to-action buttons ({cta_count} detected)")
            else:
                score += 10.0
                reasons.append("Clear call-to-action buttons present")

            if has_form and cta_count > 2:
                score = 15.0
                reasons.append("Comprehensive lead capture mechanisms present")
        else:
            score = 60.0
            reasons.append("Lead capture evaluation pending website audit")

        return ComponentScoreResult("lead_capture", score, weight, reasons, evidence)

    @staticmethod
    def calculate_automation_potential(ctx: ScoringContext, weight: float) -> ComponentScoreResult:
        reasons: List[str] = []
        evidence: List[str] = []
        score = 40.0

        if ctx.audit:
            evidence.append(f"audit:{ctx.audit.id}")
            findings = ctx.audit.findings or []
            finding_codes = [f.get("code") for f in findings if isinstance(f, dict)]

            if "MISSING_CONTACT_FORM" in finding_codes or "NO_OBVIOUS_LEAD_CAPTURE" in finding_codes:
                score += 40.0
                reasons.append("Manual contact channels require workflow automation")
            if "SLOW_HOMEPAGE_RESPONSE" in finding_codes:
                score += 15.0
                reasons.append("Performance bottlenecks indicate potential cloud automation opportunity")
        else:
            reasons.append("Standard automation potential based on business workflow profile")

        if ctx.business.industry in ("Technology", "Professional Services", "Healthcare", "E-commerce"):
            score = min(100.0, score + 15.0)
            reasons.append(f"Industry '{ctx.business.industry}' has high software automation fit")

        return ComponentScoreResult("automation_potential", score, weight, reasons, evidence)

    @staticmethod
    def calculate_business_activity(ctx: ScoringContext, weight: float) -> ComponentScoreResult:
        reasons: List[str] = []
        evidence: List[str] = []

        if ctx.business.status == "ACTIVE":
            score = 80.0
            reasons.append("Business status is ACTIVE in CRM")
            evidence.append("crm:business:status=ACTIVE")
        elif ctx.business.status == "INACTIVE":
            score = 40.0
            reasons.append("Business status is INACTIVE in CRM")
            evidence.append("crm:business:status=INACTIVE")
        else:
            score = 20.0
            reasons.append(f"Business status is {ctx.business.status}")
            evidence.append(f"crm:business:status={ctx.business.status}")

        if len(ctx.research_records) > 0:
            score = min(100.0, score + 15.0)
            reasons.append("Recent research activity observed")

        return ComponentScoreResult("business_activity", score, weight, reasons, evidence)

    @staticmethod
    def calculate_contactability(ctx: ScoringContext, weight: float) -> ComponentScoreResult:
        reasons: List[str] = []
        evidence: List[str] = []
        score = 0.0

        if ctx.business.phone:
            score += 40.0
            reasons.append("Public phone number available")
            evidence.append(f"crm:business:phone={ctx.business.phone}")

        if ctx.business.email:
            score += 40.0
            reasons.append("Public email address available")
            evidence.append(f"crm:business:email={ctx.business.email}")

        if ctx.business.address or ctx.business.city:
            score += 20.0
            reasons.append("Physical business location recorded")
            evidence.append(f"crm:business:location={ctx.business.city or 'Address'}")

        if score == 0.0:
            reasons.append("No direct public contact channels recorded")

        return ComponentScoreResult("contactability", score, weight, reasons, evidence)

    @staticmethod
    def calculate_service_fit(ctx: ScoringContext, weight: float) -> ComponentScoreResult:
        reasons: List[str] = []
        evidence: List[str] = []
        score = 50.0

        if ctx.available_services:
            evidence.append(f"services:catalog_size={len(ctx.available_services)}")
            score = 75.0
            reasons.append("Strong fit with North's Web, Software & AI Automation service catalog")
        else:
            score = 60.0
            reasons.append("General service catalog alignment")

        if ctx.business.industry:
            reasons.append(f"Industry '{ctx.business.industry}' aligned with digital transformation services")

        return ComponentScoreResult("service_fit", score, weight, reasons, evidence)
