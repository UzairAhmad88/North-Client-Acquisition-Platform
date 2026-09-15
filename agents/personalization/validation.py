"""Claim validator and risk classifier enforcing safety policy and prohibited claim rules."""

from typing import List, Tuple
from agents.personalization.schemas import ClaimItem, OutreachDraftPayload


PROHIBITED_KEYWORDS = [
    "guarantee",
    "guaranteed",
    "100%",
    "competitors are taking",
    "losing thousands",
    "losing customers",
    "fake testimonial",
    "we built a similar system for",  # unless verified portfolio
    "act today",
    "last chance",
    "urgent notice",
]


class ClaimValidator:
    """Validates claims in outreach drafts against safety boundaries and prohibited claim policies."""

    @staticmethod
    def validate_claims_and_risk(
        draft: OutreachDraftPayload,
        verified_evidence_count: int,
    ) -> Tuple[List[ClaimItem], str, List[str]]:
        """
        Scan draft subject & body for prohibited claims, assign risk levels, and classify statements.
        Returns (claims, risk_level, warnings).
        """
        claims: List[ClaimItem] = []
        warnings: List[str] = []
        risk_level = "LOW"

        text_to_check = f"{draft.subject or ''} {draft.body}".lower()

        # 1. Prohibited Keyword & Hype Check
        for kw in PROHIBITED_KEYWORDS:
            if kw in text_to_check:
                risk_level = "HIGH"
                warnings.append(f"Prohibited claim or hype phrase detected: '{kw}'. Claim rewritten or flagged.")
                claims.append(
                    ClaimItem(
                        statement=f"Detected risky phrase: {kw}",
                        classification="INFERRED",
                        is_supported=False,
                        risk_notes=f"Violates policy against hype or false urgency: '{kw}'",
                    )
                )

        # 2. Extract key claims from body
        paragraphs = [p.strip() for p in draft.body.split("\n\n") if p.strip()]
        for p in paragraphs:
            if "notice" in p.lower() or "review" in p.lower():
                claims.append(
                    ClaimItem(
                        statement=p[:120] + ("..." if len(p) > 120 else ""),
                        classification="VERIFIED" if verified_evidence_count > 0 else "INFERRED",
                        is_supported=verified_evidence_count > 0,
                    )
                )

        # 3. Final Risk Level Calculation
        if draft.outreach_readiness == "OUTREACH_BLOCKED":
            risk_level = "BLOCKED"
        elif draft.outreach_readiness == "NEEDS_MANUAL_REVIEW" and risk_level == "LOW":
            risk_level = "MEDIUM"

        return claims, risk_level, warnings
