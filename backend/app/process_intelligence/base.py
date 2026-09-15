"""
Canonical base types, enums, and domain schemas for Phase 49: Unified Process Intelligence.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class ProcessDomain(str, Enum):
    LEAD_DISCOVERY = "LEAD_DISCOVERY"
    RESEARCH = "RESEARCH"
    QUALIFICATION = "QUALIFICATION"
    OUTREACH = "OUTREACH"
    SALES = "SALES"
    CLIENT_ONBOARDING = "CLIENT_ONBOARDING"
    REQUIREMENTS = "REQUIREMENTS"
    SOLUTION_DESIGN = "SOLUTION_DESIGN"
    ESTIMATION = "ESTIMATION"
    PROPOSAL = "PROPOSAL"
    CONTRACT = "CONTRACT"
    PROJECT_INITIATION = "PROJECT_INITIATION"
    PROJECT_DELIVERY = "PROJECT_DELIVERY"
    CHANGE_MANAGEMENT = "CHANGE_MANAGEMENT"
    QA = "QA"
    UAT = "UAT"
    DELIVERY = "DELIVERY"
    HANDOVER = "HANDOVER"
    SUPPORT = "SUPPORT"
    MAINTENANCE = "MAINTENANCE"
    BILLING = "BILLING"
    PAYMENTS = "PAYMENTS"
    CUSTOMER_SUCCESS = "CUSTOMER_SUCCESS"
    RENEWALS = "RENEWALS"
    AI_OPERATIONS = "AI_OPERATIONS"
    SECURITY = "SECURITY"
    GOVERNANCE = "GOVERNANCE"
    INCIDENT_MANAGEMENT = "INCIDENT_MANAGEMENT"
    VENDOR_MANAGEMENT = "VENDOR_MANAGEMENT"


class ProcessLifecycle(str, Enum):
    DRAFT = "DRAFT"
    DESIGNED = "DESIGNED"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    MONITORING = "MONITORING"
    OPTIMIZATION = "OPTIMIZATION"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"


class ProcessHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class ActorType(str, Enum):
    USER = "USER"
    AGENT = "AGENT"
    WORKER = "WORKER"
    SYSTEM = "SYSTEM"
    CLIENT = "CLIENT"
    PROVIDER = "PROVIDER"


class ViolationType(str, Enum):
    SKIPPED_STEP = "SKIPPED_STEP"
    EXTRA_STEP = "EXTRA_STEP"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    UNAUTHORIZED_TRANSITION = "UNAUTHORIZED_TRANSITION"
    UNEXPECTED_LOOP = "UNEXPECTED_LOOP"
    MISSING_APPROVAL = "MISSING_APPROVAL"
    SLA_BREACH = "SLA_BREACH"


class BottleneckType(str, Enum):
    WAIT_TIME = "WAIT_TIME"
    QUEUE_DEPTH = "QUEUE_DEPTH"
    MANUAL_HANDOFF = "MANUAL_HANDOFF"
    APPROVAL_DELAY = "APPROVAL_DELAY"
    PROVIDER_DELAY = "PROVIDER_DELAY"
    RESOURCE_CONTENTION = "RESOURCE_CONTENTION"


class ReworkDriver(str, Enum):
    REQUIREMENTS_QUALITY = "REQUIREMENTS_QUALITY"
    CLIENT_CONFIRMATION = "CLIENT_CONFIRMATION"
    SCOPE_INSTABILITY = "SCOPE_INSTABILITY"
    QA_REJECTION = "QA_REJECTION"
    COMMUNICATION_ISSUE = "COMMUNICATION_ISSUE"


class AutomationSuitability(str, Enum):
    LOW_RISK_AUTOMATION = "LOW_RISK_AUTOMATION"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    HIGH_RISK_AUTOMATION = "HIGH_RISK_AUTOMATION"
    NOT_SUITABLE = "NOT_SUITABLE"


class OptimizationStatus(str, Enum):
    DRAFT = "DRAFT"
    ANALYSIS = "ANALYSIS"
    SIMULATION = "SIMULATION"
    RISK_REVIEW = "RISK_REVIEW"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANARY = "CANARY"
    FULL_ROLLOUT = "FULL_ROLLOUT"


class DeploymentStrategy(str, Enum):
    SHADOW = "SHADOW"
    CANARY = "CANARY"
    PERCENTAGE_ROLLOUT = "PERCENTAGE_ROLLOUT"
    TENANT_LIMITED = "TENANT_LIMITED"
    FULL = "FULL"


class SimulationScenario(str, Enum):
    BASELINE = "BASELINE"
    OPTIMIZED = "OPTIMIZED"
    CONSERVATIVE = "CONSERVATIVE"
    AGGRESSIVE = "AGGRESSIVE"
    HIGH_VOLUME = "HIGH_VOLUME"
    LOW_RESOURCE = "LOW_RESOURCE"


# Pydantic Schemas

class ProcessDefinition(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    process_code: str
    name: str
    description: Optional[str] = None
    domain: ProcessDomain = ProcessDomain.SALES
    owner_id: str = "system"
    version: int = 1
    status: ProcessLifecycle = ProcessLifecycle.ACTIVE
    scope: str = "ORGANIZATION"
    trigger_type: str = "EVENT"
    expected_outcome: Optional[str] = None
    workflow_definition_id: Optional[str] = None
    policy_requirements: List[str] = Field(default_factory=list)
    governance_controls: List[str] = Field(default_factory=list)
    kpis: Dict[str, Any] = Field(default_factory=dict)
    metadata_payload: Dict[str, Any] = Field(default_factory=dict)


class ProcessEvent(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    event_code: str = Field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8].upper()}")
    case_id: Optional[str] = None
    process_id: Optional[str] = None
    activity: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str = "system"
    actor_type: ActorType = ActorType.SYSTEM
    resource: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    workflow_id: Optional[str] = None
    task_id: Optional[str] = None
    status: str = "COMPLETED"
    duration_ms: int = 0
    attributes: Dict[str, Any] = Field(default_factory=dict)
    source: str = "SYSTEM_TELEMETRY"


class ProcessCase(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    case_code: str
    process_id: str
    entity_type: str
    entity_id: str
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    cycle_time_seconds: Optional[float] = None
    waiting_time_seconds: Optional[float] = None
    processing_time_seconds: Optional[float] = None
    status: str = "ACTIVE"
    outcome: Optional[str] = None
    owner_id: Optional[str] = None
    variant_id: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class ProcessVariant(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    process_id: str
    variant_code: str
    event_sequence: List[str]
    sequence_hash: str
    frequency: int = 1
    percentage: float = 0.0
    average_cycle_time_seconds: float = 0.0
    conversion_rate: float = 0.0
    failure_rate: float = 0.0
    rework_rate: float = 0.0
    is_conforming: bool = True


class TransitionEdge(BaseModel):
    source_activity: str
    target_activity: str
    transition_frequency: int = 1
    average_latency_seconds: float = 0.0
    median_latency_seconds: float = 0.0
    failure_count: int = 0


class ProcessMap(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    process_id: str
    map_type: str = "OBSERVED"
    version_number: int = 1
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[TransitionEdge] = Field(default_factory=list)
    metrics_summary: Dict[str, Any] = Field(default_factory=dict)


class ConformanceViolation(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    process_id: str
    case_id: Optional[str] = None
    rule_id: Optional[str] = None
    violation_code: str
    violation_type: ViolationType
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    activity_involved: str
    severity: str = "HIGH"
    description: str
    evidence_payload: Dict[str, Any] = Field(default_factory=dict)
    status: str = "DETECTED"


class BottleneckRecord(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    process_id: str
    bottleneck_code: str
    activity_name: str
    bottleneck_type: BottleneckType = BottleneckType.WAIT_TIME
    average_wait_seconds: float = 0.0
    average_processing_seconds: float = 0.0
    queue_depth: int = 0
    frequency: int = 1
    affected_cases_count: int = 0
    root_cause_summary: str
    business_impact: str
    severity: str = "MEDIUM"
    recommendation: Optional[str] = None
    evidence_payload: Dict[str, Any] = Field(default_factory=dict)


class ReworkRecord(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    process_id: str
    case_id: Optional[str] = None
    activity_name: str
    repetition_count: int = 2
    wasted_duration_seconds: float = 0.0
    probable_driver: ReworkDriver = ReworkDriver.SCOPE_INSTABILITY
    evidence_payload: Dict[str, Any] = Field(default_factory=dict)


class HandoffRecord(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    process_id: str
    source_role: str
    target_role: str
    handoff_type: str = "DEPARTMENTAL"
    average_delay_seconds: float = 0.0
    handoff_count: int = 1
    friction_score: float = 0.0
    common_issues: List[str] = Field(default_factory=list)


class AutomationCandidate(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    candidate_code: str
    process_id: str
    task_name: str
    frequency_per_month: int = 0
    average_duration_minutes: float = 0.0
    error_rate: float = 0.0
    reversibility: str = "HIGH"
    suitability_score: float = 0.0
    classification: AutomationSuitability = AutomationSuitability.REVIEW_REQUIRED
    expected_savings_hours_month: float = 0.0
    status: str = "IDENTIFIED"


class OptimizationProposal(BaseModel):
    id: Optional[str] = None
    tenant_id: str = "default_tenant"
    proposal_code: str
    process_id: str
    title: str
    current_version: int = 1
    proposed_version: int = 2
    problem_statement: str
    evidence_summary: str
    proposed_changes: Dict[str, Any] = Field(default_factory=dict)
    tradeoff_scorecard: Dict[str, Any] = Field(default_factory=dict)
    expected_benefits: Dict[str, Any] = Field(default_factory=dict)
    expected_cost: float = 0.0
    risk_level: str = "LOW"
    rollback_plan: str
    owner_id: str = "system"
    status: OptimizationStatus = OptimizationStatus.DRAFT


class SimulationResult(BaseModel):
    simulation_code: str
    process_id: str
    scenario_type: SimulationScenario
    iterations: int = 1000
    predicted_throughput: float
    predicted_cycle_time_seconds: float
    predicted_cost: float
    predicted_failure_rate: float
    predicted_rework_rate: float
    results_summary: Dict[str, Any] = Field(default_factory=dict)
    assumptions: Dict[str, Any] = Field(default_factory=dict)


class ProcessHealthReport(BaseModel):
    process_id: str
    health_status: ProcessHealthStatus
    cycle_time_score: float
    conformance_score: float
    failure_score: float
    rework_score: float
    slo_compliance_rate: float
    factors_summary: Dict[str, Any] = Field(default_factory=dict)
