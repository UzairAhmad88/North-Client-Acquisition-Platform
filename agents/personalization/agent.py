"""Personalization Agent Implementation built on Phase 14 Agent Core Runtime."""

from typing import Any, Dict, List, Optional
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.personalization.angles import AngleSelector
from agents.personalization.confidence import PersonalizationConfidenceCalculator
from agents.personalization.draft import DraftGenerator
from agents.personalization.evidence import PersonalizationEvidenceCollector
from agents.personalization.planner import PersonalizationPlanner
from agents.personalization.profile import PersonalizationProfileGenerator
from agents.personalization.schemas import PersonalizationProfile
from agents.personalization.validation import ClaimValidator
from integrations.ai.models import AICompletionRequest
from integrations.ai.router import AIRouter


class PersonalizationAgent(BaseAgent):
    """Production Personalization Agent creating evidence-backed outreach profiles and communication drafts."""

    name: str = "personalization_agent"
    version: str = "1.0"
    description: str = "Creates evidence-backed personalized outreach context and communication drafts for qualified leads."
    enabled: bool = True
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "READ_AUDIT",
        "READ_SCORE",
        "READ_SERVICES",
        "READ_QUALIFICATION",
        "READ_CRM_CONTEXT",
        "CREATE_OUTREACH_DRAFT",
    }
    max_steps: int = 10
    max_tool_calls: int = 8
    max_runtime_seconds: int = 60

    async def run(self, context: AgentContext) -> AgentResult:
        """Execute structured personalization workflow asynchronously."""
        business_profile = context.business_profile
        lead_profile = context.lead_profile
        research_data = context.research_data
        audit_data = context.audit_data
        score_data = context.score_data
        recommendations_data = context.service_recommendations
        qualification_data = context.metadata.get("qualification_data", {})
        is_dnc = context.metadata.get("is_dnc", False)
        
        req_channel = context.metadata.get("channel", "EMAIL")
        req_tone = context.metadata.get("tone", "PROFESSIONAL")
        req_depth = context.metadata.get("personalization_depth", "STANDARD")
        req_objective = context.metadata.get("objective", "INTRODUCE_SERVICE")

        has_contact = bool(
            business_profile.get("phone") or business_profile.get("email") or
            lead_profile.get("phone") or lead_profile.get("email") or
            business_profile.get("website_url")
        )

        # 1. Eligibility Check & Qualification Gate
        is_eligible, readiness, gate_reason = PersonalizationPlanner.evaluate_eligibility(
            qualification_data=qualification_data,
            is_dnc=is_dnc,
            has_valid_contact=has_contact,
        )

        # 2. Extract Verified Signals & Business Needs
        signals = PersonalizationProfileGenerator.extract_signals(
            business_profile=business_profile,
            research_data=research_data,
            audit_data=audit_data,
            score_data=score_data,
            recommendations_data=recommendations_data,
            qualification_data=qualification_data,
        )
        needs = PersonalizationProfileGenerator.map_business_needs(signals)

        # 3. Angle Selection
        primary_angle, supporting_angles = AngleSelector.select_angles(signals, needs)

        # 4. Evidence Collection
        evidence_list = PersonalizationEvidenceCollector.collect_evidence(
            research_data=research_data,
            audit_data=audit_data,
            score_data=score_data,
            recommendations_data=recommendations_data,
            qualification_data=qualification_data,
        )

        # 5. Draft Generation
        biz_name = business_profile.get("name", "Target Business")
        lead_name = lead_profile.get("contact_name") or lead_profile.get("title")
        draft = DraftGenerator.generate_draft(
            business_name=biz_name,
            lead_name=lead_name,
            primary_angle=primary_angle,
            signals=signals,
            channel=req_channel,
            tone=req_tone,
            depth=req_depth,
            objective=req_objective,
        )
        draft.outreach_readiness = readiness

        # 6. Optional AI Synthesis Enhancement
        if is_eligible and readiness != "OUTREACH_BLOCKED":
            try:
                ai_router = AIRouter()
                prompt = (
                    f"Refine communication draft for {biz_name}. Channel: {req_channel}, Tone: {req_tone}. "
                    f"Primary Angle: {primary_angle.title}. "
                    f"Draft Subject: {draft.subject or 'N/A'}\nDraft Body:\n{draft.body}"
                )
                ai_req = AICompletionRequest(prompt=prompt)
                ai_resp = await ai_router.complete(ai_req)
                if ai_resp.structured_data:
                    res_body = ai_resp.structured_data.get("result", {}).get("body")
                    if res_body:
                        draft.body = res_body
            except Exception:
                pass  # Fallback to deterministic template draft

        # 7. Claim & Risk Validation
        claims, risk_level, warnings = ClaimValidator.validate_claims_and_risk(
            draft=draft,
            verified_evidence_count=len(evidence_list),
        )
        draft.claims = claims
        draft.risk_level = risk_level

        # 8. Confidence Rating
        overall_confidence = PersonalizationConfidenceCalculator.calculate_confidence(
            evidence_list=evidence_list,
            qualification_data=qualification_data,
        )

        # 9. Build Personalization Profile
        profile = PersonalizationProfile(
            business_summary=f"Personalization context generated for {biz_name}.",
            audience_context=f"Targeting {lead_name or 'Business Contact'} via {req_channel}.",
            verified_signals=signals,
            business_needs=needs,
            relevant_services=recommendations_data,
            value_opportunities=[primary_angle.value_proposition],
            primary_angle=primary_angle,
            supporting_angles=supporting_angles,
            evidence=evidence_list,
            confidence=overall_confidence,
            warnings=warnings,
            limitations=[gate_reason] if not is_eligible else [],
            prohibited_claims=[],
        )

        result_payload = {
            "personalization_profile": profile.model_dump(),
            "primary_angle": primary_angle.model_dump(),
            "supporting_angles": [a.model_dump() for a in supporting_angles],
            "draft": draft.model_dump(),
            "evidence": evidence_list,
            "risks": [c.statement for c in claims if not c.is_supported],
            "limitations": [gate_reason] if not is_eligible else [],
            "outreach_readiness": readiness,
        }

        return AgentResult(
            status="COMPLETED",
            result=result_payload,
            confidence=overall_confidence,
            evidence=evidence_list,
            warnings=warnings,
            errors=[],
            next_action="HUMAN_REVIEW",
        )
