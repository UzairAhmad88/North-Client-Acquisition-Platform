"""
Phase 75: Autonomous Enterprise Simulation, Digital Twin, Predictive Intelligence,
Scenario Planning & Strategic Decision Intelligence Models.
Database table prefix: dtwin_*
"""

from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Float,
    Integer,
    Text,
    JSON,
    ForeignKey,
    Index
)
from app.models.base import Base


# -------------------------------------------------------------------
# 1. Enterprise Digital Twin & State Engine
# -------------------------------------------------------------------
class DecisionTwinEntityModel(Base):
    __tablename__ = "dtwin_entities"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    entity_code = Column(String(64), nullable=False, index=True)
    entity_type = Column(String(64), nullable=False)  # ORG, PRODUCT, SERVICE, PROJECT, ASSET, SUPPLIER, FINANCE, RISK
    name = Column(String(255), nullable=False)
    current_state = Column(JSON, nullable=False)
    historical_state_summary = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=False, default=0.95)
    owner = Column(String(128), nullable=False, default="Executive Leadership")
    source_system = Column(String(64), nullable=False, default="ENTERPRISE_EVENT_BUS")
    is_active = Column(Boolean, nullable=False, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DecisionTwinRelationshipModel(Base):
    __tablename__ = "dtwin_relationships"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    source_entity_id = Column(String(64), ForeignKey("dtwin_entities.id"), nullable=False)
    target_entity_id = Column(String(64), ForeignKey("dtwin_entities.id"), nullable=False)
    relationship_type = Column(String(64), nullable=False)  # DEPENDS_ON, IMPACTS, CONSTRAINS, FUNDS, GOVERNS
    weight = Column(Float, nullable=False, default=1.0)
    elasticity = Column(Float, nullable=True, default=1.0)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 2. Predictive Models & Forecasts
# -------------------------------------------------------------------
class DecisionModelRegistryModel(Base):
    __tablename__ = "dtwin_models"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    model_code = Column(String(64), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    purpose = Column(String(128), nullable=False)  # REVENUE_FORECAST, CHURN_PREDICTION, LIQUIDITY_RUNWAY
    algorithm_type = Column(String(64), nullable=False, default="PROBABILISTIC_ENSEMBLE")
    version = Column(String(32), nullable=False, default="1.0.0")
    mape = Column(Float, nullable=True, default=2.8)
    rmse = Column(Float, nullable=True)
    validation_status = Column(String(32), nullable=False, default="APPROVED")
    assumptions = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DecisionForecastRunModel(Base):
    __tablename__ = "dtwin_forecasts"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    model_id = Column(String(64), ForeignKey("dtwin_models.id"), nullable=False)
    metric_name = Column(String(64), nullable=False, index=True)
    forecast_horizon_days = Column(Integer, nullable=False, default=90)
    point_estimate = Column(Float, nullable=False, default=0.0)
    prediction_interval_p10 = Column(Float, nullable=False, default=0.0)
    prediction_interval_p50 = Column(Float, nullable=False, default=0.0)
    prediction_interval_p90 = Column(Float, nullable=False, default=0.0)
    confidence_level = Column(Float, nullable=False, default=0.90)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 3. Scenarios & Monte Carlo Simulations
# -------------------------------------------------------------------
class DtwinScenarioModel(Base):
    __tablename__ = "dtwin_scenarios"


    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    scenario_code = Column(String(64), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False, default="MACROECONOMIC")  # GROWTH, RECESSION, SHOCK, CYBER, CLIMATE
    assumptions_summary = Column(Text, nullable=False)
    variables_mutated = Column(JSON, nullable=False)  # e.g. {"demand_pct": 20, "supplier_lead_days": 14}
    time_horizon_months = Column(Integer, nullable=False, default=12)
    status = Column(String(32), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DecisionSimulationModel(Base):
    __tablename__ = "dtwin_simulations"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    scenario_id = Column(String(64), ForeignKey("dtwin_scenarios.id"), nullable=False)
    simulation_type = Column(String(64), nullable=False, default="MONTE_CARLO")
    iterations_count = Column(Integer, nullable=False, default=10000)
    random_seed = Column(Integer, nullable=False, default=42)
    mean_outcome = Column(Float, nullable=False, default=0.0)
    var_95_percentile = Column(Float, nullable=False, default=0.0)
    cvar_expected_shortfall = Column(Float, nullable=False, default=0.0)
    output_distributions = Column(JSON, nullable=True)
    reproducibility_hash = Column(String(64), nullable=False, default="sha256-verified")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 4. Multi-Objective Decision Optimization & Pareto
# -------------------------------------------------------------------
class DecisionOptimizationModel(Base):
    __tablename__ = "dtwin_optimizations"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    optimization_code = Column(String(64), nullable=False, unique=True)
    objective_function = Column(String(128), nullable=False, default="MAX_PROFIT_MIN_RISK")
    objectives_list = Column(JSON, nullable=False)  # ["profit", "risk", "customer_satisfaction"]
    constraints_list = Column(JSON, nullable=False)  # ["capital_limit", "esg_threshold"]
    pareto_frontier_points = Column(JSON, nullable=True)
    recommended_option = Column(String(128), nullable=False, default="PARETO_BALANCED_OPTION_B")
    status = Column(String(32), nullable=False, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 5. Strategic Decisions, Memory & Register
# -------------------------------------------------------------------
class DecisionRecordModel(Base):
    __tablename__ = "dtwin_decision_records"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    decision_code = Column(String(64), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    strategic_objective = Column(String(255), nullable=False)
    options_evaluated = Column(JSON, nullable=False)
    recommended_option = Column(String(128), nullable=False)
    decision_maker = Column(String(128), nullable=True)
    final_decision_selected = Column(String(128), nullable=True)
    approval_status = Column(String(32), nullable=False, default="PENDING_EXECUTIVE_APPROVAL")
    actual_outcome = Column(Text, nullable=True)
    decision_quality_score = Column(Float, nullable=True, default=94.5)
    lessons_learned = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 6. Strategic Planning, OKRs & Capital Allocation
# -------------------------------------------------------------------
class DecisionOkrModel(Base):
    __tablename__ = "dtwin_okrs"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    objective_title = Column(String(255), nullable=False)
    key_result = Column(String(255), nullable=False)
    baseline_value = Column(Float, nullable=False, default=0.0)
    target_value = Column(Float, nullable=False, default=100.0)
    current_value = Column(Float, nullable=False, default=45.0)
    progress_pct = Column(Float, nullable=False, default=45.0)
    confidence_level = Column(String(16), nullable=False, default="HIGH")
    owner = Column(String(128), nullable=False)
    cycle = Column(String(32), nullable=False, default="2026_ANNUAL")


# -------------------------------------------------------------------
# 7. Early Warning & Weak Signals
# -------------------------------------------------------------------
class DecisionEarlyWarningModel(Base):
    __tablename__ = "dtwin_early_warnings"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    signal_code = Column(String(64), nullable=False, unique=True)
    category = Column(String(64), nullable=False, default="STRATEGIC_DEPENDENCY")
    severity = Column(String(16), nullable=False, default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW
    signal_description = Column(Text, nullable=False)
    observed_evidence = Column(JSON, nullable=False)
    confidence = Column(Float, nullable=False, default=0.88)
    alternative_explanations = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE")
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 8. Crisis Management & Executive War Room
# -------------------------------------------------------------------
class DecisionCrisisCaseModel(Base):
    __tablename__ = "dtwin_crisis_cases"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    case_code = Column(String(64), nullable=False, unique=True)
    crisis_type = Column(String(64), nullable=False, default="SUPPLY_NETWORK_COLLAPSE")
    title = Column(String(255), nullable=False)
    containment_status = Column(String(32), nullable=False, default="CONTAINING")
    financial_exposure_estimate = Column(Float, nullable=False, default=250000.0)
    impacted_business_units = Column(JSON, nullable=False)
    war_room_lead = Column(String(128), nullable=False, default="Chief Operating Officer")
    action_log = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# Dual-naming compatibility aliases
DecisionTwinEntity = DecisionTwinEntityModel
DecisionTwinRelationship = DecisionTwinRelationshipModel
DecisionModelRegistry = DecisionModelRegistryModel
DecisionForecastRun = DecisionForecastRunModel
DecisionScenario = DtwinScenarioModel
DecisionScenarioModel = DtwinScenarioModel
DecisionSimulation = DecisionSimulationModel

DecisionOptimization = DecisionOptimizationModel
DecisionRecord = DecisionRecordModel
DecisionOkr = DecisionOkrModel
DecisionEarlyWarning = DecisionEarlyWarningModel
DecisionCrisisCase = DecisionCrisisCaseModel
