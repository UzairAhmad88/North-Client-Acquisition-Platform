"""Pydantic Request & Response Schemas for Phase 63 AI Model Factory."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AiProjectCreateRequest(BaseModel):
    name: str = Field(..., description="Project workspace name")
    owner: str = Field(..., description="Owner email or lead ID")
    team: str = Field(..., description="Responsible team name")
    domain: str = Field("GENERAL", description="Domain classification")
    description: Optional[str] = None
    objective: Optional[str] = None
    budget_allocated_usd: float = Field(10000.0, ge=0.0)


class AiDatasetVersionRegisterRequest(BaseModel):
    project_id: str
    dataset_name: str
    version: str
    features_list: List[str]
    label_column: Optional[str] = None
    source_lakehouse_dataset_id: Optional[str] = None
    splits: Optional[Dict[str, float]] = None
    row_count: int = 50000


class AiExperimentCreateRequest(BaseModel):
    project_id: str
    name: str
    model_type: str = "CLASSIFICATION"
    framework: str = "PYTORCH"
    search_strategy: str = "BAYESIAN"
    best_metric_name: str = "f1_score"
    description: Optional[str] = None


class AiExperimentRunLogRequest(BaseModel):
    experiment_id: str
    run_number: int = 1
    hyperparameters: Dict[str, Any]
    metrics: Dict[str, float]
    git_commit_hash: Optional[str] = None
    dataset_version_id: Optional[str] = None
    duration_seconds: float = 120.0
    cost_usd: float = 1.45


class AiModelRegisterRequest(BaseModel):
    project_id: str
    name: str
    owner: str
    model_type: str = "CLASSIFICATION"
    framework: str = "PYTORCH"
    steward: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class AiModelVersionCreateRequest(BaseModel):
    model_id: str
    version: str
    training_run_id: Optional[str] = None
    dataset_version_id: Optional[str] = None
    metrics_summary: Optional[Dict[str, float]] = None


class AiModelStagePromoteRequest(BaseModel):
    version_id: str
    target_stage: str  # STAGING, PRODUCTION, RETIRED
    approver: str


class AiEvaluationSuiteCreateRequest(BaseModel):
    name: str
    target_model_type: str
    suite_type: str = "GOLDEN_DATASET"
    thresholds_config: Optional[Dict[str, float]] = None
    test_cases_count: int = 100


class AiEvaluationRunRequest(BaseModel):
    suite_id: str
    model_version_id: str
    evaluator_engine: str = "AUTOMATED_DETERMINISTIC"
    judge_model: Optional[str] = None


class AiPromptRegisterRequest(BaseModel):
    name: str
    purpose: str
    system_prompt: str
    user_template: str
    version: str = "1.0.0"
    variables: Optional[List[str]] = None
    target_model_family: str = "ANY"
    token_budget_max: int = 4096


class AiDeploymentCreateRequest(BaseModel):
    model_version_id: str
    environment: str = "PRODUCTION"
    strategy: str = "CANARY"
    traffic_weight_pct: float = 10.0
    min_replicas: int = 2
    max_replicas: int = 10
    rollback_target_version_id: Optional[str] = None


class AiInferencePredictRequest(BaseModel):
    endpoint_id: str
    input_payload: Dict[str, Any]


class AiFeedbackSubmitRequest(BaseModel):
    model_version_id: str
    user_id: str
    feedback_type: str = "THUMBS_UP"
    rating_score: Optional[float] = 5.0
    correction_text: Optional[str] = None


class AiModelCardCreateRequest(BaseModel):
    model_version_id: str
    owner: str
    steward: str
    intended_use: str
    limitations: str
    training_data_summary: str
    evaluation_summary: str
    ethical_considerations: str
    risk_level: str = "MEDIUM"


class AiCopilotQueryRequest(BaseModel):
    query: str
