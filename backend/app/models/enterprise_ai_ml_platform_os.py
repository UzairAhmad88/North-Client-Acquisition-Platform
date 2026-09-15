"""
Phase 83: Enterprise AI/ML Platform, MLOps, Model Governance, Model Registry, Evaluation, Deployment & Autonomous AI Operations Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class AiPlatformProject(Base):
    __tablename__ = "ai_platform_projects"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    business_objective = Column(Text, nullable=True)
    owner = Column(String, nullable=False)
    team = Column(String, default="AI Engineering")
    status = Column(String, default="ACTIVE") # ACTIVE, ARCHIVED, DEPRECATED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AiPlatformExperiment(Base):
    __tablename__ = "ai_platform_experiments"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("ai_platform_projects.id"), nullable=True)
    name = Column(String, nullable=False, index=True)
    framework = Column(String, default="PyTorch") # PyTorch, TensorFlow, Scikit-Learn, HuggingFace
    hyperparameters = Column(JSON, default=dict)
    metrics = Column(JSON, default=dict)
    best_accuracy = Column(Float, default=0.0)
    best_loss = Column(Float, default=0.0)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformModel(Base):
    __tablename__ = "ai_platform_models"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    model_type = Column(String, nullable=False) # LLM, Classifier, Regressor, Embedding, RAG, Agent
    framework = Column(String, default="HuggingFace")
    current_version = Column(String, default="v1.0.0")
    lifecycle_stage = Column(String, default="PRODUCTION") # Draft, Candidate, Staged, Production, Retired
    risk_level = Column(String, default="MODERATE") # LOW, MODERATE, HIGH, CRITICAL
    owner = Column(String, nullable=False)
    accuracy_score = Column(Float, default=94.5)
    drift_status = Column(String, default="NORMAL") # NORMAL, WARNING, DRIFT_DETECTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AiPlatformModelVersion(Base):
    __tablename__ = "ai_platform_model_versions"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("ai_platform_models.id"), nullable=False)
    version = Column(String, nullable=False)
    artifact_uri = Column(String, nullable=False)
    training_run_id = Column(String, nullable=True)
    metrics = Column(JSON, default=dict)
    approval_status = Column(String, default="APPROVED") # PENDING, APPROVED, REJECTED
    approved_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformEvaluation(Base):
    __tablename__ = "ai_platform_evaluations"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("ai_platform_models.id"), nullable=False)
    version = Column(String, nullable=False)
    eval_dataset = Column(String, default="Golden Safety & Accuracy Test Suite")
    accuracy_score = Column(Float, default=96.2)
    latency_p95_ms = Column(Float, default=45.0)
    safety_score = Column(Float, default=99.8)
    cost_per_1k_tokens = Column(Float, default=0.0015)
    passed_all_gates = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformDeployment(Base):
    __tablename__ = "ai_platform_deployments"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("ai_platform_models.id"), nullable=False)
    endpoint_name = Column(String, nullable=False, index=True)
    deployment_strategy = Column(String, default="CANARY") # BLUE_GREEN, CANARY, ROLLING, SHADOW
    traffic_percent = Column(Float, default=100.0)
    replicas = Column(Integer, default=3)
    status = Column(String, default="HEALTHY") # HEALTHY, DEGRADED, FAILED, ROLLING_BACK
    environment = Column(String, default="Production")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformPrompt(Base):
    __tablename__ = "ai_platform_prompts"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    current_version = Column(String, default="v2.1")
    template_text = Column(Text, nullable=False)
    variables = Column(JSON, default=list)
    owner = Column(String, nullable=False)
    status = Column(String, default="APPROVED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformRagSource(Base):
    __tablename__ = "ai_platform_rag_sources"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    embedding_model = Column(String, default="text-embedding-3-large")
    vector_index_name = Column(String, default="idx_enterprise_knowledge")
    chunk_count = Column(Integer, default=142000)
    retrieval_accuracy = Column(Float, default=98.4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformAgent(Base):
    __tablename__ = "ai_platform_agents"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    allowed_tools = Column(JSON, default=list)
    autonomy_level = Column(Integer, default=3)
    success_rate = Column(Float, default=99.1)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformCost(Base):
    __tablename__ = "ai_platform_costs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    category = Column(String, nullable=False) # GPU Compute, LLM Tokens, Vector Store, Training
    monthly_spend_usd = Column(Float, default=0.0)
    total_tokens_processed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiPlatformAgentTask(Base):
    __tablename__ = "ai_platform_agent_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    autonomy_level = Column(Integer, default=2)
    status = Column(String, default="COMPLETED")
    target_scope = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
