"""REST API endpoints for Contract, Scope Commitment & Client Approval Workflow."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.contract import (
    ClientAcceptanceRequestSchema,
    ContractBaselineResponseSchema,
    ContractCreateSchema,
    ContractDetailSchema,
    ContractResponseSchema,
)
from app.services.contract import ContractService

router = APIRouter(prefix="/contracts", tags=["Contracts & Scope Commitment"])


@router.post("", response_model=ContractResponseSchema, status_code=status.HTTP_201_CREATED)
def create_contract(
    payload: ContractCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new contract draft from an approved proposal and estimate."""
    try:
        return ContractService.create_contract(
            db,
            proposal_id=payload.proposal_id,
            estimate_id=payload.estimate_id,
            user_id=current_user.id,
            title=payload.title,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[ContractResponseSchema])
def list_contracts(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List contracts with optional status filter."""
    return ContractService.list_contracts(db, status=status_filter, limit=limit, offset=offset)


@router.get("/{id}", response_model=ContractDetailSchema)
def get_contract_detail(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve detailed contract workspace with sections, discrepancies, and committed baselines."""
    contract_obj = ContractService.get_contract(db, id)
    if not contract_obj:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract_obj


@router.post("/{id}/generate", response_model=ContractDetailSchema)
async def generate_contract(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger ContractAgent section composition, completeness scoring, and discrepancy detection."""
    try:
        return await ContractService.generate_contract(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/approve", response_model=ContractResponseSchema)
def approve_contract_internally(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approve a contract draft internally (Operator Action)."""
    try:
        return ContractService.approve_contract_internally(db, id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/accept", response_model=ContractResponseSchema)
def client_accept_contract(
    id: uuid.UUID,
    payload: ClientAcceptanceRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record explicit client acceptance for a contract version."""
    try:
        return ContractService.client_accept_contract(
            db,
            contract_id=id,
            client_email=payload.client_email,
            acceptance_statement=payload.acceptance_statement,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/sign", response_model=ContractResponseSchema)
async def complete_contract_signature(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Complete mock signature execution for an accepted contract."""
    try:
        return await ContractService.complete_contract_signature(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/baseline", response_model=ContractBaselineResponseSchema)
def lock_contract_baseline(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lock an immutable committed project baseline once contract signature is verified."""
    try:
        return ContractService.lock_contract_baseline(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
