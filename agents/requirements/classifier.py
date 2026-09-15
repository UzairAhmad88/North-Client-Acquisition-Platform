"""Requirement Classifier module categorizing priority, explicit vs inferred tags, and confidence."""

from typing import List
from agents.requirements.models import ExtractedRequirementSchema


class RequirementClassifier:
    """Classifies requirement attributes and enforces policy rules."""

    @classmethod
    def classify_and_refine(
        cls, requirements: List[ExtractedRequirementSchema]
    ) -> List[ExtractedRequirementSchema]:
        refined = []
        for req in requirements:
            # Enforce rule: AI inferences are never explicit
            if req.source_type in ("AI_INFERENCE", "SYSTEM_INFERENCE"):
                req.explicit = False
                if req.status == "CONFIRMED":
                    req.status = "PROPOSED"  # Reset unverified confirmation attempts

            # Set priority defaults if needed
            if req.category in ("BOOKING", "WEBSITE", "PAYMENT"):
                req.priority = "HIGH"
            elif req.category in ("AI_FEATURE", "AUTOMATION", "CRM"):
                req.priority = "MEDIUM"

            refined.append(req)
        return refined
