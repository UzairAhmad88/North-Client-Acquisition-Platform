"""Repository layer for Unified Business Operating System (Business OS) & Executive Intelligence."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_os import (
    BusinessCalendarEventModel,
    BusinessHealthSnapshotModel,
    DecisionRecordModel,
    ExecutiveAlertModel,
    ExecutiveBriefingModel,
    InitiativeDependencyModel,
    InitiativeMilestoneModel,
    InitiativeModel,
    KPIDefinitionModel,
    KPIValueSnapshotModel,
    KeyResultModel,
    OrganizationalRiskModel,
    ScenarioModel,
    ScorecardRecordModel,
    StrategicObjectiveModel,
)


class BusinessOSRepository:
    """Database persistence and query layer for Business OS, Strategy, KPIs, and Executive decisions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # --- Strategic Objectives & OKRs ---
    async def create_objective(self, objective: StrategicObjectiveModel) -> StrategicObjectiveModel:
        self.session.add(objective)
        await self.session.commit()
        await self.session.refresh(objective)
        return objective

    async def get_objective(self, objective_id: str) -> Optional[StrategicObjectiveModel]:
        stmt = select(StrategicObjectiveModel).where(StrategicObjectiveModel.id == objective_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_objectives(self) -> List[StrategicObjectiveModel]:
        stmt = select(StrategicObjectiveModel).order_by(desc(StrategicObjectiveModel.created_at))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- KPIs & Scorecards ---
    async def create_kpi_definition(self, kpi: KPIDefinitionModel) -> KPIDefinitionModel:
        self.session.add(kpi)
        await self.session.commit()
        await self.session.refresh(kpi)
        return kpi

    async def list_kpi_definitions(self, category: Optional[str] = None) -> List[KPIDefinitionModel]:
        stmt = select(KPIDefinitionModel)
        if category:
            stmt = stmt.where(KPIDefinitionModel.category == category)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def record_health_snapshot(self, snapshot: BusinessHealthSnapshotModel) -> BusinessHealthSnapshotModel:
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def list_health_snapshots(self, limit: int = 30) -> List[BusinessHealthSnapshotModel]:
        stmt = select(BusinessHealthSnapshotModel).order_by(desc(BusinessHealthSnapshotModel.evaluated_at)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Organizational Risk Register ---
    async def create_risk(self, risk: OrganizationalRiskModel) -> OrganizationalRiskModel:
        self.session.add(risk)
        await self.session.commit()
        await self.session.refresh(risk)
        return risk

    async def list_risks(self, category: Optional[str] = None) -> List[OrganizationalRiskModel]:
        stmt = select(OrganizationalRiskModel).order_by(desc(OrganizationalRiskModel.risk_score))
        if category:
            stmt = stmt.where(OrganizationalRiskModel.category == category)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Decision Records ---
    async def create_decision(self, decision: DecisionRecordModel) -> DecisionRecordModel:
        self.session.add(decision)
        await self.session.commit()
        await self.session.refresh(decision)
        return decision

    async def get_decision(self, decision_id: str) -> Optional[DecisionRecordModel]:
        stmt = select(DecisionRecordModel).where(DecisionRecordModel.id == decision_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_decisions(self, status: Optional[str] = None) -> List[DecisionRecordModel]:
        stmt = select(DecisionRecordModel).order_by(desc(DecisionRecordModel.created_at))
        if status:
            stmt = stmt.where(DecisionRecordModel.status == status)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Scenarios ---
    async def create_scenario(self, scenario: ScenarioModel) -> ScenarioModel:
        self.session.add(scenario)
        await self.session.commit()
        await self.session.refresh(scenario)
        return scenario

    async def list_scenarios(self) -> List[ScenarioModel]:
        stmt = select(ScenarioModel).order_by(desc(ScenarioModel.created_at))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Briefings & Calendar ---
    async def create_briefing(self, briefing: ExecutiveBriefingModel) -> ExecutiveBriefingModel:
        self.session.add(briefing)
        await self.session.commit()
        await self.session.refresh(briefing)
        return briefing

    async def list_calendar_events(self) -> List[BusinessCalendarEventModel]:
        stmt = select(BusinessCalendarEventModel).order_by(BusinessCalendarEventModel.event_date)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
