"""Independent Emergency Kill Switch & Safety Circuit-Breaker."""

from typing import Any, Dict, Optional, Set
from agents.governance.models import KillSwitchCommand


class KillSwitchEngine:
    """Independent circuit breaker providing global and granular disablement of agents, models, and tools."""

    def __init__(self):
        # In-memory fast circuit breaker state (synced with DB)
        self.global_disabled: bool = False
        self.disabled_agents: Set[str] = set()
        self.disabled_models: Set[str] = set()
        self.disabled_tools: Set[str] = set()

    def set_kill_switch(self, command: KillSwitchCommand) -> Dict[str, Any]:
        """Activate or deactivate emergency kill switch at the specified granularity."""
        level = command.level.upper()
        target = command.target_key

        if level == "GLOBAL_AI_OFF":
            self.global_disabled = command.is_active
        elif level == "AGENT_OFF":
            if command.is_active:
                self.disabled_agents.add(target)
            else:
                self.disabled_agents.discard(target)
        elif level == "MODEL_OFF":
            if command.is_active:
                self.disabled_models.add(target)
            else:
                self.disabled_models.discard(target)
        elif level == "TOOL_OFF":
            if command.is_active:
                self.disabled_tools.add(target)
            else:
                self.disabled_tools.discard(target)

        return {
            "status": "SUCCESS",
            "level": level,
            "target": target,
            "is_active": command.is_active,
            "activated_by": command.activated_by,
            "reason": command.reason,
        }

    def check_execution_allowed(
        self,
        agent_key: Optional[str] = None,
        model_key: Optional[str] = None,
        tool_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Check whether execution is permitted under current kill-switch state."""
        if self.global_disabled:
            return {
                "allowed": False,
                "reason": "Global emergency kill switch is active. All AI operations are halted.",
                "level": "GLOBAL_AI_OFF",
            }

        if agent_key and agent_key in self.disabled_agents:
            return {
                "allowed": False,
                "reason": f"Agent '{agent_key}' is emergency-disabled by kill switch.",
                "level": "AGENT_OFF",
            }

        if model_key and model_key in self.disabled_models:
            return {
                "allowed": False,
                "reason": f"Model '{model_key}' is emergency-disabled by kill switch.",
                "level": "MODEL_OFF",
            }

        if tool_name and tool_name in self.disabled_tools:
            return {
                "allowed": False,
                "reason": f"Tool '{tool_name}' is emergency-disabled by kill switch.",
                "level": "TOOL_OFF",
            }

        return {"allowed": True, "reason": "Operational"}
