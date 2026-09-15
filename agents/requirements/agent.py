"""Production Client Requirements & Discovery Intelligence Agent."""

from typing import Any, Dict, List
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.requirements.classifier import RequirementClassifier
from agents.requirements.contradictions import ContradictionDetector
from agents.requirements.dependencies import DependencyAnalyzer
from agents.requirements.extractor import RequirementExtractor
from agents.requirements.models import RequirementsAnalysisResult
from agents.requirements.questions import DiscoveryQuestionGenerator
from agents.requirements.readiness import ReadinessEvaluator
from agents.requirements.scope import ScopeManager


class RequirementsAgent(BaseAgent):
    """
    Production Client Requirements & Discovery Intelligence Agent.
    Converts client messages and conversation history into structured, evidence-backed requirements,
    dependency graphs, prioritized discovery questions, scope items, and readiness metrics.
    """

    agent_id = "requirements_agent"
    name = "Requirements Agent"
    version = "1.0"
    description = "Extracts structured requirements, dependency graphs, discovery questions, and readiness metrics from client conversations."
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "READ_AUDIT",
        "READ_SCORE",
        "READ_SERVICES",
        "READ_CONVERSATION",
        "READ_CRM_CONTEXT",
        "CREATE_REQUIREMENT_DRAFT",
    }

    def get_permissions(self) -> list[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        latest_message = context.metadata.get("latest_message", {})
        message_body = latest_message.get("body", "")
        message_id = latest_message.get("id")

        # 1. Requirement Extraction
        raw_reqs, goal, problem, target_users = RequirementExtractor.extract(message_body, message_id)

        # 2. Classification & Policy Refinement
        requirements = RequirementClassifier.classify_and_refine(raw_reqs)

        # 3. Dependency Analysis
        dependencies = DependencyAnalyzer.analyze(requirements)

        # 4. Contradiction Detection
        contradictions = ContradictionDetector.detect(message_body, requirements)

        # 5. Question Generation
        questions = DiscoveryQuestionGenerator.generate(requirements, message_body)

        # 6. Scope Management
        scope_items, scope_expansion = ScopeManager.process_scope(requirements)

        # 7. Readiness Evaluation
        readiness = ReadinessEvaluator.evaluate(requirements, scope_items, len(questions), message_body)

        result_payload = RequirementsAnalysisResult(
            business_goal=goal,
            business_problem=problem,
            target_users=target_users,
            project_type="Web & Business System",
            requirements=requirements,
            dependencies=dependencies,
            questions=questions,
            scope_items=scope_items,
            contradictions=contradictions,
            readiness=readiness,
            scope_expansion_detected=scope_expansion,
            unsupported_assumptions=[],
        )

        return AgentResult(
            status="COMPLETED",
            result=result_payload.model_dump(),
            confidence="HIGH",
            evidence=[{"source": "CLIENT_MESSAGE", "message_id": message_id}],
            warnings=[f"Detected {len(contradictions)} contradiction(s)"] if contradictions else [],
            errors=[],
            next_action={"action": "HUMAN_REQUIREMENTS_REVIEW", "reason": "Review and confirm extracted requirements."},
            metadata={"run_id": context.agent_run_id, "agent_id": self.name},
        )


requirements_agent = RequirementsAgent()
