"""
Organizational Learning Agent (Section 25, 30, 73).
Extracts retrospective lessons from completed projects, support tickets, incident postmortems, and sales outcomes.
Enforces Rule 19: Organizational learning must NOT autonomously rewrite critical pricing, security, or legal policies.
"""

from typing import Any, Dict, List, Optional, Set
import uuid
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.knowledge.base import LessonItem
    from backend.app.knowledge.service import KnowledgePlatformService
except ImportError:
    from app.knowledge.base import LessonItem
    from app.knowledge.service import KnowledgePlatformService


class OrganizationalLearningAgent(BaseAgent):
    """
    Agent synthesizing lessons learned and operational retrospectives into structured memory items.
    Enforces Rule 19: Produces recommendations and drafts for human review, NEVER autonomous policy changes.
    """

    agent_id = "organizational_learning_agent"
    name = "Organizational Learning Agent"
    version = "1.0"
    description = "Extracts reusable operational lessons from project postmortems and incident resolutions."

    def __init__(self, service: Optional[KnowledgePlatformService] = None):
        super().__init__()
        self.service = service or KnowledgePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_KNOWLEDGE,
            AgentPermission.CREATE_LESSON_DRAFT,
            AgentPermission.CREATE_DECISION_SUMMARY,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        title = str(params.get("title") or "Retrospective Operational Lesson")
        context_scope = str(params.get("context_scope") or "Delivery & Architecture")
        problem = str(params.get("problem") or "")
        root_cause = str(params.get("root_cause") or "")
        what_worked = str(params.get("what_worked") or "")
        what_failed = str(params.get("what_failed") or "")
        recommendation = str(params.get("recommendation") or "")
        applicability_domain = str(params.get("applicability_domain") or "TECHNICAL")
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")
        owner_id = str(params.get("owner_id") or "learning_lead")

        if not problem or not recommendation:
            return {
                "status": "ERROR",
                "message": "Problem description and recommendation are required to formulate a lesson.",
            }

        lesson_code = f"LES-{uuid.uuid4().hex[:8].upper()}"
        lesson = LessonItem(
            lesson_code=lesson_code,
            tenant_id=tenant_id,
            title=title,
            context_scope=context_scope,
            problem=problem,
            root_cause=root_cause,
            what_worked=what_worked,
            what_failed=what_failed,
            recommendation=recommendation,
            applicability_domain=applicability_domain,
            owner_id=owner_id,
            confidence=0.9,
        )

        saved = self.service.store.create_lesson(lesson)

        return {
            "status": "SUCCESS",
            "lesson_code": saved.lesson_code,
            "title": saved.title,
            "applicability_domain": saved.applicability_domain,
            "confidence": saved.confidence,
            "policy_notice": "Lesson recorded for future project estimation and planning. Policy changes require human approval.",
        }
