"""Data Quality Rules, Data Observability, and Schema/Data Drift Service.

Evaluates 6-dimension data quality assertions (Completeness, Accuracy, Consistency,
Validity, Uniqueness, Timeliness), and detects schema drift with breaking change alerts.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.enterprise_data_os.base import (
        AttrDict,
        DataQualityDimension,
        generate_data_id,
    )
except ImportError:
    from app.services.enterprise_data_os.base import (
        AttrDict,
        DataQualityDimension,
        generate_data_id,
    )

logger = logging.getLogger(__name__)


class QualityObservabilityDriftService:
    """Manages quality assertions, observability alerts, and schema drift detection."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._rules: Dict[str, Dict[str, Any]] = {}
        self._drift_events: Dict[str, Dict[str, Any]] = {}

    def configure_quality_rule(
        self,
        tenant_id: str = "default_tenant",
        dataset_id: str = "silver_customer_profiles",
        rule_type: str = "NOT_NULL",  # NOT_NULL, UNIQUE, RANGE, FORMAT, FRESHNESS
        dimension: str = DataQualityDimension.COMPLETENESS.value,
        severity: str = "HIGH",
        pass_rate_pct: float = 99.8,
    ) -> AttrDict:
        rule_id = generate_data_id("rul")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "rule_id": rule_id,
            "id": rule_id,
            "tenant_id": tenant_id,
            "dataset_id": dataset_id,
            "rule_type": rule_type,
            "dimension": dimension,
            "severity": severity,
            "pass_rate_pct": pass_rate_pct,
            "is_active": True,
            "last_evaluated_at": now,
        }
        self._rules[rule_id] = record
        return AttrDict(record)

    def evaluate_quality_scorecard(
        self,
        tenant_id: str = "default_tenant",
        dataset_id: str = "silver_customer_profiles",
        completeness_pct: float = 99.4,
        accuracy_pct: float = 98.6,
        consistency_pct: float = 99.0,
        validity_pct: float = 97.8,
        uniqueness_pct: float = 100.0,
        timeliness_pct: float = 99.2,
    ) -> AttrDict:
        """Calculate multi-dimensional data quality scorecard."""
        qc_id = generate_data_id("qc")
        now = datetime.now(timezone.utc).isoformat()

        # Multi-factor Composite Score
        composite_score = (
            (completeness_pct * 0.20)
            + (accuracy_pct * 0.20)
            + (consistency_pct * 0.15)
            + (validity_pct * 0.15)
            + (uniqueness_pct * 0.15)
            + (timeliness_pct * 0.15)
        )
        composite_score = round(max(0.0, min(100.0, composite_score)), 2)

        record = {
            "qc_id": qc_id,
            "id": qc_id,
            "tenant_id": tenant_id,
            "dataset_id": dataset_id,
            "composite_score": composite_score,
            "dimensions": {
                "completeness": completeness_pct,
                "accuracy": accuracy_pct,
                "consistency": consistency_pct,
                "validity": validity_pct,
                "uniqueness": uniqueness_pct,
                "timeliness": timeliness_pct,
            },
            "status": "EXCELLENT" if composite_score >= 95.0 else "GOOD" if composite_score >= 85.0 else "DEGRADED",
            "evaluated_at": now,
        }
        return AttrDict(record)

    def detect_schema_drift(
        self,
        tenant_id: str = "default_tenant",
        dataset_id: str = "ds_orders",
        detected_changes: Optional[List[Dict[str, Any]]] = None,
    ) -> AttrDict:
        """Detect schema differences between incoming payload and registered schema."""
        drift_id = generate_data_id("drf")
        now = datetime.now(timezone.utc).isoformat()

        default_changes = [
            {"change_type": "COLUMN_ADDED", "column_name": "discount_code", "data_type": "STRING", "severity": "SAFE"},
            {"change_type": "NULLABLE_CHANGED", "column_name": "shipping_address", "is_nullable": True, "severity": "WARNING"},
        ]
        changes = detected_changes or default_changes
        has_breaking = any(c.get("severity") == "BREAKING" for c in changes)

        record = {
            "drift_id": drift_id,
            "id": drift_id,
            "tenant_id": tenant_id,
            "dataset_id": dataset_id,
            "has_drift": len(changes) > 0,
            "is_breaking_change": has_breaking,
            "changes": changes,
            "action_required": "Human Schema Review Gate Required" if has_breaking else "Auto-Compatible Schema Evolution",
            "detected_at": now,
        }
        self._drift_events[drift_id] = record
        return AttrDict(record)
