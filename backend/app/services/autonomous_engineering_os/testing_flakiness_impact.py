"""Phase 64 — Testing Platform, Flakiness & Test Impact Analysis Service."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.services.autonomous_engineering_os.base import (
    BaseAutonomousEngineeringOsService,
    AttrDict,
    TestSuiteModel,
)


class TestingFlakinessImpactService(BaseAutonomousEngineeringOsService):
    """Service managing test suites, flakiness detection, and test impact analysis."""

    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)
        self._suites: Dict[str, Any] = {}

    def register_test_suite(
        self,
        tenant_id: str,
        repository_id: str,
        suite_name: str,
        suite_type: str = "UNIT",
        total_tests: int = 150,
        passed_tests: int = 150,
        failed_tests: int = 0,
        flaky_rate_pct: float = 0.0,
        duration_seconds: float = 14.2,
    ) -> Any:
        """Register automated test suite run."""
        suite_id = self.generate_id("eng_test")
        now = datetime.utcnow()

        if self.db is not None and TestSuiteModel is not None:
            suite = TestSuiteModel(
                id=suite_id,
                tenant_id=tenant_id,
                repository_id=repository_id,
                suite_name=suite_name,
                suite_type=suite_type,
                total_tests_count=total_tests,
                passed_tests_count=passed_tests,
                failed_tests_count=failed_tests,
                flaky_rate_pct=flaky_rate_pct,
                duration_seconds=duration_seconds,
                last_run_at=now,
            )
            self.db.add(suite)
            self.db.commit()
            self.db.refresh(suite)
            return suite
        else:
            suite = AttrDict({
                "id": suite_id,
                "tenant_id": tenant_id,
                "repository_id": repository_id,
                "suite_name": suite_name,
                "suite_type": suite_type,
                "total_tests_count": total_tests,
                "passed_tests_count": passed_tests,
                "failed_tests_count": failed_tests,
                "flaky_rate_pct": flaky_rate_pct,
                "duration_seconds": duration_seconds,
                "last_run_at": now,
            })
            self._suites[suite_id] = suite
            return suite

    def list_test_suites(
        self,
        tenant_id: str,
        repository_id: Optional[str] = None,
    ) -> List[Any]:
        """List test suites."""
        if self.db is not None and TestSuiteModel is not None:
            q = self.db.query(TestSuiteModel).filter(TestSuiteModel.tenant_id == tenant_id)
            if repository_id:
                q = q.filter(TestSuiteModel.repository_id == repository_id)
            return q.all()
        results = [s for s in self._suites.values() if s.tenant_id == tenant_id]
        if repository_id:
            results = [s for s in results if s.repository_id == repository_id]
        return results

    def run_test_impact_analysis(
        self,
        tenant_id: str,
        repository_id: str,
        changed_files: List[str],
    ) -> Dict[str, Any]:
        """Determine smallest safe test subset based on code modifications."""
        suites = self.list_test_suites(tenant_id, repository_id)
        targeted_suites = []
        for s in suites:
            if any("service" in f for f in changed_files) or s.suite_type == "UNIT":
                targeted_suites.append({
                    "suite_id": s.id,
                    "suite_name": s.suite_name,
                    "type": s.suite_type,
                    "tests_count": s.total_tests_count,
                    "estimated_duration_seconds": s.duration_seconds,
                })

        return {
            "repository_id": repository_id,
            "changed_files_count": len(changed_files),
            "changed_files": changed_files,
            "selected_test_suites": targeted_suites,
            "estimated_test_time_savings_pct": 65.0 if len(targeted_suites) < len(suites) else 0.0,
            "analyzed_at": datetime.utcnow().isoformat(),
        }
