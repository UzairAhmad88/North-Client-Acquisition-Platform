"""Reliability platform service coordinating deep health, dependencies, resilience, SLOs, and incidents."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.reliability.base import (
    DeepHealthResult,
    DependencyStatus,
    ErrorBudgetStatus,
    IncidentSeverity,
    IncidentStatus,
    ServiceHealthStatus,
    SLOType,
)
from app.reliability.dependencies import CircuitBreaker, DependencyManager
from app.reliability.health import DeepHealthEngine
from app.reliability.incidents import IncidentManager
from app.reliability.integrity import DataIntegrityChecker
from app.reliability.resilience import GracefulDegradationManager, IdempotencyGuard, RetryPolicy
from app.reliability.slo import SLOSnapshot, SLOEngine


class ReliabilityPlatformService:
    """Consolidated reliability, SRE, and platform resilience orchestrator."""

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.health_engine = DeepHealthEngine(db)
        self.dep_manager = DependencyManager()
        self.idempotency_guard = IdempotencyGuard()
        self.degradation_manager = GracefulDegradationManager()
        self.slo_engine = SLOEngine()
        self.incident_manager = IncidentManager()
        self.integrity_checker = DataIntegrityChecker(db)

    def get_deep_health(self) -> DeepHealthResult:
        return self.health_engine.evaluate_deep_health()

    def evaluate_slos(self, custom_metrics: Optional[List[Dict[str, Any]]] = None) -> List[SLOSnapshot]:
        results = []
        metrics = custom_metrics or [
            {"name": "API Availability", "target": Decimal("99.90"), "total": 10000, "good": 9996, "type": SLOType.AVAILABILITY},
            {"name": "Critical Workflow Completion", "target": Decimal("99.95"), "total": 2000, "good": 1999, "type": SLOType.COMPLETION_RATE},
            {"name": "Payment & Ledger Reconciliations", "target": Decimal("99.99"), "total": 5000, "good": 5000, "type": SLOType.AVAILABILITY},
            {"name": "API p95 Latency (< 500ms)", "target": Decimal("99.00"), "total": 10000, "good": 9920, "type": SLOType.LATENCY},
        ]
        for m in metrics:
            snap = self.slo_engine.evaluate_slo(
                name=m["name"],
                target_percentage=m["target"],
                total_events=m["total"],
                good_events=m["good"],
                slo_type=m.get("type", SLOType.AVAILABILITY),
                window_days=m.get("window_days", 30),
            )
            results.append(snap)
        return results

    def get_integrity_report(self) -> Dict[str, Any]:
        return self.integrity_checker.scan_all_domains()
