"""
Phase 94 — Global Intelligence Infrastructure, Planetary Digital Twin, Civilization Simulation & Long-Horizon Strategic Foresight Models
"""

import uuid
import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class PlanetaryEntityNode(Base):
    """Multi-scale planetary entity node (Earth, Region, Country, City, Org, Infrastructure, Resource, System, Event)."""
    __tablename__ = "planetary_entity_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    entity_name = Column(String, nullable=False, index=True)
    scale_level = Column(String, default="NATIONAL")  # GLOBAL, REGIONAL, NATIONAL, CITY, ORGANIZATION, PROJECT, INDIVIDUAL
    entity_type = Column(String, default="COUNTRY")  # COUNTRY, CITY, INSTITUTION, INFRASTRUCTURE, RESOURCE, SYSTEM, EVENT
    historical_state_snapshot = Column(JSON, default=dict)
    current_state_snapshot = Column(JSON, default=dict)
    future_state_projections = Column(JSON, default=list)  # Explicitly labeled as Forecasts/Scenarios, NOT facts
    data_provenance = Column(JSON, default=dict)  # Source, Timestamp, Method, Confidence
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class GeospatialInfrastructureNode(Base):
    """Critical infrastructure digital twins (Power, Water, Ports, Telecom, Transportation) and cascading dependency graphs."""
    __tablename__ = "geospatial_infrastructure_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    infrastructure_name = Column(String, nullable=False, index=True)
    sector = Column(String, default="POWER_GRID")  # POWER_GRID, WATER, PORTS, TELECOM, TRANSPORTATION, HEALTH
    capacity_rating = Column(Float, default=100.0)
    failure_risk_score = Column(Float, default=0.08)
    cascading_dependencies = Column(JSON, default=list)
    recovery_time_pathways = Column(JSON, default=dict)
    is_protected_vulnerability = Column(Boolean, default=True)  # Masked actionable vulnerabilities
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ClimateEnvironmentalScenario(Base):
    """Climate simulation datasets (SSP/RCP scenarios, extreme events, agricultural impact maps, ecosystem feedback)."""
    __tablename__ = "climate_environmental_scenarios"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    scenario_code = Column(String, nullable=False, index=True)  # SSP1_2.6, SSP2_4.5, SSP5_8.5
    horizon_year = Column(Integer, default=2050)
    extreme_event_simulations = Column(JSON, default=list)  # Flood, Heat, Drought, Storm, Wildfire
    water_stress_index = Column(Float, default=0.45)
    food_security_risk = Column(Float, default=0.32)
    ecosystem_feedback_loops = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MacroEconomicDemographicModel(Base):
    """Macroeconomic contagion state, financial system risk, labor AI impact scenarios, and skill transformation pathways."""
    __tablename__ = "macro_economic_demographic_models"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    region_code = Column(String, nullable=False, index=True)
    gdp_growth_forecast = Column(Float, default=2.8)
    financial_contagion_risk = Column(Float, default=0.12)
    ai_labor_impact_scenario = Column(JSON, default=dict)
    skill_transformation_roadmap = Column(JSON, default=list)
    compute_infrastructure_capacity_tflops = Column(Float, default=5000000.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class StrategicForesightScenario(Base):
    """Long-horizon strategic scenarios (5, 10, 25, 50, 100 years), megatrend signals, and robustness indicators."""
    __tablename__ = "strategic_foresight_scenarios"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    scenario_title = Column(String, nullable=False, index=True)
    horizon_years = Column(Integer, default=25)  # 5, 10, 25, 50, 100
    scenario_matrix_type = Column(String, default="TRANSFORMATIVE")  # BASELINE, OPTIMISTIC, ADVERSE, TRANSFORMATIVE, DISRUPTIVE
    megatrend_signals = Column(JSON, default=list)
    wildcard_events = Column(JSON, default=list)
    robustness_score = Column(Float, default=0.88)
    reversibility_rating = Column(String, default="PARTIALLY_REVERSIBLE")  # REVERSIBLE, PARTIALLY_REVERSIBLE, IRREVERSIBLE
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PolicyCrisisSimulationRun(Base):
    """Global policy Red/Blue team trade-off synthesis, crisis cascade simulations, and resource coordination models."""
    __tablename__ = "policy_crisis_simulation_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    simulation_type = Column(String, default="GLOBAL_CRISIS_CASCADE")  # POLICY_RED_BLUE, GLOBAL_CRISIS_CASCADE, RESOURCE_COORDINATION
    scenario_inputs = Column(JSON, default=dict)
    red_blue_team_synthesis = Column(JSON, default=dict)  # Trade-offs: Efficiency, Equity, Resilience, Cost
    cascade_propagation_graph = Column(JSON, default=list)
    fairness_distribution_analysis = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PlanetaryTwinGovernanceAudit(Base):
    """Model validation records, uncertainty layer logs, expert review panel dissent, and model archives."""
    __tablename__ = "planetary_twin_governance_audits"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    model_name = Column(String, nullable=False)
    version = Column(String, default="1.0.0")
    calibration_accuracy_score = Column(Float, default=0.94)
    uncertainty_bounds = Column(JSON, default=dict)
    expert_dissent_records = Column(JSON, default=list)
    privacy_aggregation_applied = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
