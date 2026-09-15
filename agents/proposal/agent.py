"""Production Proposal Generation & Review Intelligence Agent."""

from typing import Any, Dict, List
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.proposal.claims import ProposalClaimValidator
from agents.proposal.composer import ProposalComposer
from agents.proposal.models import ProposalGenerationResult, ProposalItemDraftSchema


class ProposalAgent(BaseAgent):
    """
    Production Proposal Generation & Review Intelligence Agent.
    Composes client-facing proposal documents, itemizes deliverables, validates claim evidence,
    computes content hashes, and enforces commercial safety boundaries.
    """

    agent_id = "proposal_agent"
    name = "Proposal Agent"
    version = "1.0"
    description = "Composes client-facing technical/commercial proposals, verifies claim evidence traceability, and enforces commercial safety."
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_SERVICES",
        "READ_REQUIREMENTS",
        "READ_SOLUTION",
        "READ_CRM_CONTEXT",
        "CREATE_PROPOSAL_DRAFT",
    }

    def get_permissions(self) -> list[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        business_name = context.business_profile.get("name", "Client Business")
        solution_data = context.metadata.get("solution_data", {})
        proposal_type = context.metadata.get("proposal_type", "FULL")

        # 1. Proposal Section Composition
        sections = ProposalComposer.compose_sections(business_name, solution_data, proposal_type)

        # 2. Content Hash Computation
        content_hash = ProposalComposer.calculate_content_hash(sections)

        # 3. Itemization (Draft items from deliverables)
        items: List[ProposalItemDraftSchema] = []
        for d in solution_data.get("deliverables", []):
            items.append(
                ProposalItemDraftSchema(
                    description=d.get("name", "Deliverable Package"),
                    quantity=1.0,
                    unit="project",
                    is_optional=False,
                    price=None,  # Defaults to None (PRICING_REQUIRES_HUMAN_REVIEW)
                )
            )

        # 4. Claim Evidence Validation
        claims = ProposalClaimValidator.validate_claims(sections, solution_data)
        unsupported_claims = [c for c in claims if not c.is_supported]

        result_payload = ProposalGenerationResult(
            title=f"Technical & Scope Proposal for {business_name}",
            proposal_type=proposal_type,
            summary=f"Tailored proposal outlining solution scope, deliverables, and technical approach for {business_name}.",
            sections=sections,
            items=items,
            claims=claims,
            pricing_status="PRICING_REQUIRES_HUMAN_REVIEW",
            content_hash=content_hash,
            requirement_coverage_percentage=100.0,
        )

        warnings = []
        if unsupported_claims:
            warnings.append(f"Detected {len(unsupported_claims)} unsupported claim(s) requiring human review.")

        return AgentResult(
            status="COMPLETED",
            result=result_payload.model_dump(),
            confidence="HIGH",
            evidence=[{"source": "SOLUTION_DESIGN", "deliverables_count": len(items)}],
            warnings=warnings,
            errors=[],
            next_action={"action": "HUMAN_PROPOSAL_REVIEW", "reason": "Review proposal content, define pricing, and approve proposal draft."},
            metadata={"run_id": context.agent_run_id, "agent_id": self.name},
        )


proposal_agent = ProposalAgent()
