"""
REST API Router for Phase 53 — Unified Human-AI Collaboration, Decision Room & Augmented Intelligence Platform.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.decision_rooms import (
    DecisionRoomCreateRequest,
    DecisionStatusTransitionRequest,
    RecordDecisionRequest,
    SetContextRequest,
    AddEvidenceRequest,
    AddAssumptionRequest,
    AddUnknownRequest,
    CreateOptionRequest,
    AddCriterionRequest,
    ScoreOptionRequest,
    SubmitAnalysisRequest,
    SubmitAdversarialReviewRequest,
    AddCommentRequest,
    RecordApprovalRequest,
    CreateActionRequest,
    RecordOutcomeRequest,
    SubmitPostReviewRequest,
    CopilotQueryRequest,
)
from backend.app.services.decision_rooms.service import global_decision_room_service
from backend.app.services.decision_rooms.base import (
    DecisionType,
    DecisionImportance,
    DecisionStatus,
    EvidenceType,
    StatementCategory,
    SpecialistRole,
    ApprovalStatus,
)

router = APIRouter(prefix="/decision-rooms", tags=["Decision Rooms & Human-AI Collaboration"])


@router.get("", summary="List Decision Rooms")
async def list_decision_rooms(
    status: Optional[str] = Query(None),
    decision_type: Optional[str] = Query(None),
    importance: Optional[str] = Query(None),
) -> Dict[str, Any]:
    rooms = global_decision_room_service.rooms.list_rooms(status, decision_type, importance)
    return {"status": "SUCCESS", "count": len(rooms), "data": rooms}


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create Decision Room")
async def create_decision_room(req: DecisionRoomCreateRequest) -> Dict[str, Any]:
    room = global_decision_room_service.rooms.create_room(
        title=req.title,
        question=req.question,
        owner_id=req.owner_id,
        decision_type=DecisionType(req.decision_type) if req.decision_type in DecisionType.__members__ else DecisionType.STRATEGIC,
        importance=DecisionImportance(req.importance) if req.importance in DecisionImportance.__members__ else DecisionImportance.MEDIUM,
        objective=req.objective,
        meta_info=req.meta_info,
    )
    return {"status": "SUCCESS", "data": room}


@router.get("/{id}", summary="Get Full Decision Room Workspace Overview")
async def get_decision_room_overview(id: str) -> Dict[str, Any]:
    try:
        overview = global_decision_room_service.get_room_overview(id)
        return {"status": "SUCCESS", "data": overview}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{id}/transition", summary="Transition Decision Room Status")
async def transition_room_status(id: str, req: DecisionStatusTransitionRequest) -> Dict[str, Any]:
    try:
        room = global_decision_room_service.rooms.transition_status(
            room_id=id,
            target_status=DecisionStatus(req.target_status) if req.target_status in DecisionStatus.__members__ else DecisionStatus.OPEN,
            actor_id=req.actor_id,
            notes=req.notes,
        )
        return {"status": "SUCCESS", "data": room}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/decide", summary="Record Final Human Executive Decision")
async def record_decision(id: str, req: RecordDecisionRequest) -> Dict[str, Any]:
    try:
        room = global_decision_room_service.rooms.record_decision(
            room_id=id,
            selected_option_id=req.selected_option_id,
            decision_summary=req.decision_summary,
            decided_by=req.decided_by,
        )
        return {"status": "SUCCESS", "data": room}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/context", summary="Set Decision Room Context")
async def set_room_context(id: str, req: SetContextRequest) -> Dict[str, Any]:
    ctx = global_decision_room_service.context_evidence.set_context(
        room_id=id,
        background=req.background,
        current_state=req.current_state,
        constraints=req.constraints,
        entities_involved=req.entities_involved,
    )
    return {"status": "SUCCESS", "data": ctx}


@router.post("/{id}/evidence", summary="Add Evidence Item with Fact/Inference Category")
async def add_evidence_item(id: str, req: AddEvidenceRequest) -> Dict[str, Any]:
    ev_type = EvidenceType(req.evidence_type) if req.evidence_type in EvidenceType.__members__ else EvidenceType.DATABASE
    cat = StatementCategory(req.statement_category) if req.statement_category in StatementCategory.__members__ else StatementCategory.FACT
    item = global_decision_room_service.context_evidence.add_evidence(
        room_id=id,
        evidence_type=ev_type,
        source=req.source,
        claim=req.claim,
        statement_category=cat,
        authority=req.authority,
        confidence=req.confidence,
    )
    return {"status": "SUCCESS", "data": item}


@router.post("/{id}/assumptions", summary="Record Assumption Item")
async def add_assumption_item(id: str, req: AddAssumptionRequest) -> Dict[str, Any]:
    item = global_decision_room_service.assumptions_options.add_assumption(
        room_id=id,
        statement=req.statement,
        confidence=req.confidence,
        impact_if_false=req.impact_if_false,
    )
    return {"status": "SUCCESS", "data": item}


@router.post("/{id}/unknowns", summary="Record Known-Unknown Item")
async def add_unknown_item(id: str, req: AddUnknownRequest) -> Dict[str, Any]:
    item = global_decision_room_service.assumptions_options.add_unknown(
        room_id=id,
        question=req.question,
        impact=req.impact,
        resolution_path=req.resolution_path,
    )
    return {"status": "SUCCESS", "data": item}


@router.post("/{id}/options", summary="Create Candidate Option")
async def create_candidate_option(id: str, req: CreateOptionRequest) -> Dict[str, Any]:
    opt = global_decision_room_service.assumptions_options.create_option(
        room_id=id,
        name=req.name,
        description=req.description,
        benefits=req.benefits,
        costs=req.costs,
        risks=req.risks,
        uncertainty_level=req.uncertainty_level,
        reversibility=req.reversibility,
    )
    return {"status": "SUCCESS", "data": opt}


@router.post("/{id}/criteria", summary="Add Decision Evaluation Criterion")
async def add_decision_criterion(id: str, req: AddCriterionRequest) -> Dict[str, Any]:
    crit = global_decision_room_service.assumptions_options.add_criterion(
        room_id=id,
        name=req.name,
        weight=req.weight,
        criterion_type=req.criterion_type,
        description=req.description,
    )
    return {"status": "SUCCESS", "data": crit}


@router.post("/{id}/scores", summary="Score Option against Criterion")
async def score_option_criterion(id: str, req: ScoreOptionRequest) -> Dict[str, Any]:
    score = global_decision_room_service.assumptions_options.score_option(
        room_id=id,
        option_id=req.option_id,
        criterion_id=req.criterion_id,
        raw_score=req.raw_score,
        justification=req.justification,
        scored_by=req.scored_by,
    )
    return {"status": "SUCCESS", "data": score}


@router.post("/{id}/analyses", summary="Submit Specialist Domain Analysis")
async def submit_specialist_analysis(id: str, req: SubmitAnalysisRequest) -> Dict[str, Any]:
    role = SpecialistRole(req.specialist_role) if req.specialist_role in SpecialistRole.__members__ else SpecialistRole.STRATEGY
    anls = global_decision_room_service.specialists.submit_specialist_analysis(
        room_id=id,
        specialist_role=role,
        summary=req.summary,
        recommendations=req.recommendations,
        key_findings=req.key_findings,
        confidence=req.confidence,
        facts=req.facts,
        inferences=req.inferences,
    )
    return {"status": "SUCCESS", "data": anls}


@router.post("/{id}/adversarial-reviews", summary="Submit Adversarial Review Critique")
async def submit_adversarial_review(id: str, req: SubmitAdversarialReviewRequest) -> Dict[str, Any]:
    rev = global_decision_room_service.specialists.submit_adversarial_review(
        room_id=id,
        critique_summary=req.critique_summary,
        reviewer_role=req.reviewer_role,
        weak_assumptions=req.weak_assumptions,
        unintended_consequences=req.unintended_consequences,
        hidden_costs=req.hidden_costs,
    )
    return {"status": "SUCCESS", "data": rev}


@router.post("/{id}/comments", summary="Post Discussion Comment or Annotation")
async def post_discussion_comment(id: str, req: AddCommentRequest) -> Dict[str, Any]:
    comment = global_decision_room_service.discussions_approvals.add_comment(
        room_id=id,
        author_id=req.author_id,
        content=req.content,
        author_role=req.author_role,
        is_human=req.is_human,
        parent_id=req.parent_id,
        mentions=req.mentions,
        annotations=req.annotations,
    )
    return {"status": "SUCCESS", "data": comment}


@router.post("/{id}/approvals", summary="Record Approval Step Decision")
async def record_approval_action(id: str, req: RecordApprovalRequest) -> Dict[str, Any]:
    try:
        status_enum = ApprovalStatus(req.status) if req.status in ApprovalStatus.__members__ else ApprovalStatus.APPROVED
        appr = global_decision_room_service.discussions_approvals.record_approval_action(
            room_id=id,
            step_id=req.step_id,
            approver_id=req.approver_id,
            status=status_enum,
            notes=req.notes,
        )
        return {"status": "SUCCESS", "data": appr}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/actions", summary="Create Action Item from Decision")
async def create_action_item(id: str, req: CreateActionRequest) -> Dict[str, Any]:
    action = global_decision_room_service.discussions_approvals.create_action_item(
        room_id=id,
        title=req.title,
        target_system=req.target_system,
        description=req.description,
        target_payload=req.target_payload,
        assigned_to=req.assigned_to,
    )
    return {"status": "SUCCESS", "data": action}


@router.post("/{id}/outcomes", summary="Record Measured Post-Execution Outcome")
async def record_decision_outcome(id: str, req: RecordOutcomeRequest) -> Dict[str, Any]:
    outcome = global_decision_room_service.outcomes_journal.record_outcome(
        room_id=id,
        metric_name=req.metric_name,
        expected_value=req.expected_value,
        actual_value=req.actual_value,
    )
    return {"status": "SUCCESS", "data": outcome}


@router.post("/{id}/post-reviews", summary="Submit Post-Decision Retrospective Review")
async def submit_post_decision_review(id: str, req: SubmitPostReviewRequest) -> Dict[str, Any]:
    prev = global_decision_room_service.outcomes_journal.submit_post_review(
        room_id=id,
        reviewed_by=req.reviewed_by,
        outcome_rating=req.outcome_rating,
        prediction_error=req.prediction_error,
        assumption_error=req.assumption_error,
        execution_error=req.execution_error,
        lessons_learned=req.lessons_learned,
    )
    return {"status": "SUCCESS", "data": prev}


@router.get("/templates/catalog", summary="List Pre-Configured Decision Room Templates")
async def list_decision_templates() -> Dict[str, Any]:
    templates = global_decision_room_service.outcomes_journal.list_templates()
    return {"status": "SUCCESS", "count": len(templates), "data": templates}


@router.post("/copilot/query", summary="Query Collaboration Copilot")
async def query_collaboration_copilot(req: CopilotQueryRequest) -> Dict[str, Any]:
    try:
        res = global_decision_room_service.ask_copilot(req.room_id, req.query)
        return {"status": "SUCCESS", "data": res}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
