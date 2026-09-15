"""
Phase 90: Planetary AI Civilization Layer, Global Knowledge Intelligence & Scientific Discovery Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class KnowledgeClaimNode(Base):
    __tablename__ = "knowledge_claim_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    claim_text = Column(Text, nullable=False, index=True)
    domain = Column(String, default="SCIENCE_BIOMEDICAL") # SCIENCE, TECHNOLOGY, ECONOMICS, ENVIRONMENT, ENGINEERING
    evidence_score = Column(Float, default=98.5) # Quality of supporting evidence
    confidence_level = Column(String, default="VERIFIED_PEER_REVIEWED") # OBSERVED, VERIFIED, INFERRED, SPECULATIVE
    provenance_source = Column(String, nullable=False)
    contradiction_detected = Column(Boolean, default=False)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ScientificHypothesis(Base):
    __tablename__ = "scientific_hypotheses"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    domain = Column(String, default="MATERIALS_SCIENCE")
    priority_score = Column(Float, default=94.2)
    novelty_score = Column(Float, default=96.8)
    testability_status = Column(String, default="SIMULATABLE_HIGH_CONFIDENCE")
    is_fact = Column(Boolean, default=False) # MUST ALWAYS BE FALSE UNTIL EXPERIMENTALLY VERIFIED
    status = Column(String, default="CANDIDATE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ScientificExperiment(Base):
    __tablename__ = "scientific_experiments"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    experiment_name = Column(String, nullable=False, index=True)
    hypothesis_id = Column(String, ForeignKey("scientific_hypotheses.id"), nullable=False)
    variables = Column(JSON, default=dict)
    controls = Column(JSON, default=dict)
    reproducibility_score = Column(Float, default=99.2)
    simulation_state = Column(String, default="SIMULATED_PASS") # SIMULATED, IN_PROGRESS, VERIFIED, FAILED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CausalReasoningNode(Base):
    __tablename__ = "causal_reasoning_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    cause_variable = Column(String, nullable=False)
    effect_variable = Column(String, nullable=False)
    confounders = Column(JSON, default=list)
    causal_effect_size = Column(Float, default=0.84)
    confidence_interval = Column(String, default="[0.78, 0.90]")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class LongHorizonScenario(Base):
    __tablename__ = "long_horizon_scenarios"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    time_horizon_years = Column(Integer, default=10) # 1, 5, 10, 20 years
    scenario_title = Column(String, nullable=False)
    megatrend_category = Column(String, default="ENERGY_TRANSITION") # ENERGY, DEMOGRAPHICS, TECHNOLOGY, ENVIRONMENT
    decision_reversibility = Column(String, default="PARTIALLY_REVERSIBLE") # REVERSIBLE, PARTIALLY_REVERSIBLE, IRREVERSIBLE
    weak_signals = Column(JSON, default=list)
    strategic_options = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ResearchDatasetRegistry(Base):
    __tablename__ = "research_dataset_registries"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    dataset_name = Column(String, nullable=False, index=True)
    domain = Column(String, nullable=False)
    license = Column(String, default="OPEN_RESEARCH_LICENSE_V2")
    privacy_preserving_method = Column(String, default="FEDERATED_DIFFERENTIAL_PRIVACY")
    is_synthetic = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ScientificGovernanceAudit(Base):
    __tablename__ = "scientific_governance_audits"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    event_type = Column(String, nullable=False) # SAFETY_GATE_APPROVAL, ETHICAL_REVIEW_QUORUM, IRREVERSIBLE_DECISION_GATE
    initiated_by = Column(String, nullable=False)
    quorum_approvers = Column(JSON, default=list)
    status = Column(String, default="APPROVED")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
