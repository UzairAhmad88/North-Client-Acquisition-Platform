"""Requirements extraction and missing information detector."""

import re
from typing import List, Optional, Tuple
from agents.response.models import ExtractedRequirement


class RequirementExtractor:
    """Extracts explicit client service requirements and identifies missing decision info."""

    CATEGORIES = {
        "WEBSITE": [r"website", r"web\s+design", r"redesign", r"landing\s+page"],
        "BOOKING": [r"booking", r"appointment", r"reservation", r"calendar"],
        "SEO": [r"seo", r"google\s+ranking", r"search\s+visibility"],
        "CRM": [r"crm", r"lead\s+management", r"customer\s+database"],
        "WHATSAPP": [r"whatsapp", r"messaging", r"chat\s+automation"],
    }

    @staticmethod
    def extract(text: str, message_id: Optional[str] = None) -> Tuple[List[ExtractedRequirement], List[str]]:
        clean = (text or "").lower()
        reqs: List[ExtractedRequirement] = []

        for category, patterns in RequirementExtractor.CATEGORIES.items():
            for pat in patterns:
                if re.search(pat, clean):
                    reqs.append(
                        ExtractedRequirement(
                            category=category,
                            item=f"Requirement identified for {category.lower()}",
                            is_explicit=True,
                            source_message_id=message_id,
                        )
                    )
                    break

        # Check missing information
        missing: List[str] = []
        if not re.search(r"budget|cost|price|\$", clean):
            missing.append("Budget Range")
        if not re.search(r"timeline|deadline|asap|month|week", clean):
            missing.append("Target Timeline")
        if not re.search(r"decision|manager|owner|team", clean):
            missing.append("Key Decision Maker")

        return reqs, missing
