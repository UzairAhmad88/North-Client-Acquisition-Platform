"""Commercial Analyzer for Change Requests."""

from typing import Any, Dict
from agents.change_management.models import ChangeCommercialAnalysis


class ChangeCommercialAnalyzer:
    """Calculates commercial value deltas based on expected effort and baseline pricing policy."""

    def calculate_commercial_delta(
        self, change_request_id: str, expected_hours: float, hourly_rate: float = 5000.0, original_contract_value: float = 0.0
    ) -> ChangeCommercialAnalysis:
        change_val = round(expected_hours * hourly_rate, 2)
        revised_val = round(original_contract_value + change_val, 2)

        return ChangeCommercialAnalysis(
            change_request_id=change_request_id,
            currency="PKR",
            original_value=original_contract_value,
            change_value=change_val,
            revised_value=revised_val,
            commercial_recommendation="ADDITIONAL_COST_REQUIRED" if change_val > 0 else "NO_COMMERCIAL_CHANGE",
            pricing_policy_version="1.0",
        )
