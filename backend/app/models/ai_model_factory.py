"""Phase 63 — Unified AI/ML Model Factory, MLOps, LLMOps, Evaluation, Model Governance & Production AI Operating System SQLAlchemy Models."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class AiProjectModel(Base):
    """AI/ML Project Workspace."""
    __tablename__ = "ai_projects"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String(128), nullable=False)
    team = Column(String(128), nullable=False)
    domain = Column(String(64), nullable=False, default="GENERAL")
    objective = Column(Text, nullable=True)
    budget_allocated_usd = Column(Float, default=10000.0)
    budget_spent_usd = Column(Float, default=0.0)
    status = Column(String(32), default="ACTIVE", index=True)  # DRAFT, ACTIVE, PAUSED, PRODUCTION, DEPRECATED, ARCHIVED
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AiDatasetVersionModel(Base):
    """Governed AI Training Dataset Version linked to Lakehouse."""
    __tablename__ = "ai_dataset_versions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("ai_projects.id"), nullable=False, index=True)
    dataset_name = Column(String(255), nullable=False)
    version = Column(String(32), nullable=False)
    source_lakehouse_dataset_id = Column(String(64), nullable=True)
    features_list = Column(JSON, default=list)
    label_column = Column(String(128), nullable=True)
    splits = Column(JSON, default=dict)  # train: 70%, val: 15%, test: 15%
    row_count = Column(Integer, default=0)
    bias_check_status = Column(String(32), default="PASSED")
    lineage_provenance = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiExperimentModel(Base):
    """AI Experiment containing multiple trials/runs."""
    __tablename__ = "ai_experiments"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("ai_projects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    model_type = Column(String(64), nullable=False)  # CLASSIFICATION, REGRESSION, LLM, EMBEDDING, RAG, AGENT
    framework = Column(String(64), nullable=False)  # PYTORCH, SKLEARN, HUGGINGFACE, ONNX, LLM_API
    search_strategy = Column(String(32), default="BAYESIAN")  # BAYESIAN, GRID, RANDOM
    best_metric_name = Column(String(64), default="f1_score")
    best_metric_value = Column(Float, nullable=True)
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiExperimentRunModel(Base):
    """Individual Experiment Run / Trial."""
    __tablename__ = "ai_experiment_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    experiment_id = Column(String(64), ForeignKey("ai_experiments.id"), nullable=False, index=True)
    run_number = Column(Integer, default=1)
    git_commit_hash = Column(String(64), nullable=True)
    dataset_version_id = Column(String(64), nullable=True)
    hyperparameters = Column(JSON, default=dict)
    metrics = Column(JSON, default=dict)
    hardware_specs = Column(JSON, default=dict)  # gpu, cpu, memory
    duration_seconds = Column(Float, default=0.0)
    cost_usd = Column(Float, default=0.0)
    artifacts_uri = Column(String(512), nullable=True)
    status = Column(String(32), default="COMPLETED")  # QUEUED, RUNNING, COMPLETED, FAILED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiTrainingJobModel(Base):
    """Distributed Training / Fine-tuning Job."""
    __tablename__ = "ai_training_jobs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("ai_projects.id"), nullable=False, index=True)
    model_name = Column(String(255), nullable=False)
    base_model_name = Column(String(255), nullable=True)
    job_type = Column(String(32), default="PRETRAINING")  # PRETRAINING, FINE_TUNING, RLHF, DISTILLATION
    gpu_type = Column(String(64), default="NVIDIA_A100_80GB")
    gpu_count = Column(Integer, default=1)
    status = Column(String(32), default="QUEUED", index=True)
    progress_pct = Column(Float, default=0.0)
    epochs_total = Column(Integer, default=10)
    current_epoch = Column(Integer, default=0)
    loss_history = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiModelRegistryModel(Base):
    """Central Registered Model Entity."""
    __tablename__ = "ai_models"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("ai_projects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    model_type = Column(String(64), nullable=False)
    framework = Column(String(64), nullable=False)
    owner = Column(String(128), nullable=False)
    steward = Column(String(128), nullable=True)
    current_stage = Column(String(32), default="EXPERIMENTAL", index=True)  # EXPERIMENTAL, VALIDATION, STAGING, PRODUCTION, DEPRECATED, RETIRED
    active_version = Column(String(32), default="1.0.0")
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AiModelVersionModel(Base):
    """Immutable Model Version Artifact & Metadata."""
    __tablename__ = "ai_model_versions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    model_id = Column(String(64), ForeignKey("ai_models.id"), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    stage = Column(String(32), default="EXPERIMENTAL")
    training_run_id = Column(String(64), nullable=True)
    dataset_version_id = Column(String(64), nullable=True)
    artifacts_manifest = Column(JSON, default=dict)  # weights, tokenizer, config, onnx
    metrics_summary = Column(JSON, default=dict)  # accuracy, f1, latency_p95, loss
    supply_chain_sbom = Column(JSON, default=dict)  # base model, licenses, packages
    is_signed = Column(Boolean, default=True)
    quality_gate_passed = Column(Boolean, default=False)
    security_scan_passed = Column(Boolean, default=False)
    governance_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiEvaluationSuiteModel(Base):
    """Standardized Benchmark Evaluation Suite."""
    __tablename__ = "ai_evaluation_suites"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    suite_type = Column(String(64), default="GOLDEN_DATASET")  # GOLDEN_DATASET, REGRESSION, SAFETY_RED_TEAM, LLM_JUDGE
    target_model_type = Column(String(64), nullable=False)
    thresholds_config = Column(JSON, default=dict)  # min_accuracy: 0.90, max_toxicity: 0.01
    test_cases_count = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiEvaluationResultModel(Base):
    """Executed Model Evaluation Run."""
    __tablename__ = "ai_evaluation_results"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    suite_id = Column(String(64), ForeignKey("ai_evaluation_suites.id"), nullable=False, index=True)
    model_version_id = Column(String(64), ForeignKey("ai_model_versions.id"), nullable=False, index=True)
    evaluator_engine = Column(String(64), default="AUTOMATED_DETERMINISTIC")  # AUTOMATED_DETERMINISTIC, LLM_AS_JUDGE, HUMAN_EVAL
    judge_model = Column(String(128), nullable=True)
    passed = Column(Boolean, default=False)
    score = Column(Float, default=0.0)
    detailed_metrics = Column(JSON, default=dict)  # accuracy, precision, recall, f1, faithfulness, toxicity
    failure_reasons = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiPromptRegistryModel(Base):
    """Governed Prompt Template Registry."""
    __tablename__ = "ai_prompts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    version = Column(String(32), default="1.0.0")
    purpose = Column(String(128), nullable=False)
    system_prompt = Column(Text, nullable=False)
    user_template = Column(Text, nullable=False)
    variables = Column(JSON, default=list)
    target_model_family = Column(String(64), default="ANY")
    stage = Column(String(32), default="TESTING")  # DRAFT, TESTING, APPROVED, PRODUCTION, DEPRECATED
    token_budget_max = Column(Integer, default=4096)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiDeploymentModel(Base):
    """Production / Staging Model Deployment."""
    __tablename__ = "ai_deployments"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    model_version_id = Column(String(64), ForeignKey("ai_model_versions.id"), nullable=False, index=True)
    environment = Column(String(32), default="PRODUCTION", index=True)  # STAGING, PRODUCTION, CANARY, SHADOW
    strategy = Column(String(32), default="CANARY")  # CANARY, BLUE_GREEN, SHADOW, CHAMPION_CHALLENGER
    traffic_weight_pct = Column(Float, default=100.0)
    endpoint_url = Column(String(512), nullable=True)
    min_replicas = Column(Integer, default=1)
    max_replicas = Column(Integer, default=5)
    current_replicas = Column(Integer, default=1)
    status = Column(String(32), default="ACTIVE")  # ACTIVE, PAUSED, ROLLING_BACK, RETIRED
    rollback_target_version_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiInferenceEndpointModel(Base):
    """Inference Gateway Route & SLA."""
    __tablename__ = "ai_inference_endpoints"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    route_name = Column(String(128), nullable=False, index=True)
    primary_deployment_id = Column(String(64), ForeignKey("ai_deployments.id"), nullable=False)
    fallback_deployment_id = Column(String(64), nullable=True)
    routing_policy = Column(String(64), default="LEAST_LATENCY")  # LEAST_LATENCY, LOWEST_COST, ROUND_ROBIN
    timeout_ms = Column(Integer, default=5000)
    rate_limit_rpm = Column(Integer, default=1000)
    total_requests = Column(Integer, default=0)
    p95_latency_ms = Column(Float, default=45.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiModelMonitoringModel(Base):
    """Live Observability & Health Aggregate."""
    __tablename__ = "ai_model_monitoring"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    deployment_id = Column(String(64), ForeignKey("ai_deployments.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    requests_count = Column(Integer, default=0)
    errors_count = Column(Integer, default=0)
    avg_latency_ms = Column(Float, default=0.0)
    input_token_count = Column(Integer, default=0)
    output_token_count = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    drift_status = Column(String(32), default="NORMAL")  # NORMAL, WARNING, CRITICAL_DRIFT


class AiDriftEventModel(Base):
    """Feature or Concept Drift Event."""
    __tablename__ = "ai_drift_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    deployment_id = Column(String(64), ForeignKey("ai_deployments.id"), nullable=False, index=True)
    drift_type = Column(String(32), default="FEATURE_DRIFT")  # FEATURE_DRIFT, PREDICTION_DRIFT, CONCEPT_DRIFT, HALLUCINATION_SPIKE
    metric_name = Column(String(64), default="PSI")  # PSI, KS_STATISTIC, JENSEN_SHANNON
    metric_value = Column(Float, default=0.0)
    threshold = Column(Float, default=0.25)
    is_breached = Column(Boolean, default=False)
    suggested_action = Column(String(64), default="TRIGGER_RETRAINING")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiFeedbackModel(Base):
    """Human Feedback & Active Correction."""
    __tablename__ = "ai_feedback"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    model_version_id = Column(String(64), nullable=False, index=True)
    user_id = Column(String(64), nullable=False)
    feedback_type = Column(String(32), default="THUMBS_UP")  # THUMBS_UP, THUMBS_DOWN, CORRECTION, RATING
    rating_score = Column(Float, nullable=True)
    correction_text = Column(Text, nullable=True)
    quality_classification = Column(String(32), default="VALID")  # VALID, INVALID, AMBIGUOUS, MALICIOUS, DUPLICATE
    is_included_in_retraining = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiModelCardModel(Base):
    """Formal Model Card for Governance & Compliance."""
    __tablename__ = "ai_model_cards"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    model_version_id = Column(String(64), ForeignKey("ai_model_versions.id"), nullable=False, index=True)
    intended_use = Column(Text, nullable=False)
    limitations = Column(Text, nullable=False)
    training_data_summary = Column(Text, nullable=False)
    evaluation_summary = Column(Text, nullable=False)
    ethical_considerations = Column(Text, nullable=False)
    risk_level = Column(String(32), default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    owner = Column(String(128), nullable=False)
    steward = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiGpuJobModel(Base):
    """GPU Resource Allocation & Queue Item."""
    __tablename__ = "ai_gpu_jobs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    training_job_id = Column(String(64), ForeignKey("ai_training_jobs.id"), nullable=True)
    gpu_cluster_node = Column(String(128), default="cluster-node-alpha-01")
    gpu_type = Column(String(64), default="NVIDIA_H100_SXM5_80GB")
    gpu_count = Column(Integer, default=1)
    memory_requested_gb = Column(Integer, default=80)
    priority = Column(Integer, default=50)  # 1-100 (100 highest)
    status = Column(String(32), default="RUNNING")  # QUEUED, RUNNING, COMPLETED, PREEMPTED
    allocated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiFinopsCostModel(Base):
    """AI FinOps Cost Allocation Record."""
    __tablename__ = "ai_finops_costs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    project_id = Column(String(64), ForeignKey("ai_projects.id"), nullable=False, index=True)
    model_id = Column(String(64), nullable=True)
    cost_category = Column(String(64), default="INFERENCE_TOKENS")  # TRAINING_GPU, INFERENCE_TOKENS, EMBEDDINGS, EVALUATION, STORAGE
    amount_usd = Column(Float, default=0.0)
    units_consumed = Column(Float, default=0.0)  # tokens or GPU hours
    period_date = Column(String(10), default=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiIncidentModel(Base):
    """AI Safety, Hallucination, or Drift Incident."""
    __tablename__ = "ai_incidents"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True, index=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    deployment_id = Column(String(64), nullable=True)
    incident_type = Column(String(64), default="HALLUCINATION")  # HALLUCINATION, DRIFT, TIMEOUT, SAFETY_VIOLATION, COST_SPIKE
    severity = Column(String(16), default="SEV2")  # SEV1, SEV2, SEV3, SEV4
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    status = Column(String(32), default="OPEN")  # OPEN, INVESTIGATING, MITIGATED, RESOLVED
    mitigation_action = Column(String(64), default="CANARY_ROLLBACK")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
