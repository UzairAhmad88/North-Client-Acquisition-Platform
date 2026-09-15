"""
SQLAlchemy repository for Phase 51: Autonomous Business Strategy & Goal Optimization Engine.
"""

from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from backend.app.models.strategy import (
        KeyResultModel,
        OptimizationRunModel,
        ParetoFrontierModel,
        StrategicAlertModel,
        StrategicDecisionRecordModel,
        StrategicInitiativeModel,
        StrategicObjectiveModel,
        StrategicOutcomeModel,
        StrategicPillarModel,
        StrategicPlanModel,
        StrategicScorecardModel,
    )
except ImportError:
    from app.models.strategy import (
        KeyResultModel,
        OptimizationRunModel,
        ParetoFrontierModel,
        StrategicAlertModel,
        StrategicDecisionRecordModel,
        StrategicInitiativeModel,
        StrategicObjectiveModel,
        StrategicOutcomeModel,
        StrategicPillarModel,
        StrategicPlanModel,
        StrategicScorecardModel,
    )


class StrategyRepository:
    """Async repository providing database queries and persistence for Strategy entities."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Plans ---
    async def create_plan(self, plan: StrategicPlanModel) -> StrategicPlanModel:
        self.session.add(plan)
        await self.session.flush()
        return plan

    async def list_plans(self, tenant_id: str, limit: int = 50) -> List[StrategicPlanModel]:
        stmt = (
            select(StrategicPlanModel)
            .where(StrategicPlanModel.tenant_id == tenant_id)
            .order_by(desc(StrategicPlanModel.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Objectives ---
    async def create_objective(self, obj: StrategicObjectiveModel) -> StrategicObjectiveModel:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def list_objectives(self, tenant_id: str, limit: int = 100) -> List[StrategicObjectiveModel]:
        stmt = (
            select(StrategicObjectiveModel)
            .where(StrategicObjectiveModel.tenant_id == tenant_id)
            .order_by(desc(StrategicObjectiveModel.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Initiatives ---
    async def create_initiative(self, init: StrategicInitiativeModel) -> StrategicInitiativeModel:
        self.session.add(init)
        await self.session.flush()
        return init

    async def list_initiatives(self, tenant_id: str, limit: int = 100) -> List[StrategicInitiativeModel]:
        stmt = (
            select(StrategicInitiativeModel)
            .where(StrategicInitiativeModel.tenant_id == tenant_id)
            .order_by(desc(StrategicInitiativeModel.priority_score))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Decisions ---
    async def create_decision(self, dec: StrategicDecisionRecordModel) -> StrategicDecisionRecordModel:
        self.session.add(dec)
        await self.session.flush()
        return dec

    async def list_decisions(self, tenant_id: str, limit: int = 50) -> List[StrategicDecisionRecordModel]:
        stmt = (
            select(StrategicDecisionRecordModel)
            .where(StrategicDecisionRecordModel.tenant_id == tenant_id)
            .order_by(desc(StrategicDecisionRecordModel.approved_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
