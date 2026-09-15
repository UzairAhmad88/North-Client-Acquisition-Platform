"""Workflow Graph Executor."""

import os
from typing import Dict, List, Optional, Tuple

from agents.core.errors import AgentExecutionFailedError, AgentPermissionDeniedError
from agents.core.state import AgentState, validate_state_transition
from agents.orchestrator.nodes import ApprovalNode, EndNode, StartNode, WorkflowNode
from agents.orchestrator.transitions import FailureType, TransitionPolicy


class WorkflowGraph:
    """Graph workflow executor driving node transitions."""

    def __init__(self, workflow_id: str) -> None:
        self.workflow_id = workflow_id
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, str] = {}

        # Register default start/end nodes
        self.add_node(StartNode())
        self.add_node(EndNode())
        self.add_node(ApprovalNode())

    def add_node(self, node: WorkflowNode) -> None:
        self.nodes[node.name] = node

    def add_edge(self, from_node: str, to_node: str) -> None:
        self.edges[from_node] = to_node

    async def execute_graph(
        self,
        initial_state: AgentState,
        start_node_name: str = "START",
    ) -> Tuple[AgentState, str]:
        """Execute workflow graph sequentially until completion or approval boundary.

        Returns:
            Tuple of (updated_state, final_status)
        """
        # Global Kill Switch Check
        if os.getenv("AGENTS_ENABLED", "true").lower() not in ("true", "1", "yes"):
            raise AgentPermissionDeniedError("Global agent execution kill switch is ACTIVE (AGENTS_ENABLED=false).")

        current_node_name = start_node_name
        state = initial_state
        state["workflow_id"] = self.workflow_id
        status = "RUNNING"

        max_steps = 20
        step = 0

        while current_node_name and step < max_steps:
            step += 1
            node = self.nodes.get(current_node_name)
            if not node:
                raise AgentExecutionFailedError(f"Node '{current_node_name}' not found in workflow graph.")

            if node.name == "APPROVAL":
                state = await node.execute(state)
                status = "WAITING_FOR_APPROVAL"
                return state, status

            if node.name == "END":
                state = await node.execute(state)
                status = "COMPLETED"
                return state, status

            try:
                state = await node.execute(state)
            except Exception as e:
                failure_type = TransitionPolicy.classify_failure(e)
                state["errors"] = state.get("errors", []) + [f"Error in node {node.name}: {str(e)}"]
                return state, "FAILED"

            current_node_name = self.edges.get(current_node_name, "END")

        return state, "COMPLETED"
