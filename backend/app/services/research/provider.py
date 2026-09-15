from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.models.business import Business


@dataclass
class ResearchEvidence:
    field_name: str
    raw_value: str
    normalized_value: str
    # Research types: IDENTITY, CONTACT, LOCATION, SERVICES,
    # WEBSITE, SOCIAL, HOURS, DESCRIPTION, PUBLIC_REVIEWS, GENERAL
    research_type: str
    source_url: Optional[str]
    source_trust: str  # OFFICIAL, HIGH_TRUST, MEDIUM_TRUST, LOW_TRUST, UNKNOWN
    confidence: str  # HIGH, MEDIUM, LOW
    evidence_text: Optional[str] = None
    observed_at: Optional[datetime] = None
    meta_info: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.observed_at:
            self.observed_at = datetime.now(timezone.utc)


class ResearchProvider(ABC):
    @abstractmethod
    async def research(
        self,
        business: Business,
        sections: List[str],
    ) -> List[ResearchEvidence]:
        """Collect research evidence for a business across requested sections."""
        pass
