"""REST API Endpoints for Outreach System, Approval Engine, Communication Guard, and DNC Registry."""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.exceptions import AppError
from app.models.business import Business
from app.models.dnc import DoNotContact
from app.models.lead import Lead
from app.models.outreach import OutreachDraft
from app.models.outreach_event import OutreachEvent
from app.models.user import User
from app.schemas.common import DataResponse, PaginatedResponse
from app.schemas.outreach import (
    DncCreateRequest,
    DncResponse,
    OutreachDraftResponse,
    OutreachDraftUpdateRequest,
    OutreachEventResponse,
    OutreachRejectRequest,
    PersonalizationRunRequest,
)
from app.services.outreach import OutreachDraftService
from app.services.outreach.approval import ApprovalEngine
from app.services.outreach.communication_service import CommunicationService
from app.services.outreach.dnc import DncService

router = APIRouter(prefix="", tags=["Outreach System & Guard"])


@router.post("/leads/{lead_id}/personalization/run", response_model=DataResponse[OutreachDraftResponse])
async def run_personalization(
    lead_id: uuid.UUID,
    payload: PersonalizationRunRequest = PersonalizationRunRequest(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Execute Personalization Agent for a lead and return created outreach draft in PENDING_APPROVAL status."""
    draft = await OutreachDraftService.run_personalization(
        db=db,
        lead_id=lead_id,
        channel=payload.channel,
        tone=payload.tone,
        language=payload.language,
        personalization_depth=payload.personalization_depth,
        objective=payload.objective,
        user_id=current_user.id,
    )
    return DataResponse(data=OutreachDraftResponse.model_validate(draft))


@router.get("/leads/{lead_id}/personalization", response_model=DataResponse[OutreachDraftResponse])
def get_latest_personalization(
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Fetch the latest outreach draft generated for a lead."""
    draft = OutreachDraftService.get_latest_draft(db, lead_id)
    if not draft:
        raise AppError(code="DRAFT_NOT_FOUND", message="No outreach draft found for this lead.", status_code=404)
    return DataResponse(data=OutreachDraftResponse.model_validate(draft))


@router.get("/outreach/drafts/{draft_id}", response_model=DataResponse[OutreachDraftResponse])
def get_draft_by_id(
    draft_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Fetch an outreach draft by its ID."""
    draft = OutreachDraftService.get_draft_by_id(db, draft_id)
    if not draft:
        raise AppError(code="DRAFT_NOT_FOUND", message="Outreach draft not found.", status_code=404)
    return DataResponse(data=OutreachDraftResponse.model_validate(draft))


@router.patch("/outreach/drafts/{draft_id}", response_model=DataResponse[OutreachDraftResponse])
def update_draft(
    draft_id: uuid.UUID,
    payload: OutreachDraftUpdateRequest,
    db: Session = Depends(get_db),
):
    """Update draft subject or body. Subject/body modifications increment version and reset approval to PENDING_APPROVAL."""
    updates = payload.model_dump(exclude_unset=True)
    draft = OutreachDraftService.update_draft(db, draft_id, updates)
    return DataResponse(data=OutreachDraftResponse.model_validate(draft))


@router.get("/outreach/drafts", response_model=PaginatedResponse[OutreachDraftResponse])
def list_drafts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    approval_status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List outreach drafts paginated."""
    offset = (page - 1) * page_size
    drafts = OutreachDraftService.list_drafts(db, limit=page_size, offset=offset, approval_status=approval_status)
    items = [OutreachDraftResponse.model_validate(d) for d in drafts]
    return PaginatedResponse(
        data=items,
        pagination={"page": page, "page_size": page_size, "total": len(items)},
    )


# --- Human Approval & Send Operations ---

@router.post("/outreach/drafts/{draft_id}/approve", response_model=DataResponse[OutreachDraftResponse])
def approve_draft(
    draft_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Human Operator approval endpoint. Binds SHA-256 content hash and sets APPROVED status."""
    draft = OutreachDraftService.get_draft_by_id(db, draft_id)
    if not draft:
        raise AppError(code="DRAFT_NOT_FOUND", message="Outreach draft not found.", status_code=404)

    business = db.query(Business).filter(Business.id == draft.business_id).first()
    recipient_email = (business.email if business else None) or "recipient@example.com"

    approved_draft = ApprovalEngine.approve_draft(
        db=db,
        draft=draft,
        user_id=current_user.id,
        recipient_email=recipient_email,
    )
    return DataResponse(data=OutreachDraftResponse.model_validate(approved_draft))


@router.post("/outreach/drafts/{draft_id}/reject", response_model=DataResponse[OutreachDraftResponse])
def reject_draft(
    draft_id: uuid.UUID,
    payload: OutreachRejectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Human Operator rejection endpoint."""
    draft = OutreachDraftService.get_draft_by_id(db, draft_id)
    if not draft:
        raise AppError(code="DRAFT_NOT_FOUND", message="Outreach draft not found.", status_code=404)

    rejected_draft = ApprovalEngine.reject_draft(
        db=db,
        draft=draft,
        user_id=current_user.id,
        reason=payload.reason,
    )
    return DataResponse(data=OutreachDraftResponse.model_validate(rejected_draft))


@router.post("/outreach/drafts/{draft_id}/send", response_model=DataResponse[OutreachDraftResponse])
async def send_outreach(
    draft_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Executes guarded outreach send through CommunicationGuard and active Provider Service."""
    sent_draft = await CommunicationService.send_outreach(
        db=db,
        draft_id=draft_id,
        user_id=current_user.id,
    )
    return DataResponse(data=OutreachDraftResponse.model_validate(sent_draft))


@router.get("/outreach/drafts/{draft_id}/events", response_model=DataResponse[List[OutreachEventResponse]])
def get_outreach_events(
    draft_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """Fetch complete timeline event history for an outreach draft."""
    events = (
        db.query(OutreachEvent)
        .filter(OutreachEvent.outreach_id == draft_id)
        .order_by(OutreachEvent.created_at.asc())
        .all()
    )
    items = [OutreachEventResponse.model_validate(e) for e in events]
    return DataResponse(data=items)


# --- DNC Registry Endpoints ---

@router.post("/outreach/dnc", response_model=DataResponse[DncResponse])
def add_dnc(
    payload: DncCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a target email, phone, contact, or business to the Do-Not-Contact registry."""
    entry = DncService.add_dnc_entry(
        db=db,
        scope=payload.scope,
        target_value=payload.target_value,
        reason=payload.reason,
        user_id=current_user.id,
    )
    return DataResponse(data=DncResponse.model_validate(entry))


@router.get("/outreach/dnc", response_model=PaginatedResponse[DncResponse])
def list_dnc(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List active Do-Not-Contact registry entries."""
    offset = (page - 1) * page_size
    entries = (
        db.query(DoNotContact)
        .filter(DoNotContact.is_active == True)
        .order_by(DoNotContact.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )
    items = [DncResponse.model_validate(e) for e in entries]
    return PaginatedResponse(
        data=items,
        pagination={"page": page, "page_size": page_size, "total": len(items)},
    )
