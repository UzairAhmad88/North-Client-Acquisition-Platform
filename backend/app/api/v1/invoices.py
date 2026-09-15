"""FastAPI endpoints for Invoices, Milestones, Approvals, and Issuance."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.finance.service import FinancialPlatformService
from app.finance.base import InvoiceStatus, PaymentTerms, TaxType
from app.models.user import User
from app.repositories.finance import FinanceRepository
from app.schemas.finance import (
    InvoiceCreate,
    InvoiceDetailResponse,
    InvoiceResponse,
    InvoiceApprovalRequest,
)

router = APIRouter(prefix="/invoices", tags=["Billing & Invoices"])
_finance_service = FinancialPlatformService()


@router.post("", response_model=InvoiceResponse, summary="Create a draft invoice")
def create_invoice(
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    items_dict = [itm.dict() for itm in payload.items]
    
    draft = _finance_service.create_invoice(
        tenant_id=tenant_id,
        client_id=payload.client_id,
        billing_profile_id=payload.billing_profile_id,
        project_id=payload.project_id,
        contract_id=payload.contract_id,
        proposal_id=payload.proposal_id,
        currency=payload.currency,
        payment_terms=PaymentTerms(payload.payment_terms),
        custom_terms_days=payload.custom_terms_days,
        line_items=items_dict,
        discount_rate_pct=payload.discount_rate_pct,
        fixed_discount_amount=payload.fixed_discount_amount,
        tax_rate_pct=payload.tax_rate_pct,
        tax_type=TaxType(payload.tax_type),
        tax_region=payload.tax_region,
        notes=payload.notes,
        terms_and_conditions=payload.terms_and_conditions,
        created_by_user_id=user_id,
    )

    invoice_model = repo.create_invoice(draft, draft["items"])
    return invoice_model


@router.get("", response_model=List[InvoiceResponse], summary="List invoices")
def list_invoices(
    client_id: Optional[str] = Query(None),
    project_id: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_invoices(
        tenant_id=tenant_id,
        client_id=client_id,
        project_id=project_id,
        status=status_filter,
        limit=limit,
        offset=offset,
    )


@router.get("/{invoice_id}", response_model=InvoiceDetailResponse, summary="Get invoice details")
def get_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    inv = repo.get_invoice(invoice_id, tenant_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    
    items = repo.get_invoice_items(invoice_id)
    resp = InvoiceDetailResponse.from_orm(inv)
    resp.items = items
    return resp


@router.post("/{invoice_id}/approve", response_model=InvoiceResponse, summary="Human approval for invoice")
def approve_invoice(
    invoice_id: str,
    payload: InvoiceApprovalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    inv = repo.get_invoice(invoice_id, tenant_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    new_status = InvoiceStatus.APPROVED.value if payload.status == "approved" else InvoiceStatus.REJECTED.value
    updated = repo.update_invoice_status(
        invoice_id=invoice_id,
        tenant_id=tenant_id,
        new_status=new_status,
        approved_by_user_id=user_id,
    )
    return updated


@router.post("/{invoice_id}/issue", response_model=InvoiceResponse, summary="Issue invoice with official numbering and ledger posting")
def issue_invoice(
    invoice_id: str,
    ar_account_id: Optional[str] = Query(None),
    revenue_account_id: Optional[str] = Query(None),
    tax_account_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    inv = repo.get_invoice(invoice_id, tenant_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")

    # Generate sequence number count
    count = len(repo.list_invoices(tenant_id=tenant_id)) + 1
    
    inv_data = {
        "id": inv.id,
        "tenant_id": inv.tenant_id,
        "status": inv.status,
        "total_amount": str(inv.total_amount),
        "currency": inv.currency,
        "tax_amount": str(inv.tax_amount),
    }

    issue_result = _finance_service.issue_invoice(
        invoice_data=inv_data,
        sequence_number=count,
        ar_account_id=ar_account_id,
        revenue_account_id=revenue_account_id,
        tax_account_id=tax_account_id,
        issued_by_user_id=user_id,
    )

    if issue_result.get("ledger_entry"):
        repo.create_ledger_entries(issue_result["ledger_entry"]["entries"])

    updated = repo.update_invoice_status(
        invoice_id=invoice_id,
        tenant_id=tenant_id,
        new_status=InvoiceStatus.ISSUED.value,
        invoice_number=issue_result["invoice"]["invoice_number"],
        issued_by_user_id=user_id,
    )
    return updated
