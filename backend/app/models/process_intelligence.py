"""
ORM models for Phase 49: Unified Workflow Intelligence, Process Mining, Business Process Optimization & Autonomous-but-Controlled Operations.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from app.models.base import BaseModel
except ImportError:
    from app.models.base import BaseModel


class ProcessDefinitionModel(BaseModel):
    """Registered business process definition."""

    __tablename__ = "process_definitions"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    process_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    domain: Mapped[str] = mapped_column(String(100), default="SALES", nullable=False, index=True)
    owner_id: Mapped[str] = mapped_column(String(100), default="system", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)  # DRAFT, DESIGNED, REVIEW, APPROVED, ACTIVE, MONITORING, OPTIMIZATION, SUPERSEDED, ARCHIVED
    scope: Mapped[str] = mapped_column(String(100), default="ORGANIZATION", nullable=False)
    trigger_type: Mapped[str] = mapped_column(String(100), default="EVENT", nullable=False)
    expected_outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    workflow_definition_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    policy_requirements: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    governance_controls: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    kpis: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProcessDefinitionVersionModel(BaseModel):
    """Immutable version history for process definitions."""

    __tablename__ = "process_definition_versions"

    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    definition_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    change_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)


class ProcessCaseModel(BaseModel):
    """Case instance representing an execution of a business process (e.g. Lead #104, Project #28)."""

    __tablename__ = "process_cases"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    case_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # lead, project, incident, contract, invoice
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cycle_time_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    waiting_time_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    processing_time_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)  # ACTIVE, COMPLETED, CANCELLED, FAILED, STALLED
    outcome: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # WON, LOST, DELIVERED, RESOLVED, ABANDONED
    owner_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    variant_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProcessCaseAttributeModel(BaseModel):
    """Dynamic key-value attributes for process cases."""

    __tablename__ = "process_case_attributes"

    case_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_cases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attribute_name: Mapped[str] = mapped_column(String(100), nullable=False)
    attribute_value: Mapped[str] = mapped_column(Text, nullable=False)
    data_type: Mapped[str] = mapped_column(String(50), default="STRING", nullable=False)


class ProcessEventLogModel(BaseModel):
    """Structured event log connecting events into traceable process instances."""

    __tablename__ = "process_event_logs"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    event_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_cases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    process_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    activity: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    actor: Mapped[str] = mapped_column(String(100), default="system", nullable=False)
    actor_type: Mapped[str] = mapped_column(String(50), default="SYSTEM", nullable=False)  # USER, AGENT, WORKER, SYSTEM, CLIENT, PROVIDER
    resource: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    entity_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    workflow_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    task_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="COMPLETED", nullable=False)  # STARTED, COMPLETED, FAILED, RETRIED, CANCELLED
    duration_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    source: Mapped[str] = mapped_column(String(100), default="SYSTEM_TELEMETRY", nullable=False)


class ProcessVariantModel(BaseModel):
    """Discovered process execution variant paths."""

    __tablename__ = "process_variants"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    variant_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_sequence: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    sequence_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    frequency: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    average_cycle_time_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    conversion_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    failure_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rework_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_conforming: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ProcessVariantEventModel(BaseModel):
    """Sequential events mapping for a variant."""

    __tablename__ = "process_variant_events"

    variant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_variants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    activity_name: Mapped[str] = mapped_column(String(255), nullable=False)
    average_duration_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class ProcessMapModel(BaseModel):
    """Graph representation of an observed or designed process."""

    __tablename__ = "process_maps"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    map_type: Mapped[str] = mapped_column(String(50), default="OBSERVED", nullable=False)  # OBSERVED, DESIGNED, OPTIMIZED, BENCHMARK
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    nodes_payload: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    edges_payload: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    metrics_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProcessTransitionModel(BaseModel):
    """Directly-follows transition edge in a process graph."""

    __tablename__ = "process_transitions"

    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_activity: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    target_activity: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    transition_frequency: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    average_latency_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    median_latency_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    failure_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class ProcessConformanceRuleModel(BaseModel):
    """Rules defining expected paths and constraints."""

    __tablename__ = "process_conformance_rules"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    rule_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    rule_type: Mapped[str] = mapped_column(String(50), default="MANDATORY_STEP", nullable=False)  # MANDATORY_STEP, STRICT_ORDER, EXCLUSIVE_CHOICE, REQUIRED_APPROVAL, MAX_REPETITIONS, SLA_MAX_HOURS
    source_activity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_activity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    parameters: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ProcessConformanceViolationModel(BaseModel):
    """Detected deviation from expected process definition."""

    __tablename__ = "process_conformance_violations"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_cases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_conformance_rules.id", ondelete="SET NULL"), nullable=True, index=True
    )
    violation_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    violation_type: Mapped[str] = mapped_column(String(50), default="SKIPPED_STEP", nullable=False)  # SKIPPED_STEP, EXTRA_STEP, OUT_OF_ORDER, UNAUTHORIZED_TRANSITION, UNEXPECTED_LOOP, MISSING_APPROVAL, SLA_BREACH
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    activity_involved: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="DETECTED", nullable=False)  # DETECTED, INVESTIGATING, EXCEPTION_GRANTED, REMEDIATED, DISMISSED


