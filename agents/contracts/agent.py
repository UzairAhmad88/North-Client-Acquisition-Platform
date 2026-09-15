"""Production Contract Intelligence Agent."""

import uuid
from typing import Any, Dict, List
from agents.contracts.discrepancies import DiscrepancyDetector
from agents.contracts.generator import ContractGenerator
from agents.contracts.models import ContractGenerationResult
from agents.contracts.validator import ContractValidator
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission


class ContractAgent(BaseAgent):
    """
    Production Contract Intelligence Agent.
    Generates contract drafts, evaluates document completeness, detects scope/commercial discrepancies
    against approved proposal and estimate baselines, and enforces commercial & legal safety boundaries.
    """

    agent_id = "contract_agent"
    name = "Contract Agent"
    version = "1.0"
    description = "Composes contract draft sections, validates document completeness, and detects scope/price discrepancies against approved baselines."
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_REQUIREMENTS",
        "READ_SOLUTION",
        "READ_ESTIMATE",
        "READ_PROPOSAL",
        "READ_CONTRACT",
        "CREATE_CONTRACT_DRAFT",
        "CREATE_CONTRACT_SUMMARY",
        "COMPARE_CONTRACT_VERSIONS",
        "CREATE_REVIEW_FINDINGS",
    }

    def get_permissions(self) -> list[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        business_name = context.business_profile.get("name", "Client Business")
        proposal_data = context.metadata.get("proposal_data", {})
        estimate_data = context.metadata.get("estimate_data", {})
        solution_data = context.metadata.get("solution_data", {})
        contract_number = context.metadata.get("contract_number", f"CTR-2026-{str(uuid.uuid4())[:4].upper()}")

        # 1. Generate Contract Sections
        sections = ContractGenerator.generate_sections(
            contract_number, business_name, proposal_data, estimate_data, solution_data
        )

        # 2. Content Hash Computation
        content_hash = ContractGenerator.calculate_content_hash(sections)

        # 3. Completeness Evaluation
        completeness = ContractValidator.evaluate_completeness(sections)

        # 4. Discrepancy Detection
        discrepancies = DiscrepancyDetector.detect_discrepancies(
            sections, proposal_data, estimate_data, solution_data
        )

        result_payload = ContractGenerationResult(
            contract_number=contract_number,
            title=f"Technical Services Agreement - {business_name}",
            summary=f"Project agreement draft outlining scope, deliverables, intellectual property terms, and commercial baseline for {business_name}.",
            status="DRAFT",
            pricing_status=proposal_data.get("pricing_status", "PRICING_REQUIRES_HUMAN_REVIEW"),
            risk_status="PENDING_REVIEW",
            sections=sections,
            discrepancies=discrepancies,
            completeness=completeness,
            content_hash=content_hash,
        )

        warnings = []
        if discrepancies:
            warnings.append(f"Detected {len(discrepancies)} discrepancy/discrepancies between contract draft and approved baselines.")

        return AgentResult(
            status="COMPLETED",
            result=result_payload.model_dump(),
            confidence="HIGH",
            evidence=[
                {"source": "PROPOSAL_BASELINE", "proposal_version": proposal_data.get("version", 1)},
                {"source": "ESTIMATE_BASELINE", "estimate_version": estimate_data.get("version", 1)},
            ],
            warnings=warnings,
            errors=[],
            next_action={"action": "HUMAN_CONTRACT_REVIEW", "reason": "Review contract draft, resolve discrepancies, and grant internal operator approval."},
            metadata={"run_id": context.agent_run_id, "agent_id": self.name},
        )


contract_agent = ContractAgent()
