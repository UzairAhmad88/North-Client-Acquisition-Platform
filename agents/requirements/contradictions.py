"""Contradiction Detector engine identifying conflicting requirement rules."""

from typing import List
from agents.requirements.models import ContradictionSchema, ExtractedRequirementSchema


class ContradictionDetector:
    """Identifies contradictory requirements in discovery session state."""

    @classmethod
    def detect(
        cls, message_body: str, requirements: List[ExtractedRequirementSchema]
    ) -> List[ContradictionSchema]:
        contradictions: List[ContradictionSchema] = []
        body_lower = message_body.lower()

        # Rule 1: Access control conflict (staff-only vs customer booking)
        if "only staff" in body_lower and "customers can book" in body_lower:
            contradictions.append(
                ContradictionSchema(
                    requirement_a="Staff-only booking restriction",
                    requirement_b="Customer self-service online booking",
                    conflict_description="Message states booking is restricted to staff only, while also requesting customer self-service booking.",
                    recommended_clarification="Clarify whether customers can directly create bookings online or if bookings require staff approval.",
                )
            )

        # Rule 2: Timeline vs scope conflict (urgent launch + custom app)
        if "asap" in body_lower and "custom mobile app" in body_lower:
            contradictions.append(
                ContradictionSchema(
                    requirement_a="Immediate ASAP launch timeline",
                    requirement_b="Custom native mobile application scope",
                    conflict_description="Custom native mobile apps require substantial build time, contradicting immediate ASAP launch expectations.",
                    recommended_clarification="Confirm if a web application / PWA can launch first as Phase 1.",
                )
            )

        return contradictions
