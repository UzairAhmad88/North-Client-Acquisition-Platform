"""Contract Impact Analyzer for Change Requests."""

from typing import Any, Dict


class ChangeContractAnalyzer:
    """Analyzes whether a proposed scope or commercial change requires a formal contract amendment."""

    def evaluate_contract_impact(
        self, change_request_id: str, is_out_of_scope: bool, commercial_change_value: float
    ) -> Dict[str, Any]:
        requires_amendment = is_out_of_scope or commercial_change_value > 0

        return {
            "change_request_id": change_request_id,
            "requires_contract_amendment": requires_amendment,
            "contract_impact_type": "CONTRACT_AMENDMENT_REQUIRED" if requires_amendment else "NO_CONTRACT_CHANGE",
            "reasoning": "Scope expansion or commercial value change exceeds committed baseline boundaries." if requires_amendment else "Change falls within existing contract terms.",
        }
