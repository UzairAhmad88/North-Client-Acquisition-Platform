"""REST API router for Phase 30 — Post-Delivery Support, Maintenance, Warranty & Client Success System."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.support import (
    ClientHealthResponseSchema,
    IncidentCreateSchema,
    IncidentResponseSchema,
    IncidentUpdateStatusSchema,
    KnowledgeArticleCreateSchema,
    KnowledgeArticleResponseSchema,
    MaintenancePlanCreateSchema,
    MaintenancePlanResponseSchema,
    MaintenanceWorkOrderCompleteSchema,
    MaintenanceWorkOrderResponseSchema,
    MaintenanceWorkOrderScheduleSchema,
    RouteToChangeRequestSchema,
    SLAPolicyCreateSchema,
    SLAPolicyResponseSchema,
    SupportOpportunityResponseSchema,
    SupportRequestCreateSchema,
    SupportRequestDetailResponseSchema,
    SupportRequestEvidenceCreateSchema,
    SupportRequestEvidenceResponseSchema,
    SupportRequestResponseSchema,
    SupportRequestUpdateStatusSchema,
    TroubleshootingRequestSchema,
    TroubleshootingResponseSchema,
    WarrantyCreateSchema,
    WarrantyEvaluationDecisionSchema,
    WarrantyResponseSchema,
)
from app.services.support import SupportService

router = APIRouter()


# --- Support Requests ---
@router.post("/requests", response_model=SupportRequestResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_support_request(payload: SupportRequestCreateSchema, db: AsyncSession = Depends(get_db)):
    """Submit a new support request/ticket."""
    service = SupportService(db)
    try:
        req = await service.create_support_request(
            title=payload.title,
            description=payload.description,
            project_id=payload.project_id,
            client_account_id=payload.client_account_id,
            business_id=payload.business_id,
            submitted_by=payload.submitted_by,
        )
        return SupportRequestResponseSchema.model_validate(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/requests", response_model=List[SupportRequestResponseSchema])
async def list_support_requests(
    project_id: Optional[str] = None,
    client_account_id: Optional[str] = None,
    business_id: Optional[str] = None,
    request_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List support requests with optional filtering."""
    service = SupportService(db)
    requests = await service.list_support_requests(
        project_id=project_id,
        client_account_id=client_account_id,
        business_id=business_id,
        request_type=request_type,
        status=status,
        limit=limit,
        offset=offset,
    )
    return [SupportRequestResponseSchema.model_validate(r) for r in requests]


@router.get("/requests/{req_id}", response_model=SupportRequestDetailResponseSchema)
async def get_support_request_detail(req_id: str, db: AsyncSession = Depends(get_db)):
    """Get full support request details including version history, events, and evidence."""
    service = SupportService(db)
    req = await service.get_support_request(req_id)
    if not req:
        raise HTTPException(status_code=404, detail="Support request not found")
    return SupportRequestDetailResponseSchema.model_validate(req)


@router.patch("/requests/{req_id}/status", response_model=SupportRequestResponseSchema)
async def update_support_request_status(
    req_id: str,
    payload: SupportRequestUpdateStatusSchema,
    db: AsyncSession = Depends(get_db),
):
    """Update support ticket status through workflow state machine."""
    service = SupportService(db)
    try:
        updated = await service.update_support_request_status(
            req_id=req_id,
            new_status=payload.status,
            actor_id="SUPPORT_ENGINEER",
            notes=payload.notes,
            rejection_reason=payload.rejection_reason,
        )
        return SupportRequestResponseSchema.model_validate(updated)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/requests/{req_id}/evidence", response_model=SupportRequestEvidenceResponseSchema)
