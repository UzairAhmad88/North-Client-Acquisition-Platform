"""Repository layer for Unified Reliability, SRE, Disaster Recovery, and Operations Platform."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reliability import (
    CircuitBreakerStateModel,
    ComponentHealthModel,
    DeploymentRecordModel,
    DisasterRecoveryDrillModel,
    DisasterRecoveryPlanModel,
    FeatureFlagModel,
    IdempotencyRecordModel,
    IncidentPostmortemModel,
    ReliabilityIncidentModel,
    RestoreVerificationTestModel,
    SLODefinitionModel,
    SLOMetricSnapshotModel,
    SystemBackupRecordModel,
    SystemHealthSnapshotModel,
)


class ReliabilityRepository:
    """Database persistence and query layer for Reliability, SRE, and Disaster Recovery entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # --- Health Snapshots ---
    async def create_health_snapshot(self, snapshot: SystemHealthSnapshotModel) -> SystemHealthSnapshotModel:
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def list_health_snapshots(self, limit: int = 50) -> List[SystemHealthSnapshotModel]:
        stmt = select(SystemHealthSnapshotModel).order_by(desc(SystemHealthSnapshotModel.timestamp)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- SLO Definitions & Metrics ---
    async def create_slo_definition(self, slo: SLODefinitionModel) -> SLODefinitionModel:
        self.session.add(slo)
        await self.session.commit()
        await self.session.refresh(slo)
        return slo

    async def list_slo_definitions(self, active_only: bool = True) -> List[SLODefinitionModel]:
        stmt = select(SLODefinitionModel)
        if active_only:
            stmt = stmt.where(SLODefinitionModel.is_active == True)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def record_slo_snapshot(self, snapshot: SLOMetricSnapshotModel) -> SLOMetricSnapshotModel:
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def list_latest_slo_snapshots(self) -> List[SLOMetricSnapshotModel]:
        stmt = select(SLOMetricSnapshotModel).order_by(desc(SLOMetricSnapshotModel.recorded_at)).limit(20)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Incidents & Postmortems ---
    async def create_incident(self, incident: ReliabilityIncidentModel) -> ReliabilityIncidentModel:
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def get_incident(self, incident_id: str) -> Optional[ReliabilityIncidentModel]:
        stmt = select(ReliabilityIncidentModel).where(ReliabilityIncidentModel.id == incident_id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def list_incidents(self, status: Optional[str] = None, limit: int = 50) -> List[ReliabilityIncidentModel]:
        stmt = select(ReliabilityIncidentModel).order_by(desc(ReliabilityIncidentModel.started_at)).limit(limit)
        if status:
            stmt = stmt.where(ReliabilityIncidentModel.status == status)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def update_incident(self, incident: ReliabilityIncidentModel) -> ReliabilityIncidentModel:
        incident.updated_at = datetime.now(timezone.utc)
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def create_postmortem(self, postmortem: IncidentPostmortemModel) -> IncidentPostmortemModel:
        self.session.add(postmortem)
        await self.session.commit()
        await self.session.refresh(postmortem)
        return postmortem

    async def get_postmortem_by_incident(self, incident_id: str) -> Optional[IncidentPostmortemModel]:
        stmt = select(IncidentPostmortemModel).where(IncidentPostmortemModel.incident_id == incident_id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    # --- Backups & Restore Tests ---
    async def create_backup_record(self, backup: SystemBackupRecordModel) -> SystemBackupRecordModel:
        self.session.add(backup)
        await self.session.commit()
        await self.session.refresh(backup)
        return backup

    async def list_backups(self, limit: int = 50) -> List[SystemBackupRecordModel]:
        stmt = select(SystemBackupRecordModel).order_by(desc(SystemBackupRecordModel.started_at)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_restore_test(self, test: RestoreVerificationTestModel) -> RestoreVerificationTestModel:
        self.session.add(test)
        await self.session.commit()
        await self.session.refresh(test)
        return test

    async def list_restore_tests(self, limit: int = 50) -> List[RestoreVerificationTestModel]:
        stmt = select(RestoreVerificationTestModel).order_by(desc(RestoreVerificationTestModel.executed_at)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- DR Plans & Drills ---
    async def save_dr_plan(self, plan: DisasterRecoveryPlanModel) -> DisasterRecoveryPlanModel:
        self.session.add(plan)
        await self.session.commit()
        await self.session.refresh(plan)
        return plan

    async def list_dr_plans(self) -> List[DisasterRecoveryPlanModel]:
        stmt = select(DisasterRecoveryPlanModel)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_dr_drill(self, drill: DisasterRecoveryDrillModel) -> DisasterRecoveryDrillModel:
        self.session.add(drill)
        await self.session.commit()
        await self.session.refresh(drill)
        return drill

    async def list_dr_drills(self, limit: int = 50) -> List[DisasterRecoveryDrillModel]:
        stmt = select(DisasterRecoveryDrillModel).order_by(desc(DisasterRecoveryDrillModel.started_at)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Deployments & Feature Flags ---
    async def record_deployment(self, deployment: DeploymentRecordModel) -> DeploymentRecordModel:
        self.session.add(deployment)
        await self.session.commit()
        await self.session.refresh(deployment)
        return deployment

    async def list_deployments(self, limit: int = 50) -> List[DeploymentRecordModel]:
        stmt = select(DeploymentRecordModel).order_by(desc(DeploymentRecordModel.deployed_at)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_feature_flag(self, flag_name: str) -> Optional[FeatureFlagModel]:
        stmt = select(FeatureFlagModel).where(FeatureFlagModel.name == flag_name)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def save_feature_flag(self, flag: FeatureFlagModel) -> FeatureFlagModel:
        self.session.add(flag)
        await self.session.commit()
        await self.session.refresh(flag)
        return flag

    async def list_feature_flags(self) -> List[FeatureFlagModel]:
        stmt = select(FeatureFlagModel)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
