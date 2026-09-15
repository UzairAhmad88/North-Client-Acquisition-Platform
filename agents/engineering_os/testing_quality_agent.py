"""Testing & Flaky Test Quarantine Agent for Phase 61."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.engineering_os.service import EngineeringOperatingSystemService
except ImportError:
    from app.services.engineering_os.service import EngineeringOperatingSystemService

logger = logging.getLogger(__name__)


class TestingQualityAgent(BaseAgent):
    """Monitors test suite stability, identifies flaky tests, and records performance benchmarks."""

    __test__ = False
    agent_id = "testing_quality_agent"
    name = "Testing & Quality Agent"

    version = "1.0"
    description = "Tracks test pass rates, detects intermittent flaky tests, and monitors p99 latency regressions."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
        AgentPermission.MANAGE_ENGINEERING_TESTS,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        test_id = context.metadata.get("test_identifier", "tests.test_kafka_sync")

        flaky = self.service.testing_service.detect_flaky_test(
            tenant_id=tenant_id,
            test_identifier=test_id,
            execution_count=50,
            flip_count=context.metadata.get("flip_count", 4),
        )

        return {
            "status": "COMPLETED",
            "test_identifier": test_id,
            "flakiness_pct": flaky.flakiness_pct,
            "is_quarantined": flaky.is_quarantined,
            "recommendation": flaky.recommendation,
        }
