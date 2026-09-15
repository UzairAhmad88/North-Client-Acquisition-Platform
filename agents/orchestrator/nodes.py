"""Workflow Node Interface and Standard Core Nodes."""

from typing import Any, Dict
from agents.core.state import AgentState


class WorkflowNode:
    """Interface for graph workflow nodes."""

    name: str = "base_node"

    async def execute(self, state: AgentState) -> AgentState:
        """Execute node logic and return updated state."""
        raise NotImplementedError


class StartNode(WorkflowNode):
    name: str = "START"

    async def execute(self, state: AgentState) -> AgentState:
        state["approval_status"] = "NOT_REQUIRED"
        return state


class ApprovalNode(WorkflowNode):
    name: str = "APPROVAL"

    async def execute(self, state: AgentState) -> AgentState:
        state["approval_status"] = "WAITING_FOR_APPROVAL"
        return state


class EndNode(WorkflowNode):
    name: str = "END"

    async def execute(self, state: AgentState) -> AgentState:
        return state
