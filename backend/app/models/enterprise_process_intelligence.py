"""
Phase 78: Enterprise Process Intelligence, Process Mining & Autonomous Process Optimization Models.
Table Prefix: epi_*
Zero-collision namespace with Phases 0-77.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class EpiProcessCatalogModel(BaseModel):
    """Governed central registry entry for an enterprise business process."""
    __tablename__ = "epi_process_catalog"

    process_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    domain = Column(String(64), nullable=False, index=True)  # FINANCE, OPERATIONS, SALES, HR, IT, CUSTOMER_SUPPORT
    department = Column(String(128), nullable=False)
    owner = Column(String(255), nullable=False)
    version = Column(String(32), default="1.0.0", nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)  # ACTIVE, UNDER_REVIEW, DEPRECATED, PROPOSED
    criticality = Column(String(32), default="HIGH", nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    automation_level = Column(String(32), default="HYBRID", nullable=False)  # MANUAL, ASSISTED, HYBRID, AUTONOMOUS
    systems = Column(JSON, default=list, nullable=False)
    kpis = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessVersionModel(BaseModel):
    """Immutable version history of a process specification with approval records."""
    __tablename__ = "epi_process_versions"

    process_code = Column(String(64), nullable=False, index=True)
    version_number = Column(String(32), nullable=False)
    change_reason = Column(Text, nullable=False)
    author = Column(String(255), nullable=False)
    approved_by = Column(String(255), nullable=True)
    bpmn_xml = Column(Text, nullable=True)
    effective_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiValueStreamModel(BaseModel):
    """End-to-end value stream mapping linking customer need to customer outcome."""
    __tablename__ = "epi_value_streams"

    value_stream_code = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(64), nullable=False)
    lead_time_days = Column(Float, default=14.0, nullable=False)
    process_time_hours = Column(Float, default=26.5, nullable=False)
    activity_waste_percentage = Column(Float, default=18.5, nullable=False)
    stages = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiEventLogModel(BaseModel):
    """Normalized process event log dataset imported from enterprise systems."""
    __tablename__ = "epi_event_logs"

    log_code = Column(String(64), unique=True, nullable=False, index=True)
    source_system = Column(String(64), nullable=False)  # SAP_ERP, SALESFORCE, JIRA, SERVICE_NOW, STRIPE
    process_code = Column(String(64), nullable=False, index=True)
    event_count = Column(Integer, default=0, nullable=False)
    case_count = Column(Integer, default=0, nullable=False)
    start_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    schema_mapping = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessCaseModel(BaseModel):
    """Individual workflow case instance tracked through end-to-end execution."""
    __tablename__ = "epi_process_cases"

    case_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    current_activity = Column(String(128), nullable=False)
    status = Column(String(32), default="RUNNING", nullable=False)  # RUNNING, COMPLETED, BLOCKED, CANCELLED
    duration_hours = Column(Float, default=0.0, nullable=False)
    is_conforming = Column(Boolean, default=True, nullable=False)
    is_bottlenecked = Column(Boolean, default=False, nullable=False)
    sla_status = Column(String(32), default="ON_TRACK", nullable=False)  # ON_TRACK, AT_RISK, BREACHED
    assigned_actor = Column(String(255), nullable=True)
    case_attributes = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessModelModel(BaseModel):
    """Discovered or designed process graph representation (BPMN / DFG / Petri Net)."""
    __tablename__ = "epi_process_models"

    model_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    model_type = Column(String(32), default="BPMN", nullable=False)  # BPMN, DFG, PETRI_NET, PROCESS_TREE
    node_count = Column(Integer, default=0, nullable=False)
    edge_count = Column(Integer, default=0, nullable=False)
    conformance_fitness = Column(Float, default=0.95, nullable=False)
    conformance_precision = Column(Float, default=0.92, nullable=False)
    graph_topology = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessVariantModel(BaseModel):
    """Distinct execution path variant observed across process cases."""
    __tablename__ = "epi_process_variants"

    variant_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    activity_sequence = Column(JSON, default=list, nullable=False)
    frequency_percentage = Column(Float, default=0.0, nullable=False)
    case_count = Column(Integer, default=0, nullable=False)
    avg_duration_hours = Column(Float, default=0.0, nullable=False)
    avg_cost_dollars = Column(Float, default=0.0, nullable=False)
    is_happy_path = Column(Boolean, default=False, nullable=False)
    is_compliant = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiConformanceRunModel(BaseModel):
    """Conformance check analysis comparing observed event traces against reference model."""
    __tablename__ = "epi_conformance_runs"

    run_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    total_cases_analyzed = Column(Integer, default=0, nullable=False)
    conforming_cases_count = Column(Integer, default=0, nullable=False)
    fitness_score = Column(Float, default=0.94, nullable=False)
    precision_score = Column(Float, default=0.91, nullable=False)
    violation_count = Column(Integer, default=0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiBottleneckModel(BaseModel):
    """Identified operational bottleneck with quantified delay and resource impact."""
    __tablename__ = "epi_bottlenecks"

    bottleneck_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    activity_name = Column(String(128), nullable=False)
    bottleneck_type = Column(String(64), nullable=False)  # QUEUE_DELAY, RESOURCE_CONTENTION, APPROVAL_STALL, MANUAL_REWORK
    severity = Column(String(32), default="HIGH", nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    avg_wait_hours = Column(Float, default=48.0, nullable=False)
    queue_depth = Column(Integer, default=24, nullable=False)
    estimated_annual_cost = Column(Float, default=125000.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiRootCauseModel(BaseModel):
    """Causal root cause analysis backing observed operational failures."""
    __tablename__ = "epi_root_causes"

    cause_code = Column(String(64), unique=True, nullable=False, index=True)
    bottleneck_code = Column(String(64), nullable=False, index=True)
    primary_factor = Column(String(255), nullable=False)
    causal_strength = Column(Float, default=0.88, nullable=False)
    evidence_summary = Column(Text, nullable=False)
    counterfactual_insight = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessWasteModel(BaseModel):
    """Lean operational waste quantification (TIMWOODS)."""
    __tablename__ = "epi_process_waste"

    waste_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    waste_category = Column(String(64), nullable=False)  # WAITING, REWORK, DUPLICATE_ENTRY, UNNECESSARY_APPROVAL
    affected_activity = Column(String(128), nullable=False)
    hours_wasted_per_month = Column(Float, default=180.0, nullable=False)
    cost_impact_dollars = Column(Float, default=22500.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessCostModel(BaseModel):
    """Activity-based costing allocation across labor, systems, and rework."""
    __tablename__ = "epi_process_costs"

    cost_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    total_cost_per_case = Column(Float, default=145.0, nullable=False)
    labor_cost_share = Column(Float, default=0.65, nullable=False)
    system_cost_share = Column(Float, default=0.15, nullable=False)
    rework_cost_share = Column(Float, default=0.20, nullable=False)
    annual_spend = Column(Float, default=580000.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessSlaModel(BaseModel):
    """Process SLA targets, compliance tracking, and predictive breach alerts."""
    __tablename__ = "epi_process_slas"

    sla_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    sla_name = Column(String(128), nullable=False)
    target_hours = Column(Float, default=24.0, nullable=False)
    current_compliance_rate = Column(Float, default=94.5, nullable=False)
    active_breaches_count = Column(Integer, default=2, nullable=False)
    predicted_breaches_count = Column(Integer, default=4, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessControlModel(BaseModel):
    """Mapping between process activities and mandatory compliance/SoD controls."""
    __tablename__ = "epi_process_controls"

    control_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    control_type = Column(String(64), nullable=False)  # SEGREGATION_OF_DUTIES, APPROVAL_GATE, AUDIT_SAMPLE
    target_activity = Column(String(128), nullable=False)
    policy_reference = Column(String(128), nullable=False)
    effectiveness_score = Column(Float, default=0.98, nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessSimulationModel(BaseModel):
    """Discrete-event simulation scenario predicting impact of proposed changes."""
    __tablename__ = "epi_process_simulations"

    sim_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    scenario_name = Column(String(255), nullable=False)
    variables = Column(JSON, default=dict, nullable=False)
    predicted_cycle_time_delta = Column(Float, default=-28.5, nullable=False)  # e.g. -28.5% time
    predicted_cost_delta = Column(Float, default=-18.0, nullable=False)        # e.g. -18% cost
    confidence_interval = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessOptimizationModel(BaseModel):
    """Multi-objective Pareto optimization balancing speed, cost, quality, and risk."""
    __tablename__ = "epi_process_optimizations"

    opt_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    objective_weights = Column(JSON, default=dict, nullable=False)
    pareto_solutions = Column(JSON, default=list, nullable=False)
    recommended_solution = Column(JSON, default=dict, nullable=False)
    status = Column(String(32), default="COMPLETED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiAutomationOpportunityModel(BaseModel):
    """Identified task automation candidate with estimated ROI and feasibility."""
    __tablename__ = "epi_automation_opportunities"

    opp_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    activity_name = Column(String(128), nullable=False)
    automation_type = Column(String(64), nullable=False)  # API_AUTOMATION, AI_AGENT, RULES_ENGINE, RPA
    feasibility_score = Column(Float, default=0.88, nullable=False)
    annual_savings_dollars = Column(Float, default=85000.0, nullable=False)
    implementation_cost_dollars = Column(Float, default=22000.0, nullable=False)
    payback_months = Column(Float, default=3.1, nullable=False)
    risk_level = Column(String(32), default="LOW", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessChangeRequestModel(BaseModel):
    """Formal, governed process change request with simulation evidence and approval record."""
    __tablename__ = "epi_process_change_requests"

    change_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    proposed_version = Column(String(32), nullable=False)
    description = Column(Text, nullable=False)
    simulation_code = Column(String(64), nullable=True)
    status = Column(String(32), default="PENDING_APPROVAL", nullable=False)  # PENDING_APPROVAL, APPROVED, REJECTED, DEPLOYED, ROLLED_BACK
    approved_by = Column(String(255), nullable=True)
    rollback_plan = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class EpiProcessDriftEventModel(BaseModel):
    """Detected deviation where observed execution drifts significantly from approved baseline."""
    __tablename__ = "epi_process_drift_events"

    drift_code = Column(String(64), unique=True, nullable=False, index=True)
    process_code = Column(String(64), nullable=False, index=True)
    drift_metric = Column(String(64), nullable=False)  # CYCLE_TIME_SPIKE, UNAPPROVED_VARIANT, UNEXPECTED_REWORK
    observed_delta_percentage = Column(Float, default=35.0, nullable=False)
    threshold_percentage = Column(Float, default=15.0, nullable=False)
    severity = Column(String(32), default="HIGH", nullable=False)
    alert_emitted = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)
