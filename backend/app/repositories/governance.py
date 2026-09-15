"""Repository layer for Phase 33: AI Agent Evaluation, Observability & Governance."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import func, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.governance import (
    AIBudgetPolicy,
    AIFailureCategory,
    AIFailureRecord,
    AIHealthSnapshot,
    AIImprovementItem,
    AIIncident,
    AIIncidentStatus,
    AIKillSwitchEvent,
    AISecurityEvent,
    AITechnicalDebtItem,
    AITrace,
    AITraceEvent,
    AgentDeployment,
    AgentHealthStatus,
    AgentRolloutStatus,
    AgentVersion,
    EvaluationCase,
    EvaluationDataset,
    EvaluationRun,
    HumanEvaluation,
    HumanRevisionRecord,
    KillSwitchLevel,
    ModelUsageRecord,
    PromptRegistryItem,
    PromptStatus,
    PromptVersion,
    ToolUsageRecord,
    TraceStatus,
)


class GovernanceRepository:
    """Database persistence and query layer for AI traces, prompt registry, evaluation runs, incidents, and health."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================================
    # 1. Traces & Spans
    # =========================================================================

    async def create_trace(self, trace: AITrace) -> AITrace:
        self.session.add(trace)
        await self.session.commit()
        await self.session.refresh(trace)
        return trace

    async def get_trace(self, trace_id: str) -> Optional[AITrace]:
        stmt = select(AITrace).options(selectinload(AITrace.events)).where(AITrace.id == trace_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_traces(
        self,
        tenant_id: str = "default_tenant",
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[AITrace]:
        stmt = (
            select(AITrace)
            .options(selectinload(AITrace.events))
            .where(AITrace.tenant_id == tenant_id)
            .order_by(desc(AITrace.started_at))
            .limit(limit)
        )
        if agent_id:
            stmt = stmt.where(AITrace.agent_id == agent_id)
        if status:
            stmt = stmt.where(AITrace.status == status)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_trace_event(self, event: AITraceEvent) -> AITraceEvent:
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    # =========================================================================
    # 2. Prompts & Versions
    # =========================================================================

    async def create_prompt_item(self, item: PromptRegistryItem) -> PromptRegistryItem:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_prompt_item(self, prompt_key: str) -> Optional[PromptRegistryItem]:
        stmt = select(PromptRegistryItem).options(selectinload(PromptRegistryItem.versions)).where(PromptRegistryItem.prompt_key == prompt_key)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_prompts(self, tenant_id: str = "default_tenant") -> List[PromptRegistryItem]:
        stmt = (
            select(PromptRegistryItem)
            .options(selectinload(PromptRegistryItem.versions))
            .where(PromptRegistryItem.tenant_id == tenant_id)
            .order_by(PromptRegistryItem.prompt_key)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_prompt_version(self, version: PromptVersion) -> PromptVersion:
        self.session.add(version)
        await self.session.commit()
        await self.session.refresh(version)
        return version

    # =========================================================================
    # 3. Evaluation Datasets & Runs
    # =========================================================================

    async def create_evaluation_dataset(self, dataset: EvaluationDataset) -> EvaluationDataset:
        self.session.add(dataset)
        await self.session.commit()
        await self.session.refresh(dataset)
        return dataset

    async def get_evaluation_dataset(self, dataset_id: str) -> Optional[EvaluationDataset]:
        stmt = select(EvaluationDataset).options(selectinload(EvaluationDataset.cases)).where(EvaluationDataset.id == dataset_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_evaluation_datasets(self, tenant_id: str = "default_tenant") -> List[EvaluationDataset]:
        stmt = (
            select(EvaluationDataset)
            .options(selectinload(EvaluationDataset.cases))
            .where(EvaluationDataset.tenant_id == tenant_id)
            .order_by(desc(EvaluationDataset.created_at))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def record_evaluation_run(self, run: EvaluationRun) -> EvaluationRun:
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def list_evaluation_runs(self, tenant_id: str = "default_tenant", agent_key: Optional[str] = None) -> List[EvaluationRun]:
        stmt = select(EvaluationRun).where(EvaluationRun.tenant_id == tenant_id).order_by(desc(EvaluationRun.completed_at))
        if agent_key:
            stmt = stmt.where(EvaluationRun.agent_key == agent_key)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # =========================================================================
    # 4. Human Evaluations & Revisions
    # =========================================================================

    async def record_human_evaluation(self, eval_rec: HumanEvaluation) -> HumanEvaluation:
        self.session.add(eval_rec)
        await self.session.commit()
        await self.session.refresh(eval_rec)
        return eval_rec

    async def record_human_revision(self, rev_rec: HumanRevisionRecord) -> HumanRevisionRecord:
        self.session.add(rev_rec)
        await self.session.commit()
        await self.session.refresh(rev_rec)
        return rev_rec

    # =========================================================================
    # 5. Incidents, Failures & Security
    # =========================================================================

    async def create_incident(self, incident: AIIncident) -> AIIncident:
        self.session.add(incident)
        await self.session.commit()
        await self.session.refresh(incident)
        return incident

    async def list_incidents(self, tenant_id: str = "default_tenant", status: Optional[str] = None) -> List[AIIncident]:
        stmt = select(AIIncident).where(AIIncident.tenant_id == tenant_id).order_by(desc(AIIncident.created_at))
        if status:
            stmt = stmt.where(AIIncident.status == status)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def record_failure(self, failure: AIFailureRecord) -> AIFailureRecord:
        self.session.add(failure)
        await self.session.commit()
        await self.session.refresh(failure)
        return failure

    async def record_security_event(self, event: AISecurityEvent) -> AISecurityEvent:
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    # =========================================================================
    # 6. Kill Switch & Health
    # =========================================================================

    async def record_kill_switch_event(self, event: AIKillSwitchEvent) -> AIKillSwitchEvent:
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_active_kill_switch_events(self, tenant_id: str = "default_tenant") -> List[AIKillSwitchEvent]:
        stmt = select(AIKillSwitchEvent).where(
            AIKillSwitchEvent.tenant_id == tenant_id,
            AIKillSwitchEvent.is_active == True,
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def record_health_snapshot(self, snapshot: AIHealthSnapshot) -> AIHealthSnapshot:
        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)
        return snapshot

    async def list_latest_health_snapshots(self, tenant_id: str = "default_tenant") -> List[AIHealthSnapshot]:
        stmt = select(AIHealthSnapshot).where(AIHealthSnapshot.tenant_id == tenant_id).order_by(desc(AIHealthSnapshot.captured_at)).limit(20)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
