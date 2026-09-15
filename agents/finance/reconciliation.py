"""Reconciliation assistant for Finance Agent.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from app.finance.reconciliation import ReconciliationManager


class FinancialReconciliationAssistant:
    """Evaluates unmatched transactions and prepares suggestions for human accountants."""

    @classmethod
    def analyze_unmatched_transactions(
        cls,
        unmatched_provider_events: List[Dict[str, Any]],
        open_invoices: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Scans unmatched provider events against open invoices to suggest possible matches."""
        suggestions = []
        for event in unmatched_provider_events:
            ev_amt = Decimal(str(event.get("amount", "0.00")))
            ev_curr = str(event.get("currency", "USD")).upper()
            ev_id = event.get("id")

            # Try exact amount and currency match
            potential_invoices = [
                inv for inv in open_invoices
                if str(inv.get("currency", "USD")).upper() == ev_curr
                and Decimal(str(inv.get("balance_due", "0.00"))) == ev_amt
            ]

            if potential_invoices:
                best_match = potential_invoices[0]
                suggestions.append({
                    "provider_event_id": ev_id,
                    "suggested_invoice_id": best_match.get("id"),
                    "suggested_invoice_number": best_match.get("invoice_number"),
                    "confidence_score": "0.95" if len(potential_invoices) == 1 else "0.75",
                    "match_reason": f"Exact balance match ({ev_amt} {ev_curr}) found on invoice {best_match.get('invoice_number')}",
                    "requires_human_approval": True,
                })
            else:
                suggestions.append({
                    "provider_event_id": ev_id,
                    "suggested_invoice_id": None,
                    "confidence_score": "0.00",
                    "match_reason": "No exact matching invoice balance found in open invoices.",
                    "requires_human_approval": True,
                })

        return suggestions

    async def run(self, context: AgentContext) -> AgentResult:
        res = await self.execute(context)
        return AgentResult(
            status=res.get("status", "completed"),
            result=res,
            confidence="HIGH",
            metadata={"agent_id": self.agent_id}
        )
