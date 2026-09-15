"""Warranty Evaluator Engine grounded in authoritative contract baselines."""

from typing import Any, Dict, Optional
from agents.support.models import WarrantyEvaluationResult


class WarrantyEvaluatorEngine:
    """Evaluates whether an identified defect is covered under active warranty terms."""

    def evaluate_warranty_coverage(
        self,
        project_id: str,
        defect_title: str,
        defect_description: str,
        warranty_data: Optional[Dict[str, Any]] = None,
        is_in_baseline: bool = True,
    ) -> WarrantyEvaluationResult:
        """Evaluate warranty eligibility against project warranty terms and delivered baseline scope."""
        if not warranty_data:
            return WarrantyEvaluationResult(
                project_id=project_id,
                is_covered="UNKNOWN",
                confidence=0.60,
                reasoning="No authoritative warranty record found in project contract. Human commercial review required.",
                requires_human_approval=True,
            )

        warranty_status = warranty_data.get("status", "NOT_STARTED")
        if warranty_status in ["EXPIRED", "CANCELLED", "SUSPENDED"]:
            return WarrantyEvaluationResult(
                project_id=project_id,
                is_covered="NOT_COVERED",
                confidence=0.95,
                reasoning=f"Warranty is currently {warranty_status}. Remediation is billable under maintenance or support.",
                requires_human_approval=True,
            )

        if not is_in_baseline:
            return WarrantyEvaluationResult(
                project_id=project_id,
                is_covered="NOT_COVERED",
                confidence=0.90,
                reasoning="The affected component was not part of the approved contract baseline deliverables. Out-of-scope.",
                requires_human_approval=True,
            )

        # Check explicit exclusions
        exclusions = str(warranty_data.get("exclusions") or "").lower()
        full_text = f"{defect_title.lower()} {defect_description.lower()}"
        if exclusions and any(exc in full_text for exc in ["third-party api", "hosting failure", "unauthorized modification"]):
            return WarrantyEvaluationResult(
                project_id=project_id,
                is_covered="NOT_COVERED",
                confidence=0.88,
                reasoning="Issue falls under contractual warranty exclusions (third-party dependency or external environment).",
                requires_human_approval=True,
            )

        if warranty_status == "ACTIVE":
            return WarrantyEvaluationResult(
                project_id=project_id,
                is_covered="COVERED",
                confidence=0.92,
                reasoning="Active warranty covers delivered baseline functionality defects. Remediated at no extra charge.",
                contract_reference=warranty_data.get("contract_reference", "Section: Warranty & SLA"),
                requires_human_approval=True,
            )

        return WarrantyEvaluationResult(
            project_id=project_id,
            is_covered="REVIEW_REQUIRED",
            confidence=0.75,
            reasoning="Warranty terms require manual operator review before confirmation.",
            requires_human_approval=True,
        )
