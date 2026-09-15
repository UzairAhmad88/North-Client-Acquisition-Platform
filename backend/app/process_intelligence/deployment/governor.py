"""
Controlled Deployment Governor for Phase 49: Manages canary rollouts, health gates, and safe rollbacks.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.process_intelligence.base import DeploymentStrategy, ProcessHealthStatus
except ImportError:
    from app.process_intelligence.base import DeploymentStrategy, ProcessHealthStatus


class ControlledDeploymentGovernor:
    """Oversees safe workflow optimization rollout with canary metrics, health checks, and rollback history."""

    def __init__(self):
        self._deployments: Dict[str, Dict[str, Any]] = {}

    def initiate_deployment(
        self,
        process_id: str,
        target_version: int,
        strategy: DeploymentStrategy = DeploymentStrategy.CANARY,
        rollout_percentage: int = 10,
        proposal_id: Optional[str] = None,
        approved_by: str = "security_and_governance_board",
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """Launches a controlled workflow version deployment."""
        deployment_code = f"DEP-{strategy.value[:3]}-{uuid.uuid4().hex[:6].upper()}"

        deployment = {
            "id": str(uuid.uuid4()),
            "tenant_id": tenant_id,
            "deployment_code": deployment_code,
            "process_id": process_id,
            "proposal_id": proposal_id,
            "strategy": strategy.value,
            "rollout_percentage": rollout_percentage,
            "target_version": target_version,
            "approved_by": approved_by,
            "approved_at": datetime.now(timezone.utc).isoformat(),
            "status": "ACTIVE",
            "health_status": ProcessHealthStatus.HEALTHY.value,
            "canary_metrics": {
                "cases_routed_to_canary": 0,
                "canary_error_rate": 0.0,
                "canary_cycle_time_seconds": 0.0,
                "canary_rollback_triggered": False,
            },
        }

        self._deployments[deployment_code] = deployment
        return deployment

    def record_canary_telemetry(
        self,
        deployment_code: str,
        cases_routed: int,
        error_rate: float,
        cycle_time_seconds: float,
        tenant_id: str = "default_tenant",
    ) -> Optional[Dict[str, Any]]:
        """Updates live canary performance metrics and trips safety gates if error rate degrades."""
        dep = self._deployments.get(deployment_code)
        if not dep or dep["tenant_id"] != tenant_id:
            return None

        dep["canary_metrics"]["cases_routed_to_canary"] = cases_routed
        dep["canary_metrics"]["canary_error_rate"] = round(error_rate, 4)
        dep["canary_metrics"]["canary_cycle_time_seconds"] = round(cycle_time_seconds, 2)

        # Health gating check
        if error_rate > 0.05:  # > 5% error trips degraded state
            dep["health_status"] = ProcessHealthStatus.DEGRADED.value
        if error_rate > 0.15:  # > 15% error trips critical state
            dep["health_status"] = ProcessHealthStatus.CRITICAL.value

        return dep

    def rollback_deployment(
        self,
        deployment_code: str,
        reason: str,
        operator_id: str,
        tenant_id: str = "default_tenant",
    ) -> Optional[Dict[str, Any]]:
        """Executes an instant rollback to the previous version without overwriting history."""
        dep = self._deployments.get(deployment_code)
        if not dep or dep["tenant_id"] != tenant_id:
            return None

        dep["status"] = "ROLLED_BACK"
        dep["health_status"] = ProcessHealthStatus.HEALTHY.value
        dep["canary_metrics"]["canary_rollback_triggered"] = True
        dep["rollback_metadata"] = {
            "rolled_back_at": datetime.now(timezone.utc).isoformat(),
            "rolled_back_by": operator_id,
            "rollback_reason": reason,
            "new_immutable_state_version": dep["target_version"] + 1,  # rollback creates new version
        }
        return dep

    def promote_to_full(
        self,
        deployment_code: str,
        promoted_by: str,
        tenant_id: str = "default_tenant",
    ) -> Optional[Dict[str, Any]]:
        """Promotes a healthy canary deployment to 100% full production rollout."""
        dep = self._deployments.get(deployment_code)
        if not dep or dep["tenant_id"] != tenant_id:
            return None

        if dep["health_status"] in (ProcessHealthStatus.CRITICAL.value, ProcessHealthStatus.DEGRADED.value):
            return None  # blocked by health gate

        dep["rollout_percentage"] = 100
        dep["status"] = "PROMOTED_TO_FULL"
        dep["promoted_at"] = datetime.now(timezone.utc).isoformat()
        dep["promoted_by"] = promoted_by
        return dep
