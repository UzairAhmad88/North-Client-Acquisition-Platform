"""Repository layer for Phase 30 — Post-Delivery Support, Maintenance, Warranty & Client Success System."""

from typing import Any, Dict, List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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


class SupportRepository:
    """Database persistence operations for Support Requests, Incidents, Warranties, Maintenance, SLAs, Knowledge Articles, and Health Snapshots."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Support Requests ---
    async def create_support_request(self, req: SupportRequest) -> SupportRequest:
        self.session.add(req)
        await self.session.commit()
        await self.session.refresh(req)
        return req

    async def get_support_request(self, req_id: str) -> Optional[SupportRequest]:
        stmt = (
            select(SupportRequest)
            .where(SupportRequest.id == req_id)
            .options(
                selectinload(SupportRequest.versions),
                selectinload(SupportRequest.events),
                selectinload(SupportRequest.evidences),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

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
        stmt = (
            select(SupportRequest)
            .options(
                selectinload(SupportRequest.versions),
                selectinload(SupportRequest.events),
                selectinload(SupportRequest.evidences),
            )
            .order_by(SupportRequest.created_at.desc())
        )
        if project_id:
            stmt = stmt.where(SupportRequest.project_id == project_id)
        if client_account_id:
            stmt = stmt.where(SupportRequest.client_account_id == client_account_id)
        if business_id:
            stmt = stmt.where(SupportRequest.business_id == business_id)
        if classification:
            stmt = stmt.where(SupportRequest.classification == classification)
        if status:
            stmt = stmt.where(SupportRequest.status == status)

        stmt = stmt.limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_support_request(self, req: SupportRequest) -> SupportRequest:
        await self.session.commit()
        await self.session.refresh(req)
        return req

    async def add_support_request_version(self, ver: SupportRequestVersion) -> SupportRequestVersion:
        self.session.add(ver)
        await self.session.commit()
        await self.session.refresh(ver)
        return ver

    async def add_support_request_event(self, ev: SupportRequestEvent) -> SupportRequestEvent:
        self.session.add(ev)
        await self.session.commit()
        await self.session.refresh(ev)
        return ev

    async def add_support_request_evidence(self, ev: SupportRequestEvidence) -> SupportRequestEvidence:
        self.session.add(ev)
        await self.session.commit()
        await self.session.refresh(ev)
        return ev

    # --- Incidents ---
    async def create_incident(self, incident: Incident) -> Incident:
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def get_incident(self, incident_id: str) -> Optional[Incident]:
        stmt = (
            select(Incident)
            .where(Incident.id == incident_id)
            .options(selectinload(Incident.timelines))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_incidents(
        self,
        project_id: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Incident]:
        stmt = (
            select(Incident)
            .options(selectinload(Incident.timelines))
            .order_by(Incident.created_at.desc())
        )
        if project_id:
            stmt = stmt.where(Incident.project_id == project_id)
        if severity:
            stmt = stmt.where(Incident.severity == severity)
        if status:
            stmt = stmt.where(Incident.status == status)

        stmt = stmt.limit(limit).offset(offset)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_incident(self, incident: Incident) -> Incident:
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def add_incident_timeline(self, timeline: IncidentTimeline) -> IncidentTimeline:
        self.session.add(timeline)
        await self.session.commit()
        await self.session.refresh(timeline)
        return timeline

    # --- Warranties ---
    async def create_warranty(self, warranty: Warranty) -> Warranty:
        self.session.add(warranty)
        await self.session.commit()
        await self.session.refresh(warranty)
        return warranty

    async def get_warranty(self, warranty_id: str) -> Optional[Warranty]:
        stmt = select(Warranty).where(Warranty.id == warranty_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_warranty_by_project(self, project_id: str) -> Optional[Warranty]:
        stmt = select(Warranty).where(Warranty.project_id == project_id).order_by(Warranty.created_at.desc())
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list_warranties(
        self,
        status: Optional[str] = None,
    ) -> List[Warranty]:
        stmt = select(Warranty).order_by(Warranty.created_at.desc())
        if status:
            stmt = stmt.where(Warranty.status == status)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_warranty(self, warranty: Warranty) -> Warranty:
        await self.session.commit()
        await self.session.refresh(warranty)
        return warranty

    # --- Maintenance Plans & Work Orders ---
    async def create_maintenance_plan(self, plan: MaintenancePlan) -> MaintenancePlan:
        self.session.add(plan)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def get_maintenance_plan(self, plan_id: str) -> Optional[MaintenancePlan]:
        stmt = (
            select(MaintenancePlan)
            .where(MaintenancePlan.id == plan_id)
            .options(selectinload(MaintenancePlan.work_orders))
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_maintenance_plans(
        self,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[MaintenancePlan]:
        stmt = (
            select(MaintenancePlan)
            .options(selectinload(MaintenancePlan.work_orders))
            .order_by(MaintenancePlan.created_at.desc())
        )
        if project_id:
            stmt = stmt.where(MaintenancePlan.project_id == project_id)
        if status:
            stmt = stmt.where(MaintenancePlan.status == status)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_maintenance_plan(self, plan: MaintenancePlan) -> MaintenancePlan:
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def create_work_order(self, order: MaintenanceWorkOrder) -> MaintenanceWorkOrder:
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_work_order(self, order_id: str) -> Optional[MaintenanceWorkOrder]:
        stmt = select(MaintenanceWorkOrder).where(MaintenanceWorkOrder.id == order_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_work_orders(
        self,
        maintenance_plan_id: Optional[str] = None,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[MaintenanceWorkOrder]:
        stmt = select(MaintenanceWorkOrder).order_by(MaintenanceWorkOrder.created_at.desc())
        if maintenance_plan_id:
            stmt = stmt.where(MaintenanceWorkOrder.maintenance_plan_id == maintenance_plan_id)
        if project_id:
            stmt = stmt.where(MaintenanceWorkOrder.project_id == project_id)
        if status:
            stmt = stmt.where(MaintenanceWorkOrder.status == status)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_work_order(self, order: MaintenanceWorkOrder) -> MaintenanceWorkOrder:
        await self.session.commit()
        await self.session.refresh(order)
        return order

    # --- SLA Policies ---
    async def create_sla_policy(self, policy: SLAPolicy) -> SLAPolicy:
        self.session.add(policy)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def get_sla_policy(self, policy_id: str) -> Optional[SLAPolicy]:
        stmt = select(SLAPolicy).where(SLAPolicy.id == policy_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # --- Knowledge Articles ---
    async def create_knowledge_article(self, article: KnowledgeArticle) -> KnowledgeArticle:
        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)
        return article

    async def get_knowledge_article(self, article_id: str) -> Optional[KnowledgeArticle]:
        stmt = select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_knowledge_articles(
        self,
        category: Optional[str] = None,
        is_published: Optional[bool] = None,
        limit: int = 50,
    ) -> List[KnowledgeArticle]:
        stmt = select(KnowledgeArticle).order_by(KnowledgeArticle.created_at.desc())
        if category:
            stmt = stmt.where(KnowledgeArticle.category == category)
        if is_published is not None:
            stmt = stmt.where(KnowledgeArticle.is_published == is_published)
        stmt = stmt.limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Monitoring Events ---
    async def create_monitoring_event(self, ev: MonitoringEvent) -> MonitoringEvent:
        self.session.add(ev)
        await self.session.commit()
        await self.session.refresh(ev)
        return ev

    async def list_monitoring_events(
        self,
        project_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[MonitoringEvent]:
        stmt = select(MonitoringEvent).order_by(MonitoringEvent.created_at.desc())
        if project_id:
            stmt = stmt.where(MonitoringEvent.project_id == project_id)
        stmt = stmt.limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Client Health Snapshots ---
    async def create_health_snapshot(self, snap: ClientHealthSnapshot) -> ClientHealthSnapshot:
        self.session.add(snap)
        await self.session.commit()
        await self.session.refresh(snap)
        return snap

    async def get_latest_health_snapshot(self, client_account_id: str) -> Optional[ClientHealthSnapshot]:
        stmt = (
            select(ClientHealthSnapshot)
            .where(ClientHealthSnapshot.client_account_id == client_account_id)
            .order_by(ClientHealthSnapshot.recorded_at.desc())
        )
        res = await self.session.execute(stmt)
        return res.scalars().first()

    # --- Support Opportunities ---
    async def create_opportunity(self, opp: SupportOpportunity) -> SupportOpportunity:
        self.session.add(opp)
        await self.session.commit()
        await self.session.refresh(opp)
        return opp

    async def list_opportunities(
        self,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[SupportOpportunity]:
        stmt = select(SupportOpportunity).order_by(SupportOpportunity.created_at.desc())
        if project_id:
            stmt = stmt.where(SupportOpportunity.project_id == project_id)
        if status:
            stmt = stmt.where(SupportOpportunity.status == status)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
