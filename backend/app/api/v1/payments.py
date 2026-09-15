"""FastAPI endpoints for Payments, Provider Charges, Refunds, and Reconciliations."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.finance.service import FinancialPlatformService
from app.finance.base import InvoiceStatus, PaymentStatus
from app.models.user import User
from app.repositories.finance import FinanceRepository
from app.schemas.finance import (
    PaymentChargeRequest,
    PaymentResponse,
    RefundProcessRequest,
    RefundResponse,
)
from integrations.payments.models import PaymentProviderType

router = APIRouter(prefix="/payments", tags=["Payments & Settlements"])
_finance_service = FinancialPlatformService()


@router.post("/charge", response_model=PaymentResponse, summary="Process invoice payment charge")
def charge_payment(
    payload: PaymentChargeRequest,
    cash_account_id: Optional[str] = Query(None),
    ar_account_id: Optional[str] = Query(None),
    fee_account_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    inv = repo.get_invoice(payload.invoice_id, tenant_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    provider_type = PaymentProviderType(payload.provider_type.lower()) if payload.provider_type else PaymentProviderType.MOCK

    result = _finance_service.process_payment(
        tenant_id=tenant_id,
        invoice_id=payload.invoice_id,
        amount=payload.amount,
        currency=payload.currency,
        payment_method=payload.payment_method,
        customer_id=payload.customer_id,
        provider_type=provider_type,
        idempotency_key=payload.idempotency_key,
        metadata=payload.metadata,
        cash_account_id=cash_account_id,
        ar_account_id=ar_account_id,
        fee_account_id=fee_account_id,
        created_by_user_id=user_id,
    )

    payment_data = result["payment"]
    payment_data["client_id"] = inv.client_id
    payment_model = repo.create_payment(payment_data)

    if result.get("ledger_entry"):
        repo.create_ledger_entries(result["ledger_entry"]["entries"])

    # Update invoice balance if payment succeeded
    if payment_model.status == PaymentStatus.SUCCEEDED.value:
        new_paid = inv.amount_paid + payment_model.amount
        new_balance = inv.total_amount - new_paid
        new_status = InvoiceStatus.PAID.value if new_balance <= Decimal("0.00") else InvoiceStatus.PARTIALLY_PAID.value
        repo.update_invoice_status(
            invoice_id=inv.id,
            tenant_id=tenant_id,
            new_status=new_status,
            amount_paid=new_paid,
            balance_due=max(Decimal("0.00"), new_balance),
        )

    return payment_model


@router.get("", response_model=List[PaymentResponse], summary="List payment transactions")
def list_payments(
    invoice_id: Optional[str] = Query(None),
    client_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_payments(tenant_id=tenant_id, invoice_id=invoice_id, client_id=client_id)


@router.post("/refund", response_model=RefundResponse, summary="Process refund for a payment")
def process_refund(
    payload: RefundProcessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    payments = repo.list_payments(tenant_id=tenant_id)
    target_payment = next((p for p in payments if p.id == payload.payment_id), None)
    if not target_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

    result = _finance_service.process_refund(
        tenant_id=tenant_id,
        payment_id=target_payment.id,
        provider_payment_id=target_payment.provider_payment_id or "mock_charge_id",
        amount=payload.amount,
        currency=payload.currency,
        reason=payload.reason,
        idempotency_key=payload.idempotency_key,
        created_by_user_id=user_id,
    )

    refund_data = result["refund"]
    refund_data["invoice_id"] = target_payment.invoice_id
    refund_model = repo.create_refund(refund_data)
    return refund_model
