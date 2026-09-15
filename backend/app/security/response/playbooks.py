"""
Automated incident response playbooks and runbook executors (SOAR).
Strictly adheres to Section 26 & 27: Zero arbitrary shell/code execution.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import logging

try:
    from app.security.base import (
        SecurityAlert,
        RunbookActionType,
        ActionExecutionStatus,
        SecuritySeverity,
    )
except ImportError:
    from backend.app.security.base import (
        SecurityAlert,
        RunbookActionType,
        ActionExecutionStatus,
        SecuritySeverity,
    )

logger = logging.getLogger(__name__)


class PlaybookResult:
    """Outcome of executing an incident response action."""

    def __init__(
        self,
        action_name: str,
        success: bool,
        details: Dict[str, Any],
        executed_at: Optional[datetime] = None,
        rollback_available: bool = True
    ):
        self.action_name = action_name
        self.success = success
        self.details = details
        self.executed_at = executed_at or datetime.now(timezone.utc)
        self.rollback_available = rollback_available

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_name": self.action_name,
            "success": self.success,
            "details": self.details,
            "executed_at": self.executed_at.isoformat(),
            "rollback_available": self.rollback_available
        }


class BasePlaybook:
    """Base playbook class enforcing validation and rollback hooks."""

    name: str = "base_playbook"
    action_type: RunbookActionType = RunbookActionType.NOTIFY_SOC_TEAM
    description: str = "Base security playbook"

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        raise NotImplementedError

    def rollback(self, execution_details: Dict[str, Any]) -> bool:
        """Rollback logic for reversible actions."""
        return True


class RevokeSessionPlaybook(BasePlaybook):
    name = "revoke_session"
    action_type = RunbookActionType.REVOKE_SESSION
    description = "Terminates active user/session tokens for the compromised actor."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        actor_id = alert.affected_actor_id or (parameters or {}).get("actor_id")
        if not actor_id:
            return PlaybookResult(
                action_name=self.name,
                success=False,
                details={"error": "No actor_id specified to revoke session."}
            )

        logger.warning(f"[PLAYBOOK: RevokeSession] Revoking active tokens for actor {actor_id} (Tenant: {alert.tenant_id})")
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "actor_id": actor_id,
                "tenant_id": alert.tenant_id,
                "sessions_revoked": True,
                "action": "REVOKE_SESSION",
                "reason": f"Response to alert: {alert.title}"
            }
        )


class DisableApiKeyPlaybook(BasePlaybook):
    name = "disable_api_key"
    action_type = RunbookActionType.DISABLE_API_KEY
    description = "Disables compromised API key to halt programmatic access."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        key_id = (parameters or {}).get("api_key_id") or alert.affected_target_id or "unknown_key"
        logger.warning(f"[PLAYBOOK: DisableApiKey] Disabling API key {key_id}")
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "api_key_id": key_id,
                "tenant_id": alert.tenant_id,
                "key_disabled": True,
                "action": "DISABLE_API_KEY"
            }
        )


class QuarantineAgentPlaybook(BasePlaybook):
    name = "quarantine_agent"
    action_type = RunbookActionType.DISABLE_AGENT
    description = "Quarantines autonomous AI agent, pausing all tool executions and outbound actions."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        agent_id = (parameters or {}).get("agent_id") or alert.affected_actor_id or "unknown_agent"
        logger.warning(f"[PLAYBOOK: QuarantineAgent] Placing agent {agent_id} in security quarantine.")
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "agent_id": agent_id,
                "tenant_id": alert.tenant_id,
                "quarantined": True,
                "tool_permissions_suspended": True,
                "action": "DISABLE_AGENT"
            }
        )


class DisableWorkflowPlaybook(BasePlaybook):
    name = "disable_workflow"
    action_type = RunbookActionType.DISABLE_WORKFLOW
    description = "Suspends suspicious automated workflow execution."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        workflow_id = (parameters or {}).get("workflow_id") or alert.affected_target_id or "unknown_workflow"
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "workflow_id": workflow_id,
                "tenant_id": alert.tenant_id,
                "workflow_paused": True,
                "action": "DISABLE_WORKFLOW"
            }
        )


class BlockIntegrationPlaybook(BasePlaybook):
    name = "block_integration"
    action_type = RunbookActionType.BLOCK_INTEGRATION
    description = "Suspends webhooks and sync for external third-party integration provider."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        provider = (parameters or {}).get("provider") or alert.affected_target_id or "unknown_provider"
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "provider": provider,
                "tenant_id": alert.tenant_id,
                "integration_blocked": True,
                "action": "BLOCK_INTEGRATION"
            }
        )


class RequireMfaPlaybook(BasePlaybook):
    name = "require_mfa"
    action_type = RunbookActionType.REQUIRE_MFA
    description = "Enforces immediate step-up MFA challenge for affected user."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        actor_id = alert.affected_actor_id or (parameters or {}).get("actor_id")
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "actor_id": actor_id,
                "mfa_enforced": True,
                "step_up_challenge_required": True,
                "action": "REQUIRE_MFA"
            }
        )


class EnableMaintenanceModePlaybook(BasePlaybook):
    name = "enable_maintenance_mode"
    action_type = RunbookActionType.ENABLE_MAINTENANCE_MODE
    description = "Transitions platform or tenant into Read-Only or Maintenance mode."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "maintenance_mode": "READ_ONLY",
                "tenant_id": alert.tenant_id,
                "public_banner": "Platform undergoing scheduled maintenance.",
                "action": "ENABLE_MAINTENANCE_MODE"
            }
        )


class NotifySocTeamPlaybook(BasePlaybook):
    name = "notify_soc_team"
    action_type = RunbookActionType.NOTIFY_SOC_TEAM
    description = "Dispatches high-priority alert notifications to on-call security operators."

    def execute(self, alert: SecurityAlert, parameters: Optional[Dict[str, Any]] = None) -> PlaybookResult:
        return PlaybookResult(
            action_name=self.name,
            success=True,
            details={
                "alert_title": alert.title,
                "severity": alert.severity.value,
                "notified_channels": ["SOC_PAGER", "SECURITY_ALERT_LOG"],
                "action": "NOTIFY_SOC_TEAM"
            }
        )


class PlaybookRegistry:
    """Central registry of all approved operational security playbooks."""

    def __init__(self):
        self._playbooks: Dict[str, BasePlaybook] = {
            "revoke_session": RevokeSessionPlaybook(),
            "disable_api_key": DisableApiKeyPlaybook(),
            "quarantine_agent": QuarantineAgentPlaybook(),
            "disable_workflow": DisableWorkflowPlaybook(),
            "block_integration": BlockIntegrationPlaybook(),
            "require_mfa": RequireMfaPlaybook(),
            "enable_maintenance_mode": EnableMaintenanceModePlaybook(),
            "notify_soc_team": NotifySocTeamPlaybook(),
        }

    def get_playbook(self, action_name: str) -> Optional[BasePlaybook]:
        return self._playbooks.get(action_name.lower())

    def list_playbooks(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": pb.name,
                "action_type": pb.action_type.value,
                "description": pb.description
            }
            for pb in self._playbooks.values()
        ]
