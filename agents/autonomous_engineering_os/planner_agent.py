"""Phase 64 — Engineering Requirements & Task Planner Agent."""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent, AgentResult
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission


class EngineeringPlannerAgent(BaseAgent):
    """Decomposes requirements and user stories into atomic engineering tasks."""

    name: str = "engineering_planner_agent"
    version: str = "1.0.0"
    description: str = "Decomposes product requirements into structured technical tasks."
    permissions: Set[str] = {
        AgentPermission.READ_AUTONOMOUS_ENGINEERING_OS,
        AgentPermission.MANAGE_ENGINEERING_REQUIREMENTS,
        AgentPermission.PLAN_ENGINEERING_TASKS,
    }

    async def run(self, context: AgentContext) -> AgentResult:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        requirement_title = context.metadata.get("requirement_title", "User Auth & Token Verification")
        complexity = context.metadata.get("complexity", "MEDIUM")

        tasks = [
            {"title": f"Database Model: {requirement_title}", "type": "SCHEMA", "agent": "coding_agent"},
            {"title": f"Service Implementation: {requirement_title}", "type": "SERVICE", "agent": "coding_agent"},
            {"title": f"Acceptance & Unit Tests: {requirement_title}", "type": "TEST", "agent": "testing_agent"},
        ]

        return AgentResult(
            status="completed",
            result={
                "requirement_title": requirement_title,
                "complexity": complexity,
                "decomposed_tasks_count": len(tasks),
                "tasks": tasks,
            },
            confidence="HIGH",
            evidence=[{"step": "Requirement decomposition via BDD rules", "tenant_id": tenant_id}],
        )
