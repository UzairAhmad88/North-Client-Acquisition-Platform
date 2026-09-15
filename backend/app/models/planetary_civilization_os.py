"""
Planetary Civilization OS SQLAlchemy Models (Phase 96)
Models for Civilization State, Global Knowledge Commons, Evidence-Based Deliberation, Institutional Design Simulator, Human-AI Collective Intelligence, Problem Solving Marketplace, Civilization Forecasting, and Digital Rights Preservation.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.base import Base


class CivilizationStateNode(Base):
    __tablename__ = "civilization_state_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"civ-{uuid.uuid4().hex[:8]}")
    state_code = Column(String(128), nullable=False, index=True)  # e.g., GLOBAL-BASELINE-2026
    dimensions = Column(JSON, nullable=False)  # Knowledge, Health, Education, Infra, Economy, Science, Tech, Environment, Institutions, Resilience, Wellbeing
    aggregate_wellbeing_index = Column(Float, default=85.0)
    distributional_equity_score = Column(Float, default=78.5)
    active_threats_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class GlobalKnowledgeNode(Base):
    __tablename__ = "global_knowledge_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"knw-{uuid.uuid4().hex[:8]}")
    title = Column(String(256), nullable=False)
    domain_category = Column(String(128), nullable=False, index=True)  # Physics, Medicine, Climate, Computer Science, Economics, etc.
    claim_summary = Column(Text, nullable=False)
    status = Column(String(64), default="Supported")  # Established, Supported, Emerging, Contested, Speculative, Disproven, Unknown
    provenance = Column(JSON, nullable=False)  # Source, Author, Timestamp, Version, Evidence, Confidence, License
    quality_score = Column(Float, default=88.5)  # Accuracy, Evidence, Reproducibility, Recency, Peer Review
    disagreement_notes = Column(Text, nullable=True)
    is_forked_branch = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DeliberationArgumentMap(Base):
    __tablename__ = "deliberation_argument_maps"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"arg-{uuid.uuid4().hex[:8]}")
    topic_title = Column(String(256), nullable=False)
    claim_nodes = Column(JSON, nullable=False)  # [{claim, reason, evidence, counterargument, response}]
    consensus_level = Column(String(64), default="Broad Agreement")  # Strong Consensus, Broad Agreement, Mixed Evidence, Active Disagreement
    minority_view_preserved = Column(Boolean, default=True)
    bias_mitigation_metrics = Column(JSON, nullable=True)
    decision_memo = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InstitutionalDesignSimulator(Base):
    __tablename__ = "institutional_design_simulators"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"inst-{uuid.uuid4().hex[:8]}")
    institution_name = Column(String(256), nullable=False)
    governance_model = Column(String(128), nullable=False)
    decision_rights_structure = Column(JSON, nullable=False)
    simulated_failure_modes = Column(JSON, nullable=False)  # Corruption, Info Failure, Coordination Failure, Incentive Misalignment
    resilience_score = Column(Float, default=82.0)
    policy_memory_records = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class HumanAiCollectiveIntelligence(Base):
    __tablename__ = "human_ai_collective_intelligences"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"coll-{uuid.uuid4().hex[:8]}")
    team_name = Column(String(256), nullable=False)
    human_experts = Column(JSON, nullable=False)
    ai_specialized_roles = Column(JSON, nullable=False)  # Researcher, Analyst, Critic, Planner, Simulator, Reviewer, Teacher
    task_decomposition = Column(JSON, nullable=False)
    cross_checking_results = Column(JSON, nullable=True)
    constitutional_ai_rules_version = Column(String(64), default="v96.1.0-constitutional")
    human_override_engaged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CivilizationProblemSolution(Base):
    __tablename__ = "civilization_problem_solutions"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"sol-{uuid.uuid4().hex[:8]}")
    problem_title = Column(String(256), nullable=False)
    category = Column(String(128), nullable=False, index=True)  # Climate, Energy, Health, Food, Water, Governance, etc.
    solution_graph = Column(JSON, nullable=False)
    readiness_stage = Column(String(64), default="Pilot")  # Research, Prototype, Pilot, Deployable, Scaled, Mature
    is_safe_to_fail = Column(Boolean, default=True)
    failure_lessons_learned = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CivilizationScenarioRecord(Base):
    __tablename__ = "civilization_scenario_records"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"scn-{uuid.uuid4().hex[:8]}")
    scenario_title = Column(String(256), nullable=False)
    horizon_years = Column(Integer, default=50)  # 1Y, 5Y, 10Y, 25Y, 50Y, 100Y+
    scenario_axes = Column(JSON, nullable=False)
    resource_accounting = Column(JSON, nullable=False)  # Energy, Materials, Land, Water, Compute, Human Capital
    wildcard_risk_analysis = Column(JSON, nullable=True)
    independent_red_team_review = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
