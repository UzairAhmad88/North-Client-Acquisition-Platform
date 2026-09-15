"""Central Agent Registry Singleton."""

from typing import Any, Dict, List, Optional

from agents.core.base import BaseAgent
from agents.core.errors import AgentDisabledError, AgentNotFoundError
from agents.core.permissions import validate_agent_permissions


class AgentRegistry:
    """Central registry managing registered agents, specifications, and permissions."""

    def __init__(self) -> None:
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """Register an agent instance."""
        if agent.name in self._agents:
            raise ValueError(f"Agent with name '{agent.name}' is already registered.")

        # Validate permissions
        validate_agent_permissions(agent.permissions)
        self._agents[agent.name] = agent

    def get(self, name: str) -> BaseAgent:
        """Fetch registered agent by name."""
        if name not in self._agents:
            raise AgentNotFoundError(f"Agent '{name}' is not registered in runtime.")

        agent = self._agents[name]
        if not agent.enabled:
            raise AgentDisabledError(f"Agent '{name}' is currently disabled.")

        return agent

    def list_agents(self) -> List[Dict[str, Any]]:
        """Return specifications for all registered agents."""
        specs: List[Dict[str, Any]] = []
        for name, agent in self._agents.items():
            specs.append(
                {
                    "name": agent.name,
                    "version": agent.version,
                    "description": agent.description,
                    "enabled": agent.enabled,
                    "permissions": sorted(list(agent.permissions)),
                    "max_steps": agent.max_steps,
                    "max_tool_calls": agent.max_tool_calls,
                    "max_runtime_seconds": agent.max_runtime_seconds,
                }
            )
        return specs

    def set_enabled(self, name: str, enabled: bool) -> None:
        """Enable or disable an agent at runtime."""
        if name not in self._agents:
            raise AgentNotFoundError(f"Agent '{name}' is not registered.")
        self._agents[name].enabled = enabled


# Global Registry Singleton Instance
global_registry = AgentRegistry()
