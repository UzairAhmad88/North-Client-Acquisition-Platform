"""Command Authorization: Default-deny verification of principal permissions."""

from typing import List, Optional, Set
from app.command.base import CommandCategory, CommandDefinition, CommandObject
from app.command.registry import CommandRegistry, global_command_registry


class CommandAuthorizer:
    """Enforces permissions and role controls with default-deny semantics."""

    def __init__(self, registry: Optional[CommandRegistry] = None):
        self.registry = registry or global_command_registry

    def is_authorized(
        self,
        command: CommandObject,
        user_id: str,
        tenant_id: str,
        user_permissions: Optional[Set[str]] = None,
        is_client: bool = False,
    ) -> bool:
        """Check if the user is permitted to invoke the command."""
        defn = self.registry.get(command.command_id)
        if not defn:
            return False

        # Client boundary: Client accounts cannot invoke sensitive actions or create tasks
        if is_client and defn.category in (CommandCategory.SAFE_CREATE, CommandCategory.SENSITIVE_ACTION):
            return False

        # Navigation and simple Query commands are permitted for authenticated users
        if defn.category in (CommandCategory.NAVIGATION, CommandCategory.QUERY):
            return True

        # Check required explicit permission
        if defn.required_permission:
            if not user_permissions or defn.required_permission not in user_permissions:
                return False

        return True
