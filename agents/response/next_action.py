"""Next action recommender mapping intent and signals to primary business action."""

from typing import Optional, Tuple
from agents.response.models import DetectedObjection, BuyingSignalDetail


class NextActionRecommender:
    """Recommends primary next action for the sales operator."""

    @staticmethod
    def recommend(
        primary_intent: str,
        buying_signal: BuyingSignalDetail,
        objection: Optional[DetectedObjection],
    ) -> Tuple[str, str, str]:
        """
        Returns (action, reason, confidence).
        Actions: REPLY_WITH_DETAILS, ASK_CLARIFYING_QUESTION, PROVIDE_PRICE_RANGE, PROVIDE_PORTFOLIO,
                 SCHEDULE_MEETING, CREATE_FOLLOW_UP, PREPARE_PROPOSAL, MARK_NOT_INTERESTED,
                 MARK_DO_NOT_CONTACT, ESCALATE_TO_HUMAN, NO_ACTION.
        """
        if primary_intent == "OPT_OUT":
            return "MARK_DO_NOT_CONTACT", "Client requested opt-out / DNC", "HIGH"

        if primary_intent == "WRONG_PERSON":
            return "ESCALATE_TO_HUMAN", "Inbound message indicated contact is wrong person", "HIGH"

        if primary_intent == "NOT_INTERESTED":
            return "MARK_NOT_INTERESTED", "Client indicated lack of interest", "HIGH"

        if primary_intent == "REQUEST_FOR_MEETING" or buying_signal.level == "STRONG":
            return "SCHEDULE_MEETING", "Client requested a call or meeting", "HIGH"

        if primary_intent == "REQUEST_FOR_PRICE":
            return "PROVIDE_PRICE_RANGE", "Client requested pricing information", "HIGH"

        if primary_intent == "REQUEST_FOR_PORTFOLIO":
            return "PROVIDE_PORTFOLIO", "Client requested examples/portfolio", "HIGH"

        if objection and objection.type in ("PRICE", "TIMING"):
            return "ASK_CLARIFYING_QUESTION", f"Client raised objection: {objection.type}", "MEDIUM"

        if primary_intent == "REQUEST_FOR_DETAILS" or primary_intent == "INTERESTED":
            return "REPLY_WITH_DETAILS", "Client expressed interest or requested details", "HIGH"

        return "ESCALATE_TO_HUMAN", "Intent is ambiguous; requires human review", "LOW"
