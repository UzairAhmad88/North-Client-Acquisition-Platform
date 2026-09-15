"""
Scientific Discovery Engine SQLAlchemy Models (Phase 97)
Models for Scientific Questions, Literature Graphs, AI-Generated Hypotheses, Experiment Design, AI Scientist Orchestrator, Scientific Simulations, Mathematical Discovery, and Discovery Registries.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.base import Base


class ScientificQuestionNode(Base):
    __tablename__ = "scientific_question_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"sq-{uuid.uuid4().hex[:8]}")
    title = Column(String(256), nullable=False)
    domain = Column(String(128), nullable=False, index=True)  # Physics, Biology, Medicine, Materials, Computer Science, etc.
    question_decomposition = Column(JSON, nullable=False)  # Subquestions, hypotheses, experiment requirements
    desired_outcome = Column(Text, nullable=False)
    status = Column(String(64), default="Active_Research")  # Defined, Decomposed, Active_Research, Answered
    created_at = Column(DateTime, default=datetime.utcnow)


class ScientificLiteratureGraph(Base):
    __tablename__ = "scientific_literature_graphs"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"lit-{uuid.uuid4().hex[:8]}")
    paper_title = Column(String(256), nullable=False)
    authors = Column(JSON, nullable=False)
    publication_year = Column(Integer, default=2026)
    extracted_claims = Column(JSON, nullable=False)  # [{claim, supporting_evidence, contradiction_status}]
    research_gaps_identified = Column(JSON, nullable=True)  # Missing, weak, or contradictory evidence areas
    citation_network = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AiHypothesisNode(Base):
    __tablename__ = "ai_hypothesis_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"hyp-{uuid.uuid4().hex[:8]}")
    hypothesis_title = Column(String(256), nullable=False)
    statement = Column(Text, nullable=False)
    is_ai_generated = Column(Boolean, default=True)  # Explicit mandatory label
    ai_generator_agent_id = Column(String(128), nullable=False)
    ranking_scores = Column(JSON, nullable=False)  # Evidence, Novelty, Testability, Potential Impact, Feasibility
    status = Column(String(64), default="Proposed")  # Proposed, Ranked, Experiment_Designed, Validated, Rejected
    hypothesis_graph = Column(JSON, nullable=True)  # Hypothesis -> Predictions -> Experiments -> Results
    version = Column(String(32), default="v1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)


class ExperimentDesignRecord(Base):
    __tablename__ = "experiment_design_records"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"exp-{uuid.uuid4().hex[:8]}")
    experiment_title = Column(String(256), nullable=False)
    hypothesis_id = Column(String(64), nullable=False, index=True)
    constraints = Column(JSON, nullable=False)  # Budget, Equipment, Time, Safety, Personnel, Materials
    information_gain_score = Column(Float, default=8.5)
    simulation_pre_run_results = Column(JSON, nullable=True)
    automated_notebook_logs = Column(JSON, nullable=True)
    requires_human_authorization = Column(Boolean, default=True)
    human_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScientificAiAgentOrchestrator(Base):
    __tablename__ = "scientific_ai_agent_orchestrators"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"orch-{uuid.uuid4().hex[:8]}")
    team_name = Column(String(256), nullable=False)
    agent_roles = Column(JSON, nullable=False)  # Literature, Hypothesis, Experiment, Simulation, Statistical, Critic, Reviewer
    auditable_research_logs = Column(JSON, nullable=False)
    peer_review_critique = Column(JSON, nullable=True)
    human_supervisor_id = Column(String(128), nullable=False)
    approval_gates = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScientificSimulationEngine(Base):
    __tablename__ = "scientific_simulation_engines"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"sim-{uuid.uuid4().hex[:8]}")
    simulation_title = Column(String(256), nullable=False)
    domain_type = Column(String(128), nullable=False)  # Physics, Engineering, Economics, Climate, Biology, Materials
    multi_model_configs = Column(JSON, nullable=False)
    sensitivity_analysis = Column(JSON, nullable=True)
    uncertainty_bounds = Column(JSON, nullable=True)
    causal_discovery_graph = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MathematicalDiscoveryEngine(Base):
    __tablename__ = "mathematical_discovery_engines"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"math-{uuid.uuid4().hex[:8]}")
    conjecture_title = Column(String(256), nullable=False)
    formal_statement = Column(Text, nullable=False)
    proof_strategy = Column(JSON, nullable=True)
    counterexample_search_results = Column(JSON, nullable=True)
    validation_status = Column(String(64), default="Unverified")  # Unverified, Counterexample_Found, Formally_Verified, Expert_Validated
    created_at = Column(DateTime, default=datetime.utcnow)


class DiscoveryRegistryRecord(Base):
    __tablename__ = "discovery_registry_records"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"disc-{uuid.uuid4().hex[:8]}")
    discovery_title = Column(String(256), nullable=False)
    confidence_level = Column(String(64), default="Supported")  # Hypothesis, Preliminary, Supported, Replicated, Established
    provenance = Column(JSON, nullable=False)  # Experiments, Researchers, Datasets, Models, Publications, Replications
    credit_attribution = Column(JSON, nullable=False)  # Researchers, Engineers, Data Scientists, AI Systems, Technicians
    replication_status = Column(String(64), default="Replicated")  # Replicated, Partially Replicated, Not Replicated, Contradicted
    retraction_status = Column(Boolean, default=False)
    published_at = Column(DateTime, default=datetime.utcnow)
