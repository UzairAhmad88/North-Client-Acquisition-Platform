"""FastAPI endpoints for Customer Success & Client Relationship Intelligence Platform."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.customer_success.service import CustomerSuccessPlatformService
from app.models.user import User
from app.repositories.customer_success import CustomerSuccessRepository
from app.schemas.customer_success import (
    Client360Response,
    ClientAccountPlanCreate,
    ClientAccountPlanResponse,
    ClientGoalCreate,
    ClientGoalResponse,
    ClientHealthHistoryResponse,
    ClientHealthScoreResponse,
    ClientOpportunityCreate,
    ClientOpportunityResponse,
    ClientProfileCreate,
    ClientProfileResponse,
    ClientReferralCreate,
    ClientReferralResponse,
    ClientRelationshipCreate,
    ClientRelationshipResponse,
    ClientReviewCreate,
    ClientReviewResponse,
    ClientRiskCreate,
    ClientRiskResponse,
    ClientSentimentAnalysisCreate,
    ClientSentimentAnalysisResponse,
    ClientSurveyAnswerCreate,
    ClientSurveyAnswerResponse,
    ClientSurveyCreate,
    ClientSurveyResponse,
    ClientTimelineEventCreate,
    ClientTimelineEventResponse,
    HealthCalculationRequest,
    HealthCalculationResponse,
    ClientRenewalCreate,
    ClientRenewalResponse,
)

router = APIRouter(prefix="/customer-success", tags=["Customer Success & Relationship Intelligence"])
_cs_service = CustomerSuccessPlatformService()


# --- Client Profiles ---

@router.post("/profiles", response_model=ClientProfileResponse, summary="Create or update client success profile")
def upsert_client_profile(
    payload: ClientProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_or_update_profile(tenant_id=tenant_id, data=payload.dict())


@router.get("/profiles", response_model=List[ClientProfileResponse], summary="List client success profiles")
def list_client_profiles(
    lifecycle_stage: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_profiles(tenant_id=tenant_id, lifecycle_stage=lifecycle_stage, limit=limit)


@router.get("/profiles/{client_id}", response_model=ClientProfileResponse, summary="Get client success profile")
def get_client_profile(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    profile = repo.get_profile_by_client_id(tenant_id=tenant_id, client_id=client_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Client profile not found")
    return profile


# --- Stakeholders & Relationships ---

@router.post("/relationships", response_model=ClientRelationshipResponse, summary="Add client stakeholder relationship")
def create_relationship(
    payload: ClientRelationshipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_relationship(tenant_id=tenant_id, data=payload.dict())


@router.get("/relationships/{client_id}", response_model=List[ClientRelationshipResponse], summary="List client stakeholders")
def list_relationships(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_relationships(tenant_id=tenant_id, client_id=client_id)


# --- Timeline Events ---

@router.post("/timeline", response_model=ClientTimelineEventResponse, summary="Log client timeline event")
def create_timeline_event(
    payload: ClientTimelineEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    data = payload.dict()
    if not data.get("actor_id"):
        data["actor_id"] = str(current_user.id)
    if not data.get("actor_name"):
        data["actor_name"] = str(current_user.full_name or current_user.email)
    return repo.create_timeline_event(tenant_id=tenant_id, data=data)


@router.get("/timeline/{client_id}", response_model=List[ClientTimelineEventResponse], summary="Get client timeline")
def get_client_timeline(
    client_id: str,
    visibility: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_timeline_events(tenant_id=tenant_id, client_id=client_id, visibility=visibility, limit=limit)


# --- Goals ---

@router.post("/goals", response_model=ClientGoalResponse, summary="Create strategic client goal")
def create_goal(
    payload: ClientGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_goal(tenant_id=tenant_id, data=payload.dict())


@router.get("/goals/{client_id}", response_model=List[ClientGoalResponse], summary="List client goals")
def list_goals(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_goals(tenant_id=tenant_id, client_id=client_id)


# --- Health Scoring ---

@router.post("/health/calculate", response_model=HealthCalculationResponse, summary="Calculate multi-factor health score")
def calculate_health(
    payload: HealthCalculationRequest,
    current_user: User = Depends(get_current_active_user),
):
    res = _cs_service.calculate_health_score(
        engagement_score=payload.engagement_score,
        project_health_score=payload.project_health_score,
        support_satisfaction_score=payload.support_satisfaction_score,
        financial_health_score=payload.financial_health_score,
        relationship_health_score=payload.relationship_health_score,
        goal_progress_score=payload.goal_progress_score,
    )
    return {
        "composite_score": res.composite_score,
        "health_band": res.health_band.value,
        "confidence_score": res.confidence_score,
        "trend": res.trend,
        "explanation_summary": res.explanation_summary,
        "calculation_breakdown": {
            k: {
                "score": v.score,
                "weight": v.weight,
                "weighted_score": v.weighted_score,
                "has_data": v.has_data,
                "status_label": v.status_label,
            }
            for k, v in res.factor_scores.items()
        },
    }


@router.post("/health/{client_id}/record", response_model=ClientHealthScoreResponse, summary="Compute and record client health score")
def record_client_health(
    client_id: str,
    payload: HealthCalculationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    
    # Retrieve past scores for trend analysis
    past = repo.list_health_history(tenant_id=tenant_id, client_id=client_id, limit=5)
    historical_scores = [Decimal(str(h.score)) for h in past]

    res = _cs_service.calculate_health_score(
        engagement_score=payload.engagement_score,
        project_health_score=payload.project_health_score,
        support_satisfaction_score=payload.support_satisfaction_score,
        financial_health_score=payload.financial_health_score,
        relationship_health_score=payload.relationship_health_score,
        goal_progress_score=payload.goal_progress_score,
        historical_scores=historical_scores,
    )

    data = {
        "client_id": client_id,
        "composite_score": res.composite_score,
        "health_band": res.health_band.value,
        "engagement_score": payload.engagement_score,
        "project_health_score": payload.project_health_score,
        "support_satisfaction_score": payload.support_satisfaction_score,
        "financial_health_score": payload.financial_health_score,
        "relationship_health_score": payload.relationship_health_score,
        "goal_progress_score": payload.goal_progress_score,
        "confidence_score": res.confidence_score,
        "trend": res.trend,
        "explanation_summary": res.explanation_summary,
        "calculation_breakdown": {
            k: {
                "score": float(v.score) if v.score is not None else None,
                "weight": float(v.weight),
                "weighted_score": float(v.weighted_score),
                "has_data": v.has_data,
                "status_label": v.status_label,
            }
            for k, v in res.factor_scores.items()
        },
    }
    return repo.record_health_score(tenant_id=tenant_id, data=data)


@router.get("/health/{client_id}/latest", response_model=Optional[ClientHealthScoreResponse], summary="Get latest client health score")
def get_latest_health(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.get_latest_health_score(tenant_id=tenant_id, client_id=client_id)


@router.get("/health/{client_id}/history", response_model=List[ClientHealthHistoryResponse], summary="Get client health history")
def get_health_history(
    client_id: str,
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_health_history(tenant_id=tenant_id, client_id=client_id, limit=limit)


# --- Risks & Opportunities ---

@router.post("/risks", response_model=ClientRiskResponse, summary="Create client risk record")
def create_risk(
    payload: ClientRiskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_risk(tenant_id=tenant_id, data=payload.dict())


@router.get("/risks", response_model=List[ClientRiskResponse], summary="List client risks")
def list_risks(
    client_id: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_risks(tenant_id=tenant_id, client_id=client_id, status=status_filter)


@router.post("/opportunities", response_model=ClientOpportunityResponse, summary="Create client expansion opportunity")
def create_opportunity(
    payload: ClientOpportunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_opportunity(tenant_id=tenant_id, data=payload.dict())


@router.get("/opportunities", response_model=List[ClientOpportunityResponse], summary="List client opportunities")
def list_opportunities(
    client_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_opportunities(tenant_id=tenant_id, client_id=client_id)


# --- Renewals ---

@router.post("/renewals", response_model=ClientRenewalResponse, summary="Schedule or create client renewal record")
def create_renewal(
    payload: ClientRenewalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.create_renewal(tenant_id=tenant_id, data=payload.dict())


@router.get("/renewals", response_model=List[ClientRenewalResponse], summary="List upcoming client renewals")
def list_renewals(
    client_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_renewals(tenant_id=tenant_id, client_id=client_id)


# --- Client 360 Synthesizer ---

@router.get("/clients/{client_id}/360", summary="Get comprehensive 360-degree client dossier")
def get_client_360(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = CustomerSuccessRepository(db)
    tenant_id = str(current_user.tenant_id)

    profile = repo.get_profile_by_client_id(tenant_id=tenant_id, client_id=client_id)
    relationships = repo.list_relationships(tenant_id=tenant_id, client_id=client_id)
    latest_health = repo.get_latest_health_score(tenant_id=tenant_id, client_id=client_id)
    goals = repo.list_goals(tenant_id=tenant_id, client_id=client_id)
    risks = repo.list_risks(tenant_id=tenant_id, client_id=client_id, status="IDENTIFIED")
    opps = repo.list_opportunities(tenant_id=tenant_id, client_id=client_id)
    renewals = repo.list_renewals(tenant_id=tenant_id, client_id=client_id)
    events = repo.list_timeline_events(tenant_id=tenant_id, client_id=client_id, limit=20)
    account_plans = repo.list_account_plans(tenant_id=tenant_id, client_id=client_id)
    reviews = repo.list_reviews(tenant_id=tenant_id, client_id=client_id)

    return _cs_service.synthesize_client_360(
        client_id=client_id,
        profile=profile,
        relationships=relationships,
        latest_health=latest_health,
        goals=goals,
        active_risks=risks,
        opportunities=opps,
        upcoming_renewals=renewals,
        recent_events=events,
        account_plans=account_plans,
        reviews=reviews,
    )
