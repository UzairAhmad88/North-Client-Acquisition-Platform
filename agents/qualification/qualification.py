"""Hybrid Qualification Decision Engine enforcing deterministic guardrails and factor evaluations."""

from typing import Any, Dict, List, Tuple
from agents.qualification.schemas import (
    QualificationAgentResult,
    QualificationFactorItem,
)


class QualificationEngine:
    """Evaluates qualification decision based on deterministic guardrails and factor alignment."""

    @classmethod
    def evaluate(
        cls,
        business_profile: Dict[str, Any],
        lead_profile: Dict[str, Any],
        research_data: Dict[str, Any],
        audit_data: Dict[str, Any],
        score_data: Dict[str, Any],
        recommended_services: List[Dict[str, Any]],
        dnc_status: bool = False,
        has_unresolved_duplicate: bool = False,
    ) -> Dict[str, Any]:
        factors: List[Dict[str, Any]] = []
        reasons: List[str] = []
        risks: List[str] = []
        missing_info: List[str] = []
        limitations: List[str] = [
            "Qualification is an internal advisor assessment only.",
            "Deterministic Opportunity Score and Service Recommendations were not altered.",
        ]

        # 1. Deterministic Guardrail 1: Do-Not-Contact (DNC) check
        if dnc_status:
            risks.append("Lead or Business is flagged on Do-Not-Contact (DNC) list.")
            return {
                "decision": "NEEDS_REVIEW",
                "confidence": "HIGH",
                "summary": "Lead is on the Do-Not-Contact list. Outreach is strictly blocked.",
                "factors": [
                    {
                        "name": "CONTACTABILITY",
                        "status": "WEAK",
                        "assessment": "Flagged on Do-Not-Contact (DNC) list.",
                        "confidence": "HIGH",
                        "evidence": [],
                    }
                ],
                "reasons": ["Do-Not-Contact (DNC) flag active."],
                "risks": risks,
                "missing_information": [],
                "limitations": limitations,
                "outreach_readiness": "OUTREACH_BLOCKED",
                "recommended_internal_action": "HOLD",
            }

        # 2. Deterministic Guardrail 2: Unresolved Duplicate check
        if has_unresolved_duplicate:
            risks.append("Unresolved duplicate business or lead record detected in CRM.")
            reasons.append("Duplicate lead record requires resolution before qualification.")

        # 3. Upstream Data Availability Evaluation
        score_val = score_data.get("score")
        score_band = score_data.get("score_band", "UNKNOWN")

        if score_val is None and not research_data.get("records") and not audit_data.get("findings"):
            missing_info.append("Deterministic Lead Opportunity Score")
            missing_info.append("Research & Digital Audit Profile")
            return {
                "decision": "INSUFFICIENT_DATA",
                "confidence": "LOW",
                "summary": "Insufficient reliable data across upstream systems to form a qualification decision.",
                "factors": [],
                "reasons": ["Lacks opportunity score and research profile."],
                "risks": risks,
                "missing_information": missing_info,
                "limitations": limitations,
                "outreach_readiness": "NOT_READY",
                "recommended_internal_action": "RESEARCH_MORE",
            }

        # 4. Service Fit & Need Assessment
        strong_services = [s for s in recommended_services if isinstance(s, dict) and s.get("relevance_band") in ("STRONG", "GOOD")]
        service_fit_status = "STRONG" if len(strong_services) >= 2 else ("MODERATE" if strong_services else "WEAK")

        factors.append({
            "name": "SERVICE_FIT",
            "status": service_fit_status,
            "assessment": f"Matched {len(strong_services)} strong/good North's service offerings.",
            "confidence": "HIGH",
            "evidence": [],
        })

        # 5. Digital Gap / Audit Findings Assessment
        audit_findings = audit_data.get("findings", [])
        high_sev_count = sum(1 for f in audit_findings if isinstance(f, dict) and f.get("severity") in ("HIGH", "MEDIUM"))
        digital_gap_status = "STRONG" if high_sev_count >= 2 else ("MODERATE" if audit_findings else "WEAK")

        factors.append({
            "name": "DIGITAL_GAP",
            "status": digital_gap_status,
            "assessment": f"Identified {high_sev_count} actionable digital presence gaps/weaknesses.",
            "confidence": "HIGH" if audit_findings else "MEDIUM",
            "evidence": [],
        })

        # 6. Contactability Assessment
        phone = business_profile.get("phone") or lead_profile.get("phone")
        email = business_profile.get("email") or lead_profile.get("email")
        website = business_profile.get("website_url")

        if phone and (email or website):
            contact_status = "STRONG"
        elif phone or email or website:
            contact_status = "MODERATE"
        else:
            contact_status = "WEAK"
            missing_info.append("Verified public contact telephone or email")

        factors.append({
            "name": "CONTACTABILITY",
            "status": contact_status,
            "assessment": "Public contact route available." if contact_status != "WEAK" else "Limited or unverified public contact route.",
            "confidence": "HIGH" if contact_status == "STRONG" else "MEDIUM",
            "evidence": [],
        })

        # 7. Decision Synthesis Logic
        if has_unresolved_duplicate:
            decision = "NEEDS_REVIEW"
            readiness = "NEEDS_VERIFICATION"
            action = "MERGE_DUPLICATE"
        elif score_band == "HIGH" and service_fit_status in ("STRONG", "MODERATE") and contact_status != "WEAK":
            decision = "QUALIFIED"
            readiness = "OUTREACH_READY"
            action = "PREPARE_OUTREACH"
            reasons.append("High opportunity score combined with strong service fit and contactability.")
        elif score_band in ("HIGH", "MEDIUM") and (service_fit_status != "WEAK" or digital_gap_status != "WEAK"):
            decision = "POTENTIALLY_QUALIFIED"
            readiness = "NEEDS_VERIFICATION"
            action = "REVIEW_LEAD"
            reasons.append("Promising opportunity signals; verification of specific digital needs recommended.")
        elif score_band == "VERY_LOW" or (service_fit_status == "WEAK" and digital_gap_status == "WEAK"):
            decision = "NOT_QUALIFIED"
            readiness = "NOT_READY"
            action = "ARCHIVE"
            reasons.append("Low opportunity score and minimal service relevance.")
        else:
            decision = "NEEDS_REVIEW"
            readiness = "NEEDS_VERIFICATION"
            action = "REVIEW_LEAD"
            reasons.append("Mixed evidence signals require human review.")

        summary = f"Lead is evaluated as {decision} with {service_fit_status} service fit alignment."

        return {
            "decision": decision,
            "confidence": "HIGH" if score_val and audit_findings else "MEDIUM",
            "summary": summary,
            "factors": factors,
            "reasons": reasons,
            "risks": risks,
            "missing_information": missing_info,
            "limitations": limitations,
            "outreach_readiness": readiness,
            "recommended_internal_action": action,
        }
