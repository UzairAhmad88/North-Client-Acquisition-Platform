"""FastAPI endpoints for Financial Accounts, Double-Entry Ledger, Profitability, and Cash Flow Forecasting."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.finance.service import FinancialPlatformService
from app.models.user import User
from app.repositories.finance import FinanceRepository
from app.schemas.finance import (
    CashFlowForecastRequest,
    FinancialAccountCreate,
    FinancialAccountResponse,
    JournalEntryRequest,
    LedgerEntryResponse,
    ProjectProfitabilityRequest,
)

router = APIRouter(prefix="/finance", tags=["Financial Operations & Intelligence"])
_finance_service = FinancialPlatformService()


# --- Financial Accounts ---

@router.post("/accounts", response_model=FinancialAccountResponse, summary="Create a chart of accounts entry")
def create_financial_account(
    payload: FinancialAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_financial_account(tenant_id=tenant_id, data=payload.dict())


@router.get("/accounts", response_model=List[FinancialAccountResponse], summary="List chart of accounts")
def list_financial_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_financial_accounts(tenant_id=tenant_id)


# --- Ledger Entries ---

@router.post("/ledger/journal", response_model=List[LedgerEntryResponse], summary="Post balanced journal entry to ledger")
def post_journal_entry(
    payload: JournalEntryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    raw_items = [itm.dict() for itm in payload.items]
    try:
        journal_group = _finance_service.ledger.create_journal_entry(
            tenant_id=tenant_id,
            description=payload.description,
            reference_type=payload.reference_type,
            reference_id=payload.reference_id,
            entries=raw_items,
            currency=payload.currency,
            created_by_user_id=user_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    records = repo.create_ledger_entries(journal_group["entries"])
    return records


@router.get("/ledger/entries", response_model=List[LedgerEntryResponse], summary="List immutable ledger entries")
def list_ledger_entries(
    account_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_ledger_entries(tenant_id=tenant_id, account_id=account_id, limit=limit)


# --- Profitability & Forecast ---

@router.post("/profitability/analyze", summary="Analyze project profitability and cost variance")
def analyze_profitability(
    payload: ProjectProfitabilityRequest,
    current_user: User = Depends(get_current_active_user),
):
    user_role = getattr(current_user, "role", "admin")
    analysis = _finance_service.analyze_project(
        project_id=payload.project_id,
        contracted_revenue=payload.contracted_revenue,
        invoiced_revenue=payload.invoiced_revenue,
        collected_revenue=payload.collected_revenue,
        estimated_cost=payload.estimated_cost,
        labor_hours_logged=payload.labor_hours_logged,
        labor_hourly_cost_rate=payload.labor_hourly_cost_rate,
        ai_token_cost=payload.ai_token_cost,
        infrastructure_cost=payload.infrastructure_cost,
        subcontractor_cost=payload.subcontractor_cost,
        other_expenses=payload.other_expenses,
        user_role=user_role,
    )
    return analysis


@router.post("/forecast/cash-flow", summary="Forecast cash flow runway and billing inflows")
def forecast_cash_flow(
    payload: CashFlowForecastRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    
    # Fetch open invoices
    invoices = repo.list_invoices(tenant_id=tenant_id, status=None)
    open_invoices = [
        {"balance_due": str(inv.balance_due)}
        for inv in invoices
        if inv.status in ("issued", "partially_paid", "overdue")
    ]

    forecast = _finance_service.profitability.forecast_cash_flow(
        active_schedules=[],
        outstanding_invoices=open_invoices,
        projected_monthly_burn=payload.projected_monthly_burn,
        months_ahead=payload.months_ahead,
    )
    return forecast
