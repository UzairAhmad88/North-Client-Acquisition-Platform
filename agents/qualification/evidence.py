"""Qualification Evidence Collector structuring evidence linking qualification decisions to upstream sources."""

from typing import Any, Dict, List, Optional
from agents.qualification.schemas import QualificationEvidenceItem


class QualificationEvidenceCollector:
    """Collects and formats traceable evidence items from upstream intelligence sources."""

    @staticmethod
    def create_evidence_item(
        source: str,
        details: str,
        source_id: Optional[str] = None,
        finding_id: Optional[str] = None,
        confidence: str = "HIGH",
    ) -> QualificationEvidenceItem:
        return QualificationEvidenceItem(
            source=source,
            source_id=source_id,
            finding_id=finding_id,
            confidence=confidence,
            details=details,
        )
