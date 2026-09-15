"""Command Executor: Safely executes commands enforcing approval and confirmation gates."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from app.command.base import (
    CommandCategory,
    CommandExecutionStatus,
    CommandObject,
    CommandRiskLevel,
)
from app.command.registry import CommandRegistry, global_command_registry


class CommandExecutor:
    """Executes validated and authorized commands with human approval gating."""

    def __init__(self, registry: Optional[CommandRegistry] = None):
        self.registry = registry or global_command_registry

    def execute(
        self,
        command: CommandObject,
        has_user_confirmation: bool = False,
        has_human_approval: bool = False,
        approval_actor_id: Optional[str] = None,
    ) -> CommandObject:
        """Execute command or flag required gates."""
        defn = self.registry.get(command.command_id)
        if not defn:
            command.status = CommandExecutionStatus.BLOCKED
            command.error = "Unregistered command"
            return command

        # 1. Enforce Approval Gate for Sensitive Actions
        if defn.requires_approval and not has_human_approval:
            command.status = CommandExecutionStatus.APPROVAL_REQUIRED
            command.approval_reason = (
                f"Command '{defn.name}' carries {defn.risk_level.value} risk and requires explicit human approval."
            )
            return command

        # 2. Enforce Confirmation Gate
        if defn.requires_confirmation and not has_user_confirmation and not has_human_approval:
            command.status = CommandExecutionStatus.CONFIRMATION_REQUIRED
            return command

        # 3. Simulate / Dispatch Safe Execution
        try:
            result = self._dispatch_handler(command)
            command.status = CommandExecutionStatus.EXECUTED
            command.execution_result = result
        except Exception as ex:
            command.status = CommandExecutionStatus.FAILED
            command.error = str(ex)

        return command

    def _dispatch_handler(self, command: CommandObject) -> Dict[str, Any]:
        """Dispatch execution to appropriate domain subsystem."""
        cid = command.command_id
        params = command.parameters

        if cid == "NAV_LEADS":
            return {"action": "REDIRECT", "url": "/leads"}
        elif cid == "NAV_PROJECTS":
            return {"action": "REDIRECT", "url": "/projects"}
        elif cid == "NAV_INBOX":
            return {"action": "REDIRECT", "url": "/inbox"}
        elif cid == "NAV_APPROVALS":
            return {"action": "REDIRECT", "url": "/approvals"}
        elif cid == "QUERY_LEADS":
            return {"action": "SEARCH", "entity": "LEAD", "status": params.get("status")}
        elif cid == "QUERY_PROJECTS_AT_RISK":
            return {"action": "SEARCH", "entity": "PROJECT", "status": params.get("status")}
        elif cid == "CREATE_TASK":
            return {
                "action": "CREATED",
                "entity": "TASK",
                "title": params.get("title"),
                "project_id": params.get("project_id"),
                "task_id": "task_sim_001",
            }
        elif cid == "SEND_PROPOSAL":
            return {
                "action": "DISPATCHED",
                "entity": "PROPOSAL",
                "proposal_id": params.get("proposal_id"),
                "recipient_id": params.get("recipient_id"),
                "guard_status": "APPROVED",
            }
        elif cid == "APPROVE_CONTRACT":
            return {
                "action": "SIGNED_OFF",
                "entity": "CONTRACT",
                "contract_id": params.get("contract_id"),
                "status": "APPROVED",
            }
        elif cid == "RETRY_WORKFLOW":
            return {
                "action": "REPLAYED",
                "entity": "WORKFLOW",
                "workflow_id": params.get("workflow_id"),
                "state": "RUNNING",
            }

        return {"status": "SUCCESS", "message": f"Command {cid} completed"}
