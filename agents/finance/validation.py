"""Financial Agent Validation & Safety Guardrails.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import PROHIBITED_PERMISSIONS


class FinancialSafetyValidator:
    """Enforces safety rules, commercial baselines, and financial integrity constraints."""

    @staticmethod
    def validate_no_prohibited_action(action: str) -> None:
        """Ensures the agent is never invoked with a prohibited financial side-effect."""
        act_upper = action.upper()
        if act_upper in PROHIBITED_PERMISSIONS or "PAYMENT" in act_upper and "EXECUTE" in act_upper:
            raise AgentPermissionDeniedError(
                f"Financial safety violation: Action '{action}' is strictly prohibited for AI agents."
            )

    @staticmethod
    def validate_invoice_baseline(
        invoice_total: Decimal,
        contract_milestone_amount: Optional[Decimal] = None,
        approved_change_amounts: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        """Validates that a proposed invoice draft does not exceed approved commercial baselines."""
        baseline = (contract_milestone_amount or Decimal("0.00")) + (approved_change_amounts or Decimal("0.00"))
        
        if baseline > Decimal("0.00") and invoice_total > baseline:
            excess = invoice_total - baseline
            return {
                "is_compliant": False,
                "reason": f"Invoice total ({invoice_total}) exceeds approved commercial baseline ({baseline}) by {excess}.",
                "baseline_amount": str(baseline),
                "excess_amount": str(excess),
                "requires_exception_review": True,
            }

        return {
            "is_compliant": True,
            "reason": "Invoice aligns with approved commercial milestones.",
            "baseline_amount": str(baseline),
            "excess_amount": "0.00",
            "requires_exception_review": False,
        }

    async def run(self, context: AgentContext) -> AgentResult:
        res = await self.execute(context)
        return AgentResult(
            status=res.get("status", "completed"),
            result=res,
            confidence="HIGH",
            metadata={"agent_id": self.agent_id}
        )
