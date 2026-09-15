"""Invoice generation, milestone mapping, sequence generation, and lifecycle management.
"""

from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from app.finance.base import (
    InvoiceStatus,
    PaymentTerms,
    TaxType,
    InvoiceTotals,
    FinancialExceptionType,
)
from app.finance.calculator import FinancialCalculator


class InvoicingManager:
    """Manages the creation, versioning, milestone conversion, and lifecycle of invoices."""

    @staticmethod
    def generate_invoice_number(prefix: str = "INV", year: Optional[int] = None, sequence: int = 1) -> str:
        """Generates a formatted sequential invoice number (e.g., INV-2026-0001)."""
        yr = year or datetime.now(timezone.utc).year
        return f"{prefix}-{yr}-{sequence:04d}"

    @staticmethod
    def calculate_due_date(issued_date: datetime, terms: PaymentTerms, custom_days: Optional[int] = None) -> datetime:
        """Calculates invoice due date based on payment terms."""
        if terms == PaymentTerms.DUE_ON_RECEIPT:
            return issued_date
        elif terms == PaymentTerms.NET_7:
            return issued_date + timedelta(days=7)
        elif terms == PaymentTerms.NET_14:
            return issued_date + timedelta(days=14)
        elif terms == PaymentTerms.NET_30:
            return issued_date + timedelta(days=30)
        elif terms == PaymentTerms.NET_60:
            return issued_date + timedelta(days=60)
        elif terms == PaymentTerms.NET_90:
            return issued_date + timedelta(days=90)
        elif terms == PaymentTerms.CUSTOM:
            days = custom_days if custom_days is not None else 30
            return issued_date + timedelta(days=days)
        return issued_date + timedelta(days=30)

    @classmethod
    def create_invoice_draft(
        cls,
        tenant_id: str,
        client_id: str,
        billing_profile_id: Optional[str] = None,
        project_id: Optional[str] = None,
        contract_id: Optional[str] = None,
        proposal_id: Optional[str] = None,
        currency: str = "USD",
        payment_terms: PaymentTerms = PaymentTerms.NET_30,
        custom_terms_days: Optional[int] = None,
        line_items: Optional[List[Dict[str, Any]]] = None,
        discount_rate_pct: Decimal = Decimal("0.00"),
        fixed_discount_amount: Decimal = Decimal("0.00"),
        tax_rate_pct: Decimal = Decimal("0.00"),
        tax_type: TaxType = TaxType.NONE,
        tax_region: Optional[str] = None,
        notes: Optional[str] = None,
        terms_and_conditions: Optional[str] = None,
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a fully calculated draft invoice with normalized line items."""
        now = datetime.now(timezone.utc)
        items = line_items or []
        
        # Calculate totals
        totals: InvoiceTotals = FinancialCalculator.calculate_invoice_totals(
            items=items,
            discount_rate_pct=discount_rate_pct,
            fixed_discount_amount=fixed_discount_amount,
            tax_rate_pct=tax_rate_pct,
            tax_type=tax_type,
            tax_region=tax_region,
        )

        due_date = cls.calculate_due_date(now, payment_terms, custom_terms_days)

        invoice_id = str(uuid.uuid4())
        draft = {
            "id": invoice_id,
            "tenant_id": tenant_id,
            "client_id": client_id,
            "billing_profile_id": billing_profile_id,
            "project_id": project_id,
            "contract_id": contract_id,
            "proposal_id": proposal_id,
            "invoice_number": f"DRAFT-{invoice_id[:8].upper()}",
            "version": 1,
            "status": InvoiceStatus.DRAFT.value,
            "currency": currency.upper(),
            "payment_terms": payment_terms.value,
            "custom_terms_days": custom_terms_days,
            "issue_date": now.isoformat(),
            "due_date": due_date.isoformat(),
            "subtotal": str(totals.subtotal),
            "discount_amount": str(totals.discount_amount),
            "taxable_amount": str(totals.taxable_amount),
            "tax_amount": str(totals.tax_amount),
            "total_amount": str(totals.total_amount),
            "amount_paid": "0.00",
            "balance_due": str(totals.total_amount),
            "tax_rate_pct": str(tax_rate_pct),
            "tax_type": tax_type.value,
            "tax_region": tax_region,
            "discount_rate_pct": str(discount_rate_pct),
            "fixed_discount_amount": str(fixed_discount_amount),
            "notes": notes,
            "terms_and_conditions": terms_and_conditions,
            "items": [item.to_dict() for item in totals.items],
            "created_by_user_id": created_by_user_id,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        return draft

    @classmethod
    def draft_from_contract_milestone(
        cls,
        tenant_id: str,
        client_id: str,
        contract_id: str,
        milestone_id: str,
        milestone_name: str,
        milestone_amount: Decimal,
        project_id: Optional[str] = None,
        currency: str = "USD",
        payment_terms: PaymentTerms = PaymentTerms.NET_30,
        tax_rate_pct: Decimal = Decimal("0.00"),
        tax_type: TaxType = TaxType.NONE,
        tax_region: Optional[str] = None,
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a draft invoice directly mapped to an approved contract milestone."""
        line_item = {
            "title": f"Milestone: {milestone_name}",
            "description": f"Deliverable billing for contract {contract_id}, milestone {milestone_id}",
            "quantity": "1.00",
            "unit_price": str(milestone_amount),
            "item_type": "milestone",
            "reference_type": "contract_milestone",
            "reference_id": milestone_id,
            "contract_id": contract_id,
        }

        return cls.create_invoice_draft(
            tenant_id=tenant_id,
            client_id=client_id,
            project_id=project_id,
            contract_id=contract_id,
            currency=currency,
            payment_terms=payment_terms,
            line_items=[line_item],
            tax_rate_pct=tax_rate_pct,
            tax_type=tax_type,
            tax_region=tax_region,
            notes=f"Generated from contract milestone: {milestone_name}",
            created_by_user_id=created_by_user_id,
        )

    @classmethod
    def draft_from_change_request(
        cls,
        tenant_id: str,
        client_id: str,
        change_request_id: str,
        change_request_title: str,
        price_amount: Decimal,
        project_id: Optional[str] = None,
        contract_id: Optional[str] = None,
        currency: str = "USD",
        payment_terms: PaymentTerms = PaymentTerms.NET_14,
        tax_rate_pct: Decimal = Decimal("0.00"),
        tax_type: TaxType = TaxType.NONE,
        tax_region: Optional[str] = None,
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a draft invoice mapped to an approved Change Request."""
        line_item = {
            "title": f"Change Request: {change_request_title}",
            "description": f"Scope addition billing for CR {change_request_id}",
            "quantity": "1.00",
            "unit_price": str(price_amount),
            "item_type": "change_request",
            "reference_type": "change_request",
            "reference_id": change_request_id,
            "contract_id": contract_id,
        }

        return cls.create_invoice_draft(
            tenant_id=tenant_id,
            client_id=client_id,
            project_id=project_id,
            contract_id=contract_id,
            currency=currency,
            payment_terms=payment_terms,
            line_items=[line_item],
            tax_rate_pct=tax_rate_pct,
            tax_type=tax_type,
            tax_region=tax_region,
            notes=f"Generated from approved change request: {change_request_title}",
            created_by_user_id=created_by_user_id,
        )

    @staticmethod
    def validate_transition(current_status: str, target_status: str) -> bool:
        """Enforces valid financial state transitions for invoices."""
        curr = InvoiceStatus(current_status.upper())
        target = InvoiceStatus(target_status.upper())

        allowed_transitions = {
            InvoiceStatus.DRAFT: [InvoiceStatus.PENDING_APPROVAL, InvoiceStatus.ISSUED, InvoiceStatus.VOID],
            InvoiceStatus.PENDING_APPROVAL: [InvoiceStatus.APPROVED, InvoiceStatus.DRAFT, InvoiceStatus.REJECTED, InvoiceStatus.VOID],
            InvoiceStatus.APPROVED: [InvoiceStatus.ISSUED, InvoiceStatus.VOID],
            InvoiceStatus.REJECTED: [InvoiceStatus.DRAFT, InvoiceStatus.VOID],
            InvoiceStatus.ISSUED: [InvoiceStatus.PARTIALLY_PAID, InvoiceStatus.PAID, InvoiceStatus.OVERDUE, InvoiceStatus.DISPUTED, InvoiceStatus.VOID, InvoiceStatus.WRITTEN_OFF],
            InvoiceStatus.PARTIALLY_PAID: [InvoiceStatus.PAID, InvoiceStatus.OVERDUE, InvoiceStatus.DISPUTED, InvoiceStatus.VOID, InvoiceStatus.WRITTEN_OFF],
            InvoiceStatus.PAID: [InvoiceStatus.REFUNDED, InvoiceStatus.PARTIALLY_REFUNDED, InvoiceStatus.DISPUTED],
            InvoiceStatus.OVERDUE: [InvoiceStatus.PARTIALLY_PAID, InvoiceStatus.PAID, InvoiceStatus.DISPUTED, InvoiceStatus.WRITTEN_OFF, InvoiceStatus.VOID],
            InvoiceStatus.DISPUTED: [InvoiceStatus.ISSUED, InvoiceStatus.PARTIALLY_PAID, InvoiceStatus.PAID, InvoiceStatus.VOID, InvoiceStatus.WRITTEN_OFF],
            InvoiceStatus.PARTIALLY_REFUNDED: [InvoiceStatus.REFUNDED],
            InvoiceStatus.REFUNDED: [],
            InvoiceStatus.VOID: [],
            InvoiceStatus.WRITTEN_OFF: [],
        }

        return target in allowed_transitions.get(curr, [])
