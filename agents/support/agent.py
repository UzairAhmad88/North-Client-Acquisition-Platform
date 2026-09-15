"""Production Support Intelligence AI Agent built on BaseAgent runtime."""

from typing import Any, Dict, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.support.classifier import SupportClassifierEngine
from agents.support.opportunity_detector import OpportunityDetectorEngine
from agents.support.troubleshooter import TroubleshooterEngine
from agents.support.warranty_evaluator import WarrantyEvaluatorEngine


class SupportAgent(BaseAgent):
    """Production Support AI Agent providing request classification, warranty evaluation, diagnostic troubleshooting, and commercial opportunity detection."""

    agent_id = "support_agent"
    name = "Support Intelligence Agent"
    version = "1.0"
    description = "Classifies client support tickets, evaluates warranty coverage, suggests troubleshooting steps, and detects expansion opportunities."

    def __init__(self):
        super().__init__()
        self.classifier = SupportClassifierEngine()
        self.warranty_evaluator = WarrantyEvaluatorEngine()
        self.troubleshooter = TroubleshooterEngine()
        self.opportunity_detector = OpportunityDetectorEngine()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_PROJECT,
            AgentPermission.READ_CONTRACT,
            AgentPermission.READ_REQUIREMENTS,
            AgentPermission.READ_SOLUTION,
            AgentPermission.READ_DELIVERABLES,
            AgentPermission.READ_RELEASES,
            AgentPermission.READ_KNOWLEDGE_BASE,
            AgentPermission.READ_SUPPORT_REQUESTS,
            AgentPermission.READ_INCIDENTS,
            AgentPermission.READ_MAINTENANCE,
            AgentPermission.READ_WARRANTY,
            AgentPermission.CREATE_CLASSIFICATION,
            AgentPermission.CREATE_SUMMARY,
            AgentPermission.CREATE_TROUBLESHOOTING_DRAFT,
            AgentPermission.CREATE_KNOWLEDGE_SUGGESTION,
            AgentPermission.CREATE_OPPORTUNITY_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute support ticket triage, warranty evaluation, troubleshooting, or opportunity detection."""
        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_action = str(input_data.get("action") or "CLASSIFY_REQUEST")

        req_id = input_data.get("request_id")
        title = str(input_data.get("title") or "Support Request")
        desc = str(input_data.get("description") or "")
        category = str(input_data.get("category") or "APPLICATION")
        project_id = str(input_data.get("project_id") or "p-1")

        if task_action == "CLASSIFY_REQUEST":
            res = self.classifier.classify_request(req_id, title, desc, category)
            return res.model_dump()

        elif task_action == "EVALUATE_WARRANTY":
            w_data = input_data.get("warranty_data")
            in_base = bool(input_data.get("is_in_baseline", True))
            res = self.warranty_evaluator.evaluate_warranty_coverage(project_id, title, desc, w_data, in_base)
            return res.model_dump()

        elif task_action == "TROUBLESHOOT":
            res = self.troubleshooter.analyze_troubleshooting(req_id, title, desc, category)
            return res.model_dump()

        elif task_action == "DETECT_OPPORTUNITY":
            res = self.opportunity_detector.detect_opportunity(project_id, title, desc)
            return res.model_dump()

        else:
            return {
                "status": "COMPLETED",
                "message": f"Support action '{task_action}' processed cleanly.",
            }
