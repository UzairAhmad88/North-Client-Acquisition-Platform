"""
Phase 78: Enterprise Process Intelligence, Process Mining & Autonomous Optimization Schemas.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# Command Center Summary
class ProcessCommandCenterSummaryResponse(BaseModel):
    total_processes_cataloged: int
    active_process_cases: int
    overall_conformance_rate: float
    active_bottlenecks_count: int
    open_sla_breaches_count: int
    identified_automation_opportunities: int
    total_annual_waste_identified_dollars: float
    active_process_agents: int
    platform_health_score: float
    status: str


# Process Discovery Schemas
class ProcessDiscoveryRequest(BaseModel):
    process_code: str
    source_system: Optional[str] = "ALL"
    model_type: str = Field("BPMN", description="BPMN, DFG, PETRI_NET, PROCESS_TREE")
    time_window_days: int = Field(30, ge=1, le=365)
    tenant_id: str = Field("tenant-default")


class ProcessDiscoveryResponse(BaseModel):
    process_code: str
    model_type: str
    discovered_nodes_count: int
    discovered_edges_count: int
    variants_count: int
    happy_path_variant_code: str
    fitness_score: float
    precision_score: float
    graph_topology: Dict[str, Any]
    discovered_at: datetime = Field(default_factory=datetime.utcnow)


# Conformance Checking Schemas
class ConformanceCheckRequest(BaseModel):
    process_code: str
    reference_model_code: str
    tenant_id: str = Field("tenant-default")


class ConformanceCheckResponse(BaseModel):
    process_code: str
    cases_analyzed: int
    conformance_rate_percentage: float
    deviations_count: int
    skipped_approvals_count: int
    unauthorized_paths_count: int
    severity_breakdown: Dict[str, int]
    top_deviations: List[Dict[str, Any]]


# Bottleneck & Waste Schemas
class BottleneckDetectionResponse(BaseModel):
    process_code: str
    total_bottlenecks: int
    critical_activity: str
    avg_wait_hours: float
    queue_depth: int
    estimated_annual_cost: float
    root_cause_factor: str
    lean_waste_category: str
    recommended_mitigation: str


class ProcessWasteAnalysisResponse(BaseModel):
    process_code: str
    total_hours_wasted_per_month: float
    total_monthly_waste_cost: float
    waste_by_category: Dict[str, float]  # WAITING, REWORK, UNNECESSARY_APPROVAL
    top_wasteful_activities: List[Dict[str, Any]]


# Simulation & What-If Schemas
class ProcessSimulationRequest(BaseModel):
    process_code: str
    scenario_name: str
    modified_variables: Dict[str, Any] = Field(
        ...,
        description="e.g. {'remove_approval': True, 'resource_capacity_delta': 2, 'arrival_rate_multiplier': 1.2}"
    )
    tenant_id: str = Field("tenant-default")


class ProcessSimulationResponse(BaseModel):
    sim_code: str
    scenario_name: str
    predicted_cycle_time_delta_percent: float
    predicted_cost_delta_percent: float
    predicted_throughput_delta_percent: float
    sla_compliance_delta_percent: float
    confidence_interval: Dict[str, float]
    discrete_event_metrics: Dict[str, Any]


# Optimization & Pareto Frontier Schemas
class ProcessOptimizationRequest(BaseModel):
    process_code: str
    weights: Dict[str, float] = Field(
        default_factory=lambda: {"cost": 0.3, "speed": 0.4, "quality": 0.2, "risk": 0.1}
    )
    tenant_id: str = Field("tenant-default")


class ProcessOptimizationResponse(BaseModel):
    opt_code: str
    process_code: str
    pareto_solutions_count: int
    recommended_option: Dict[str, Any]
    tradeoff_matrix: List[Dict[str, Any]]


# Automation Opportunity Schemas
class AutomationOpportunityItem(BaseModel):
    opp_code: str
    activity_name: str
    automation_type: str  # AI_AGENT, API_AUTOMATION, RULES_ENGINE, RPA
    feasibility_score: float
    annual_savings: float
    implementation_cost: float
    payback_months: float
    risk_level: str


class AutomationOpportunitiesResponse(BaseModel):
    process_code: str
    total_opportunities: int
    total_potential_annual_savings: float
    opportunities: List[AutomationOpportunityItem]


# Change Control Schemas
class ProcessChangeSubmitRequest(BaseModel):
    process_code: str
    proposed_version: str
    description: str
    simulation_code: Optional[str] = None
    rollback_plan: str
    submitter: str = "ProcessArchitect"
    tenant_id: str = Field("tenant-default")


class ProcessChangeResponse(BaseModel):
    change_code: str
    process_code: str
    proposed_version: str
    status: str  # PENDING_APPROVAL, APPROVED, DEPLOYED
    audit_id: str


# Case Routing & Copilot
class CaseRoutingRequest(BaseModel):
    case_code: str
    process_code: str
    urgency: str = "HIGH"
    risk_tier: str = "MEDIUM"
    tenant_id: str = Field("tenant-default")


class CaseRoutingResponse(BaseModel):
    case_code: str
    routed_actor_type: str  # AI_AGENT, HUMAN_EXPERT, HYBRID_WORKFLOW
    assigned_target: str
    priority_rank: int
    sla_hours_remaining: float


class ProcessCopilotQueryRequest(BaseModel):
    query: str
    process_code: Optional[str] = None
    tenant_id: str = Field("tenant-default")


class ProcessCopilotQueryResponse(BaseModel):
    query: str
    answer: str
    grounded_evidence: List[str]
    suggested_actions: List[str]
