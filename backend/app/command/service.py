"""Command Service Orchestrator for parsing, validating, confirming, and executing commands."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from app.command.authorization import CommandAuthorizer
from app.command.base import (
    CommandCategory,
    CommandDefinition,
    CommandExecutionStatus,
    CommandObject,
    CommandRiskLevel,
)
from app.command.executor import CommandExecutor
from app.command.parser import CommandParser
from app.command.registry import CommandRegistry, global_command_registry
from app.command.validator import CommandValidator


class GlobalCommandService:
    """Orchestrates natural-language command workflow with strict authorization and approval barriers."""

    def __init__(self, registry: Optional[CommandRegistry] = None):
        self.registry = registry or global_command_registry
        self.parser = CommandParser(self.registry)
        self.validator = CommandValidator(self.registry)
        self.authorizer = CommandAuthorizer(self.registry)
        self.executor = CommandExecutor(self.registry)

    def parse_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse natural language command into structured representation."""
        obj = self.parser.parse(text)
        if not obj:
            return None
        return self._serialize_command(obj)

    def validate_command(self, command_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate command parameters."""
        defn = self.registry.get(command_id)
        if not defn:
            return {"valid": False, "error": f"Unknown command: {command_id}"}

        obj = CommandObject(
            request_id="temp_val",
            command_id=command_id,
            category=defn.category,
            risk_level=defn.risk_level,
            parameters=parameters,
        )
        valid, err = self.validator.validate(obj)
        return {
            "valid": valid,
            "error": err,
            "requires_confirmation": defn.requires_confirmation,
            "requires_approval": defn.requires_approval,
            "risk_level": defn.risk_level.value,
        }

    def execute_command(
        self,
        command_id: str,
        parameters: Dict[str, Any],
        user_id: str,
        tenant_id: str,
        user_permissions: Optional[Set[str]] = None,
        is_client: bool = False,
        has_confirmation: bool = False,
        has_approval: bool = False,
    ) -> Dict[str, Any]:
        """Validate, authorize, and execute command."""
        defn = self.registry.get(command_id)
        if not defn:
            raise ValueError(f"Unregistered command: {command_id}")

        obj = CommandObject(
            request_id=f"cmd_{datetime.now(timezone.utc).timestamp()}",
            command_id=command_id,
            category=defn.category,
            risk_level=defn.risk_level,
            parameters=parameters,
            requires_confirmation=defn.requires_confirmation,
            requires_approval=defn.requires_approval,
        )

        # 1. Validation
        valid, err = self.validator.validate(obj)
        if not valid:
            obj.status = CommandExecutionStatus.FAILED
            obj.error = err
            return self._serialize_command(obj)

        # 2. Authorization
        authorized = self.authorizer.is_authorized(
            command=obj,
            user_id=user_id,
            tenant_id=tenant_id,
            user_permissions=user_permissions,
            is_client=is_client,
        )
        if not authorized:
            obj.status = CommandExecutionStatus.BLOCKED
            obj.error = "Permission denied: principal is not authorized for this command"
            return self._serialize_command(obj)

        # 3. Execution
        executed = self.executor.execute(
            command=obj,
            has_user_confirmation=has_confirmation,
            has_human_approval=has_approval,
            approval_actor_id=user_id if has_approval else None,
        )

        return self._serialize_command(executed)

    def list_registered_commands(self) -> List[Dict[str, Any]]:
        """Return list of all registered commands with metadata."""
        return [
            {
                "command_id": c.command_id,
                "name": c.name,
                "description": c.description,
                "category": c.category.value,
                "risk_level": c.risk_level.value,
                "requires_confirmation": c.requires_confirmation,
                "requires_approval": c.requires_approval,
                "parameters_schema": c.parameters_schema,
            }
            for c in self.registry.list_commands()
        ]

    @staticmethod
    def _serialize_command(obj: CommandObject) -> Dict[str, Any]:
        return {
            "request_id": obj.request_id,
            "command_id": obj.command_id,
            "category": obj.category.value,
            "risk_level": obj.risk_level.value,
            "parameters": obj.parameters,
            "status": obj.status.value,
            "requires_confirmation": obj.requires_confirmation,
            "requires_approval": obj.requires_approval,
            "approval_reason": obj.approval_reason,
            "execution_result": obj.execution_result,
            "error": obj.error,
            "created_at": obj.created_at.isoformat(),
        }
