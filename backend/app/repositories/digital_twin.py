"""
SQLAlchemy repository for Phase 50: Unified Digital Twin & Simulation Engine.
"""

from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

try:
    from backend.app.models.digital_twin import (
        DigitalTwinCalibrationRecordModel,
        DigitalTwinCounterfactualModel,
        DigitalTwinDecisionOptionModel,
        DigitalTwinDecisionRecordModel,
        DigitalTwinEntityModel,
        DigitalTwinModelModel,
        DigitalTwinOutcomeModel,
        DigitalTwinParameterModel,
        DigitalTwinRelationshipModel,
        DigitalTwinScenarioModel,
        DigitalTwinSensitivityResultModel,
        DigitalTwinSimulationModel,
        DigitalTwinSimulationResultModel,
        DigitalTwinStateSnapshotModel,
    )
except ImportError:
    from app.models.digital_twin import (
        DigitalTwinCalibrationRecordModel,
        DigitalTwinCounterfactualModel,
        DigitalTwinDecisionOptionModel,
        DigitalTwinDecisionRecordModel,
        DigitalTwinEntityModel,
        DigitalTwinModelModel,
        DigitalTwinOutcomeModel,
        DigitalTwinParameterModel,
        DigitalTwinRelationshipModel,
        DigitalTwinScenarioModel,
        DigitalTwinSensitivityResultModel,
        DigitalTwinSimulationModel,
        DigitalTwinSimulationResultModel,
        DigitalTwinStateSnapshotModel,
    )


class DigitalTwinRepository:
    """Async repository providing database queries and persistence for Digital Twin entities."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Models ---
    async def get_model(self, model_id: uuid.UUID, tenant_id: str) -> Optional[DigitalTwinModelModel]:
        stmt = select(DigitalTwinModelModel).where(
            DigitalTwinModelModel.id == model_id,
            DigitalTwinModelModel.tenant_id == tenant_id,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_models(self, tenant_id: str, limit: int = 50) -> List[DigitalTwinModelModel]:
        stmt = (
            select(DigitalTwinModelModel)
            .where(DigitalTwinModelModel.tenant_id == tenant_id)
            .order_by(desc(DigitalTwinModelModel.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- State Snapshots ---
    async def create_snapshot(self, snapshot: DigitalTwinStateSnapshotModel) -> DigitalTwinStateSnapshotModel:
        self.session.add(snapshot)
        await self.session.flush()
        return snapshot

    async def list_snapshots(self, tenant_id: str, limit: int = 20) -> List[DigitalTwinStateSnapshotModel]:
        stmt = (
            select(DigitalTwinStateSnapshotModel)
            .where(DigitalTwinStateSnapshotModel.tenant_id == tenant_id)
            .order_by(desc(DigitalTwinStateSnapshotModel.snapshot_timestamp))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Scenarios ---
    async def create_scenario(self, scenario: DigitalTwinScenarioModel) -> DigitalTwinScenarioModel:
        self.session.add(scenario)
        await self.session.flush()
        return scenario

    async def list_scenarios(self, tenant_id: str, limit: int = 50) -> List[DigitalTwinScenarioModel]:
        stmt = (
            select(DigitalTwinScenarioModel)
            .where(DigitalTwinScenarioModel.tenant_id == tenant_id)
            .order_by(desc(DigitalTwinScenarioModel.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Decisions ---
    async def create_decision_record(self, record: DigitalTwinDecisionRecordModel) -> DigitalTwinDecisionRecordModel:
        self.session.add(record)
        await self.session.flush()
        return record

    async def list_decisions(self, tenant_id: str, limit: int = 50) -> List[DigitalTwinDecisionRecordModel]:
        stmt = (
            select(DigitalTwinDecisionRecordModel)
            .where(DigitalTwinDecisionRecordModel.tenant_id == tenant_id)
            .order_by(desc(DigitalTwinDecisionRecordModel.approved_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Outcomes ---
    async def create_outcome(self, outcome: DigitalTwinOutcomeModel) -> DigitalTwinOutcomeModel:
        self.session.add(outcome)
        await self.session.flush()
        return outcome

    async def list_outcomes(self, tenant_id: str, limit: int = 50) -> List[DigitalTwinOutcomeModel]:
        stmt = (
            select(DigitalTwinOutcomeModel)
            .where(DigitalTwinOutcomeModel.tenant_id == tenant_id)
            .order_by(desc(DigitalTwinOutcomeModel.observed_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
