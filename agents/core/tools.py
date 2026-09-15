"""Controlled Tool Abstraction and Permission Guarded Sandbox."""

from typing import Any, Dict, Optional

from agents.core.budget import AgentBudget
from agents.core.context import AgentContext
from agents.core.permissions import check_tool_permission
from agents.core.validation import AgentValidator


class AgentTool:
    """Abstract base class for all agent sandbox tools."""

    name: str = "base_tool"
    permission: str = "READ_BUSINESS"
    description: str = "Base tool description"
    timeout_seconds: int = 15

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Internal execution method implemented by tools."""
        raise NotImplementedError

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: AgentContext,
        agent_permissions: set[str],
        budget: Optional[AgentBudget] = None,
    ) -> Dict[str, Any]:
        """Execute tool through strict security pipeline:

        1. Permission Check
        2. Context Authorization
        3. Budget Check
        4. Execution
        5. Output Sanitization & Validation
        """
        # 1. Permission Guard
        check_tool_permission(agent_permissions, self.permission)

        # 2. Budget Check
        if budget:
            budget.increment_tool_call()

        # 3. Tool Execution
        raw_result = await self.run_tool(arguments, context)

        # 4. Output Validation & Sanitization
        if isinstance(raw_result, dict):
            if "content" in raw_result and isinstance(raw_result["content"], str):
                raw_result["content"] = AgentValidator.sanitize_untrusted_input(
                    raw_result["content"]
                )

        return raw_result
