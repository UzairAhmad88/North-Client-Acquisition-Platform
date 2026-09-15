"""Production Solution Design Intelligence Agent."""

from typing import Any, Dict, List
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.solution.architecture import ArchitectureBuilder
from agents.solution.deliverables import DeliverableBuilder
from agents.solution.mapper import RequirementMapper
from agents.solution.models import SolutionAssumptionSchema, SolutionDesignResult


class SolutionAgent(BaseAgent):
    """
    Production Solution Design Intelligence Agent.
    Transforms confirmed client requirements into a structured solution design, feature mappings,
    proportional architecture diagrams, deliverable items, integrations, and assumptions.
    """

    agent_id = "solution_agent"
    name = "Solution Agent"
    version = "1.0"
    description = "Transforms confirmed client requirements into a structured technical solution design, feature mapping, architecture diagram, and deliverable specs."
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "READ_AUDIT",
        "READ_SCORE",
        "READ_SERVICES",
        "READ_REQUIREMENTS",
        "READ_DISCOVERY",
        "READ_CONVERSATION",
        "READ_CRM_CONTEXT",
        "CREATE_SOLUTION_DRAFT",
    }

    def get_permissions(self) -> list[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        reqs_data = context.metadata.get("requirements", [])

        # 1. Feature Mapping
        features = RequirementMapper.map_requirements(reqs_data)

        # 2. Architecture & Integration Spec
        architecture = ArchitectureBuilder.build(features)
        integrations = ArchitectureBuilder.extract_integrations(features)

        # 3. Deliverables Generation
        deliverables = DeliverableBuilder.build_deliverables(features)

        # 4. Standard Solution Assumptions
        assumptions = [
            SolutionAssumptionSchema(
                assumption_text="Client will provide website branding assets, logo, and copy content.",
                status="UNCONFIRMED",
                risk_level="LOW",
            ),
            SolutionAssumptionSchema(
                assumption_text="Third-party service provider accounts (e.g. Stripe, Twilio) will be provided by client.",
                status="UNCONFIRMED",
                risk_level="MEDIUM",
            ),
        ]

        # Complexity determination
        complexity = "LOW"
        if len(features) >= 5:
            complexity = "HIGH"
        elif len(features) >= 3:
            complexity = "MEDIUM"

        result_payload = SolutionDesignResult(
            overview=f"Solution design providing {len(features)} core modules addressing confirmed requirements.",
            architecture_summary=architecture.diagram_summary,
            complexity_tier=complexity,
            features=features,
            deliverables=deliverables,
            dependencies=[],
            integrations=integrations,
            assumptions=assumptions,
            architecture=architecture,
            out_of_scope=["Custom Mobile Application", "Legacy Data Migration"],
            optional_features=[f.title for f in features if f.status == "OPTIONAL"],
        )

        return AgentResult(
            status="COMPLETED",
            result=result_payload.model_dump(),
            confidence="HIGH",
            evidence=[{"source": "REQUIREMENTS_DISCOVERY", "requirements_count": len(reqs_data)}],
            warnings=[],
            errors=[],
            next_action={"action": "HUMAN_SOLUTION_REVIEW", "reason": "Review and approve recommended solution design."},
            metadata={"run_id": context.agent_run_id, "agent_id": self.name},
        )


solution_agent = SolutionAgent()
