"""Client-Facing Portal Endpoints for Goals, Health Overview, Surveys, and Masked 360 View."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.customer_success.authorization import CustomerSuccessAuthorizationManager
from app.customer_success.service import CustomerSuccessPlatformService
from app.models.user import User
from app.repositories.customer_success import CustomerSuccessRepository
from app.schemas.customer_success import (
    ClientGoalResponse,
    ClientSurveyAnswerCreate,
    ClientSurveyAnswerResponse,
    ClientTimelineEventResponse,
)

router = APIRouter(prefix="/portal/success", tags=["Client Portal - Success & Transparency"])
_cs_service = CustomerSuccessPlatformService()
_auth_manager = CustomerSuccessAuthorizationManager()


@router.get("/overview", summary="Get client portal transparency 360 view (strictly masked)")
def get_client_portal_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    # The client_id is derived from user association
    client_id = getattr(current_user, "client_id", None) or str(current_user.id)

    profile = repo.get_profile_by_client_id(tenant_id=tenant_id, client_id=client_id)
    latest_health = repo.get_latest_health_score(tenant_id=tenant_id, client_id=client_id)
    goals = repo.list_goals(tenant_id=tenant_id, client_id=client_id)
    events = repo.list_timeline_events(tenant_id=tenant_id, client_id=client_id, visibility="CLIENT_VISIBLE", limit=20)
    renewals = repo.list_renewals(tenant_id=tenant_id, client_id=client_id)

    raw_360 = _cs_service.synthesize_client_360(
        client_id=client_id,
        profile=profile,
        relationships=[],
        latest_health=latest_health,
        goals=goals,
        active_risks=[],
        opportunities=[],
        upcoming_renewals=renewals,
        recent_events=events,
        account_plans=[],
        reviews=[],
    )

    # Enforce strict client portal boundary masking
    return _auth_manager.mask_client_360_payload(raw_360)


@router.get("/goals", response_model=List[ClientGoalResponse], summary="List client visible shared goals")
def list_client_portal_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    client_id = getattr(current_user, "client_id", None) or str(current_user.id)
    return repo.list_goals(tenant_id=tenant_id, client_id=client_id)


@router.get("/timeline", response_model=List[ClientTimelineEventResponse], summary="List client visible milestones and timeline")
def list_client_portal_timeline(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    client_id = getattr(current_user, "client_id", None) or str(current_user.id)
    return repo.list_timeline_events(tenant_id=tenant_id, client_id=client_id, visibility="CLIENT_VISIBLE", limit=limit)


@router.post("/surveys/submit", response_model=ClientSurveyAnswerResponse, summary="Submit client CSAT/NPS survey response")
def submit_survey_response(
    payload: ClientSurveyAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    data = payload.dict()
    if not data.get("respondent_id"):
        data["respondent_id"] = str(current_user.id)
    if not data.get("respondent_name"):
        data["respondent_name"] = str(current_user.full_name or current_user.email)
    return repo.submit_survey_response(data=data)