async def add_evidence_to_request(
    req_id: str,
    payload: SupportRequestEvidenceCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Attach diagnostic evidence or logs to a support request."""
    service = SupportService(db)
    try:
        evidence = await service.add_evidence_to_request(
            req_id=req_id,
            evidence_type=payload.evidence_type,
            title=payload.title,
            file_path=payload.file_path,
            file_size_bytes=payload.file_size_bytes,
            mime_type=payload.mime_type,
            data_payload=payload.data_payload,
        )
        return SupportRequestEvidenceResponseSchema.model_validate(evidence)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/requests/{req_id}/troubleshoot", response_model=TroubleshootingResponseSchema)
async def troubleshoot_support_request(
    req_id: str,
    payload: TroubleshootingRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    """Run AI diagnostic troubleshooting and suggestion engine on support ticket."""
    service = SupportService(db)
    try:
        analysis = await service.run_ai_troubleshooting(req_id, system_logs=payload.logs)
        return TroubleshootingResponseSchema(
            possible_root_causes=analysis.get("possible_root_causes", []),
            suggested_steps=analysis.get("suggested_steps", []),
            confidence=analysis.get("confidence", 0.8),
            prevention_tips=analysis.get("prevention_tips", []),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/requests/{req_id}/evaluate-warranty")
async def evaluate_warranty(
    req_id: str,
    payload: Optional[WarrantyEvaluationDecisionSchema] = None,
    db: AsyncSession = Depends(get_db),
):
    """Evaluate warranty coverage eligibility (AI advisory) and record human approval."""
    service = SupportService(db)
    try:
        approve_val = payload.approve_warranty if payload else None
        exclusion_reason = payload.exclusion_reason if payload else None
        human_id = "HUMAN_OPERATIONS_LEAD" if payload else None

        result = await service.evaluate_warranty_for_request(
            req_id=req_id,
            human_evaluator_id=human_id,
            approve_warranty=approve_val,
            exclusion_reason=exclusion_reason,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/requests/{req_id}/route-to-change", response_model=SupportRequestResponseSchema)
async def route_to_change_request(
    req_id: str,
    payload: RouteToChangeRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    """Route an out-of-scope ticket to Phase 28 Change Management."""
    service = SupportService(db)
    try:
        routed = await service.route_to_change_request(
            req_id=req_id,
            actor_id="SUPPORT_ENGINEER",
            change_request_id=payload.change_request_id,
            notes=payload.notes,
        )
        return SupportRequestResponseSchema.model_validate(routed)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Incidents ---
@router.post("/incidents", response_model=IncidentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_incident(payload: IncidentCreateSchema, db: AsyncSession = Depends(get_db)):
    """Declare a new operational incident (SEV-1 to SEV-4)."""
    service = SupportService(db)
    try:
        inc = await service.create_incident(
            title=payload.title,
            summary=payload.summary,
            severity=payload.severity,
            project_id=payload.project_id,
            lead_incident_commander=payload.lead_incident_commander,
        )
        loaded = await service.get_incident(inc.id)
        return IncidentResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/incidents", response_model=List[IncidentResponseSchema])
async def list_incidents(
    project_id: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List operational incidents."""
    service = SupportService(db)
    incidents = await service.list_incidents(
        project_id=project_id,
        severity=severity,
        status=status,
        limit=limit,
        offset=offset,
    )
    return [IncidentResponseSchema.model_validate(i) for i in incidents]


@router.get("/incidents/{incident_id}", response_model=IncidentResponseSchema)
async def get_incident_detail(incident_id: str, db: AsyncSession = Depends(get_db)):
    """Get incident details with timeline logs."""
    service = SupportService(db)
    inc = await service.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentResponseSchema.model_validate(inc)


@router.patch("/incidents/{incident_id}/status", response_model=IncidentResponseSchema)
async def update_incident_status(
    incident_id: str,
    payload: IncidentUpdateStatusSchema,
    db: AsyncSession = Depends(get_db),
):
    """Update incident status and add timeline event."""
    service = SupportService(db)
    try:
        updated = await service.update_incident_status(
            incident_id=incident_id,
            status=payload.status,
            actor_id="INCIDENT_COMMANDER",
            message=payload.message,
            root_cause=payload.root_cause,
            resolution_summary=payload.resolution_summary,
        )
        loaded = await service.get_incident(updated.id)
        return IncidentResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Warranties ---
@router.post("/warranties", response_model=WarrantyResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_warranty(payload: WarrantyCreateSchema, db: AsyncSession = Depends(get_db)):
    """Create a post-delivery warranty for a project."""
    service = SupportService(db)
    try:
        warranty = await service.create_warranty(
            project_id=payload.project_id,
            contract_id=payload.contract_id,
            client_account_id=payload.client_account_id,
            title=payload.title,
            start_date=payload.start_date,
            end_date=payload.end_date,
            coverage_terms=payload.coverage_terms,
            covered_defect_categories=payload.covered_defect_categories,
            excluded_conditions=payload.excluded_conditions,
        )
        return WarrantyResponseSchema.model_validate(warranty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/warranty", response_model=Optional[WarrantyResponseSchema])
async def get_project_warranty(project_id: str, db: AsyncSession = Depends(get_db)):
    """Get active warranty for a project."""
    service = SupportService(db)
    warranty = await service.get_warranty_by_project(project_id)
    if not warranty:
        raise HTTPException(status_code=404, detail="No warranty found for project")
    return WarrantyResponseSchema.model_validate(warranty)


@router.get("/warranties", response_model=List[WarrantyResponseSchema])
async def list_warranties(
    client_account_id: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List warranties."""
    service = SupportService(db)
    warranties = await service.list_warranties(client_account_id=client_account_id, status=status)
    return [WarrantyResponseSchema.model_validate(w) for w in warranties]


# --- Maintenance Plans & Work Orders ---
@router.post("/maintenance-plans", response_model=MaintenancePlanResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_maintenance_plan(payload: MaintenancePlanCreateSchema, db: AsyncSession = Depends(get_db)):
    """Create a scheduled maintenance plan."""
    service = SupportService(db)
    try:
        plan = await service.create_maintenance_plan(
            project_id=payload.project_id,
            title=payload.title,
            plan_type=payload.plan_type,
            cadence=payload.cadence,
            client_account_id=payload.client_account_id,
            contract_id=payload.contract_id,
            scope_summary=payload.scope_summary,
            tasks_checklist=payload.tasks_checklist,
        )
        loaded = await service.get_maintenance_plan(plan.id)
        return MaintenancePlanResponseSchema.model_validate(loaded)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/maintenance-plans", response_model=List[MaintenancePlanResponseSchema])
async def list_maintenance_plans(
    project_id: Optional[str] = None,
    client_account_id: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List maintenance plans."""
    service = SupportService(db)
    plans = await service.list_maintenance_plans(
        project_id=project_id,
        client_account_id=client_account_id,
        status=status,
    )
    return [MaintenancePlanResponseSchema.model_validate(p) for p in plans]


@router.get("/maintenance-plans/{plan_id}", response_model=MaintenancePlanResponseSchema)
async def get_maintenance_plan_detail(plan_id: str, db: AsyncSession = Depends(get_db)):
    """Get maintenance plan details with work orders."""
    service = SupportService(db)
    plan = await service.get_maintenance_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Maintenance plan not found")
    return MaintenancePlanResponseSchema.model_validate(plan)


@router.post("/maintenance-plans/{plan_id}/work-orders", response_model=MaintenanceWorkOrderResponseSchema)
async def schedule_work_order(
    plan_id: str,
    payload: MaintenanceWorkOrderScheduleSchema,
    db: AsyncSession = Depends(get_db),
):
    """Schedule a maintenance work order."""
    service = SupportService(db)
    try:
        order = await service.schedule_work_order(
            plan_id=plan_id,
            title=payload.title,
            scheduled_for=payload.scheduled_for,
            project_id=payload.project_id,
            assigned_to=payload.assigned_to,
            tasks_to_execute=payload.tasks_to_execute,
        )
        return MaintenanceWorkOrderResponseSchema.model_validate(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/work-orders", response_model=List[MaintenanceWorkOrderResponseSchema])
async def list_work_orders(
    plan_id: Optional[str] = None,
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List maintenance work orders."""
    service = SupportService(db)
    orders = await service.list_work_orders(plan_id=plan_id, project_id=project_id, status=status)
    return [MaintenanceWorkOrderResponseSchema.model_validate(o) for o in orders]


@router.post("/work-orders/{order_id}/complete", response_model=MaintenanceWorkOrderResponseSchema)
async def complete_work_order(
    order_id: str,
    payload: MaintenanceWorkOrderCompleteSchema,
    db: AsyncSession = Depends(get_db),
):
    """Complete and sign off on a maintenance work order."""
    service = SupportService(db)
    try:
        order = await service.complete_work_order(
            order_id=order_id,
            actor_id="MAINTENANCE_ENGINEER",
            execution_notes=payload.execution_notes,
            checklist_results=payload.checklist_results,
        )
        return MaintenanceWorkOrderResponseSchema.model_validate(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- SLA Policies ---
@router.post("/sla-policies", response_model=SLAPolicyResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_sla_policy(payload: SLAPolicyCreateSchema, db: AsyncSession = Depends(get_db)):
    """Create or configure an SLA policy for a project."""
    service = SupportService(db)
    try:
        policy = await service.create_sla_policy(
            project_id=payload.project_id,
            tier=payload.tier,
            contract_id=payload.contract_id,
            target_response_hours=payload.target_response_hours,
            target_resolution_hours=payload.target_resolution_hours,
            coverage_hours_type=payload.coverage_hours_type,
        )
        return SLAPolicyResponseSchema.model_validate(policy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/sla-policy", response_model=Optional[SLAPolicyResponseSchema])
async def get_project_sla_policy(project_id: str, db: AsyncSession = Depends(get_db)):
    """Get active SLA policy for a project."""
    service = SupportService(db)
    policy = await service.get_sla_policy_by_project(project_id)
    if not policy:
        raise HTTPException(status_code=404, detail="No SLA policy found for project")
    return SLAPolicyResponseSchema.model_validate(policy)


# --- Knowledge Articles ---
@router.post("/knowledge-articles", response_model=KnowledgeArticleResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_knowledge_article(payload: KnowledgeArticleCreateSchema, db: AsyncSession = Depends(get_db)):
    """Publish a knowledge base article."""
    service = SupportService(db)
    try:
        article = await service.create_knowledge_article(
            title=payload.title,
            content=payload.content,
            category=payload.category,
            business_id=payload.business_id,
            summary=payload.summary,
            tags=payload.tags,
            author_id="KNOWLEDGE_CURATOR",
        )
        return KnowledgeArticleResponseSchema.model_validate(article)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/knowledge-articles", response_model=List[KnowledgeArticleResponseSchema])
async def list_knowledge_articles(
    business_id: Optional[str] = None,
    category: Optional[str] = None,
    is_published: Optional[bool] = True,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search and list knowledge articles."""
    service = SupportService(db)
    articles = await service.list_knowledge_articles(
        business_id=business_id,
        category=category,
        is_published=is_published,
        limit=limit,
    )
    return [KnowledgeArticleResponseSchema.model_validate(a) for a in articles]


# --- Client Health & Opportunities ---
@router.get("/clients/{client_account_id}/health", response_model=ClientHealthResponseSchema)
async def get_client_health(
    client_account_id: str,
    open_tickets: int = Query(0),
    incidents: int = Query(0),
    sla_breaches: int = Query(0),
    csat: float = Query(4.5),
    db: AsyncSession = Depends(get_db),
):
    """Calculate or get latest client health score snapshot."""
    service = SupportService(db)
    snapshot = await service.calculate_client_health(
        client_account_id=client_account_id,
        open_tickets_count=open_tickets,
        unresolved_incidents_count=incidents,
        sla_breach_count=sla_breaches,
        csat_score=csat,
    )
    return ClientHealthResponseSchema.model_validate(snapshot)


@router.get("/opportunities", response_model=List[SupportOpportunityResponseSchema])
async def list_support_opportunities(
    client_account_id: Optional[str] = None,
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List expansion opportunities surfaced from support interactions."""
    service = SupportService(db)
    opps = await service.list_opportunities(
        client_account_id=client_account_id,
        project_id=project_id,
        status=status,
    )
    return [SupportOpportunityResponseSchema.model_validate(o) for o in opps]


@router.post("/clients/{client_account_id}/detect-opportunities", response_model=List[SupportOpportunityResponseSchema])
async def detect_support_opportunities(
    client_account_id: str,
    project_id: Optional[str] = None,
    ticket_summaries: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
):
    """Run AI opportunity detector over support ticket histories to generate draft opportunities."""
    service = SupportService(db)
    opps = await service.detect_support_opportunities(
        client_account_id=client_account_id,
        project_id=project_id,
        ticket_history_summaries=ticket_summaries or [],
    )
    return [SupportOpportunityResponseSchema.model_validate(o) for o in opps]
