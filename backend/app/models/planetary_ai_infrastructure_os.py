"""
Phase 89: Planetary-Scale AI Infrastructure, Global Agent Mesh & Civilization-Scale Intelligence Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class PlanetaryFabricNode(Base):
    __tablename__ = "planetary_fabric_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    region = Column(String, nullable=False) # US_EAST, US_WEST, EU_CENTRAL, APAC_SINGAPORE, EDGE_FACILITY
    cluster_type = Column(String, default="CLOUD_CLUSTER") # CLOUD_CLUSTER, REGIONAL_DC, EDGE_NODE, FACTORY_RACK
    carbon_intensity_g_kwh = Column(Float, default=180.5)
    active_workloads_count = Column(Integer, default=142)
    health_score = Column(Float, default=99.9)
    status = Column(String, default="HEALTHY")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class GlobalAgentMeshNode(Base):
    __tablename__ = "global_agent_mesh_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, nullable=False, index=True)
    agent_name = Column(String, nullable=False)
    organization_domain = Column(String, nullable=False)
    attestation_token_hash = Column(String, nullable=False)
    trust_score = Column(Float, default=99.8)
    quarantine_status = Column(String, default="CLEAN") # CLEAN, MONITORED, QUARANTINED, REVOKED
    promotion_tier = Column(String, default="PRODUCTION") # EXPERIMENTAL, VALIDATED, CERTIFIED, PRODUCTION
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PlanetaryResilienceConfig(Base):
    __tablename__ = "planetary_resilience_configs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    service_name = Column(String, nullable=False, index=True)
    rto_seconds = Column(Integer, default=5)
    rpo_seconds = Column(Integer, default=0)
    deployment_architecture = Column(String, default="ACTIVE_ACTIVE_MULTI_REGION")
    active_region = Column(String, default="US_EAST")
    standby_region = Column(String, default="EU_CENTRAL")
    failover_status = Column(String, default="STANDBY_READY")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class InfrastructureTwinState(Base):
    __tablename__ = "infrastructure_twin_states"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    facility_name = Column(String, nullable=False)
    power_kw = Column(Float, default=450.0)
    cooling_efficiency_pue = Column(Float, default=1.15)
    network_latency_ms = Column(Float, default=12.4)
    failure_propagation_risk = Column(Float, default=2.1) # Percentage risk
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class AgentPromotionRecord(Base):
    __tablename__ = "agent_promotion_records"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, nullable=False, index=True)
    previous_tier = Column(String, nullable=False)
    new_tier = Column(String, nullable=False)
    certification_hash = Column(String, nullable=False)
    promoted_by = Column(String, default="CHIEF_AI_OFFICER_APPROVED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PlanetaryStrategicScenario(Base):
    __tablename__ = "planetary_strategic_scenarios"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    scenario_type = Column(String, default="GLOBAL_SUPPLY_SHOCK") # SUPPLY_SHOCK, REGION_OUTAGE, AI_SURGE, ENERGY_DISRUPTION
    simulated_impact = Column(JSON, default=dict)
    early_warning_level = Column(String, default="NORMAL") # NORMAL, ELEVATED, SEVERE, CRITICAL
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PlanetaryGovernanceAudit(Base):
    __tablename__ = "planetary_governance_audits"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    event_type = Column(String, nullable=False) # GLOBAL_KILL_SWITCH, SAFE_MODE, POLICY_CANARY, EMERGENCY_SHUTDOWN
    initiated_by = Column(String, nullable=False)
    status = Column(String, default="COMPLETED")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
