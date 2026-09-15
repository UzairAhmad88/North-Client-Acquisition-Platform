"""API Endpoints for Executive Decision Queue, Decision Authorizations, and Learning Loop."""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.business_os.base import DecisionStatus
from app.business_os.service import BusinessOSPlatformService
from app.schemas.business_os import (
    DecisionCreate,
    DecisionOutcomeRecordAction,
    DecisionRecordAction,
    DecisionResponse,
)

router = APIRouter(prefix="/decisions", tags=["executive-decision-queue"])

_service_instance = BusinessOSPlatformService()


def get_business_os_service() -> BusinessOSPlatformService:
    return _service_instance


@router.get("", response_model=List[DecisionResponse])
async def list_decisions(
    status: Optional[DecisionStatus] = Query(None),
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """List pending or decided executive decision items."""
    recs = service.list_decisions(status=status)
    return [
        DecisionResponse(
            decision_id=d.decision_id,
            title=d.title,
            business_question=d.business_question,
            context_summary=d.context_summary,
            priority=d.priority,
            status=d.status,
            candidate_options=[opt.model_dump() for opt in d.candidate_options],
            ai_recommendation=d.ai_recommendation,
            ai_recommendation_rationale=d.ai_recommendation_rationale,
            chosen_option_id=d.chosen_option_id,
            chosen_option_title=d.chosen_option_title,
            decision_rationale=d.decision_rationale,
            decided_by=d.decided_by,
            decided_at=d.decided_at,
            evidence_signals=d.evidence_signals,
            expected_outcome=d.expected_outcome,
            actual_outcome=d.actual_outcome,
            outcome_variance_analysis=d.outcome_variance_analysis,
            lessons_learned=d.lessons_learned,
            created_at=d.created_at,
            review_due_date=d.review_due_date,
        )
        for d in recs
    ]


@router.post("", response_model=DecisionResponse, status_code=status.HTTP_201_CREATED)
async def create_decision_item(
    payload: DecisionCreate,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Create a new decision item in the executive queue."""
    dec = service.decision_engine.create_decision_item(
        title=payload.title,
        business_question=payload.business_question,
        context_summary=payload.context_summary,
        priority=payload.priority,
        evidence_signals=payload.evidence_signals,
        expected_outcome=payload.expected_outcome,
        review_due_date=payload.review_due_date,
    )
    return DecisionResponse(
        decision_id=dec.decision_id,
        title=dec.title,
        business_question=dec.business_question,
        context_summary=dec.context_summary,
        priority=dec.priority,
        status=dec.status,
        candidate_options=[],
        evidence_signals=dec.evidence_signals,
        expected_outcome=dec.expected_outcome,
        lessons_learned=[],
        created_at=dec.created_at,
        review_due_date=dec.review_due_date,
    )


@router.post("/{decision_id}/decide", response_model=DecisionResponse)
async def record_human_decision(
    decision_id: str,
    payload: DecisionRecordAction,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Record human executive authorization on a decision item."""
    dec = service.record_decision(
        decision_id=decision_id,
        chosen_option_id=payload.chosen_option_id,
        decision_rationale=payload.decision_rationale,
        decided_by=payload.decided_by,
    )
    if not dec:
        raise HTTPException(status_code=404, detail="Decision record not found.")

    return DecisionResponse(
        decision_id=dec.decision_id,
        title=dec.title,
        business_question=dec.business_question,
        context_summary=dec.context_summary,
        priority=dec.priority,
        status=dec.status,
        candidate_options=[opt.model_dump() for opt in dec.candidate_options],
        ai_recommendation=dec.ai_recommendation,
        ai_recommendation_rationale=dec.ai_recommendation_rationale,
        chosen_option_id=dec.chosen_option_id,
        chosen_option_title=dec.chosen_option_title,
        decision_rationale=dec.decision_rationale,
        decided_by=dec.decided_by,
        decided_at=dec.decided_at,
        evidence_signals=dec.evidence_signals,
        expected_outcome=dec.expected_outcome,
        actual_outcome=dec.actual_outcome,
        outcome_variance_analysis=dec.outcome_variance_analysis,
        lessons_learned=dec.lessons_learned,
        created_at=dec.created_at,
        review_due_date=dec.review_due_date,
    )


@router.post("/{decision_id}/outcome", response_model=DecisionResponse)
async def record_decision_outcome(
    decision_id: str,
    payload: DecisionOutcomeRecordAction,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Record post-decision actual outcome and lessons learned for strategic learning loop."""
    dec = service.record_decision_outcome(
        decision_id=decision_id,
        actual_outcome=payload.actual_outcome,
        outcome_variance_analysis=payload.outcome_variance_analysis,
        lessons_learned=payload.lessons_learned,
    )
    if not dec:
        raise HTTPException(status_code=404, detail="Decision record not found.")

    return DecisionResponse(
        decision_id=dec.decision_id,
        title=dec.title,
        business_question=dec.business_question,
        context_summary=dec.context_summary,
        priority=dec.priority,
        status=dec.status,
        candidate_options=[opt.model_dump() for opt in dec.candidate_options],
        chosen_option_id=dec.chosen_option_id,
        chosen_option_title=dec.chosen_option_title,
        decision_rationale=dec.decision_rationale,
        decided_by=dec.decided_by,
        decided_at=dec.decided_at,
        evidence_signals=dec.evidence_signals,
        expected_outcome=dec.expected_outcome,
        actual_outcome=dec.actual_outcome,
        outcome_variance_analysis=dec.outcome_variance_analysis,
        lessons_learned=dec.lessons_learned,
        created_at=dec.created_at,
        review_due_date=dec.review_due_date,
    )
