"""Server-controlled versioned RiskPolicy and configuration matrix."""

from typing import Any, Dict
from pydantic import BaseModel, Field


class RiskPolicy(BaseModel):
    """Server-controlled immutable risk policy parameters."""

    policy_version: str = "v1"
    engine_version: str = "1.0.0"
    max_allowed_risk_level: str = Field(default="MEDIUM", description="Max risk level acceptable for PASS: LOW, MEDIUM")
    require_human_review_for_medium_risk: bool = True
    block_unsupported_claims: bool = True
    block_sensitive_data: bool = True
    block_deceptive_content: bool = True
    min_evidence_coverage: float = 0.5
    min_quality_score: float = 50.0
    ai_semantic_review_enabled: bool = True
    fail_safe_behavior: str = Field(default="REVIEW", description="Behavior when AI evaluator fails: REVIEW or BLOCK")

    def to_context_dict(self) -> Dict[str, Any]:
        return {
            "policy_version": self.policy_version,
            "engine_version": self.engine_version,
            "max_allowed_risk_level": self.max_allowed_risk_level,
            "min_evidence_coverage": self.min_evidence_coverage,
            "min_quality_score": self.min_quality_score,
            "fail_safe_behavior": self.fail_safe_behavior,
        }


DEFAULT_RISK_POLICY = RiskPolicy()
