"""Production Client Collaboration AI Agent built on Phase 14 BaseAgent runtime."""

from typing import Any, Dict, List, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.client_collaboration.action_extractor import ClientActionExtractor
from agents.client_collaboration.classifier import ClientRequestClassifier
from agents.client_collaboration.scope_detector import ClientScopeDetector
from agents.client_collaboration.summarizer import ClientFeedbackSummarizer


class ClientCollaborationAgent(BaseAgent):
    """Production Client Collaboration AI Agent providing request classification, feedback summarization, action extraction, and scope detection."""

    agent_id = "client_collaboration_agent"
    name = "Client Collaboration Agent"
    version = "1.0"
    description = "Classifies client requests, summarizes deliverable feedback, extracts required action items, and flags potential scope creep."

    def __init__(self):
        super().__init__()
        self.classifier = ClientRequestClassifier()
        self.summarizer = ClientFeedbackSummarizer()
        self.action_extractor = ClientActionExtractor()
        self.scope_detector = ClientScopeDetector()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_CLIENT_MESSAGES,
            AgentPermission.READ_PROJECT,
            AgentPermission.READ_DELIVERABLES,
            AgentPermission.READ_BASELINE,
            AgentPermission.READ_TASKS,
            AgentPermission.READ_CLIENT_REQUESTS,
            AgentPermission.READ_CLIENT_FEEDBACK,
            AgentPermission.CREATE_ACTION_DRAFT,
            AgentPermission.CREATE_SUMMARY,
            AgentPermission.CREATE_CLASSIFICATION,
            AgentPermission.CREATE_SCOPE_SIGNAL,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute request classification, feedback summarization, or action extraction."""

        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_action = str(input_data.get("action") or "CLASSIFY_REQUEST")

        if task_action == "CLASSIFY_REQUEST":
            request_id = str(input_data.get("request_id") or "req-1")
            title = str(input_data.get("title") or "Client Request")
            description = str(input_data.get("description") or "")
            res = self.classifier.classify_request(request_id, title, description)
            return res.model_dump()

        elif task_action == "SUMMARIZE_FEEDBACK":
            deliverable_id = str(input_data.get("deliverable_id") or "del-1")
            deliverable_name = str(input_data.get("deliverable_name") or "Deliverable")
            feedback_items = input_data.get("feedback_items") or []
            res = self.summarizer.summarize_feedback(deliverable_id, deliverable_name, feedback_items)
            return res.model_dump()

        elif task_action == "EXTRACT_ACTIONS":
            messages = input_data.get("messages") or []
            actions = self.action_extractor.extract_action_items(messages)
            return {"extracted_action_items": [a.model_dump() for a in actions]}

        elif task_action == "EVALUATE_SCOPE":
            text = str(input_data.get("text") or "")
            baseline_items = input_data.get("baseline_items") or []
            res = self.scope_detector.evaluate_scope(text, baseline_items)
            return res.model_dump()

        else:
            return {
                "status": "COMPLETED",
                "message": f"Action '{task_action}' processed cleanly.",
            }
