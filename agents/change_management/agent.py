"""Production Change Management AI Agent built on Phase 14 BaseAgent runtime."""

from typing import Any, Dict, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.change_management.classifier import ChangeClassifier
from agents.change_management.impact_analyzer import ChangeImpactAnalyzer
from agents.change_management.scope_analyzer import ChangeScopeAnalyzer
from agents.change_management.effort_analyzer import ChangeEffortAnalyzer
from agents.change_management.commercial_analyzer import ChangeCommercialAnalyzer
from agents.change_management.contract_analyzer import ChangeContractAnalyzer
from agents.change_management.summary import ChangeSummaryEngine


class ChangeAgent(BaseAgent):
    """Production Change Management AI Agent providing triage, impact analysis, PERT re-estimation, commercial calculation, and proposal summarization."""

    agent_id = "change_agent"
    name = "Change Management Agent"
    version = "1.0"
    description = "Classifies change requests, analyzes multi-dimensional scope impact, re-estimates effort, calculates commercial deltas, and prepares change summaries."

    def __init__(self):
        super().__init__()
        self.classifier = ChangeClassifier()
        self.impact_analyzer = ChangeImpactAnalyzer()
        self.scope_analyzer = ChangeScopeAnalyzer()
        self.effort_analyzer = ChangeEffortAnalyzer()
        self.commercial_analyzer = ChangeCommercialAnalyzer()
        self.contract_analyzer = ChangeContractAnalyzer()
        self.summary_engine = ChangeSummaryEngine()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_PROJECT,
            AgentPermission.READ_BASELINE,
            AgentPermission.READ_CONTRACT,
            AgentPermission.READ_ESTIMATE,
            AgentPermission.READ_REQUIREMENTS,
            AgentPermission.READ_SOLUTION,
            AgentPermission.READ_CLIENT_REQUESTS,
            AgentPermission.READ_CHANGE_REQUEST,
            AgentPermission.CREATE_CHANGE_DRAFT,
            AgentPermission.CREATE_CHANGE_ANALYSIS,
            AgentPermission.CREATE_IMPACT_ANALYSIS,
            AgentPermission.CREATE_CLASSIFICATION,
            AgentPermission.CREATE_SUMMARY,
            AgentPermission.CREATE_SCOPE_SIGNAL,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute change triage, impact analysis, effort re-estimation, or proposal summary generation."""

        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_action = str(input_data.get("action") or "CLASSIFY_CHANGE")

        change_request_id = str(input_data.get("change_request_id") or "cr-1")
        title = str(input_data.get("title") or "Change Request")
        description = str(input_data.get("description") or "")

        if task_action == "CLASSIFY_CHANGE":
            res = self.classifier.classify_change(change_request_id, title, description)
            return res.model_dump()

        elif task_action == "ANALYZE_IMPACT":
            res = self.impact_analyzer.analyze_impact(change_request_id, title, description)
            return res.model_dump()

        elif task_action == "ESTIMATE_EFFORT":
            res = self.effort_analyzer.calculate_effort(change_request_id, title, description)
            return res.model_dump()

        elif task_action == "CALCULATE_COMMERCIAL":
            expected_hours = float(input_data.get("expected_hours") or 20.0)
            orig_val = float(input_data.get("original_value") or 0.0)
            res = self.commercial_analyzer.calculate_commercial_delta(change_request_id, expected_hours, original_contract_value=orig_val)
            return res.model_dump()

        elif task_action == "EVALUATE_CONTRACT":
            is_out_of_scope = bool(input_data.get("is_out_of_scope", True))
            change_val = float(input_data.get("change_value") or 100000.0)
            return self.contract_analyzer.evaluate_contract_impact(change_request_id, is_out_of_scope, change_val)

        elif task_action == "SUMMARIZE_CHANGE":
            change_num = str(input_data.get("change_number") or "CR-0001")
            hours = float(input_data.get("expected_hours") or 20.0)
            val = float(input_data.get("change_value") or 100000.0)
            res = self.summary_engine.summarize_change(change_request_id, change_num, title, description, hours, val)
            return res.model_dump()

        else:
            return {
                "status": "COMPLETED",
                "message": f"Change action '{task_action}' processed cleanly.",
            }
