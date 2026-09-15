"""High-level service unifying deployment management, rollbacks, smoke tests, and feature flagging."""

from typing import Any, Dict, List, Optional

from app.operations.deployments import DeploymentManager
from app.operations.feature_flags import FeatureFlagManager
from app.operations.rollbacks import RollbackManager


class OperationsService:
    """Operations platform service for deployments, feature flags, and automated recovery actions."""

    def __init__(
        self,
        deployment_mgr: Optional[DeploymentManager] = None,
        rollback_mgr: Optional[RollbackManager] = None,
        flag_mgr: Optional[FeatureFlagManager] = None,
    ) -> None:
        self.deployment_mgr = deployment_mgr or DeploymentManager()
        self.rollback_mgr = rollback_mgr or RollbackManager()
        self.flag_mgr = flag_mgr or FeatureFlagManager()
        self._deployments: List[Dict[str, Any]] = [
            {
                "id": "dep-current-prod",
                "version": "1.43.0",
                "environment": "PRODUCTION",
                "deployed_by": "ci-cd-bot@agencyos.local",
                "git_commit_sha": "a1b2c3d4",
                "status": "HEALTHY",
                "smoke_tests_passed": True,
                "migrations_applied": True,
                "release_notes": "Phase 43: Reliability, SRE & Disaster Recovery Platform",
                "deployed_at": "2026-09-09T00:00:00Z",
            }
        ]
        self._rollbacks: List[Dict[str, Any]] = []

    def record_deployment(
        self,
        version: str,
        deployed_by: str,
        environment: str = "PRODUCTION",
        git_commit_sha: Optional[str] = None,
        release_notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        dep = self.deployment_mgr.record_deployment(
            version=version,
            deployed_by=deployed_by,
            environment=environment,
            git_commit_sha=git_commit_sha,
            release_notes=release_notes,
        )
        self._deployments.append(dep)
        return dep

    def list_deployments(self) -> List[Dict[str, Any]]:
        return self._deployments

    def evaluate_and_rollback(
        self,
        current_version: str,
        target_version: str,
        error_rate_pct: float,
        p99_latency_ms: float,
        smoke_tests_passed: bool,
        initiated_by: str,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        eval_result = self.rollback_mgr.evaluate_rollback_triggers(
            error_rate_pct=error_rate_pct,
            p99_latency_ms=p99_latency_ms,
            smoke_tests_passed=smoke_tests_passed,
        )
        if not eval_result["should_rollback"] and not reason:
            return {
                "triggered": False,
                "evaluation": eval_result,
                "message": "Metrics healthy, rollback not required.",
            }

        effective_reason = reason or "Automated trigger: " + "; ".join(eval_result["reasons"])
        rollback_result = self.rollback_mgr.execute_rollback(
            current_version=current_version,
            target_version=target_version,
            initiated_by=initiated_by,
            reason=effective_reason,
        )
        self._rollbacks.append(rollback_result)
        return {
            "triggered": True,
            "evaluation": eval_result,
            "rollback": rollback_result,
        }

    def list_rollbacks(self) -> List[Dict[str, Any]]:
        return self._rollbacks

    def evaluate_flag(
        self,
        flag_name: str,
        tenant_id: Optional[str] = None,
        tenant_tier: Optional[str] = None,
    ) -> bool:
        return self.flag_mgr.is_enabled(flag_name=flag_name, tenant_id=tenant_id, tenant_tier=tenant_tier)

    def set_flag(
        self,
        flag_name: str,
        enabled: bool,
        percentage_rollout: int = 100,
        allowed_tiers: Optional[List[str]] = None,
        tenant_whitelist: Optional[List[str]] = None,
        tenant_blacklist: Optional[List[str]] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.flag_mgr.set_flag(
            flag_name=flag_name,
            enabled=enabled,
            percentage_rollout=percentage_rollout,
            allowed_tiers=allowed_tiers,
            tenant_whitelist=tenant_whitelist,
            tenant_blacklist=tenant_blacklist,
            description=description,
        )

    def list_flags(self) -> List[Dict[str, Any]]:
        return self.flag_mgr.list_flags()
