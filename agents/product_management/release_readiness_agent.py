"""
Release Readiness & Gate Agent for Phase 56.
Evaluates deterministic release criteria, verifies test status, security reviews, and rollback readiness.
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.product_management.service import (
        ProductManagementPlatformService,
        global_product_management_service,
    )
except ImportError:
    from app.services.product_management.service import (
        ProductManagementPlatformService,
        global_product_management_service,
    )

logger = logging.getLogger(__name__)


class ReleaseReadinessAgent(BaseAgent):
    """Evaluates deterministic release gates, zero-critical-defect barriers, and launch prerequisites."""

    agent_id = "release_readiness_agent"
    name = "Release Readiness Agent"
    version = "1.0"
    description = "Enforces strict quality, QA, performance, security, and rollback readiness gating before release."
    permissions = {
        AgentPermission.READ_PRODUCT,
        AgentPermission.EVALUATE_RELEASE_READINESS,
        AgentPermission.PLAN_RELEASE,
    }

    def __init__(self, service: Optional[ProductManagementPlatformService] = None):
        super().__init__()
        self.service = service or global_product_management_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        release_id = context.metadata.get("release_id")
        product_id = context.metadata.get("product_id")

        if not release_id:
            return {"status": "FAILED", "error": "release_id is required"}

        # Perform deterministic readiness evaluation
        readiness = self.service.sprints_releases.evaluate_release_readiness(
            release_id=release_id,
            product_id=product_id,
            qa_passed=context.metadata.get("qa_passed", True),
            critical_defects=context.metadata.get("critical_defects", 0),
            security_reviewed=context.metadata.get("security_reviewed", True),
            performance_benchmarked=context.metadata.get("performance_benchmarked", True),
            rollback_tested=context.metadata.get("rollback_tested", True),
        )

        return {
            "status": "SUCCESS",
            "release_id": release_id,
            "readiness": readiness,
            "is_ready_for_approval": readiness.get("readiness_status") == "ready",
            "blocking_reasons": readiness.get("blocking_reasons", []),
        }
