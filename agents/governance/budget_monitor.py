"""AI Budget Monitor & Financial Ceiling Enforcement Layer."""

from typing import Any, Dict, Optional
from agents.governance.models import BudgetCheckResult


class AIBudgetMonitor:
    """Enforces token usage and financial budget limits to prevent cost overruns."""

    def evaluate_budget_allowance(
        self,
        current_daily_cost: float,
        daily_limit: float = 50.0,
        estimated_call_cost: float = 0.05,
        enforcement_action: str = "BLOCK",
    ) -> BudgetCheckResult:
        """Verify that projected call cost does not exceed the configured daily limit."""
        projected = current_daily_cost + estimated_call_cost

        if projected > daily_limit:
            return BudgetCheckResult(
                allowed=False,
                enforcement_action=enforcement_action,
                current_daily_cost=current_daily_cost,
                daily_limit=daily_limit,
                reason=f"Daily AI cost threshold reached (${current_daily_cost:.2f} + ${estimated_call_cost:.2f} > ${daily_limit:.2f}).",
            )

        return BudgetCheckResult(
            allowed=True,
            enforcement_action="ALLOW",
            current_daily_cost=current_daily_cost,
            daily_limit=daily_limit,
            reason="Within allocated budget.",
        )
