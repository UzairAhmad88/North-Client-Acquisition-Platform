"""
Universal Intelligence OS SQLAlchemy Models (Phase 98)
Models for Capability Graphs, Layered Memory Architecture, World Model Representations, Hierarchical Action Plans, Specialized Agent Profiles, Evaluation & Drift Suites, Deployment Canaries, and Personal AI Symbiosis Profiles.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.base import Base


class UniversalIntelligenceCapabilityGraph(Base):
    __tablename__ = "universal_intelligence_capability_graphs"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"cap-{uuid.uuid4().hex[:8]}")
    system_name = Column(String(256), nullable=False)
    capabilities_scores = Column(JSON, nullable=False)  # Reasoning, Learning, Planning, Memory, Language, Perception, Tool Use, Science, Social, Adaptation, Creativity, Self-Eval
    generalization_score = Column(Float, default=88.5)
    transfer_learning_index = Column(Float, default=85.2)
    continual_learning_retention = Column(Float, default=94.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class LayeredMemoryNode(Base):
    __tablename__ = "layered_memory_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"mem-{uuid.uuid4().hex[:8]}")
    memory_layer = Column(String(64), nullable=False, index=True)  # Working, Episodic, Semantic, Procedural, Institutional, Research
    user_id = Column(String(128), nullable=True, index=True)
    organization_id = Column(String(128), nullable=True, index=True)
    content_summary = Column(Text, nullable=False)
    provenance = Column(JSON, nullable=False)  # Source, Timestamp, Confidence, Scope, Permissions, Version
    is_corrected = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class WorldModelRepresentation(Base):
    __tablename__ = "world_model_representations"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"wm-{uuid.uuid4().hex[:8]}")
    model_name = Column(String(256), nullable=False)
    entities = Column(JSON, nullable=False)
    relationships = Column(JSON, nullable=False)
    events_and_processes = Column(JSON, nullable=False)
    constraints_and_causal_hypotheses = Column(JSON, nullable=False)
    uncertainty_bounds = Column(JSON, nullable=False)
    competing_interpretations = Column(JSON, nullable=True)
    version = Column(String(32), default="v1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)


class HierarchicalActionPlan(Base):
    __tablename__ = "hierarchical_action_plans"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"plan-{uuid.uuid4().hex[:8]}")
    goal = Column(String(256), nullable=False)
    strategy_summary = Column(Text, nullable=False)
    hierarchical_tasks = Column(JSON, nullable=False)  # [{task_id, description, subactions, status, reversibility}]
    autonomy_level = Column(String(64), default="Level 0 — Advisory")  # Level 0 Advisory to Level 4 Sandbox; NO unrestricted
    simulation_validation_results = Column(JSON, nullable=True)
    requires_human_approval = Column(Boolean, default=True)
    human_approval_status = Column(String(64), default="Pending_Approval")
    is_interrupted = Column(Boolean, default=False)
    is_rolled_back = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SpecializedAgentProfile(Base):
    __tablename__ = "specialized_agent_profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"agt-{uuid.uuid4().hex[:8]}")
    agent_name = Column(String(256), nullable=False)
    role = Column(String(128), nullable=False, index=True)  # Researcher, Planner, Engineer, Scientist, Analyst, Critic, Teacher, Negotiator, Reviewer
    capabilities_profile = Column(JSON, nullable=False)
    least_privilege_tools = Column(JSON, nullable=False)  # Read, Write, Execute, Publish, Admin permissions
    reputation_score = Column(Float, default=92.0)
    failure_history = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ModelEvaluationBenchmarkSuite(Base):
    __tablename__ = "model_evaluation_benchmark_suites"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"eval-{uuid.uuid4().hex[:8]}")
    model_version_id = Column(String(128), nullable=False, index=True)
    reasoning_score = Column(Float, default=94.5)
    knowledge_accuracy_score = Column(Float, default=96.0)
    planning_horizon_score = Column(Float, default=91.2)
    generalization_score = Column(Float, default=89.0)
    robustness_score = Column(Float, default=93.5)
    calibration_error = Column(Float, default=0.035)  # ECE Error
    deception_resistance_score = Column(Float, default=98.0)
    goal_stability_score = Column(Float, default=97.5)
    created_at = Column(DateTime, default=datetime.utcnow)


class DeploymentMonitoringCanary(Base):
    __tablename__ = "deployment_monitoring_canaries"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"dmon-{uuid.uuid4().hex[:8]}")
    model_id = Column(String(128), nullable=False, index=True)
    deployment_type = Column(String(64), default="Canary")  # Shadow, Canary, Production
    drift_metrics = Column(JSON, nullable=False)  # Model Drift, Data Drift, Capability Drift, Behavior Drift
    automatic_rollback_triggered = Column(Boolean, default=False)
    kill_switch_status = Column(String(64), default="Standby_Independent_Armed")
    created_at = Column(DateTime, default=datetime.utcnow)


class PersonalAiProfile(Base):
    __tablename__ = "personal_ai_profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(String(64), primary_key=True, default=lambda: f"pai-{uuid.uuid4().hex[:8]}")
    user_id = Column(String(128), nullable=False, index=True)
    cognitive_preferences = Column(JSON, nullable=False)
    personal_memory_index = Column(JSON, nullable=False)
    data_portability_manifest = Column(JSON, nullable=False)
    model_replacement_status = Column(String(64), default="Interoperable")
    created_at = Column(DateTime, default=datetime.utcnow)
