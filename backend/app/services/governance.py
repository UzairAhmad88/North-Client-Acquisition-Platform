"""Service layer for Phase 33: AI Agent Evaluation, Observability & Governance."""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

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
    AITrace,
    AITraceEvent,
    AgentHealthStatus,
    EvaluationCase,
    EvaluationDataset,
    EvaluationRun,
    EvaluationType,
    HumanEvaluation,
    HumanRevisionRecord,
    KillSwitchLevel,
    PromptRegistryItem,
    PromptStatus,
    PromptVersion,
    TraceStatus,
)
from app.repositories.governance import GovernanceRepository
from agents.governance.agent import AIGovernanceAgent
from agents.governance.models import KillSwitchCommand, PromptDraft


class GovernanceService:
    """Orchestrates AI Tracing, Prompt Management, Golden Benchmark Evaluations, and Kill-Switch controls."""

    def __init__(self, repository: GovernanceRepository):
        self.repo = repository
        self.agent = AIGovernanceAgent()

    # =========================================================================
    # 1. Traces & Observability
    # =========================================================================

    async def start_trace(
        self,
        workflow_id: str,
        agent_id: str,
        agent_version: str = "v1.0",
        model_id: str = "gpt-4o-mini",
        model_version: str = "v1.0",
        prompt_version: str = "v1.0",
        project_id: Optional[str] = None,
        lead_id: Optional[str] = None,
        tenant_id: str = "default_tenant",
    ) -> AITrace:
        trace = AITrace(
            tenant_id=tenant_id,
            workflow_id=workflow_id,
            project_id=project_id,
            lead_id=lead_id,
            agent_id=agent_id,
            agent_version=agent_version,
            model_id=model_id,
            model_version=model_version,
            prompt_version=prompt_version,
            status=TraceStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        return await self.repo.create_trace(trace)

    async def complete_trace(
        self,
        trace_id: str,
        total_tokens: int,
        estimated_cost: float,
        total_duration_ms: float,
        status: str = "COMPLETED",
    ) -> Optional[AITrace]:
        trace = await self.repo.get_trace(trace_id)
        if not trace:
            return None
        trace.total_tokens = total_tokens
        trace.estimated_cost = estimated_cost
        trace.total_duration_ms = total_duration_ms
        trace.status = TraceStatus(status) if status in TraceStatus.__members__ else TraceStatus.COMPLETED
        trace.completed_at = datetime.utcnow()
        await self.repo.session.commit()
        await self.repo.session.refresh(trace)
        return trace

    async def add_trace_event(
        self,
        trace_id: str,
        span_type: str,
        name: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        tokens_consumed: int = 0,
        duration_ms: float = 0.0,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
        tenant_id: str = "default_tenant",
    ) -> AITraceEvent:
        clean_in = self.agent.tracer.sanitize_event_summary(input_data)
        clean_out = self.agent.tracer.sanitize_event_summary(output_data)

        event = AITraceEvent(
            tenant_id=tenant_id,
            trace_id=trace_id,
            span_type=span_type,
            name=name,
            input_summary=clean_in,
            output_summary=clean_out,
            tokens_consumed=tokens_consumed,
            duration_ms=duration_ms,
            status=status,
            error_message=error_message,
        )
        return await self.repo.add_trace_event(event)

    async def list_traces(
        self,
        tenant_id: str = "default_tenant",
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[AITrace]:
        return await self.repo.list_traces(tenant_id, agent_id, status, limit)

    async def get_trace(self, trace_id: str) -> Optional[AITrace]:
        return await self.repo.get_trace(trace_id)

    # =========================================================================
    # 2. Prompts & Version Registry
    # =========================================================================

    async def register_prompt(
        self,
        prompt_key: str,
        name: str,
        agent_target: str,
        purpose: str,
        content: str,
        version: str = "v1.0",
        tenant_id: str = "default_tenant",
    ) -> PromptRegistryItem:
        validation = self.agent.prompt_registry.validate_prompt_safety(content)
        if not validation["is_valid"]:
            raise ValueError(f"Prompt safety violations: {'; '.join(validation['violations'])}")

        existing = await self.repo.get_prompt_item(prompt_key)
        if not existing:
            item = PromptRegistryItem(
                tenant_id=tenant_id,
                prompt_key=prompt_key,
                name=name,
                agent_target=agent_target,
                purpose=purpose,
                current_version=version,
            )
            created_item = await self.repo.create_prompt_item(item)
            p_id = created_item.id
        else:
            existing.current_version = version
            await self.repo.session.commit()
            p_id = existing.id
            created_item = existing

        # Add prompt version
        p_version = PromptVersion(
            tenant_id=tenant_id,
            prompt_id=p_id,
            version=version,
            content=content,
            content_hash=validation["content_hash"],
            status=PromptStatus.APPROVED,
            approved_by="system_governance_admin",
            approved_at=datetime.utcnow(),
        )
        await self.repo.add_prompt_version(p_version)
        return await self.repo.get_prompt_item(prompt_key) or created_item

    async def list_prompts(self, tenant_id: str = "default_tenant") -> List[PromptRegistryItem]:
        return await self.repo.list_prompts(tenant_id)

    # =========================================================================
    # 3. Evaluation Datasets & Regression Testing
    # =========================================================================

    async def create_dataset_with_cases(
        self,
        dataset_key: str,
        name: str,
        description: str,
        task_type: str,
        cases_data: List[Dict[str, Any]],
        is_golden: bool = True,
        tenant_id: str = "default_tenant",
    ) -> EvaluationDataset:
        dataset = EvaluationDataset(
            tenant_id=tenant_id,
            dataset_key=dataset_key,
            name=name,
            description=description,
            task_type=task_type,
            is_golden=is_golden,
            version="v1.0",
        )
        created_ds = await self.repo.create_evaluation_dataset(dataset)

        for case_info in cases_data:
            case = EvaluationCase(
                tenant_id=tenant_id,
                dataset_id=created_ds.id,
                title=case_info.get("title") or "Benchmark Test Case",
                input_context=case_info.get("input_context") or {},
                expected_output=case_info.get("expected_output") or {},
                evaluation_criteria=case_info.get("evaluation_criteria") or [],
                difficulty=case_info.get("difficulty") or "MEDIUM",
            )
            self.repo.session.add(case)

        await self.repo.session.commit()
        return await self.repo.get_evaluation_dataset(created_ds.id) or created_ds

    async def run_evaluation_benchmark(
        self,
        dataset_id: str,
        agent_key: str,
        agent_version: str = "v1.0",
        prompt_version: str = "v1.0",
        model_version: str = "v1.0",
        baseline_score: float = 90.0,
        tenant_id: str = "default_tenant",
    ) -> EvaluationRun:
        ds = await self.repo.get_evaluation_dataset(dataset_id)
        if not ds:
            raise ValueError(f"Evaluation dataset '{dataset_id}' not found.")

        cases_payload = [
            {
                "output": case.expected_output,
                "required_fields": list(case.expected_output.keys()) if case.expected_output else ["status"],
                "evidence_context": case.input_context,
            }
            for case in ds.cases
        ]

        benchmark = self.agent.regression_engine.execute_golden_suite_benchmark(
            agent_key=agent_key,
            agent_version=agent_version,
            prompt_version=prompt_version,
            model_version=model_version,
            cases=cases_payload,
            baseline_score=baseline_score,
        )

        run = EvaluationRun(
            tenant_id=tenant_id,
            dataset_id=dataset_id,
            agent_key=agent_key,
            agent_version=agent_version,
            prompt_version=prompt_version,
            model_version=model_version,
            evaluation_type=EvaluationType.REGRESSION_EVALUATION,
            overall_score=benchmark.overall_score,
            passed_cases_count=benchmark.passed_cases_count,
            failed_cases_count=benchmark.failed_cases_count,
            regression_detected=benchmark.regression_detected,
            regression_details=benchmark.regression_details,
            completed_at=datetime.utcnow(),
        )
        return await self.repo.record_evaluation_run(run)

    async def list_evaluation_datasets(self, tenant_id: str = "default_tenant") -> List[EvaluationDataset]:
        return await self.repo.list_evaluation_datasets(tenant_id)

    async def list_evaluation_runs(self, tenant_id: str = "default_tenant", agent_key: Optional[str] = None) -> List[EvaluationRun]:
        return await self.repo.list_evaluation_runs(tenant_id, agent_key)

    # =========================================================================
    # 4. Human Reviews, Incidents & Emergency Kill Switch
    # =========================================================================

    async def record_human_evaluation(
        self,
        trace_id: str,
        reviewer: str,
        correctness: int,
        completeness: int,
        evidence: int,
        safety: int,
        usefulness: int,
        notes: Optional[str] = None,
        tenant_id: str = "default_tenant",
    ) -> HumanEvaluation:
        eval_rec = HumanEvaluation(
            tenant_id=tenant_id,
            trace_id=trace_id,
            reviewer=reviewer,
            correctness_score=correctness,
            completeness_score=completeness,
            evidence_score=evidence,
            safety_score=safety,
            usefulness_score=usefulness,
            notes=notes,
        )
        return await self.repo.record_human_evaluation(eval_rec)

    async def create_incident(
        self,
        title: str,
        affected_agent: str,
        description: str,
        severity: str = "HIGH",
        containment_action: Optional[str] = None,
        tenant_id: str = "default_tenant",
    ) -> AIIncident:
        incident = AIIncident(
            tenant_id=tenant_id,
            incident_number=f"INC-AI-{uuid.uuid4().hex[:6].upper()}",
            title=title,
            severity=severity,
            status=AIIncidentStatus.DETECTED,
            affected_agent=affected_agent,
            description=description,
            containment_action=containment_action,
        )
        return await self.repo.create_incident(incident)

    async def list_incidents(self, tenant_id: str = "default_tenant", status: Optional[str] = None) -> List[AIIncident]:
        return await self.repo.list_incidents(tenant_id, status)

    async def trigger_kill_switch(
        self,
        level: str,
        target_key: str,
        is_active: bool,
        activated_by: str,
        reason: str,
        tenant_id: str = "default_tenant",
    ) -> AIKillSwitchEvent:
        cmd = KillSwitchCommand(
            level=level,
            target_key=target_key,
            is_active=is_active,
            activated_by=activated_by,
            reason=reason,
        )
        self.agent.kill_switch.set_kill_switch(cmd)

        event = AIKillSwitchEvent(
            tenant_id=tenant_id,
            level=KillSwitchLevel(level),
            target_key=target_key,
            is_active=is_active,
            activated_by=activated_by,
            reason=reason,
        )
        return await self.repo.record_kill_switch_event(event)

    async def get_active_kill_switches(self, tenant_id: str = "default_tenant") -> List[AIKillSwitchEvent]:
        return await self.repo.get_active_kill_switch_events(tenant_id)
