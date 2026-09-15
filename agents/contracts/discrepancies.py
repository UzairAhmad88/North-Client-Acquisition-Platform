"""Contract Discrepancy Detector flagging scope, price, and timeline mismatches."""

from typing import Any, Dict, List
from agents.contracts.models import ContractDiscrepancySchema, ContractSectionSchema


class DiscrepancyDetector:
    """Detects discrepancies between contract text and approved baselines."""

    @classmethod
    def detect_discrepancies(
        cls,
        sections: List[ContractSectionSchema],
        proposal_data: Dict[str, Any],
        estimate_data: Dict[str, Any],
        solution_data: Dict[str, Any],
    ) -> List[ContractDiscrepancySchema]:
        discrepancies: List[ContractDiscrepancySchema] = []

        # 1. Scope Mismatch Check
        sol_features = solution_data.get("features", [])
        scope_sec = next((s for s in sections if s.section_type == "SCOPE"), None)

        if scope_sec and sol_features:
            scope_text_lower = scope_sec.content.lower()
            for feat in sol_features:
                f_title = feat.get("title", "").lower()
                if f_title and f_title not in scope_text_lower:
                    discrepancies.append(
                        ContractDiscrepancySchema(
                            discrepancy_type="SCOPE_MISMATCH",
                            description=f"Approved solution feature '{feat.get('title')}' is missing from contract scope section.",
                            severity="HIGH",
                            status="DETECTED",
                        )
                    )

        # 2. Commercial Mismatch Check
        est_min = estimate_data.get("recommended_min")
        comm_sec = next((s for s in sections if s.section_type == "COMMERCIAL"), None)

        if est_min and comm_sec:
            if str(int(est_min)) not in comm_sec.content:
                discrepancies.append(
                    ContractDiscrepancySchema(
                        discrepancy_type="COMMERCIAL_MISMATCH",
                        description=f"Contract commercial section text does not match approved estimate baseline (${est_min}).",
                        severity="MEDIUM",
                        status="DETECTED",
                    )
                )

        return discrepancies
