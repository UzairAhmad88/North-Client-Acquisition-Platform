"""Contract Completeness Scorer evaluating required document sections."""

from typing import List
from agents.contracts.models import ContractCompletenessSchema, ContractSectionSchema


class ContractValidator:
    """Evaluates contract completeness score and checks for required contract sections."""

    MANDATORY_SECTION_TYPES = [
        "PARTIES",
        "OVERVIEW",
        "SCOPE",
        "DELIVERABLES",
        "COMMERCIAL",
        "IP",
        "SIGNATURES",
    ]

    @classmethod
    def evaluate_completeness(
        cls, sections: List[ContractSectionSchema]
    ) -> ContractCompletenessSchema:
        present_types = {s.section_type for s in sections}
        missing: List[str] = []

        for req_type in cls.MANDATORY_SECTION_TYPES:
            if req_type not in present_types:
                missing.append(req_type)

        total_req = len(cls.MANDATORY_SECTION_TYPES)
        found_req = total_req - len(missing)
        score = round((found_req / total_req) * 100.0, 1)

        recommendations: List[str] = []
        if missing:
            recommendations.append(f"Add missing mandatory section(s): {', '.join(missing)}")

        return ContractCompletenessSchema(
            completeness_score=score,
            missing_sections=missing,
            recommendations=recommendations,
        )
