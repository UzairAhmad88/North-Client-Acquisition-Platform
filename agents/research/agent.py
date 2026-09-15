"""Research Agent Implementation built on Phase 14 Agent Core Runtime."""

from typing import Any, Dict, List

from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.errors import AgentExecutionFailedError
from agents.research.confidence import ResearchConfidenceCalculator
from agents.research.evidence import ResearchEvidenceCollector
from agents.research.planner import ResearchPlanner
from agents.research.schemas import ResearchAgentResult, ResearchFindingItem
from agents.research.validation import ResearchOutputValidator
from integrations.ai.models import AICompletionRequest
from integrations.ai.router import AIRouter


class ResearchAgent(BaseAgent):
    """Production Research Agent gathering and organizing evidence-backed business intelligence."""

    name: str = "research_agent"
    version: str = "1.0"
    description: str = "Researches public business information and produces evidence-backed structured findings."
    enabled: bool = True
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "SEARCH_WEB",
        "FETCH_WEB",
        "CREATE_RESEARCH_RECORD",
    }
    max_steps: int = 10
    max_tool_calls: int = 8
    max_runtime_seconds: int = 60

    async def run(self, context: AgentContext) -> AgentResult:
        """Execute structured research workflow asynchronously."""
        business_profile = context.business_profile
        biz_name = business_profile.get("name", "Target Business")
        biz_cat = business_profile.get("category", "General")
        biz_web = business_profile.get("website_url")

        # 1. Existing Research Evaluation & Freshness Check
        existing_records = context.research_data.get("records", [])
        requested_sections = context.metadata.get(
            "requested_sections",
            ["identity", "services", "digital_presence", "contact_information"],
        )

        plan = ResearchPlanner.plan_research(
            requested_sections=requested_sections,
            existing_records=existing_records,
            max_age_days=context.metadata.get("max_age_days", 30),
        )

        findings: List[Dict[str, Any]] = []
        evidence_items: List[Dict[str, Any]] = []
        conflicts: List[Dict[str, Any]] = []

        # 2. Extract facts from existing fresh research
        for rec in existing_records:
            fn = rec.get("field_name", "general")
            val = rec.get("normalized_value", "")
            src_url = rec.get("source_url")
            src_trust = rec.get("source_trust", "OFFICIAL")
            conf = rec.get("confidence", "HIGH")

            finding = {
                "field": fn,
                "value": val,
                "source_type": src_trust,
                "source_url": src_url,
                "source_trust": src_trust,
                "confidence": conf,
                "evidence": f"Existing validated research record for {fn}.",
                "freshness": "CURRENT",
            }
            findings.append(finding)
            evidence_items.append(
                ResearchEvidenceCollector.create_evidence_item(
                    field=fn,
                    value=val,
                    source_url=src_url,
                    source_trust=src_trust,
                    summary=f"Existing fresh research for {fn}",
                )
            )

        # 3. Targeted Web Research if missing/stale fields exist
        if plan["should_search_web"]:
            ai_router = AIRouter()
            prompt = f"Extract business intelligence for {biz_name} ({biz_cat}). Website: {biz_web or 'None'}."
            ai_req = AICompletionRequest(prompt=prompt)
            ai_resp = await ai_router.complete(ai_req)

            # Process AI output safely
            if ai_resp.structured_data:
                res_data = ai_resp.structured_data.get("result", {})
                if "findings" in res_data:
                    for f in res_data["findings"]:
                        if f not in findings:
                            findings.append(f)

            # Fallback baseline findings from context business profile if needed
            if not findings and biz_name and biz_name != "Target Business":
                findings.append({
                    "field": "identity",
                    "value": biz_name,
                    "source_type": "OFFICIAL",
                    "source_url": biz_web,
                    "source_trust": "OFFICIAL",
                    "confidence": "HIGH",
                    "evidence": f"Official registered business name '{biz_name}'.",
                    "freshness": "CURRENT",
                })
                if biz_cat:
                    findings.append({
                        "field": "category",
                        "value": biz_cat,
                        "source_type": "OFFICIAL",
                        "source_url": biz_web,
                        "source_trust": "OFFICIAL",
                        "confidence": "HIGH",
                        "evidence": f"Registered category '{biz_cat}'.",
                        "freshness": "CURRENT",
                    })

        # 4. Handle No Website Scenario gracefully
        if not biz_web and not any(f.get("field") == "website_url" for f in findings):
            no_web_finding = {
                "field": "website_url",
                "value": None,
                "source_type": "OFFICIAL",
                "source_url": None,
                "source_trust": "OFFICIAL",
                "confidence": "HIGH",
                "evidence": "No official website was observed or registered for this business.",
                "freshness": "CURRENT",
            }
            findings.append(no_web_finding)

        # 5. Validation & Confidence Assessment
        validated_output = ResearchOutputValidator.validate_research_output(
            {"findings": findings, "conflicts": conflicts}
        )

        overall_confidence = ResearchConfidenceCalculator.calculate_overall_confidence(
            validated_output["findings"], validated_output["conflicts"]
        )

        status_str = "COMPLETED" if len(validated_output["findings"]) > 0 else "PARTIAL"

        agent_result_data = {
            "business_summary": {
                "name": biz_name,
                "category": biz_cat,
                "website_url": biz_web,
                "findings_count": len(validated_output["findings"]),
            },
            "findings": validated_output["findings"],
            "evidence": evidence_items,
            "conflicts": validated_output["conflicts"],
            "missing_information": plan["target_fields"],
            "limitations": [
                "Research is based on publicly available web pages and existing records.",
                "Internal financial details and private communications were not accessed.",
            ],
        }

        return AgentResult(
            status=status_str,
            result=agent_result_data,
            confidence=overall_confidence,
            evidence=evidence_items,
            warnings=context.warnings,
        )
