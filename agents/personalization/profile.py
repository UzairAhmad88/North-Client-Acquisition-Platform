"""Profile generator extracting verified signals and mapping business needs."""

from typing import Any, Dict, List
from agents.personalization.schemas import BusinessNeedMapping, VerifiedSignal


class PersonalizationProfileGenerator:
    """Extracts factual verified signals from business intelligence sources and maps business needs."""

    @staticmethod
    def extract_signals(
        business_profile: Dict[str, Any],
        research_data: Dict[str, Any],
        audit_data: Dict[str, Any],
        score_data: Dict[str, Any],
        recommendations_data: List[Dict[str, Any]],
        qualification_data: Dict[str, Any],
    ) -> List[VerifiedSignal]:
        signals: List[VerifiedSignal] = []

        # 1. Business Profile & Contact signals
        biz_name = business_profile.get("name")
        website = business_profile.get("website_url")
        phone = business_profile.get("phone")
        email = business_profile.get("email")

        if biz_name:
            signals.append(
                VerifiedSignal(
                    source_type="CRM",
                    signal_name="BUSINESS_NAME",
                    description=f"Verified business entity name: {biz_name}",
                    confidence="HIGH",
                )
            )

        if website:
            signals.append(
                VerifiedSignal(
                    source_type="AUDIT",
                    signal_name="WEBSITE_EXISTS",
                    description=f"Active public website URL: {website}",
                    confidence="HIGH",
                )
            )

        if phone or email:
            signals.append(
                VerifiedSignal(
                    source_type="CRM",
                    signal_name="PUBLIC_CONTACT_AVAILABLE",
                    description=f"Verified contact route available (Phone: {bool(phone)}, Email: {bool(email)})",
                    confidence="HIGH",
                )
            )

        # 2. Research Signals
        records = research_data.get("records", [])
        for r in records:
            if isinstance(r, dict):
                fact = r.get("fact_summary") or r.get("value")
                if fact:
                    signals.append(
                        VerifiedSignal(
                            source_type="RESEARCH",
                            signal_name="RESEARCH_FACT",
                            description=str(fact),
                            evidence_id=str(r.get("id")) if r.get("id") else None,
                            confidence=r.get("confidence", "HIGH"),
                        )
                    )

        # 3. Audit Findings Signals
        findings = audit_data.get("findings", [])
        for f in findings:
            if isinstance(f, dict):
                code = f.get("code") or f.get("title", "AUDIT_FINDING")
                desc = f.get("description") or f.get("assessment", "")
                sev = f.get("severity", "MEDIUM")
                signals.append(
                    VerifiedSignal(
                        source_type="AUDIT",
                        signal_name=f"AUDIT_{code.upper()}",
                        description=f"Audit finding ({sev}): {desc}",
                        evidence_id=str(f.get("id")) if f.get("id") else None,
                        confidence="HIGH",
                    )
                )

        # 4. Score Signals
        band = score_data.get("band") or score_data.get("score_band")
        total_score = score_data.get("total_score") or score_data.get("score")
        if band and total_score is not None:
            signals.append(
                VerifiedSignal(
                    source_type="SCORE",
                    signal_name="OPPORTUNITY_SCORE",
                    description=f"Deterministic Opportunity Score: {total_score} ({band} Priority)",
                    confidence="HIGH",
                )
            )

        # 5. Service Recommendation Signals
        for rec in recommendations_data:
            if isinstance(rec, dict):
                title = rec.get("service_title") or rec.get("name", "North's Service")
                band_rel = rec.get("relevance_band", "GOOD")
                if band_rel in ("STRONG", "GOOD"):
                    signals.append(
                        VerifiedSignal(
                            source_type="RECOMMENDATION",
                            signal_name="SERVICE_FIT",
                            description=f"Strong North's service match: {title} ({band_rel})",
                            evidence_id=str(rec.get("id")) if rec.get("id") else None,
                            confidence="HIGH",
                        )
                    )

        return signals

    @staticmethod
    def map_business_needs(signals: List[VerifiedSignal]) -> List[BusinessNeedMapping]:
        needs: List[BusinessNeedMapping] = []

        audit_signals = [s for s in signals if s.source_type == "AUDIT"]
        for s in audit_signals:
            if "NO_WEBSITE" in s.signal_name or "WEBSITE" in s.description.upper():
                needs.append(
                    BusinessNeedMapping(
                        observed_gap="Website availability or dynamic digital presence gap",
                        potential_need="Modern responsive website to capture online demand",
                        relevant_service_slug="business-website",
                        evidence_ids=[s.evidence_id] if s.evidence_id else [],
                    )
                )
            elif "BOOKING" in s.description.upper() or "CTA" in s.description.upper():
                needs.append(
                    BusinessNeedMapping(
                        observed_gap="Lack of clear online booking or inquiry capture path",
                        potential_need="Streamlined online booking and inquiry capture flow",
                        relevant_service_slug="booking-system",
                        evidence_ids=[s.evidence_id] if s.evidence_id else [],
                    )
                )
            elif "MOBILE" in s.description.upper() or "SPEED" in s.description.upper():
                needs.append(
                    BusinessNeedMapping(
                        observed_gap="Mobile optimization or loading speed constraint",
                        potential_need="Fast, mobile-optimized visitor experience",
                        relevant_service_slug="website-audit-optimization",
                        evidence_ids=[s.evidence_id] if s.evidence_id else [],
                    )
                )

        if not needs:
            needs.append(
                BusinessNeedMapping(
                    observed_gap="Observed opportunity for digital presence enhancement",
                    potential_need="High-converting digital presence and automated customer inquiry flow",
                    relevant_service_slug="business-website",
                    evidence_ids=[],
                )
            )

        return needs
