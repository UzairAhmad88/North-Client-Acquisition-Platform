"""AI Data Governance service for Phase 65."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class AiDataGovernanceService:
    """Tracks permitted use of training, evaluation, synthetic, and user data for AI."""

    def __init__(self):
        self._policies: List[Dict[str, Any]] = [
            {"data_tier": "PUBLIC", "ai_training_allowed": True, "ai_rag_allowed": True},
            {"data_tier": "INTERNAL", "ai_training_allowed": True, "ai_rag_allowed": True},
            {"data_tier": "CONFIDENTIAL", "ai_training_allowed": False, "ai_rag_allowed": True},
            {"data_tier": "RESTRICTED", "ai_training_allowed": False, "ai_rag_allowed": False},
        ]

    def verify_ai_usage_permission(self, data_tier: str, usage_intent: str = "INFERENCE") -> Dict[str, Any]:
        tier = data_tier.upper()
        policy = next((p for p in self._policies if p["data_tier"] == tier), None)
        if not policy:
            return {"allowed": False, "reason": f"Unknown data tier '{data_tier}'"}

        if usage_intent == "TRAINING":
            allowed = policy["ai_training_allowed"]
        else:
            allowed = policy["ai_rag_allowed"]

        return {
            "data_tier": tier,
            "usage_intent": usage_intent,
            "allowed": allowed,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
