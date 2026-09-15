"""Feature Context & Data Leakage Prevention Engine."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from agents.decision_intelligence.models import FeatureVector


class FeatureContextEngine:
    """Manages point-in-time feature extraction and enforces strict data leakage prevention."""

    # Prohibited post-event feature keywords that indicate outcome leakage
    PROHIBITED_POST_EVENT_KEYS = {
        "final_invoice_amount",
        "client_signature_timestamp",
        "actual_completion_date",
        "post_delivery_defect_count",
        "realized_margin",
        "churn_confirmed_date",
        "settled_contract_value",
    }

    def validate_feature_leakage(
        self,
        features: Dict[str, Any],
        inference_timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Verify that feature payload contains zero prohibited post-event data or future timestamps."""
        leakage_detected = False
        reasons = []

        now_t = inference_timestamp or datetime.utcnow()

        for k, v in features.items():
            if k.lower() in self.PROHIBITED_POST_EVENT_KEYS:
                leakage_detected = True
                reasons.append(f"Feature '{k}' is a prohibited post-event outcome variable (Data Leakage).")

            # Check if any timestamp features are in the future relative to inference time
            if isinstance(v, str) and ("date" in k.lower() or "timestamp" in k.lower() or "at" in k.lower()):
                try:
                    parsed_dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
                    if parsed_dt.tzinfo is not None:
                        parsed_dt = parsed_dt.replace(tzinfo=None)
                    if parsed_dt > now_t:
                        leakage_detected = True
                        reasons.append(f"Feature '{k}' has future timestamp ({v}) beyond inference time ({now_t.isoformat()}).")
                except Exception:
                    pass

        return {
            "is_valid": not leakage_detected,
            "leakage_detected": leakage_detected,
            "reasons": reasons,
        }

    def assemble_feature_vector(
        self,
        entity_id: str,
        raw_entity_data: Dict[str, Any],
        as_of_timestamp: Optional[str] = None,
    ) -> FeatureVector:
        """Assemble a clean feature snapshot with point-in-time timestamping."""
        ts = as_of_timestamp or datetime.utcnow().isoformat()
        # Clean and extract numerical/categorical signals
        snapshot: Dict[str, Any] = {}
        for k, v in raw_entity_data.items():
            if k.startswith("_"):
                continue
            if isinstance(v, (int, float, str, bool)):
                snapshot[k] = v

        return FeatureVector(
            entity_id=entity_id,
            feature_snapshot=snapshot,
            as_of_timestamp=ts,
        )
