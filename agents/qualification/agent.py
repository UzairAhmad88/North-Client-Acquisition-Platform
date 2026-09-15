"""Qualification Agent Implementation built on Phase 14 Agent Core Runtime."""

from typing import Any, Dict, List

from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.qualification.confidence import QualificationConfidenceCalculator
from agents.qualification.qualification import QualificationEngine
from agents.qualification.validation import QualificationOutputValidator
from integrations.ai.models import AICompletionRequest
from integrations.ai.router import AIRouter


class QualificationAgent(BaseAgent):
    """Production Qualification Agent evaluating lead opportunities as an internal advisor."""

    name: str = "qualification_agent"
    version: str = "1.0"
    description: str = "Evaluates whether a business lead appears worth pursuing using evidence-backed business intelligence."
    enabled: bool = True
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "READ_AUDIT",
        "READ_SCORE",
        "READ_SERVICES",
        "READ_CRM_CONTEXT",
        "CREATE_QUALIFICATION_RESULT",
    }
    max_steps: int = 10
    max_tool_calls: int = 8
    max_runtime_seconds: int = 60

    async def run(self, context: AgentContext) -> AgentResult:
        """Execute structured qualification workflow asynchronously."""
        business_profile = context.business_profile
        lead_profile = context.lead_profile
        research_data = context.research_data
        audit_data = context.audit_data
        score_data = context.score_data
        recommended_services = context.service_recommendations
        is_dnc = context.metadata.get("is_dnc", False)
        has_duplicate = context.metadata.get("has_duplicate", False)

        # 1. Deterministic Guardrail & Factor Evaluation Engine
        eval_result = QualificationEngine.evaluate(
            business_profile=business_profile,
            lead_profile=lead_profile,
            research_data=research_data,
            audit_data=audit_data,
            score_data=score_data,
            recommended_services=recommended_services,
            dnc_status=is_dnc,
            has_unresolved_duplicate=has_duplicate,
        )

        # 2. AI Synthesis for Explanation Summary (Optional Enhancement)
        biz_name = business_profile.get("name", "Target Business")
        lead_title = lead_profile.get("title", "Lead")

        if eval_result["decision"] not in ("INSUFFICIENT_DATA", "OUTREACH_BLOCKED"):
            ai_router = AIRouter()
            prompt = f"Synthesize qualification explanation for {biz_name} ({lead_title}). Decision: {eval_result['decision']}."
            ai_req = AICompletionRequest(prompt=prompt)
            ai_resp = await ai_router.complete(ai_req)
            if ai_resp.structured_data:
                res_summary = ai_resp.structured_data.get("result", {}).get("summary")
                if res_summary:
                    eval_result["summary"] = res_summary

        # 3. Output Validation & Confidence Rating
        validated = QualificationOutputValidator.validate_result(eval_result)
        overall_conf = QualificationConfidenceCalculator.calculate_overall_confidence(
            factors=[],
            data_quality_score=context.metadata.get("data_quality_score", 100.0),
        )

        result_data = {
            "decision": validated["decision"],
            "confidence": validated["confidence"],
            "summary": validated["summary"],
            "factors": validated["factors"],
            "reasons": validated["reasons"],
            "evidence": validated["evidence"],
            "risks": validated["risks"],
            "missing_information": validated["missing_information"],
            "limitations": validated["limitations"],
            "outreach_readiness": validated["outreach_readiness"],
            "recommended_internal_action": validated["recommended_internal_action"],
            "qualification_version": "1.0",
        }

        return AgentResult(
            status="COMPLETED",
            result=result_data,
            confidence=validated["confidence"],
            evidence=validated["evidence"],
            warnings=[],
            errors=[],
        )
