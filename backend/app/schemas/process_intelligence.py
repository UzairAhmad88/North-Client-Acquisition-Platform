"""
Pydantic Schemas for Phase 49:
Unified Workflow Intelligence, Process Mining, Business Process Optimization & Operations.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProcessCreateRequest(BaseModel):
    name: str
    domain: str = "SALES"
    owner_id: str = "system"
    scope: str = "ORGANIZATION"
    expected_outcome: Optional[str] = None
    policy_requirements: List[str] = Field(default_factory=list)
    governance_controls: List[str] = Field(default_factory=list)


class ProcessResponse(BaseModel):
    id: str
    process_code: str
    tenant_id: str
    name: str
    description: Optional[str] = None
    domain: str
    owner_id: str
    version: int
    status: str
    scope: str
    expected_outcome: Optional[str] = None
    policy_requirements: List[str] = Field(default_factory=list)
    governance_controls: List[str] = Field(default_factory=list)
    kpis: Dict[str, Any] = Field(default_factory=dict)


class ProcessEventIngestRequest(BaseModel):
    process_id: str
    activity: str
    case_id: Optional[str] = None
    actor: str = "system"
    actor_type: str = "SYSTEM"
    resource: Optional[str] = None
    duration_ms: int = 0
    attributes: Dict[str, Any] = Field(default_factory=dict)
    anonymize_actor: bool = False


class ProcessEventResponse(BaseModel):
    id: str
    event_code: str
    process_id: Optional[str] = None
    case_id: Optional[str] = None
    activity: str
    timestamp: datetime
    actor: str
    actor_type: str
    resource: Optional[str] = None
    status: str
    duration_ms: int
    attributes: Dict[str, Any] = Field(default_factory=dict)


class ProcessCaseCreateRequest(BaseModel):
    process_id: str
    entity_type: str
    entity_id: str
    owner_id: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=list)


class ConformanceRuleCreateRequest(BaseModel):
    process_id: str
    rule_code: str
    rule_type: str
    source_activity: Optional[str] = None
    target_activity: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    severity: str = "HIGH"


class OptimizationProposalCreateRequest(BaseModel):
    process_id: str
    title: str
    problem_statement: str
    evidence_summary: str
    proposed_changes: Dict[str, Any] = Field(default_factory=dict)
    cycle_time_improvement_pct: float
    cost_savings_pct: float
    quality_score: float = 0.9
    risk_level: str = "LOW"
    compliance_score: float = 1.0
    expected_cost: float = 0.0
    rollback_plan: str


class SimulationRunRequest(BaseModel):
    process_id: str
    scenario_type: str = "OPTIMIZED"
    baseline_cycle_time_seconds: float = 36000.0
    baseline_cost_per_case: float = 150.0
    baseline_failure_rate: float = 0.08
    baseline_rework_rate: float = 0.15
    arrival_rate_multiplier: float = 1.0
    automation_efficiency_gain: float = 0.25
    resource_capacity_multiplier: float = 1.0
    iterations: int = 1000


class DeploymentInitiateRequest(BaseModel):
    process_id: str
    target_version: int
    strategy: str = "CANARY"
    rollout_percentage: int = 10
    proposal_id: Optional[str] = None
    approved_by: str = "governance_committee"


class DeploymentRollbackRequest(BaseModel):
    deployment_code: str
    reason: str
    operator_id: str


class ProcessCopilotRequest(BaseModel):
    process_id: str
    query: str
