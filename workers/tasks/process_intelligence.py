"""
Background Tasks for Phase 49:
Unified Workflow Intelligence, Process Mining, Business Process Optimization & Operations.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

try:
    from app.process_intelligence.service import ProcessIntelligencePlatformService
except ImportError:
    from backend.app.process_intelligence.service import ProcessIntelligencePlatformService

_process_service = ProcessIntelligencePlatformService()


def task_mine_process_variants(process_id: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Reconstructs execution variants from case event logs."""
    variants = _process_service.discovery_engine.discover_variants(process_id, tenant_id)
    return {
        "task": "mine_process_variants",
        "status": "SUCCESS",
        "process_id": process_id,
        "variants_discovered": len(variants),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_audit_process_conformance(process_id: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Sweeps cases against conformance rules to detect skipped steps and missing approvals."""
    violations = _process_service.conformance_checker.check_process_conformance(process_id, tenant_id)
    return {
        "task": "audit_process_conformance",
        "status": "SUCCESS",
        "process_id": process_id,
        "violations_detected": len(violations),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_detect_process_bottlenecks(process_id: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Analyzes queue latencies and activities exceeding wait thresholds."""
    bottlenecks = _process_service.bottleneck_detector.detect_bottlenecks(process_id, tenant_id=tenant_id)
    return {
        "task": "detect_process_bottlenecks",
        "status": "SUCCESS",
        "process_id": process_id,
        "bottlenecks_detected": len(bottlenecks),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_evaluate_automation_candidates(process_id: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Scans for repetitive deterministic tasks and updates automation suitability scores."""
    candidates = _process_service.automation_evaluator.scan_for_candidates(process_id, tenant_id)
    return {
        "task": "evaluate_automation_candidates",
        "status": "SUCCESS",
        "process_id": process_id,
        "candidates_evaluated": len(candidates),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