class ProcessBottleneckModel(BaseModel):
    """Identified bottlenecks with queue latency and root-cause evidence."""

    __tablename__ = "process_bottlenecks"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    bottleneck_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    activity_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bottleneck_type: Mapped[str] = mapped_column(String(50), default="WAIT_TIME", nullable=False)  # WAIT_TIME, QUEUE_DEPTH, MANUAL_HANDOFF, APPROVAL_DELAY, PROVIDER_DELAY, RESOURCE_CONTENTION
    average_wait_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    average_processing_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    queue_depth: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    frequency: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    affected_cases_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    root_cause_summary: Mapped[str] = mapped_column(Text, nullable=False)
    business_impact: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProcessReworkRecordModel(BaseModel):
    """Detection of repeated/looping activities indicating rework friction."""

    __tablename__ = "process_rework_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_cases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    activity_name: Mapped[str] = mapped_column(String(255), nullable=False)
    repetition_count: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    wasted_duration_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    probable_driver: Mapped[str] = mapped_column(String(100), default="SCOPE_INSTABILITY", nullable=False)  # REQUIREMENTS_QUALITY, CLIENT_CONFIRMATION, SCOPE_INSTABILITY, QA_REJECTION, COMMUNICATION
    evidence_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProcessHandoffRecordModel(BaseModel):
    """Metrics tracking transitions and latency between teams/roles."""

    __tablename__ = "process_handoff_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_role: Mapped[str] = mapped_column(String(100), nullable=False)
    target_role: Mapped[str] = mapped_column(String(100), nullable=False)
    handoff_type: Mapped[str] = mapped_column(String(100), default="DEPARTMENTAL", nullable=False)
    average_delay_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    handoff_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    friction_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    common_issues: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)


class ProcessResourceMetricModel(BaseModel):
    """Resource capacity and workload utilization metrics (strictly aggregated)."""

    __tablename__ = "process_resource_metrics"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="ROLE", nullable=False)  # ROLE, TEAM, AGENT, WORKER, SERVICE
    resource_identifier: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    active_cases_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    utilization_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    average_handling_time_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    blocked_time_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    snapshot_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ProcessAutomationCandidateModel(BaseModel):
    """Repetitive task candidates evaluated for workflow automation."""

    __tablename__ = "process_automation_candidates"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    candidate_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    task_name: Mapped[str] = mapped_column(String(255), nullable=False)
    frequency_per_month: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_duration_minutes: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    error_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reversibility: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)  # HIGH, MODERATE, LOW, IRREVERSIBLE
    suitability_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    classification: Mapped[str] = mapped_column(String(50), default="REVIEW_REQUIRED", nullable=False)  # LOW_RISK_AUTOMATION, REVIEW_REQUIRED, HIGH_RISK_AUTOMATION, NOT_SUITABLE
    expected_savings_hours_month: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="IDENTIFIED", nullable=False)  # IDENTIFIED, UNDER_REVIEW, APPROVED, REJECTED, IMPLEMENTED


