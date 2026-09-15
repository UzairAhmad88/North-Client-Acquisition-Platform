"""Discovery Question Generator producing prioritized, client-friendly discovery questions."""

from typing import List
from agents.requirements.models import DiscoveryQuestionSchema, ExtractedRequirementSchema


class DiscoveryQuestionGenerator:
    """Generates prioritized, non-technical questions to clarify missing details."""

    @classmethod
    def generate(
        cls, requirements: List[ExtractedRequirementSchema], message_body: str
    ) -> List[DiscoveryQuestionSchema]:
        questions: List[DiscoveryQuestionSchema] = []
        categories = {req.category for req in requirements}
        body_lower = message_body.lower()

        # 1. Booking System Questions
        if "BOOKING" in categories:
            if "hours" not in body_lower and "schedule" not in body_lower:
                questions.append(
                    DiscoveryQuestionSchema(
                        question="What are your business working hours and appointment time slots?",
                        category="WORKFLOW",
                        priority="CRITICAL",
                        reason="Needed to configure booking schedule availability constraints.",
                        related_requirement_title="Booking System",
                    )
                )
            if "service" not in body_lower:
                questions.append(
                    DiscoveryQuestionSchema(
                        question="What specific services or appointment types can clients book?",
                        category="SCOPE",
                        priority="HIGH",
                        reason="Needed to define the booking options catalog.",
                        related_requirement_title="Booking System",
                    )
                )

        # 2. Payment Questions
        if "PAYMENT" in categories and "stripe" not in body_lower:
            questions.append(
                DiscoveryQuestionSchema(
                    question="Which payment gateway do you currently use (e.g. Stripe, PayPal, Square)?",
                    category="INTEGRATION",
                    priority="HIGH",
                    reason="Needed to determine payment integration provider.",
                    related_requirement_title="Payment Gateway",
                )
            )

        # 3. Budget & Timeline (Always check if unknown)
        if "budget" not in body_lower and "cost" not in body_lower:
            questions.append(
                DiscoveryQuestionSchema(
                    question="What is your target budget range for this project?",
                    category="BUDGET",
                    priority="HIGH",
                    reason="Needed to ensure proposed scope fits target budget expectations.",
                )
            )

        if "timeline" not in body_lower and "launch" not in body_lower:
            questions.append(
                DiscoveryQuestionSchema(
                    question="What is your desired target launch date?",
                    category="TIMELINE",
                    priority="MEDIUM",
                    reason="Needed for project milestone scheduling.",
                )
            )

        # Return top prioritized questions (avoid interrogating with > 4 questions)
        return questions[:4]
