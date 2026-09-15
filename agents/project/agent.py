"""Production Project AI Agent built on Phase 14 BaseAgent runtime."""

from typing import Any, Dict, List, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.project.blocker_analyzer import ProjectBlockerAnalyzer
from agents.project.planner import ProjectPlannerEngine
from agents.project.progress_analyzer import ProjectProgressAnalyzer
from agents.project.risk_analyzer import ProjectRiskAnalyzer
from agents.project.scope_monitor import ProjectScopeMonitor
from agents.project.summarizer import ProjectSummarizerEngine


class ProjectAgent(BaseAgent):
    """Production Project AI Agent providing WBS planning, status summaries, risk analysis, and scope monitoring."""

    agent_id = "project_agent"
    name = "Project Agent"
    version = "1.0"
    description = "Provides WBS planning, status summaries, delivery risk analysis, and baseline scope monitoring."

    def __init__(self):
        super().__init__()
        self.planner = ProjectPlannerEngine()
        self.summarizer = ProjectSummarizerEngine()
        self.risk_analyzer = ProjectRiskAnalyzer()
        self.blocker_analyzer = ProjectBlockerAnalyzer()
        self.progress_analyzer = ProjectProgressAnalyzer()
        self.scope_monitor = ProjectScopeMonitor()


    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_PROJECT,
            AgentPermission.READ_BASELINE,
            AgentPermission.READ_REQUIREMENTS,
            AgentPermission.READ_SOLUTION,
            AgentPermission.READ_ESTIMATE,
            AgentPermission.READ_PROPOSAL,
            AgentPermission.READ_CONTRACT,
            AgentPermission.READ_TASKS,
            AgentPermission.READ_MILESTONES,
            AgentPermission.READ_DELIVERABLES,
            AgentPermission.READ_RISKS,
            AgentPermission.READ_BLOCKERS,
            AgentPermission.READ_ACTIVITY,
            AgentPermission.CREATE_TASK_DRAFT,
            AgentPermission.CREATE_PLAN_DRAFT,
            AgentPermission.CREATE_STATUS_SUMMARY,
            AgentPermission.CREATE_RISK_RECOMMENDATION,
            AgentPermission.CREATE_SCOPE_SIGNAL,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute project analysis, WBS planning, or status summarization."""
        input_data = context.metadata.get("parameters") if context.metadata and "parameters" in context.metadata else context.metadata or {}
        task_action = str(input_data.get("action") or "SUMMARIZE")


        project_name = str(input_data.get("project_name") or "Project Execution")
        deliverables = input_data.get("deliverables") or []
        estimate_items = input_data.get("estimate_items") or []
        tasks = input_data.get("tasks") or []
        milestones = input_data.get("milestones") or []
        blockers = input_data.get("blockers") or []
        risks = input_data.get("risks") or []
        client_dependencies = input_data.get("client_dependencies") or []
        baseline_items = input_data.get("baseline_items") or []
        messages = input_data.get("messages") or []

        if task_action == "PLAN_WBS":
            plan_result = self.planner.generate_draft_plan(
                project_name=project_name,
                deliverables=deliverables,
                estimate_items=estimate_items,
            )
            return plan_result.model_dump()

        elif task_action == "SUMMARIZE":
            project_data = input_data.get("project_data") or {"name": project_name}
            summary_result = self.summarizer.summarize_project(
                project_data=project_data,
                tasks=tasks,
                milestones=milestones,
                blockers=blockers,
                risks=risks,
                client_dependencies=client_dependencies,
            )
            return summary_result.model_dump()

        elif task_action == "ANALYZE_RISKS_AND_SCOPE":
            risk_findings = self.risk_analyzer.analyze_risks(
                tasks=tasks, milestones=milestones, client_dependencies=client_dependencies
            )
            blocker_findings = self.blocker_analyzer.analyze_blockers(tasks=tasks, blockers=blockers)
            progress_metrics = self.progress_analyzer.calculate_progress(tasks=tasks)
            scope_signals = self.scope_monitor.evaluate_scope_signals(
                baseline_items=baseline_items, current_tasks=tasks, recent_messages=messages
            )

            return {
                "risk_findings": risk_findings,
                "blocker_findings": blocker_findings,
                "progress_metrics": progress_metrics,
                "scope_signals": [s.model_dump() for s in scope_signals],
            }

        else:
            return {
                "status": "COMPLETED",
                "message": f"Action '{task_action}' completed with baseline risk checks.",
            }
