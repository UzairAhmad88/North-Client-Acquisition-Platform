"""Proposal Claim Validator verifying claim traceability and factual grounding."""

from typing import Any, Dict, List
from agents.proposal.models import ProposalClaimSchema, ProposalSectionSchema


class ProposalClaimValidator:
    """Validates factual claims made in proposal sections against solution features and requirements."""

    PROHIBITED_CLAIM_PATTERNS = [
        "100% guarantee",
        "guaranteed revenue",
        "double your sales",
        "worked with hundreds of businesses",
        "trusted by 500",
    ]

    @classmethod
    def validate_claims(
        cls, sections: List[ProposalSectionSchema], solution_data: Dict[str, Any]
    ) -> List[ProposalClaimSchema]:
        claims: List[ProposalClaimSchema] = []
        features = solution_data.get("features", [])
        feature_titles = {f.get("title") for f in features}

        for sec in sections:
            content_lower = sec.content.lower()

            # Check prohibited claims
            for pattern in cls.PROHIBITED_CLAIM_PATTERNS:
                if pattern in content_lower:
                    claims.append(
                        ProposalClaimSchema(
                            statement=f"Prohibited or unsupported claim found in section '{sec.title}': {pattern}",
                            supporting_requirement_title=None,
                            supporting_feature_title=None,
                            is_supported=False,
                        )
                    )

            # Traceable feature claims
            for f in features:
                f_title = f.get("title", "")
                if f_title and f_title.lower() in content_lower:
                    claims.append(
                        ProposalClaimSchema(
                            statement=f"Feature proposal claim: {f_title}",
                            supporting_requirement_title=f.get("category"),
                            supporting_feature_title=f_title,
                            is_supported=True,
                        )
                    )

        return claims
