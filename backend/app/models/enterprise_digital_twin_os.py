"""
Phase 84: Enterprise Digital Twin, Simulation, Scenario Planning, Predictive Operations & Autonomous Optimization Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class DigitalTwinEntity(Base):
    __tablename__ = "digital_twin_entities"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False) # Person, Team, Customer, Project, Product, System, Resource, Process
    domain = Column(String, nullable=False) # Operations, Finance, IT, Sales, HR, Security
    status = Column(String, default="HEALTHY")
    confidence_score = Column(Float, default=0.98)
    attributes = Column(JSON, default=dict)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class DigitalTwinRelationship(Base):
    __tablename__ = "digital_twin_relationships"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    source_entity_id = Column(String, ForeignKey("digital_twin_entities.id"), nullable=False)
    target_entity_id = Column(String, ForeignKey("digital_twin_entities.id"), nullable=False)
    relationship_type = Column(String, nullable=False) # DEPENDS_ON, OWNS, USES, CONSUMES, PRODUCES
    strength = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalTwinStateSnapshot(Base):
    __tablename__ = "digital_twin_state_snapshots"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    snapshot_name = Column(String, nullable=False)
    snapshot_type = Column(String, default="ACTUAL") # ACTUAL, HISTORICAL, SIMULATED, SCENARIO
    health_score = Column(Float, default=98.5)
    financial_mrr_usd = Column(Float, default=450000.0)
    operational_efficiency = Column(Float, default=94.2)
    resource_utilization = Column(Float, default=82.5)
    captured_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalTwinScenario(Base):
    __tablename__ = "digital_twin_scenarios"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    scenario_type = Column(String, default="WHAT_IF") # WHAT_IF, MONTE_CARLO, OPTIMIZATION, DISASTER
    starting_snapshot_id = Column(String, ForeignKey("digital_twin_state_snapshots.id"), nullable=True)
    variables = Column(JSON, default=dict)
    constraints = Column(JSON, default=dict)
    owner = Column(String, nullable=False)
    status = Column(String, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalTwinSimulation(Base):
    __tablename__ = "digital_twin_simulations"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    scenario_id = Column(String, ForeignKey("digital_twin_scenarios.id"), nullable=False)
    simulation_method = Column(String, default="MONTE_CARLO") # DISCRETE_EVENT, MONTE_CARLO, AGENT_BASED, SYSTEM_DYNAMICS
    iterations = Column(Integer, default=10000)
    p10_outcome = Column(JSON, default=dict)
    p50_outcome = Column(JSON, default=dict)
    p90_outcome = Column(JSON, default=dict)
    expected_value = Column(Float, default=0.0)
    variance = Column(Float, default=0.0)
    duration_seconds = Column(Float, default=1.4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalTwinOptimization(Base):
    __tablename__ = "digital_twin_optimizations"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    objective = Column(String, nullable=False) # MAXIMIZE_REVENUE, MINIMIZE_COST, MINIMIZE_RISK, OPTIMIZE_RESOURCE
    multi_objectives = Column(JSON, default=list)
    decision_variables = Column(JSON, default=dict)
    constraints = Column(JSON, default=dict)
    recommended_solution = Column(JSON, default=dict)
    pareto_frontier_count = Column(Integer, default=5)
    confidence_score = Column(Float, default=0.96)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalTwinRecommendation(Base):
    __tablename__ = "digital_twin_recommendations"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    optimization_id = Column(String, ForeignKey("digital_twin_optimizations.id"), nullable=True)
    title = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    expected_benefit_usd = Column(Float, default=0.0)
    expected_cost_usd = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW") # LOW, MODERATE, HIGH
    approval_required = Column(Boolean, default=False)
    status = Column(String, default="PROPOSED") # PROPOSED, APPROVED, EXECUTED, REJECTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalTwinAgentTask(Base):
    __tablename__ = "digital_twin_agent_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    autonomy_level = Column(Integer, default=2)
    status = Column(String, default="COMPLETED")
    target_scope = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
