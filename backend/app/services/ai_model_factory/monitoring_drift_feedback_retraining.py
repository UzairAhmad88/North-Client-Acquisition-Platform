"""Live Observability, Multi-Type Drift Detection, Feedback, and Retraining Triggers Service for Phase 63."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

try:
    from backend.app.services.ai_model_factory.base import (
        AttrDict,
        DriftType,
        generate_ai_id,
    )
except ImportError:
    from app.services.ai_model_factory.base import (
        AttrDict,
        DriftType,
        generate_ai_id,
    )

logger = logging.getLogger(__name__)


class MonitoringDriftFeedbackRetrainingService:
    """Manages Live Model Monitoring, Population Stability Index (PSI) / KS Drift Detection, Feedback, and Automated Retraining."""

    def __init__(self):
        self._monitoring_snapshots: List[AttrDict] = []
        self._drift_events: Dict[str, AttrDict] = {}
        self._feedbacks: Dict[str, AttrDict] = {}
        self._retraining_jobs: List[AttrDict] = []

    def record_monitoring_snapshot(
        self,
        tenant_id: str,
        deployment_id: str,
        requests_count: int,
        errors_count: int,
        avg_latency_ms: float,
        cost_usd: float,
        input_token_count: int = 0,
        output_token_count: int = 0,
    ) -> AttrDict:
        """Record an hourly/daily monitoring rollup snapshot."""
        snap_id = generate_ai_id("aimon")
        now = datetime.utcnow()

        error_rate = errors_count / max(requests_count, 1)
        drift_status = "NORMAL"
        if error_rate > 0.05 or avg_latency_ms > 150.0:
            drift_status = "WARNING"

        snap = AttrDict({
            "id": snap_id,
            "tenant_id": tenant_id,
            "deployment_id": deployment_id,
            "timestamp": now,
            "requests_count": requests_count,
            "errors_count": errors_count,
            "avg_latency_ms": avg_latency_ms,
            "input_token_count": input_token_count,
            "output_token_count": output_token_count,
            "cost_usd": cost_usd,
            "drift_status": drift_status,
        })
        self._monitoring_snapshots.append(snap)
        return snap

    def detect_and_record_drift(
        self,
        tenant_id: str,
        deployment_id: str,
        drift_type: str = DriftType.FEATURE_DRIFT.value,
        metric_name: str = "PSI",
        metric_value: float = 0.12,
        threshold: float = 0.25,
    ) -> AttrDict:
        """Detect and store drift events using statistical divergence metrics."""
        drift_id = generate_ai_id("drift")
        now = datetime.utcnow()

        is_breached = metric_value >= threshold
        action = "TRIGGER_RETRAINING" if is_breached else "NO_ACTION_REQUIRED"

        event = AttrDict({
            "id": drift_id,
            "tenant_id": tenant_id,
            "deployment_id": deployment_id,
            "drift_type": drift_type,
            "metric_name": metric_name,
            "metric_value": metric_value,
            "threshold": threshold,
            "is_breached": is_breached,
            "suggested_action": action,
            "created_at": now,
        })
        self._drift_events[drift_id] = event
        if is_breached:
            logger.warning(f"Drift breach detected on Deployment {deployment_id}: {metric_name}={metric_value} >= {threshold}")
        return event

    def submit_feedback(
        self,
        tenant_id: str,
        model_version_id: str,
        user_id: str,
        feedback_type: str = "THUMBS_UP",
        rating_score: Optional[float] = 5.0,
        correction_text: Optional[str] = None,
    ) -> AttrDict:
        """Submit and validate human feedback for RLHF / active learning dataset curation."""
        fb_id = generate_ai_id("aifb")
        now = datetime.utcnow()

        # Feedback Quality Gate
        quality = "VALID"
        if correction_text and len(correction_text.strip()) < 3 and feedback_type == "CORRECTION":
            quality = "AMBIGUOUS"

        feedback = AttrDict({
            "id": fb_id,
            "tenant_id": tenant_id,
            "model_version_id": model_version_id,
            "user_id": user_id,
            "feedback_type": feedback_type,
            "rating_score": rating_score,
            "correction_text": correction_text,
            "quality_classification": quality,
            "is_included_in_retraining": quality == "VALID",
            "created_at": now,
        })
        self._feedbacks[fb_id] = feedback
        logger.info(f"Recorded feedback {fb_id} for ModelVersion {model_version_id} ({feedback_type})")
        return feedback

    def trigger_retraining_workflow(
        self,
        tenant_id: str,
        model_id: str,
        reason: str = "DRIFT_BREACH",
    ) -> AttrDict:
        """Trigger an automated retraining workflow from drift or schedule."""
        job_id = generate_ai_id("retrain")
        now = datetime.utcnow()

        job = AttrDict({
            "id": job_id,
            "tenant_id": tenant_id,
            "model_id": model_id,
            "trigger_reason": reason,
            "status": "QUEUED",
            "generated_dataset_id": f"aids_retrain_{job_id}",
            "created_at": now,
        })
        self._retraining_jobs.append(job)
        logger.info(f"Triggered Retraining Workflow {job_id} for Model {model_id} (Reason: {reason})")
        return job

    def list_drift_events(self, tenant_id: str, deployment_id: Optional[str] = None) -> List[AttrDict]:
        """List drift events."""
        events = [e for e in self._drift_events.values() if e.tenant_id == tenant_id]
        if deployment_id:
            events = [e for e in events if e.deployment_id == deployment_id]
        return events

    def list_feedbacks(self, tenant_id: str, model_version_id: Optional[str] = None) -> List[AttrDict]:
        """List feedbacks."""
        fbs = [f for f in self._feedbacks.values() if f.tenant_id == tenant_id]
        if model_version_id:
            fbs = [f for f in fbs if f.model_version_id == model_version_id]
        return fbs

    def list_retraining_jobs(self, tenant_id: str) -> List[AttrDict]:
        """List retraining jobs."""
        return [r for r in self._retraining_jobs if r.tenant_id == tenant_id]
