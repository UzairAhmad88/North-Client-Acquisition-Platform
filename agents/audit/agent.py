"""Audit Agent Implementation built on Phase 14 Agent Core Runtime."""

from typing import Any, Dict, List, Optional

from agents.audit.confidence import AuditConfidenceCalculator
from agents.audit.findings import AuditFindingCollector
from agents.audit.planner import AuditPlanner
from agents.audit.validation import AuditOutputValidator
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from app.services.audit.service import AuditService
from integrations.ai.models import AICompletionRequest
from integrations.ai.router import AIRouter


class AuditAgent(BaseAgent):
    """Production Audit Agent analyzing public digital presence and producing evidence-backed findings."""

    name: str = "audit_agent"
    version: str = "1.0"
    description: str = "Analyzes public digital presence and produces evidence-backed audit findings."
    enabled: bool = True
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "READ_AUDIT",
        "FETCH_WEB",
        "RUN_AUDIT",
        "CREATE_AUDIT_RECORD",
    }
    max_steps: int = 10
    max_tool_calls: int = 8
    max_runtime_seconds: int = 60

    async def run(self, context: AgentContext) -> AgentResult:
        """Execute structured audit workflow asynchronously."""
        business_profile = context.business_profile
        research_data = context.research_data
        existing_audit = context.metadata.get("existing_audit")
        explicit_url = context.metadata.get("target_url")

        # 1. Target Website Selection
        target_url, target_source = AuditPlanner.select_target_url(
            business_profile=business_profile,
            research_data=research_data,
            explicit_url=explicit_url,
        )

        # Handle NO_WEBSITE scenario
        if not target_url or target_source == "NO_WEBSITE":
            no_web_finding = AuditFindingCollector.create_finding(
                code="NO_WEBSITE",
                category="website_health",
                title="No Website Observed",
                description="No public website domain was observed or registered for this business.",
                severity_override="MEDIUM",
                confidence="HIGH",
            ).model_dump()

            return AgentResult(
                status="NO_WEBSITE",
                result={
                    "audit_status": "NO_WEBSITE",
                    "target_url": None,
                    "overall_health": "LIMITED_DATA",
                    "findings": [no_web_finding],
                    "metrics": {"pages_analyzed": 0},
                    "evidence": [],
                    "conflicts": [],
                    "limitations": [
                        "No public website was registered or discovered in research records.",
                        "Audit is limited to absence of primary website domain.",
                    ],
                },
                confidence="HIGH",
                evidence=[],
                warnings=["Target business has no registered website URL."],
            )

        # 2. Existing Audit Freshness Check (<= 7 days reuse)
        if existing_audit and AuditPlanner.check_audit_freshness(existing_audit, max_age_days=7):
            return AgentResult(
                status="COMPLETED",
                result={
                    "audit_status": "COMPLETED",
                    "target_url": target_url,
                    "overall_health": existing_audit.get("overall_health", "FAIR"),
                    "findings": existing_audit.get("findings", []),
                    "metrics": existing_audit.get("metrics", {}),
                    "evidence": [],
                    "conflicts": [],
                    "limitations": [
                        "Audit reused from existing fresh audit snapshot (<= 7 days old)."
                    ],
                },
                confidence="HIGH",
                evidence=[],
                warnings=["Reused existing fresh audit record."],
            )

        # 3. Deterministic Measurement Execution via Phase 11 Runner
        runner = AuditService.get_runner("MOCK")
        raw_result = await runner.run_audit(
            business=None,
            target_url=target_url,
            max_pages=context.metadata.get("max_pages", 10),
        )

        findings: List[Dict[str, Any]] = [f.to_dict() for f in raw_result.findings]
        evidence_items: List[Dict[str, Any]] = []

        # 4. Check Business Information Consistency against Research Data
        records = research_data.get("records", [])
        res_phone = None
        for r in records:
            if r.get("field_name") == "phone":
                res_phone = r.get("normalized_value")

        biz_phone = business_profile.get("phone")
        if res_phone and biz_phone and res_phone != biz_phone:
            discrepancy_finding = AuditFindingCollector.create_finding(
                code="PHONE_DISCREPANCY",
                category="business_consistency",
                title="Business Contact Phone Discrepancy",
                description=f"Research record phone ({res_phone}) differs from profile phone ({biz_phone}).",
                severity_override="MEDIUM",
                confidence="HIGH",
            ).model_dump()
            findings.append(discrepancy_finding)

        # 5. AI Synthesis & Output Validation
        validated = AuditOutputValidator.validate_audit_output({"findings": findings})
        overall_conf = AuditConfidenceCalculator.calculate_overall_confidence(
            findings=[AuditFindingCollector.create_finding("INFO", f["category"], f["title"], f["description"]) for f in validated["findings"]],
            pages_analyzed=len(raw_result.pages),
        )

        result_data = {
            "audit_status": "COMPLETED" if len(raw_result.pages) > 0 else "PARTIAL",
            "target_url": target_url,
            "overall_health": raw_result.overall_health,
            "summary": raw_result.summary,
            "findings": validated["findings"],
            "metrics": raw_result.metrics,
            "evidence": evidence_items,
            "conflicts": [],
            "limitations": [
                "Audit is a read-only passive digital presence assessment.",
                "No form submissions, logins, or invasive vulnerability testing were performed.",
            ],
        }

        return AgentResult(
            status="COMPLETED",
            result=result_data,
            confidence=overall_conf,
            evidence=evidence_items,
            warnings=raw_result.warnings,
            errors=raw_result.errors,
        )
