"""
Workforce Evaluation, Telemetry, Security & Kill Switch Subsystem for Phase 52.
Tracks grounding accuracy, task success rates, policy compliance, and executes authoritative kill switches.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional, Tuple
import uuid

try:
    from backend.app.services.workforce.base import KillSwitchTarget
except ImportError:
    from app.services.workforce.base import KillSwitchTarget

logger = logging.getLogger(__name__)


class WorkerEvaluationEngine:
    """Evaluates grounding, factuality, policy compliance, and quality metrics."""

    def compute_worker_scorecard(
        self,
        worker_code: str,
        tasks_evaluated: int = 25,
        success_count: int = 24,
        grounding_score: float = 0.96,
        factuality_score: float = 0.94,
        policy_compliance_rate: float = 0.98,
        human_overrides: int = 1,
    ) -> Dict[str, Any]:
        """Aggregates worker performance into a formal quality score."""
        success_rate = (success_count / max(1, tasks_evaluated)) * 100.0
        override_rate = (human_overrides / max(1, tasks_evaluated)) * 100.0

        return {
            "worker_code": worker_code,
            "period": "CURRENT_EVALUATION_WINDOW",
            "tasks_evaluated": tasks_evaluated,
            "task_success_rate": round(success_rate, 1),
            "grounding_score": round(grounding_score, 2),
            "factuality_score": round(factuality_score, 2),
            "policy_compliance_rate": round(policy_compliance_rate, 2),
            "human_override_rate": round(override_rate, 1),
            "health_grade": "A+" if success_rate >= 95 and grounding_score >= 0.9 else "B",
        }


class WorkforceSecurityManager:
    """Enforces emergency kill switches, tenant sandboxing, and threat containment."""

    def __init__(self):
        self._active_kill_switches: Dict[str, Dict[str, Any]] = {}

    def trigger_kill_switch(
        self,
        target_type: KillSwitchTarget,
        target_identifier: str,
        reason: str,
        operator_id: str = "security_admin",
    ) -> Dict[str, Any]:
        """Instantly halts execution for the target workforce boundary."""
        switch_id = f"KS-{uuid.uuid4().hex[:6].upper()}"
        key = f"{target_type.value}:{target_identifier}"
        record = {
            "kill_switch_id": switch_id,
            "target_type": target_type.value,
            "target_identifier": target_identifier,
            "reason": reason,
            "triggered_by": operator_id,
            "triggered_at": datetime.now(timezone.utc).isoformat(),
            "status": "ACTIVE",
        }
        self._active_kill_switches[key] = record
        logger.critical(f"EMERGENCY KILL SWITCH ACTIVATED: {key}. Reason: {reason}")
        return record

    def is_blocked_by_kill_switch(
        self,
        worker_code: Optional[str] = None,
        department_code: Optional[str] = None,
        team_code: Optional[str] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Checks if any active kill switch applies to the execution context."""
        if f"{KillSwitchTarget.GLOBAL_WORKFORCE.value}:GLOBAL" in self._active_kill_switches:
            return True, "Global AI Workforce is suspended by active emergency kill switch."

        if department_code and f"{KillSwitchTarget.DEPARTMENT.value}:{department_code}" in self._active_kill_switches:
            return True, f"Department {department_code} is suspended by active kill switch."

        if team_code and f"{KillSwitchTarget.TEAM.value}:{team_code}" in self._active_kill_switches:
            return True, f"Team {team_code} is suspended by active kill switch."

        if worker_code and f"{KillSwitchTarget.WORKER.value}:{worker_code}" in self._active_kill_switches:
            return True, f"Worker {worker_code} is suspended by active kill switch."

        return False, None

    def release_kill_switch(self, key: str, operator_id: str) -> bool:
        if key in self._active_kill_switches:
            del self._active_kill_switches[key]
            logger.info(f"Kill switch {key} released by {operator_id}.")
            return True
        return False

    def list_active_kill_switches(self) -> List[Dict[str, Any]]:
        return list(self._active_kill_switches.values())
