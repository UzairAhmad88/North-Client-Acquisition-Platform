"""Reusable Confidence Utility and Evidence Validator for Agent Output."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from agents.core.errors import AgentOutputInvalidError


@dataclass
class EvidenceItem:
    """Standard traceable evidence item."""

    type: str
    source: str
    summary: str
    id: str = ""
    field: str = ""
    confidence: str = "MEDIUM"


@dataclass
class ConfidenceRating:
    """Structured confidence evaluation with justification reasons."""

    level: str  # HIGH, MEDIUM, LOW
    reasons: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.level = self.level.upper()
        if self.level not in ("HIGH", "MEDIUM", "LOW"):
            raise ValueError(f"Invalid confidence level '{self.level}'. Must be HIGH, MEDIUM, or LOW.")


class ConfidenceValidator:
    """Enforces evidence requirements on agent output confidence levels."""

    @staticmethod
    def validate_confidence(
        level: str,
        evidence: List[Dict[str, Any]],
        reasons: List[str],
    ) -> ConfidenceRating:
        """Validate confidence rating against available evidence.

        Agents cannot claim HIGH confidence without at least one explicit evidence item.
        """
        lvl = level.upper()
        if lvl == "HIGH" and len(evidence) == 0:
            # Downgrade or reject
            reasons.append("Confidence downgraded from HIGH to MEDIUM: No supporting evidence items supplied.")
            lvl = "MEDIUM"

        return ConfidenceRating(level=lvl, reasons=reasons)
