"""Planner module evaluating lead eligibility, DNC guardrails, and qualification gating for Personalization Agent."""

from typing import Any, Dict, Tuple


class PersonalizationPlanner:
    """Evaluates lead qualification status, DNC status, and context eligibility before personalization."""

    @staticmethod
    def evaluate_eligibility(
        qualification_data: Dict[str, Any],
        is_dnc: bool = False,
        has_valid_contact: bool = True,
    ) -> Tuple[bool, str, str]:
        """
        Evaluate if lead is eligible for personalized outreach drafting.
        Returns (is_eligible, outreach_readiness, reason).
        """
        if is_dnc:
            return False, "OUTREACH_BLOCKED", "Lead is listed on Do-Not-Contact (DNC) registry."

        if not has_valid_contact:
            return False, "NOT_RECOMMENDED", "No verified telephone, email, or digital contact route found."

        decision = qualification_data.get("decision") or qualification_data.get("human_override_decision", "UNKNOWN")

        if decision == "NOT_QUALIFIED":
            return False, "NOT_RECOMMENDED", "Lead has been evaluated as NOT_QUALIFIED for outreach."

        if decision == "INSUFFICIENT_DATA":
            return False, "NOT_RECOMMENDED", "Lead lacks sufficient business research or audit data for personalization."

        if decision == "NEEDS_REVIEW":
            return True, "NEEDS_MANUAL_REVIEW", "Lead requires manual review before final approval, but internal draft is permitted."

        if decision in ("QUALIFIED", "POTENTIALLY_QUALIFIED"):
            return True, "READY", "Lead is qualified and eligible for evidence-backed personalization."

        # Fallback if qualification status is missing/unrun
        return True, "NEEDS_MANUAL_REVIEW", "No formal qualification record found; draft requires manual review."
