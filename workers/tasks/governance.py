"""
Celery Background Tasks for Phase 47 GRC & Privacy Platform (Section 63).
"""

from datetime import datetime, timezone
from typing import Any, Dict

try:
    from app.governance.service import GovernancePlatformService
except ImportError:
    from backend.app.governance.service import GovernancePlatformService

_gov_service = GovernancePlatformService()


def task_continuous_control_monitoring() -> Dict[str, Any]:
    """Scheduled task probing live control operational health."""
    results = _gov_service.run_continuous_monitoring()
    return {
        "task": "continuous_control_monitoring",
        "status": "SUCCESS",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": results,
    }


def task_audit_evidence_freshness() -> Dict[str, Any]:
    """Scheduled task auditing evidence expiration and freshness states."""
    results = _gov_service.audit_evidence_freshness()
    return {
        "task": "audit_evidence_freshness",
        "status": "SUCCESS",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": results,
    }


def task_sweep_expired_exceptions() -> Dict[str, Any]:
    """Scheduled task invalidating policy exceptions that passed their expiration date."""
    expired_count = _gov_service.sweep_expired_exceptions()
    return {
        "task": "sweep_expired_exceptions",
        "status": "SUCCESS",
        "expired_count": expired_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_capture_posture_snapshot() -> Dict[str, Any]:
    """Scheduled task persisting daily enterprise compliance posture snapshot."""
    snapshot = _gov_service.get_posture_snapshot()
    return {
        "task": "capture_posture_snapshot",
        "status": "SUCCESS",
        "score": snapshot.composite_compliance_score,
        "health": snapshot.overall_health,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
