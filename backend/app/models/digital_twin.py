"""
ORM models for Phase 50: Unified Digital Twin, Business Simulation, Scenario Intelligence & Strategic What-If Engine.
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


class DigitalTwinModelModel(BaseModel):
    """Registered digital twin model definition."""

    __tablename__ = "digital_twin_models"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    organization_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    model_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scope: Mapped[str] = mapped_column(String(100), default="ORGANIZATION", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)  # DRAFT, ACTIVE, CALIBRATING, SUPERSEDED, ARCHIVED
    default_time_horizon: Mapped[str] = mapped_column(String(50), default="12_MONTHS", nullable=False)
    simulation_methods_supported: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class DigitalTwinModelVersionModel(BaseModel):
    """Immutable version history for digital twin model configurations."""

    __tablename__ = "digital_twin_model_versions"

    twin_model_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    change_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)


class DigitalTwinEntityModel(BaseModel):
    """Synchronized digital twin entity mapping to primary business records."""

    __tablename__ = "digital_twin_entities"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    twin_model_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True
    )
    entity_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # CLIENT, PROJECT, SERVICE, EMPLOYEE, PROCESS, AI_AGENT, INFRASTRUCTURE, RISK
    source_domain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source_entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    state_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class DigitalTwinEntityVersionModel(BaseModel):
    """Version lineage of digital twin entity states."""

    __tablename__ = "digital_twin_entity_versions"

    entity_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    state_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class DigitalTwinStateSnapshotModel(BaseModel):
    """Point-in-time state snapshot of the entire enterprise twin."""

    __tablename__ = "digital_twin_state_snapshots"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    twin_model_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    snapshot_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    commercial_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    delivery_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    operational_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    financial_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    ai_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    reliability_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    risk_state: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    composite_health_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    state_hash: Mapped[str] = mapped_column(String(64), nullable=False)


class DigitalTwinRelationshipModel(BaseModel):
    """Typed graph relationship between twin entities."""

    __tablename__ = "digital_twin_relationships"

    twin_model_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_entity_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_entity_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # DEPENDS_ON, GENERATES_REVENUE, INCURS_COST, EXECUTES_PROCESS, ALLOCATED_TO
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    properties: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class DigitalTwinParameterModel(BaseModel):
    """Configurable baseline or scenario parameter."""

    __tablename__ = "digital_twin_parameters"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    twin_model_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parameter_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="COMMERCIAL", nullable=False, index=True)  # COMMERCIAL, DELIVERY, OPERATIONS, FINANCE, AI, RELIABILITY
    current_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), default="RATIO", nullable=False)
    min_bound: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_bound: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class DigitalTwinParameterVersionModel(BaseModel):
    """Version history of calibrated parameters."""

    __tablename__ = "digital_twin_parameter_versions"

    parameter_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_parameters.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    calibration_reason: Mapped[str] = mapped_column(String(255), nullable=False)


class DigitalTwinAssumptionModel(BaseModel):
    """Explicit assumption attached to a simulation scenario."""

    __tablename__ = "digital_twin_assumptions"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    assumption_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    parameter_code: Mapped[str] = mapped_column(String(100), nullable=False)
    baseline_value: Mapped[float] = mapped_column(Float, nullable=False)
    assumed_value: Mapped[float] = mapped_column(Float, nullable=False)
    delta_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    source_basis: Mapped[str] = mapped_column(String(100), default="HISTORICAL_ANALYTICS", nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)


class DigitalTwinConstraintModel(BaseModel):
    """Hard or soft operational boundary constraint."""

    __tablename__ = "digital_twin_constraints"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    constraint_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="CAPACITY", nullable=False)  # BUDGET, CAPACITY, CASH_RUNWAY, SLA, COMPLIANCE
    threshold_value: Mapped[float] = mapped_column(Float, nullable=False)
    is_hard_constraint: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class DigitalTwinScenarioModel(BaseModel):
    """What-if simulation scenario configuration."""

    __tablename__ = "digital_twin_scenarios"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    twin_model_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_models.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scenario_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scenario_type: Mapped[str] = mapped_column(String(100), default="GROWTH", nullable=False, index=True)  # GROWTH, PRICING, RESOURCE, PROJECT, PROCESS, AI, INFRASTRUCTURE, RISK
    time_horizon: Mapped[str] = mapped_column(String(50), default="12_MONTHS", nullable=False)
    simulation_method: Mapped[str] = mapped_column(String(50), default="MONTE_CARLO", nullable=False)  # DETERMINISTIC, MONTE_CARLO, DISCRETE_EVENT
    baseline_snapshot_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_state_snapshots.id", ondelete="SET NULL"), nullable=True
    )
    parameter_overrides: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    assumptions_payload: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    constraints_payload: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="CONFIGURED", nullable=False, index=True)  # DRAFT, CONFIGURED, VALIDATED, SIMULATING, COMPLETED, ANALYZED, DECIDED, CANCELLED
    created_by: Mapped[str] = mapped_column(String(100), default="system", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class DigitalTwinScenarioVersionModel(BaseModel):
    """Version history for scenario parameters."""

    __tablename__ = "digital_twin_scenario_versions"

    scenario_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    scenario_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)


class DigitalTwinSimulationModel(BaseModel):
    """Simulation run configuration and results summary."""

    __tablename__ = "digital_twin_simulations"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    simulation_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    method: Mapped[str] = mapped_column(String(50), default="MONTE_CARLO", nullable=False)
    iterations: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    runtime_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="COMPLETED", nullable=False)
    metrics_summary: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    uncertainty_distribution: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)  # P10, P25, P50, P75, P90
    constraint_violations: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    is_sandboxed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class DigitalTwinSimulationRunModel(BaseModel):
    """Detailed trace records of individual simulation runs."""

    __tablename__ = "digital_twin_simulation_runs"

    simulation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_simulations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    run_index: Mapped[int] = mapped_column(Integer, nullable=False)
    simulated_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_profit: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_margin: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_capacity_utilization: Mapped[float] = mapped_column(Float, nullable=False)


class DigitalTwinSimulationResultModel(BaseModel):
    """Aggregated simulation result metrics."""

    __tablename__ = "digital_twin_simulation_results"

    simulation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_simulations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    p10_value: Mapped[float] = mapped_column(Float, nullable=False)
    p50_value: Mapped[float] = mapped_column(Float, nullable=False)
    p90_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), default="USD", nullable=False)


class DigitalTwinSensitivityResultModel(BaseModel):
    """Sensitivity ranking and Tornado analysis output."""

    __tablename__ = "digital_twin_sensitivity_results"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    parameter_code: Mapped[str] = mapped_column(String(100), nullable=False)
    target_metric: Mapped[str] = mapped_column(String(100), default="REVENUE", nullable=False)
    sensitivity_score: Mapped[float] = mapped_column(Float, nullable=False)
    impact_level: Mapped[str] = mapped_column(String(50), default="HIGH", nullable=False)  # HIGH, MEDIUM, LOW
    low_impact_value: Mapped[float] = mapped_column(Float, nullable=False)
    high_impact_value: Mapped[float] = mapped_column(Float, nullable=False)


class DigitalTwinCounterfactualModel(BaseModel):
    """Counterfactual retrospective scenario evaluation."""

    __tablename__ = "digital_twin_counterfactuals"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    counterfactual_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    historical_event_id: Mapped[str] = mapped_column(String(100), nullable=False)
    hypothetical_condition: Mapped[Text] = mapped_column(Text, nullable=False)
    historical_actual: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    simulated_alternative: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    divergence_summary: Mapped[Text] = mapped_column(Text, nullable=False)


class DigitalTwinDecisionOptionModel(BaseModel):
    """Comparative strategic option generated by decision support."""

    __tablename__ = "digital_twin_decision_options"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    option_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_scenarios.id", ondelete="CASCADE"), nullable=False, index=True
    )
    expected_benefit_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    expected_cost_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, default=0.2, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.85, nullable=False)
    tradeoff_summary: Mapped[Text] = mapped_column(Text, nullable=False)


class DigitalTwinDecisionRecordModel(BaseModel):
    """Human executive decision log linked to simulated scenarios."""

    __tablename__ = "digital_twin_decision_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    decision_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    question: Mapped[Text] = mapped_column(Text, nullable=False)
    selected_option_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_decision_options.id", ondelete="SET NULL"), nullable=True
    )
    rationale: Mapped[Text] = mapped_column(Text, nullable=False)
    decision_owner: Mapped[str] = mapped_column(String(100), nullable=False)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    scenario_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="APPROVED", nullable=False)


class DigitalTwinOutcomeModel(BaseModel):
    """Observed real-world outcome tracked for twin calibration."""

    __tablename__ = "digital_twin_outcomes"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    decision_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_decision_records.id", ondelete="SET NULL"), nullable=True, index=True
    )
    scenario_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("digital_twin_scenarios.id", ondelete="SET NULL"), nullable=True, index=True
    )
    observed_period: Mapped[str] = mapped_column(String(100), nullable=False)
    predicted_metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    actual_metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    variance_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)


class DigitalTwinCalibrationRecordModel(BaseModel):
    """Calibration update for model parameters based on historical accuracy."""

    __tablename__ = "digital_twin_calibration_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    parameter_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    old_value: Mapped[float] = mapped_column(Float, nullable=False)
    calibrated_value: Mapped[float] = mapped_column(Float, nullable=False)
    calibration_basis: Mapped[Text] = mapped_column(Text, nullable=False)
    calibrated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    model_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
