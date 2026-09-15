"""Financial Platform Service coordinating billing, invoicing, payments, reconciliation, ledger, and profitability.
"""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from app.finance.base import (
    InvoiceStatus,
    PaymentStatus,
    PaymentTerms,
    TaxType,
    LedgerDirection,
    FinancialAccountType,
    InvoiceTotals,
)
from app.finance.calculator import FinancialCalculator
from app.finance.invoicing import InvoicingManager
from app.finance.reconciliation import ReconciliationManager
from app.finance.ledger import LedgerManager
from app.finance.profitability import ProfitabilityManager
from app.finance.authorization import FinancialAuthorizationManager
from integrations.payments.service import PaymentService
from integrations.payments.models import PaymentProviderType
from integrations.payments.base import PaymentRequest, RefundRequest


class FinancialPlatformService:
    """Unified service orchestrating end-to-end commercial operations."""

    def __init__(
        self,
        payment_service: Optional[PaymentService] = None,
        default_provider_type: PaymentProviderType = PaymentProviderType.MOCK,
    ):
        self.payment_service = payment_service or PaymentService(default_provider=default_provider_type)
        self.invoicing = InvoicingManager()
        self.reconciliation = ReconciliationManager()
        self.ledger = LedgerManager()
        self.profitability = ProfitabilityManager()
        self.auth = FinancialAuthorizationManager()

    # --- Invoicing Operations ---

    def create_invoice(
        self,
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
        """Creates a new draft invoice."""
        return self.invoicing.create_invoice_draft(
            tenant_id=tenant_id,
            client_id=client_id,
            billing_profile_id=billing_profile_id,
            project_id=project_id,
            contract_id=contract_id,
            proposal_id=proposal_id,
            currency=currency,
            payment_terms=payment_terms,
            custom_terms_days=custom_terms_days,
            line_items=line_items,
            discount_rate_pct=discount_rate_pct,
            fixed_discount_amount=fixed_discount_amount,
            tax_rate_pct=tax_rate_pct,
            tax_type=tax_type,
            tax_region=tax_region,
            notes=notes,
            terms_and_conditions=terms_and_conditions,
            created_by_user_id=created_by_user_id,
        )

    def issue_invoice(
        self,
        invoice_data: Dict[str, Any],
        sequence_number: int,
        prefix: str = "INV",
        ar_account_id: Optional[str] = None,
        revenue_account_id: Optional[str] = None,
        tax_account_id: Optional[str] = None,
        issued_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Finalizes and issues an invoice, assigning an official invoice number and posting ledger entries."""
        now = datetime.now(timezone.utc)
        inv = dict(invoice_data)
        
        if not self.invoicing.validate_transition(inv.get("status", InvoiceStatus.DRAFT.value), InvoiceStatus.ISSUED.value):
            raise ValueError(f"Invalid transition from {inv.get('status')} to {InvoiceStatus.ISSUED.value}")

        inv_num = self.invoicing.generate_invoice_number(prefix=prefix, sequence=sequence_number)
        inv["invoice_number"] = inv_num
        inv["status"] = InvoiceStatus.ISSUED.value
        inv["issue_date"] = now.isoformat()
        inv["issued_by_user_id"] = issued_by_user_id
        inv["updated_at"] = now.isoformat()

        # Optional automatic ledger posting
        ledger_entry = None
        if ar_account_id and revenue_account_id:
            ledger_entry = self.ledger.post_invoice_issuance(
                tenant_id=inv["tenant_id"],
                invoice_id=inv["id"],
                invoice_number=inv_num,
                accounts_receivable_account_id=ar_account_id,
                revenue_account_id=revenue_account_id,
                total_amount=Decimal(str(inv["total_amount"])),
                currency=inv["currency"],
                tax_account_id=tax_account_id,
                tax_amount=Decimal(str(inv.get("tax_amount", "0.00"))),
                created_by_user_id=issued_by_user_id,
            )

        return {
            "invoice": inv,
            "ledger_entry": ledger_entry,
        }

    # --- Payment & Reconciliation Operations ---

    def process_payment(
        self,
        tenant_id: str,
        invoice_id: str,
        amount: Decimal,
        currency: str = "USD",
        payment_method: str = "credit_card",
        customer_id: Optional[str] = None,
        provider_type: Optional[PaymentProviderType] = None,
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        cash_account_id: Optional[str] = None,
        ar_account_id: Optional[str] = None,
        fee_account_id: Optional[str] = None,
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Processes a payment through provider, updates payment status, and posts ledger entries."""
        req = PaymentRequest(
            amount=amount,
            currency=currency.upper(),
            payment_method=payment_method,
            customer_id=customer_id,
            invoice_id=invoice_id,
            tenant_id=tenant_id,
            idempotency_key=idempotency_key or str(uuid.uuid4()),
            metadata=metadata or {},
        )

        result = self.payment_service.charge(req, provider_type=provider_type)

        payment_record = {
            "id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "invoice_id": invoice_id,
            "provider_type": (provider_type or self.payment_service.default_provider).value,
            "provider_payment_id": result.provider_payment_id,
            "amount": str(result.amount),
            "currency": result.currency,
            "status": PaymentStatus.SUCCEEDED.value if result.is_success else PaymentStatus.FAILED.value,
            "payment_method": payment_method,
            "fee_amount": str(result.fee_amount),
            "error_code": result.error_code,
            "error_message": result.error_message,
            "raw_response": result.raw_response,
            "created_by_user_id": created_by_user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # Ledger posting on success
        ledger_entry = None
        if result.is_success and cash_account_id and ar_account_id:
            ledger_entry = self.ledger.post_payment_received(
                tenant_id=tenant_id,
                payment_id=payment_record["id"],
                invoice_id=invoice_id,
                cash_account_id=cash_account_id,
                accounts_receivable_account_id=ar_account_id,
                amount_paid=result.amount,
                currency=result.currency,
                fee_account_id=fee_account_id,
                processing_fee=result.fee_amount,
                created_by_user_id=created_by_user_id,
            )

        return {
            "payment": payment_record,
            "result": result.to_dict(),
            "ledger_entry": ledger_entry,
        }

    def process_refund(
        self,
        tenant_id: str,
        payment_id: str,
        provider_payment_id: str,
        amount: Decimal,
        currency: str = "USD",
        reason: str = "Customer requested refund",
        provider_type: Optional[PaymentProviderType] = None,
        idempotency_key: Optional[str] = None,
        created_by_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Issues a refund through provider and records the refund transaction."""
        req = RefundRequest(
            payment_id=provider_payment_id,
            amount=amount,
            currency=currency.upper(),
            reason=reason,
            tenant_id=tenant_id,
            idempotency_key=idempotency_key or str(uuid.uuid4()),
        )

        result = self.payment_service.refund(req, provider_type=provider_type)

        refund_record = {
            "id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "payment_id": payment_id,
            "provider_refund_id": result.provider_refund_id,
            "amount": str(result.amount),
            "currency": result.currency,
            "status": "succeeded" if result.is_success else "failed",
            "reason": reason,
            "error_code": result.error_code,
            "error_message": result.error_message,
            "created_by_user_id": created_by_user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        return {
            "refund": refund_record,
            "result": result.to_dict(),
        }

    # --- Financial Intelligence & Profitability ---

    def analyze_project(
        self,
        project_id: str,
        contracted_revenue: Decimal,
        invoiced_revenue: Decimal,
        collected_revenue: Decimal,
        estimated_cost: Decimal,
        labor_hours_logged: Decimal = Decimal("0.00"),
        labor_hourly_cost_rate: Decimal = Decimal("0.00"),
        ai_token_cost: Decimal = Decimal("0.00"),
        infrastructure_cost: Decimal = Decimal("0.00"),
        subcontractor_cost: Decimal = Decimal("0.00"),
        other_expenses: Decimal = Decimal("0.00"),
        user_role: str = "admin",
    ) -> Dict[str, Any]:
        """Calculates project profitability and applies client privacy masking."""
        raw_analysis = self.profitability.analyze_project_profitability(
            project_id=project_id,
            contracted_revenue=contracted_revenue,
            invoiced_revenue=invoiced_revenue,
            collected_revenue=collected_revenue,
            estimated_cost=estimated_cost,
            labor_hours_logged=labor_hours_logged,
            labor_hourly_cost_rate=labor_hourly_cost_rate,
            ai_token_cost=ai_token_cost,
            infrastructure_cost=infrastructure_cost,
            subcontractor_cost=subcontractor_cost,
            other_expenses=other_expenses,
        )

        is_client = (user_role.lower() == "client")
        return self.auth.mask_client_payload(raw_analysis, is_client=is_client)
