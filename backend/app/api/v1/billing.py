"""FastAPI endpoints for Billing Profiles, Tax Profiles, and Currencies."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.repositories.finance import FinanceRepository
from app.schemas.finance import (
    BillingProfileCreate,
    BillingProfileResponse,
    CurrencyCreate,
    CurrencyResponse,
    TaxProfileCreate,
    TaxProfileResponse,
)

router = APIRouter(prefix="/billing", tags=["Billing Configuration & Profiles"])


# --- Billing Profiles ---

@router.post("/profiles", response_model=BillingProfileResponse, summary="Create a billing profile")
def create_billing_profile(
    payload: BillingProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_billing_profile(tenant_id=tenant_id, data=payload.dict())


@router.get("/profiles", response_model=List[BillingProfileResponse], summary="List billing profiles")
def list_billing_profiles(
    client_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_billing_profiles(tenant_id=tenant_id, client_id=client_id)


# --- Tax Profiles ---

@router.post("/taxes", response_model=TaxProfileResponse, summary="Create a tax profile")
def create_tax_profile(
    payload: TaxProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_tax_profile(tenant_id=tenant_id, data=payload.dict())


@router.get("/taxes", response_model=List[TaxProfileResponse], summary="List tax profiles")
def list_tax_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_tax_profiles(tenant_id=tenant_id)


# --- Currencies ---

@router.post("/currencies", response_model=CurrencyResponse, summary="Create a supported currency")
def create_currency(
    payload: CurrencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    return repo.create_currency(data=payload.dict())


@router.get("/currencies", response_model=List[CurrencyResponse], summary="List active currencies")
def list_currencies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = FinanceRepository(db)
    return repo.list_currencies()
