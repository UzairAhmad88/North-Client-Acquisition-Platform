"""
Phase 95 — Planetary Resilience, Global Crisis Coordination, Civilization Recovery & Existential-Risk Preparedness Models
"""

import uuid
import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class CriticalSystemNode(Base):
    """Critical system registry (Energy, Water, Food, Healthcare, Comms, Transport, Finance, Cloud, Govt)."""
    __tablename__ = "critical_system_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    system_name = Column(String, nullable=False, index=True)
    sector = Column(String, default="HEALTHCARE")  # ENERGY, WATER, FOOD, HEALTHCARE, COMMS, TRANSPORT, FINANCE, CLOUD, GOVT
    resilience_state = Column(String, default="STABLE")  # STABLE, STRESSED, DISRUPTED, CRITICAL, RECOVERING, RECOVERED
    criticality_class = Column(String, default="ESSENTIAL")  # ESSENTIAL, IMPORTANT, NON_CRITICAL
    rto_hours = Column(Float, default=4.0)
    rpo_hours = Column(Float, default=1.0)
    dependencies = Column(JSON, default=list)
    fallbacks = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class GlobalCrisisIncident(Base):
    """Crisis registry (Level 1–5), incident command dashboard, decision log, and escalation state."""
    __tablename__ = "global_crisis_incidents"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False, index=True)
    classification = Column(String, default="COMPOUND_CRISIS")  # NATURAL_DISASTER, INFRASTRUCTURE, ECONOMIC, CYBER, SUPPLY, PUBLIC_HEALTH, GEOPOLITICAL, COMPOUND
    severity_level = Column(String, default="LEVEL_3")  # LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5
    affected_regions = Column(JSON, default=list)
    incident_commander_human = Column(String, nullable=True)
    assigned_command_roles = Column(JSON, default=dict)
    decision_log = Column(JSON, default=list)
    signal_confidence = Column(Float, default=0.92)
    verification_status = Column(String, default="CONFIRMED")  # CONFIRMED, PROBABLE, UNCONFIRMED, FALSE_CORRECTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class HumanitarianResourceMatch(Base):
    """Humanitarian needs modeling, resource availability, emergency logistics, and anti-fraud audit."""
    __tablename__ = "humanitarian_resource_matches"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    incident_id = Column(String, nullable=False, index=True)
    need_category = Column(String, default="MEDICAL_SUPPLIES")  # FOOD, WATER, SHELTER, MEDICAL_SUPPLIES, TRANSPORT, COMMS
    quantity_requested = Column(Float, default=1000.0)
    quantity_matched = Column(Float, default=1000.0)
    resource_owner_id = Column(String, nullable=False)
    logistics_route_plan = Column(JSON, default=dict)
    anti_fraud_verified = Column(Boolean, default=True)
    temporary_access_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SystemicResilienceBuffer(Base):
    """Systemic resilience buffer depletion tracking and compound crisis cascade state."""
    __tablename__ = "systemic_resilience_buffers"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    buffer_name = Column(String, nullable=False, index=True)  # CAPACITY, FINANCIAL, INVENTORY, ENERGY, TIME, HUMAN
    initial_capacity = Column(Float, default=100.0)
    current_capacity = Column(Float, default=85.0)
    depletion_rate_per_day = Column(Float, default=2.5)
    restoration_actions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiContinuityDegradationState(Base):
    """AI degradation modes (Full AI -> Reduced -> Manual), agent quarantine, and model rollback tracking."""
    __tablename__ = "ai_continuity_degradation_states"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    service_name = Column(String, nullable=False, index=True)
    current_mode = Column(String, default="FULL_AI")  # FULL_AI, REDUCED_AI, HUMAN_ASSISTED, MANUAL
    fallback_defined = Column(Boolean, default=True)
    quarantined_agents = Column(JSON, default=list)
    model_rollback_hash = Column(String, nullable=True)
    last_degradation_trigger = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CriticalKnowledgeArchiveNode(Base):
    """Protected knowledge continuity repository with cryptographic signature integrity."""
    __tablename__ = "critical_knowledge_archive_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    knowledge_title = Column(String, nullable=False, index=True)
    category = Column(String, default="MEDICAL")  # SCIENTIFIC, ENGINEERING, MEDICAL, OPERATIONAL, HISTORICAL, CULTURAL
    cryptographic_hash = Column(String, nullable=False)
    redundant_storage_locations = Column(JSON, default=list)
    verification_signature = Column(String, nullable=False)
    is_archived = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ExistentialRiskResearchRecord(Base):
    """Extreme systemic risk research models (Climate, AI Control/Containment, Biosecurity Detection, Infra Collapse)."""
    __tablename__ = "existential_risk_research_records"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    risk_category = Column(String, nullable=False, index=True)  # EXTREME_CLIMATE, INFRA_FAILURE, AI_CONTROL, BIOSECURITY_DETECTION, ASTEROID, COMPOUND
    uncertainty_classification = Column(String, default="PLAUSIBLE")  # KNOWN, PLAUSIBLE, SPECULATIVE, UNKNOWN
    containment_scenarios = Column(JSON, default=list)
    human_capability_preservation_plan = Column(JSON, default=dict)
    safety_boundary_checked = Column(Boolean, default=True)  # Strictly no harmful operational pathogen instructions
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
