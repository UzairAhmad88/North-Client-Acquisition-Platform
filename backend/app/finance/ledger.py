"""Append-only immutable financial ledger and accounting entries.
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from app.finance.base import (
    LedgerDirection,
    FinancialAccountType,
)
from app.finance.calculator import FinancialCalculator


class LedgerManager:
    """Manages the creation and balancing of immutable, append-only financial ledger entries."""

    @staticmethod
    def create_journal_entry(
        tenant_id: str,
        description: str,
        reference_type: str,
        reference_id: str,
        entries: List[Dict[str, Any]],
        currency: str = "USD",
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a balanced double-entry set of ledger postings.
        
        entries format:
        [
            {"account_id": "acc_1", "direction": "debit", "amount": "100.00"},
            {"account_id": "acc_2", "direction": "credit", "amount": "100.00"},
        ]
        """
        now = datetime.now(timezone.utc)
        group_id = str(uuid.uuid4())

        total_debits = Decimal("0.00")
        total_credits = Decimal("0.00")
        posted_entries = []

        for e in entries:
            amt = FinancialCalculator.round_currency(Decimal(str(e["amount"])))
            dir_str = str(e["direction"]).upper()
            if dir_str == LedgerDirection.DEBIT.value:
                total_debits += amt
            elif dir_str == LedgerDirection.CREDIT.value:
                total_credits += amt
            else:
                raise ValueError(f"Invalid ledger direction: {dir_str}")

            entry_id = str(uuid.uuid4())
            posted_entries.append({
                "id": entry_id,
                "tenant_id": tenant_id,
                "entry_group_id": group_id,
                "account_id": e["account_id"],
                "account_type": e.get("account_type"),
                "direction": dir_str.lower(),
                "amount": str(amt),
                "currency": currency.upper(),
                "reference_type": reference_type,
                "reference_id": reference_id,
                "description": e.get("description", description),
                "created_by_user_id": created_by_user_id,
                "posted_at": now.isoformat(),
                "is_reversed": False,
            })

        # Balance verification
        if total_debits != total_credits:
            raise ValueError(f"Unbalanced journal entry: Debits ({total_debits}) != Credits ({total_credits})")

        return {
            "entry_group_id": group_id,
            "tenant_id": tenant_id,
            "description": description,
            "reference_type": reference_type,
            "reference_id": reference_id,
            "currency": currency.upper(),
            "total_amount": str(total_debits),
            "entries_count": len(posted_entries),
            "entries": posted_entries,
            "posted_at": now.isoformat(),
        }

    @classmethod
    def post_invoice_issuance(
        cls,
        tenant_id: str,
        invoice_id: str,
        invoice_number: str,
        accounts_receivable_account_id: str,
        revenue_account_id: str,
        total_amount: Decimal,
        currency: str = "USD",
        tax_account_id: Optional[str] = None,
        tax_amount: Decimal = Decimal("0.00"),
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Posts invoice issuance: Debit Accounts Receivable, Credit Revenue (+ Credit Tax Payable)."""
        rev_amount = total_amount - tax_amount
        entries = [
            {
                "account_id": accounts_receivable_account_id,
                "account_type": FinancialAccountType.ACCOUNTS_RECEIVABLE.value,
                "direction": LedgerDirection.DEBIT.value,
                "amount": str(total_amount),
                "description": f"Invoice {invoice_number} issued",
            },
            {
                "account_id": revenue_account_id,
                "account_type": FinancialAccountType.REVENUE.value,
                "direction": LedgerDirection.CREDIT.value,
                "amount": str(rev_amount),
                "description": f"Revenue recognized from Invoice {invoice_number}",
            }
        ]

        if tax_amount > Decimal("0.00") and tax_account_id:
            entries.append({
                "account_id": tax_account_id,
                "account_type": FinancialAccountType.TAX_PAYABLE.value,
                "direction": LedgerDirection.CREDIT.value,
                "amount": str(tax_amount),
                "description": f"Sales tax payable on Invoice {invoice_number}",
            })

        return cls.create_journal_entry(
            tenant_id=tenant_id,
            description=f"Invoice Issued: {invoice_number}",
            reference_type="invoice",
            reference_id=invoice_id,
            entries=entries,
            currency=currency,
            created_by_user_id=created_by_user_id,
        )

    @classmethod
    def post_payment_received(
        cls,
        tenant_id: str,
        payment_id: str,
        invoice_id: str,
        cash_account_id: str,
        accounts_receivable_account_id: str,
        amount_paid: Decimal,
        currency: str = "USD",
        fee_account_id: Optional[str] = None,
        processing_fee: Decimal = Decimal("0.00"),
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Posts payment receipt: Debit Cash/Bank (+ Debit Fee Expense), Credit Accounts Receivable."""
        net_cash = amount_paid - processing_fee
        entries = [
            {
                "account_id": cash_account_id,
                "account_type": FinancialAccountType.CASH.value,
                "direction": LedgerDirection.DEBIT.value,
                "amount": str(net_cash),
                "description": f"Cash received for Payment {payment_id}",
            },
            {
                "account_id": accounts_receivable_account_id,
                "account_type": FinancialAccountType.ACCOUNTS_RECEIVABLE.value,
                "direction": LedgerDirection.CREDIT.value,
                "amount": str(amount_paid),
                "description": f"A/R cleared for Payment {payment_id} on Invoice {invoice_id}",
            }
        ]

        if processing_fee > Decimal("0.00") and fee_account_id:
            entries.append({
                "account_id": fee_account_id,
                "account_type": FinancialAccountType.EXPENSE.value,
                "direction": LedgerDirection.DEBIT.value,
                "amount": str(processing_fee),
                "description": f"Payment processing fee for Payment {payment_id}",
            })

        return cls.create_journal_entry(
            tenant_id=tenant_id,
            description=f"Payment Received: {payment_id}",
            reference_type="payment",
            reference_id=payment_id,
            entries=entries,
            currency=currency,
            created_by_user_id=created_by_user_id,
        )

    @classmethod
    def create_reversing_adjustment(
        cls,
        tenant_id: str,
        original_entry_group_id: str,
        original_entries: List[Dict[str, Any]],
        reason: str,
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a non-destructive reversing entry for a prior journal group."""
        reversing_entries = []
        for e in original_entries:
            # Invert direction
            orig_dir = e["direction"].lower()
            new_dir = LedgerDirection.CREDIT.value if orig_dir == LedgerDirection.DEBIT.value else LedgerDirection.DEBIT.value
            reversing_entries.append({
                "account_id": e["account_id"],
                "account_type": e.get("account_type"),
                "direction": new_dir,
                "amount": e["amount"],
                "description": f"Reversal of {e.get('description', '')}: {reason}",
            })

        return cls.create_journal_entry(
            tenant_id=tenant_id,
            description=f"Adjustment Reversal: {reason}",
            reference_type="ledger_reversal",
            reference_id=original_entry_group_id,
            entries=reversing_entries,
            created_by_user_id=created_by_user_id,
        )
