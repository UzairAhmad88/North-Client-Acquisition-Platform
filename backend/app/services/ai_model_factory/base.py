"""Base utilities, Enums, and constants for Phase 63 AI Model Factory."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ModelType(str, Enum):
    CLASSIFICATION = "CLASSIFICATION"
    REGRESSION = "REGRESSION"
    CLUSTERING = "CLUSTERING"
    FORECASTING = "FORECASTING"
    RANKING = "RANKING"
    RECOMMENDATION = "RECOMMENDATION"
    ANOMALY_DETECTION = "ANOMALY_DETECTION"
    NLP = "NLP"
    VISION = "VISION"
    SPEECH = "SPEECH"
    MULTIMODAL = "MULTIMODAL"
    EMBEDDING = "EMBEDDING"
    LLM = "LLM"
    RERANKER = "RERANKER"
    GENERATION = "GENERATION"
    AGENT = "AGENT"


class FrameworkType(str, Enum):
    PYTORCH = "PYTORCH"
    TENSORFLOW = "TENSORFLOW"
    SKLEARN = "SKLEARN"
    XGBOOST = "XGBOOST"
    LIGHTGBM = "LIGHTGBM"
    HUGGINGFACE = "HUGGINGFACE"
    ONNX = "ONNX"
    CUSTOM_PYTHON = "CUSTOM_PYTHON"
    EXTERNAL_API = "EXTERNAL_API"
    HOSTED_MODEL = "HOSTED_MODEL"


class ModelStage(str, Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    VALIDATION = "VALIDATION"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


class DeploymentStrategy(str, Enum):
    CANARY = "CANARY"
    BLUE_GREEN = "BLUE_GREEN"
    SHADOW = "SHADOW"
    ROLLING = "ROLLING"
    AB_TESTING = "AB_TESTING"
    CHAMPION_CHALLENGER = "CHAMPION_CHALLENGER"


class DriftType(str, Enum):
    FEATURE_DRIFT = "FEATURE_DRIFT"
    PREDICTION_DRIFT = "PREDICTION_DRIFT"
    LABEL_DRIFT = "LABEL_DRIFT"
    CONCEPT_DRIFT = "CONCEPT_DRIFT"
    HALLUCINATION_SPIKE = "HALLUCINATION_SPIKE"


class EvaluationMetricType(str, Enum):
    ACCURACY = "ACCURACY"
    PRECISION = "PRECISION"
    RECALL = "RECALL"
    F1_SCORE = "F1_SCORE"
    ROC_AUC = "ROC_AUC"
    RMSE = "RMSE"
    MAE = "MAE"
    FAITHFULNESS = "FAITHFULNESS"
    GROUNDEDNESS = "GROUNDEDNESS"
    TOXICITY = "TOXICITY"
    LATENCY_P95 = "LATENCY_P95"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AiIncidentSeverity(str, Enum):
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"


def generate_ai_id(prefix: str) -> str:
    """Generate deterministic or random prefixed ID."""
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class AttrDict(dict):
    """Dictionary supporting attribute dot notation access."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
