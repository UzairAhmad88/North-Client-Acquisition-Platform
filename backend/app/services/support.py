"""Service layer for Phase 30 — Post-Delivery Support, Maintenance, Warranty & Client Success System."""

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.support import (
    ClientHealthSnapshot,
    Incident,
    IncidentTimeline,
    KnowledgeArticle,
    MaintenancePlan,
    MaintenanceWorkOrder,
    MonitoringEvent,
    SLAPolicy,
    SupportOpportunity,
    SupportRequest,
    SupportRequestEvent,
    SupportRequestEvidence,
    SupportRequestVersion,
    Warranty,
)
from app.repositories.project import ProjectRepository
from app.repositories.support import SupportRepository
from agents.support.classifier import SupportClassifierEngine
from agents.support.opportunity_detector import OpportunityDetectorEngine
from agents.support.troubleshooter import TroubleshooterEngine
from agents.support.warranty_evaluator import WarrantyEvaluatorEngine


class SupportService:
    """Business logic for Support Requests, Warranty Governance, Incident Response, Maintenance, SLAs, and Client Success."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SupportRepository(session)
        self.project_repo = ProjectRepository(session)

        # AI Subsystem Engines (Advisory Only)
        self.classifier = SupportClassifierEngine()
        self.warranty_evaluator = WarrantyEvaluatorEngine()
        self.troubleshooter = TroubleshooterEngine()
        self.opportunity_detector = OpportunityDetectorEngine()

    # --- Support Requests ---
    async def create_support_request(
        self,
        project_id: str,
        title: str,
        description: str,
        requester: str = "Client User",
        requester_email: Optional[str] = None,
        business_id: Optional[str] = None,
        client_account_id: Optional[str] = None,
        category: str = "APPLICATION",
        actor_id: str = "CLIENT_USER",
    ) -> SupportRequest:
        req_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        req_number = f"SUP-{uuid.uuid4().hex[:6].upper()}"

        # 1. AI Advisory Classification
        classification = self.classifier.classify_request(
            request_id=req_id,
            title=title,
            description=description,
            category=category,
        )

        req = SupportRequest(
            id=req_id,
            request_number=req_number,
            project_id=project_id,
            business_id=business_id,
            client_account_id=client_account_id,
            requester=requester,
            requester_email=requester_email,
            title=title,
            description=description,
            category=category,
            classification=classification.classification,
            priority=classification.priority,
            severity=classification.severity,
            status="NEW",
            warranty_status="REVIEW_REQUIRED" if classification.classification == "DEFECT" else "NOT_APPLICABLE",
            maintenance_status="NOT_APPLICABLE",
            sla_status="ACTIVE",
            created_at=now,
            updated_at=now,
        )

        created_req = await self.repo.create_support_request(req)

        # Version 1 record
        content_hash = hashlib.sha256(description.encode("utf-8")).hexdigest()
        ver = SupportRequestVersion(
            id=str(uuid.uuid4()),
            support_request_id=req_id,
            version_number=1,
            description=description,
            content_hash=content_hash,
            created_by=actor_id,
            created_at=now,
        )
        await self.repo.add_support_request_version(ver)

        # Audit Event
        ev = SupportRequestEvent(
            id=str(uuid.uuid4()),
            support_request_id=req_id,
            event_type="TICKET_SUBMITTED",
            actor_id=actor_id,
            actor_type="USER",
            event_data={
                "initial_classification": classification.classification,
                "confidence": classification.confidence,
                "priority": classification.priority,
            },
            created_at=now,
        )
        await self.repo.add_support_request_event(ev)

        return created_req

    async def get_support_request(self, req_id: str) -> Optional[SupportRequest]:
        return await self.repo.get_support_request(req_id)

    async def list_support_requests(
        self,
        project_id: Optional[str] = None,
        client_account_id: Optional[str] = None,
        business_id: Optional[str] = None,
        classification: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[SupportRequest]:
        return await self.repo.list_support_requests(
            project_id=project_id,
            client_account_id=client_account_id,
            business_id=business_id,
            classification=classification,
            status=status,
            limit=limit,
            offset=offset,
        )

    async def update_support_request_status(
        self,
        req_id: str,
        new_status: str,
        actor_id: str,
        actor_type: str = "ENGINEER",
        notes: Optional[str] = None,
    ) -> SupportRequest:
        req = await self.repo.get_support_request(req_id)
        if not req:
            raise ValueError(f"Support Request '{req_id}' not found.")

        old_status = req.status
        now = datetime.now(timezone.utc)

        # SLA pause management: if moving into WAITING_FOR_CLIENT, pause SLA
        if new_status == "WAITING_FOR_CLIENT" and old_status != "WAITING_FOR_CLIENT":
            req.sla_status = "PAUSED"
        elif old_status == "WAITING_FOR_CLIENT" and new_status != "WAITING_FOR_CLIENT":
            req.sla_status = "ACTIVE"

        req.status = new_status
        req.updated_at = now
        if new_status == "RESOLVED":
            req.resolved_at = now
            if notes:
                req.resolution_summary = notes
        elif new_status == "CLOSED":
            req.closed_at = now

        # Create Version Snapshot
        content_hash = hashlib.sha256((req.description + (notes or "")).encode("utf-8")).hexdigest()
        ver = SupportRequestVersion(
            id=str(uuid.uuid4()),
            support_request_id=req_id,
            version_number=len(req.versions or []) + 1,
            description=req.description,
            content_hash=content_hash,
            created_by=actor_id,
            created_at=now,
        )
        await self.repo.add_support_request_version(ver)

        # Log Event
        ev = SupportRequestEvent(
            id=str(uuid.uuid4()),
            support_request_id=req_id,
            event_type="STATUS_CHANGED",
            actor_id=actor_id,
            actor_type=actor_type,
            event_data={
                "old_status": old_status,
                "new_status": new_status,
                "notes": notes,
            },
            created_at=now,
        )
        await self.repo.add_support_request_event(ev)

        return await self.repo.update_support_request(req)

    async def add_evidence_to_request(
        self,
        req_id: str,
        file_name: str,
        file_path: str,
        file_type: str = "SCREENSHOT",
        file_size_bytes: int = 0,
        uploaded_by: str = "ENGINEER",
        data_payload: Optional[str] = None,
    ) -> SupportRequestEvidence:
        req = await self.repo.get_support_request(req_id)
        if not req:
            raise ValueError(f"Support Request '{req_id}' not found.")

        ev_id = str(uuid.uuid4())
        checksum = hashlib.sha256((data_payload or file_name).encode("utf-8")).hexdigest()

        evidence = SupportRequestEvidence(
            id=ev_id,
            support_request_id=req_id,
            file_name=file_name,
            file_path=file_path,
            file_type=file_type,
            sha256_hash=checksum,
            file_size_bytes=file_size_bytes,
            uploaded_by=uploaded_by,
            created_at=datetime.now(timezone.utc),
        )
        return await self.repo.add_support_request_evidence(evidence)

    # --- AI Troubleshooting & Warranty ---
    async def run_ai_troubleshooting(
        self,
        req_id: str,
    ) -> Dict[str, Any]:
        req = await self.repo.get_support_request(req_id)
        if not req:
            raise ValueError(f"Support Request '{req_id}' not found.")

        diag = self.troubleshooter.analyze_troubleshooting(
            request_id=req_id,
            title=req.title,
            description=req.description,
            category=req.category,
        )

        analysis = {
            "possible_root_causes": diag.inferred_causes or diag.possible_solutions,
            "suggested_steps": diag.recommended_next_steps,
            "confidence": 0.85,
            "prevention_tips": ["Review deployment checklist", "Add automated integration tests"],
            "observed_symptoms": diag.observed_symptoms,
        }

        ev = SupportRequestEvent(
            id=str(uuid.uuid4()),
            support_request_id=req_id,
            event_type="AI_TROUBLESHOOTING_GENERATED",
            actor_id="SUPPORT_AGENT_AI",
            actor_type="AGENT",
            event_data=analysis,
            created_at=datetime.now(timezone.utc),
        )
        await self.repo.add_support_request_event(ev)

        return analysis

    async def evaluate_warranty_for_request(
        self,
        req_id: str,
        human_evaluator_id: Optional[str] = None,
        approve_warranty: Optional[bool] = None,
    ) -> Dict[str, Any]:
        req = await self.repo.get_support_request(req_id)
        if not req:
            raise ValueError(f"Support Request '{req_id}' not found.")

        warranty = None
        if req.project_id:
            warranty = await self.repo.get_warranty_by_project(req.project_id)

        warranty_data = {
            "status": warranty.status if warranty else "NOT_STARTED",
            "exclusions": "third-party API, hosting failure, unauthorized modification",
        } if warranty else None

        eval_res = self.warranty_evaluator.evaluate_warranty_coverage(
            project_id=req.project_id or "default",
            defect_title=req.title,
            defect_description=req.description,
            warranty_data=warranty_data,
        )

        ai_assessment = {
            "is_covered": eval_res.is_covered,
            "confidence": eval_res.confidence,
            "reasoning": eval_res.reasoning,
            "requires_human_approval": eval_res.requires_human_approval,
        }

        # Human in the loop decision
        if approve_warranty is not None and human_evaluator_id:
            req.warranty_status = "COVERED" if approve_warranty else "NOT_COVERED"
            req.updated_at = datetime.now(timezone.utc)
            await self.repo.update_support_request(req)

            ev = SupportRequestEvent(
                id=str(uuid.uuid4()),
                support_request_id=req_id,
                event_type="WARRANTY_DECIDED",
                actor_id=human_evaluator_id,
                actor_type="USER",
                event_data={
                    "warranty_status": req.warranty_status,
                    "ai_assessment": ai_assessment,
                },
                created_at=datetime.now(timezone.utc),
            )
            await self.repo.add_support_request_event(ev)

        return {
            "ai_assessment": ai_assessment,
            "warranty_status": req.warranty_status,
            "evaluated_by": human_evaluator_id,
        }

    # --- Change Request Handoff ---
    async def route_to_change_request(
        self,
        req_id: str,
        actor_id: str,
        change_request_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> SupportRequest:
        req = await self.repo.get_support_request(req_id)
        if not req:
            raise ValueError(f"Support Request '{req_id}' not found.")

        now = datetime.now(timezone.utc)
        req.status = "RESOLVED"
        req.resolution_summary = f"Routed to Change Request ID {change_request_id or 'CR-NEW'}. {notes or ''}"
        req.updated_at = now

        ev = SupportRequestEvent(
            id=str(uuid.uuid4()),
            support_request_id=req_id,
            event_type="ROUTED_TO_CHANGE_REQUEST",
            actor_id=actor_id,
            actor_type="USER",
            event_data={
                "routed_change_request_id": change_request_id,
                "notes": notes,
            },
            created_at=now,
        )
        await self.repo.add_support_request_event(ev)

        return await self.repo.update_support_request(req)

    # --- Incidents ---
    async def create_incident(
        self,
        project_id: str,
        title: str,
        description: str,
        severity: str = "SEV-2",
        affected_service: str = "CORE_APP",
        impact_summary: Optional[str] = None,
        actor_id: str = "OPERATIONS",
    ) -> Incident:
        inc_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        inc_num = f"INC-{uuid.uuid4().hex[:6].upper()}"

        incident = Incident(
            id=inc_id,
            incident_number=inc_num,
            project_id=project_id,
            title=title,
            description=description,
            severity=severity,
            status="DETECTED",
            affected_service=affected_service,
            impact_summary=impact_summary or description,
            detected_at=now,
            created_at=now,
        )
        created_incident = await self.repo.create_incident(incident)

        timeline = IncidentTimeline(
            id=str(uuid.uuid4()),
            incident_id=inc_id,
            milestone="DETECTED",
            description=f"Incident '{title}' detected with severity {severity}.",
            recorded_by=actor_id,
            recorded_at=now,
        )
        await self.repo.add_incident_timeline(timeline)

        return created_incident

    async def get_incident(self, incident_id: str) -> Optional[Incident]:
        return await self.repo.get_incident(incident_id)

    async def list_incidents(
        self,
        project_id: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Incident]:
        return await self.repo.list_incidents(
            project_id=project_id,
            severity=severity,
            status=status,
            limit=limit,
            offset=offset,
        )

    async def update_incident_status(
        self,
        incident_id: str,
        status: str,
        actor_id: str,
        message: str,
        root_cause: Optional[str] = None,
        mitigation_steps: Optional[str] = None,
        postmortem: Optional[str] = None,
    ) -> Incident:
        incident = await self.repo.get_incident(incident_id)
        if not incident:
            raise ValueError(f"Incident '{incident_id}' not found.")

        now = datetime.now(timezone.utc)
        incident.status = status

        if status == "ACKNOWLEDGED" and not incident.acknowledged_at:
            incident.acknowledged_at = now
        elif status in ["MITIGATING", "CONTAINMENT"] and not incident.mitigated_at:
            incident.mitigated_at = now
        elif status == "RESOLVED" and not incident.resolved_at:
            incident.resolved_at = now
        elif status in ["CLOSED", "POST_INCIDENT_REVIEW"]:
            incident.closed_at = now
            if root_cause:
                incident.root_cause = root_cause
            if mitigation_steps:
                incident.mitigation_steps = mitigation_steps
            if postmortem:
                incident.postmortem = postmortem

        timeline = IncidentTimeline(
            id=str(uuid.uuid4()),
            incident_id=incident_id,
            milestone=status,
            description=message,
            recorded_by=actor_id,
            recorded_at=now,
        )
        await self.repo.add_incident_timeline(timeline)

        return await self.repo.update_incident(incident)

    # --- Warranties ---
    async def create_warranty(
        self,
        project_id: str,
        contract_id: Optional[str] = None,
        title: str = "Standard Deliverable Warranty",
        terms: Optional[str] = None,
        exclusions: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Warranty:
        now = datetime.now(timezone.utc)
        warranty = Warranty(
            id=str(uuid.uuid4()),
            project_id=project_id,
            contract_id=contract_id,
            title=title,
            terms=terms or "Standard 90-day defect warranty covering all delivered project baselines.",
            exclusions=exclusions or "Third-party APIs, external infrastructure outages, unauthorized modifications.",
            start_date=start_date or now,
            end_date=end_date or now,
            status="ACTIVE",
            created_at=now,
        )
        return await self.repo.create_warranty(warranty)

    async def get_warranty_by_project(self, project_id: str) -> Optional[Warranty]:
        return await self.repo.get_warranty_by_project(project_id)

    async def list_warranties(self, status: Optional[str] = None) -> List[Warranty]:
        return await self.repo.list_warranties(status=status)

    # --- Maintenance Plans & Work Orders ---
    async def create_maintenance_plan(
        self,
        project_id: str,
        title: str,
        scope_description: str,
        plan_type: str = "STANDARD",
        frequency: str = "MONTHLY",
        start_date: Optional[datetime] = None,
    ) -> MaintenancePlan:
        now = datetime.now(timezone.utc)
        plan = MaintenancePlan(
            id=str(uuid.uuid4()),
            project_id=project_id,
            title=title,
            plan_type=plan_type,
            scope_description=scope_description,
            frequency=frequency,
            status="ACTIVE",
            start_date=start_date or now,
            created_at=now,
        )
        return await self.repo.create_maintenance_plan(plan)

    async def get_maintenance_plan(self, plan_id: str) -> Optional[MaintenancePlan]:
        return await self.repo.get_maintenance_plan(plan_id)

    async def list_maintenance_plans(
        self,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[MaintenancePlan]:
        return await self.repo.list_maintenance_plans(project_id=project_id, status=status)

    async def schedule_work_order(
        self,
        maintenance_plan_id: str,
        project_id: str,
        task_name: str,
        scheduled_at: datetime,
        category: str = "ROUTINE_BACKUP",
        priority: str = "MEDIUM",
    ) -> MaintenanceWorkOrder:
        now = datetime.now(timezone.utc)
        work_order = MaintenanceWorkOrder(
            id=str(uuid.uuid4()),
            maintenance_plan_id=maintenance_plan_id,
            project_id=project_id,
            task_name=task_name,
            category=category,
            priority=priority,
            status="PLANNED",
            scheduled_at=scheduled_at,
            created_at=now,
        )
        return await self.repo.create_work_order(work_order)

    async def complete_work_order(
        self,
        order_id: str,
        actor_id: str,
        result_summary: str,
    ) -> MaintenanceWorkOrder:
        order = await self.repo.get_work_order(order_id)
        if not order:
            raise ValueError(f"Work Order '{order_id}' not found.")

        now = datetime.now(timezone.utc)
        order.status = "COMPLETED"
        order.executed_at = now
        order.executed_by = actor_id
        order.result_summary = result_summary

        return await self.repo.update_work_order(order)

    async def list_work_orders(
        self,
        maintenance_plan_id: Optional[str] = None,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[MaintenanceWorkOrder]:
        return await self.repo.list_work_orders(
            maintenance_plan_id=maintenance_plan_id,
            project_id=project_id,
            status=status,
        )

    # --- Knowledge Articles ---
    async def create_knowledge_article(
        self,
        title: str,
        content: str,
        article_type: str = "USER_GUIDE",
        project_id: Optional[str] = None,
        visibility: str = "CLIENT_VISIBLE",
        author: str = "Support System",
    ) -> KnowledgeArticle:
        now = datetime.now(timezone.utc)
        article = KnowledgeArticle(
            id=str(uuid.uuid4()),
            project_id=project_id,
            title=title,
            content=content,
            article_type=article_type,
            visibility=visibility,
            status="PUBLISHED",
            author=author,
            version=1,
            created_at=now,
            updated_at=now,
        )
        return await self.repo.create_knowledge_article(article)

    # --- Client Health & Opportunities ---
    async def calculate_client_health(
        self,
        project_id: str,
        business_id: Optional[str] = None,
        open_tickets_count: int = 0,
        incident_count: int = 0,
        satisfaction_score: float = 4.8,
    ) -> ClientHealthSnapshot:
        score = 100.0 - (open_tickets_count * 5.0) - (incident_count * 20.0)
        score = max(0.0, min(100.0, score * (satisfaction_score / 5.0)))

        status = "HEALTHY"
        if score < 50.0:
            status = "CRITICAL"
        elif score < 75.0:
            status = "AT_RISK"
        elif score < 85.0:
            status = "STABLE"

        now = datetime.now(timezone.utc)
        snapshot = ClientHealthSnapshot(
            id=str(uuid.uuid4()),
            project_id=project_id,
            business_id=business_id,
            health_score=round(score, 1),
            health_status=status,
            open_tickets_count=open_tickets_count,
            incident_count=incident_count,
            satisfaction_score=satisfaction_score,
            evaluated_at=now,
        )
        return await self.repo.create_health_snapshot(snapshot)

    async def detect_support_opportunities(
        self,
        project_id: str,
        business_id: Optional[str] = None,
        ticket_history_summaries: Optional[List[str]] = None,
    ) -> List[SupportOpportunity]:
        now = datetime.now(timezone.utc)
        created_opps = []

        for summary in (ticket_history_summaries or []):
            detected = self.opportunity_detector.detect_opportunity(
                project_id=project_id,
                title=summary[:50],
                description=summary,
            )
            if detected.opportunity_detected:
                opp = SupportOpportunity(
                    id=str(uuid.uuid4()),
                    project_id=project_id,
                    business_id=business_id,
                    title=detected.title,
                    description=detected.description,
                    opportunity_type=detected.opportunity_type,
                    estimated_value=100000.0,
                    confidence=detected.confidence,
                    status="OPPORTUNITY_DRAFT",
                    created_at=now,
                )
                saved = await self.repo.create_opportunity(opp)
                created_opps.append(saved)

        return created_opps

    async def list_opportunities(
        self,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[SupportOpportunity]:
        return await self.repo.list_opportunities(
            project_id=project_id,
            status=status,
        )
