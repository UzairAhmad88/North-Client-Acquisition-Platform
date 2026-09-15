"""
Control Testing & Effectiveness Engine (Section 16 & 17).
Differentiates design effectiveness from operational effectiveness.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

from backend.app.governance.base import (
    ControlHealthStatus,
    GovernanceControl,
    TestResult,
)


class ControlTestRun(BaseModel):
    test_run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    control_code: str
    test_type: str  # DESIGN_EFFECTIVENESS, OPERATING_EFFECTIVENESS
    result: TestResult
    details: str
    executed_by: str
    evidence_ids: List[str] = Field(default_factory=list)
    executed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ControlTestingEngine:
    """Executes and records design and operating effectiveness assessments for GRC controls."""

    def __init__(self):
        self._test_runs: List[ControlTestRun] = []

    def execute_test(
        self,
        control: Optional[Any] = None,
        test_type: str = "OPERATING_EFFECTIVENESS",
        result: TestResult = TestResult.PASS,
        details: str = "",
        executed_by: str = "",
        evidence_ids: Optional[List[str]] = None,
        control_code: Optional[str] = None,
    ) -> ControlTestRun:
        """Executes a formal control test and updates control health accordingly."""
        if not executed_by:
            raise ValueError("Control testing requires an accountable tester or system executor ID.")

        code = control_code
        ctrl_obj = None
        if isinstance(control, GovernanceControl):
            code = control.control_code
            ctrl_obj = control
        elif isinstance(control, str):
            code = control

        if not code:
            raise ValueError("control or control_code is required for testing.")

        run = ControlTestRun(
            control_code=code,
            test_type=str(test_type.value if hasattr(test_type, "value") else test_type),
            result=result,
            details=details,
            executed_by=executed_by,
            evidence_ids=evidence_ids or []
        )
        self._test_runs.append(run)

        # Update control operational health based on test outcome if control object provided
        if ctrl_obj is not None:
            if result == TestResult.PASS:
                ctrl_obj.health_status = ControlHealthStatus.HEALTHY
            elif result == TestResult.PARTIAL:
                ctrl_obj.health_status = ControlHealthStatus.DEGRADED
            elif result == TestResult.FAIL:
                ctrl_obj.health_status = ControlHealthStatus.FAILED

        return run

    def get_test_history(self, control_code: Optional[str] = None) -> List[ControlTestRun]:
        if control_code:
            return [r for r in self._test_runs if r.control_code == control_code]
        return list(self._test_runs)

    def get_latest_test(self, control_code: str) -> Optional[ControlTestRun]:
        history = self.get_test_history(control_code)
        if history:
            return sorted(history, key=lambda x: x.executed_at, reverse=True)[0]
        return None
