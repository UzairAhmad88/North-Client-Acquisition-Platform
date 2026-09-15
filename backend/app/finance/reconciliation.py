"""Payment reconciliation logic, transaction matching, discrepancy detection, and suggestions.
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from app.finance.base import (
    InvoiceStatus,
    PaymentStatus,
    FinancialExceptionType,
)
from app.finance.calculator import FinancialCalculator


class ReconciliationManager:
    """Handles automated matching of payment provider transactions with invoices and system payments."""

    @classmethod
    def match_transaction(
        cls,
        provider_transaction_id: str,
        provider_amount: Decimal,
        provider_currency: str,
        provider_status: str,
        invoice_id: Optional[str],
        invoice_balance_due: Optional[Decimal],
        invoice_currency: Optional[str],
        existing_payment_amount: Optional[Decimal] = None,
        provider_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Evaluates a provider transaction against an invoice and determines match status and recommendations."""
        meta = provider_metadata or {}
        now = datetime.now(timezone.utc)
        reconciliation_id = str(uuid.uuid4())

        # If no invoice could be matched
        if not invoice_id or invoice_balance_due is None:
            return {
                "id": reconciliation_id,
                "status": "unmatched",
                "discrepancy_type": "missing_invoice_reference",
                "matched_amount": "0.00",
                "discrepancy_amount": str(provider_amount),
                "is_exact_match": False,
                "recommendation": "Manual review required. Transaction received without valid invoice reference.",
                "requires_human_approval": True,
                "processed_at": now.isoformat(),
            }

        # Currency mismatch check
        if invoice_currency and provider_currency.upper() != invoice_currency.upper():
            return {
                "id": reconciliation_id,
                "status": "mismatch",
                "discrepancy_type": "currency_mismatch",
                "matched_amount": "0.00",
                "discrepancy_amount": str(provider_amount),
                "is_exact_match": False,
                "recommendation": f"Currency mismatch: provider sent {provider_currency} for invoice currency {invoice_currency}.",
                "requires_human_approval": True,
                "processed_at": now.isoformat(),
            }

        # Compare amounts
        amount_diff = provider_amount - invoice_balance_due

        if amount_diff == Decimal("0.00"):
            return {
                "id": reconciliation_id,
                "status": "matched",
                "discrepancy_type": None,
                "matched_amount": str(provider_amount),
                "discrepancy_amount": "0.00",
                "is_exact_match": True,
                "resulting_invoice_status": InvoiceStatus.PAID.value,
                "recommendation": "Auto-reconcile exact match. Mark invoice as PAID.",
                "requires_human_approval": False,
                "processed_at": now.isoformat(),
            }
        elif amount_diff < Decimal("0.00"):
            # Partial payment
            remaining = invoice_balance_due - provider_amount
            return {
                "id": reconciliation_id,
                "status": "partial_match",
                "discrepancy_type": "partial_payment",
                "matched_amount": str(provider_amount),
                "discrepancy_amount": str(remaining),
                "is_exact_match": False,
                "resulting_invoice_status": InvoiceStatus.PARTIALLY_PAID.value,
                "remaining_balance": str(remaining),
                "recommendation": f"Partial payment received. Remaining balance: {remaining} {provider_currency}.",
                "requires_human_approval": False,
                "processed_at": now.isoformat(),
            }
        else:
            # Overpayment
            overage = amount_diff
            return {
                "id": reconciliation_id,
                "status": "overpaid",
                "discrepancy_type": "overpayment",
                "matched_amount": str(invoice_balance_due),
                "discrepancy_amount": str(overage),
                "is_exact_match": False,
                "resulting_invoice_status": InvoiceStatus.PAID.value,
                "overpaid_amount": str(overage),
                "recommendation": f"Overpayment detected: excess of {overage} {provider_currency}. Credit note or refund recommended.",
                "requires_human_approval": True,
                "processed_at": now.isoformat(),
            }

    @classmethod
    def generate_reconciliation_batch_summary(
        cls,
        records: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generates statistical metrics for a batch of reconciliations."""
        total_count = len(records)
        matched_count = sum(1 for r in records if r.get("status") == "matched")
        partial_count = sum(1 for r in records if r.get("status") == "partial_match")
        unmatched_count = sum(1 for r in records if r.get("status") in ("unmatched", "mismatch", "overpaid"))

        total_matched_volume = sum(
            (Decimal(str(r.get("matched_amount", "0.00"))) for r in records),
            Decimal("0.00")
        )
        total_discrepancy_volume = sum(
            (Decimal(str(r.get("discrepancy_amount", "0.00"))) for r in records),
            Decimal("0.00")
        )

        return {
            "total_transactions": total_count,
            "fully_matched": matched_count,
            "partially_matched": partial_count,
            "unmatched_or_discrepant": unmatched_count,
            "match_rate_pct": str(
                FinancialCalculator.calculate_margin_pct(Decimal(str(matched_count)), Decimal(str(total_count)))
                if total_count > 0 else Decimal("0.00")
            ),
            "total_matched_volume": str(FinancialCalculator.round_currency(total_matched_volume)),
            "total_discrepancy_volume": str(FinancialCalculator.round_currency(total_discrepancy_volume)),
        }
