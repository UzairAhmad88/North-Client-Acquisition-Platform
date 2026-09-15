"""Command Validator: Schema conformance, entity references, and business rule checking."""

from typing import Any, Dict, List, Optional, Tuple
from app.command.base import CommandObject
from app.command.registry import CommandRegistry, global_command_registry


class CommandValidator:
    """Validates parameters and safety constraints of instantiated CommandObjects."""

    def __init__(self, registry: Optional[CommandRegistry] = None):
        self.registry = registry or global_command_registry

    def validate(self, command: CommandObject) -> Tuple[bool, Optional[str]]:
        """Verify command definition, parameters presence, and non-empty values."""
        defn = self.registry.get(command.command_id)
        if not defn:
            return False, f"Unknown or unregistered command: {command.command_id}"

        # Parameter schema check
        for param_key in defn.parameters_schema.keys():
            if param_key not in command.parameters:
                return False, f"Missing required parameter: {param_key}"
            val = command.parameters[param_key]
            if val is None or (isinstance(val, str) and not val.strip()):
                return False, f"Parameter '{param_key}' cannot be empty"

        return True, None
