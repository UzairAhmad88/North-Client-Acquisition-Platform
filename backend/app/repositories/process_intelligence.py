"""
SQLAlchemy repository for Phase 49: Unified Process Intelligence.
"""

from typing import Any, Dict, List, Optional
import uuid
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.process_intelligence import (
    ProcessAutomationCandidateModel,
    ProcessBottleneckModel,
    ProcessCaseModel,
    ProcessConformanceRuleModel,
    ProcessConformanceViolationModel,
    ProcessDefinitionModel,
    ProcessDeploymentModel,
    ProcessEventLogModel,
    ProcessOptimizationProposalModel,
    ProcessSimulationRunModel,
    ProcessVariantModel,
)


class ProcessIntelligenceRepository:
    """Async repository providing database queries for process intelligence entities."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_process(self, process_id: uuid.UUID, tenant_id: str) -> Optional[ProcessDefinitionModel]:
        stmt = select(ProcessDefinitionModel).where(
            ProcessDefinitionModel.id == process_id,
            ProcessDefinitionModel.tenant_id == tenant_id,
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_processes(self, tenant_id: str, limit: int = 50) -> List[ProcessDefinitionModel]:
        stmt = (
            select(ProcessDefinitionModel)
            .where(ProcessDefinitionModel.tenant_id == tenant_id)
            .order_by(desc(ProcessDefinitionModel.created_at))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_event_logs(self, process_id: uuid.UUID, tenant_id: str, limit: int = 100) -> List[ProcessEventLogModel]:
        stmt = (
            select(ProcessEventLogModel)
            .where(
                ProcessEventLogModel.process_id == process_id,
                ProcessEventLogModel.tenant_id == tenant_id,
            )
            .order_by(desc(ProcessEventLogModel.timestamp))
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_bottlenecks(self, process_id: uuid.UUID, tenant_id: str) -> List[ProcessBottleneckModel]:
        stmt = (
            select(ProcessBottleneckModel)
            .where(
                ProcessBottleneckModel.process_id == process_id,
                ProcessBottleneckModel.tenant_id == tenant_id,
            )
            .order_by(desc(ProcessBottleneckModel.average_wait_seconds))
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_conformance_violations(self, process_id: uuid.UUID, tenant_id: str) -> List[ProcessConformanceViolationModel]:
        stmt = (
            select(ProcessConformanceViolationModel)
            .where(
                ProcessConformanceViolationModel.process_id == process_id,
                ProcessConformanceViolationModel.tenant_id == tenant_id,
            )
            .order_by(desc(ProcessConformanceViolationModel.detected_at))
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_automation_candidates(self, process_id: uuid.UUID, tenant_id: str) -> List[ProcessAutomationCandidateModel]:
        stmt = (
            select(ProcessAutomationCandidateModel)
            .where(
                ProcessAutomationCandidateModel.process_id == process_id,
                ProcessAutomationCandidateModel.tenant_id == tenant_id,
            )
            .order_by(desc(ProcessAutomationCandidateModel.suitability_score))
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