class ProcessOptimizationProposalModel(BaseModel):
    """Multi-objective optimization proposal for controlled workflow deployment."""

    __tablename__ = "process_optimization_proposals"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    proposal_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    proposed_version: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    problem_statement: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_summary: Mapped[str] = mapped_column(Text, nullable=False)
    proposed_changes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    tradeoff_scorecard: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)  # cycle_time, cost, quality, risk, compliance
    expected_benefits: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    expected_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)  # LOW, MODERATE, HIGH
    rollback_plan: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(100), default="system", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False)  # DRAFT, ANALYSIS, SIMULATION, RISK_REVIEW, GOVERNANCE_REVIEW, HUMAN_APPROVAL, APPROVED, REJECTED, CANARY, FULL_ROLLOUT


class ProcessSimulationRunModel(BaseModel):
    """Isolated what-if simulation run (never mutates production state)."""

    __tablename__ = "process_simulation_runs"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    simulation_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    proposal_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_optimization_proposals.id", ondelete="SET NULL"), nullable=True, index=True
    )
    scenario_type: Mapped[str] = mapped_column(String(50), default="OPTIMIZED", nullable=False)  # BASELINE, OPTIMIZED, CONSERVATIVE, AGGRESSIVE, HIGH_VOLUME, LOW_RESOURCE
    iterations: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    assumptions_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    predicted_throughput: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    predicted_cycle_time_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    predicted_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    predicted_failure_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    predicted_rework_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    results_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="COMPLETED", nullable=False)


class ProcessSimulationAssumptionModel(BaseModel):
    """Explicit parameters and constraints used during what-if simulation."""

    __tablename__ = "process_simulation_assumptions"

    simulation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_simulation_runs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assumption_key: Mapped[str] = mapped_column(String(100), nullable=False)
    assumption_value: Mapped[str] = mapped_column(String(255), nullable=False)
    source_basis: Mapped[str] = mapped_column(String(100), default="HISTORICAL_LOG", nullable=False)


class ProcessExperimentModel(BaseModel):
    """A/B process comparison experiment."""

    __tablename__ = "process_experiments"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    experiment_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    variant_a_definition: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    variant_b_definition: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    allocation_percentage_b: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PLANNED", nullable=False)  # PLANNED, ACTIVE, PAUSED, CONCLUDED
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    results_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProcessDeploymentModel(BaseModel):
    """Controlled deployment record for approved workflow optimizations."""

    __tablename__ = "process_deployments"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    deployment_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    proposal_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_optimization_proposals.id", ondelete="SET NULL"), nullable=True, index=True
    )
    strategy: Mapped[str] = mapped_column(String(50), default="CANARY", nullable=False)  # SHADOW, CANARY, PERCENTAGE_ROLLOUT, TENANT_LIMITED, FULL
    rollout_percentage: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    target_version: Mapped[int] = mapped_column(Integer, nullable=False)
    approved_by: Mapped[str] = mapped_column(String(100), nullable=False)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)  # ACTIVE, PAUSED, PROMOTED_TO_FULL, ROLLED_BACK
    health_status: Mapped[str] = mapped_column(String(50), default="HEALTHY", nullable=False)  # HEALTHY, DEGRADED, CRITICAL
    canary_metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class ProcessHealthSnapshotModel(BaseModel):
    """Periodic health state snapshot of a business process."""

    __tablename__ = "process_health_snapshots"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    health_status: Mapped[str] = mapped_column(String(50), default="HEALTHY", nullable=False)  # HEALTHY, DEGRADED, AT_RISK, CRITICAL, BLOCKED, UNKNOWN
    cycle_time_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    conformance_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    failure_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    rework_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    slo_compliance_rate: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    factors_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    snapshot_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ProcessRiskAssessmentModel(BaseModel):
    """Pre-deployment and runtime multi-dimension risk assessment."""

    __tablename__ = "process_risk_assessments"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    process_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("process_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    security_risk: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    compliance_risk: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    operational_risk: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    financial_risk: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    customer_risk: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    composite_risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    risk_tier: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)  # LOW, MODERATE, HIGH, CRITICAL
    findings: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
