"""Confidence Calculation Module for Research Findings."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class ResearchConfidenceCalculator:
    """Calculates confidence levels for individual research findings and overall run."""

    @staticmethod
    def calculate_finding_confidence(
        source_trust: str,
        has_corroboration: bool = False,
        is_fresh: bool = True,
        has_conflict: bool = False,
    ) -> str:
        """Compute confidence level (HIGH, MEDIUM, LOW) based on source trust, freshness, and conflicts."""
        if has_conflict:
            return "LOW"

        if source_trust in ("OFFICIAL", "HIGH_TRUST") and is_fresh:
            return "HIGH"

        if source_trust in ("OFFICIAL", "HIGH_TRUST") or (source_trust == "MEDIUM_TRUST" and has_corroboration):
            return "MEDIUM"

        return "LOW"

    @staticmethod
    def calculate_overall_confidence(findings: List[Dict[str, Any]], conflicts: List[Any]) -> str:
        """Calculate overall confidence for the research agent output."""
        if len(conflicts) > 0:
            return "MEDIUM"

        if not findings:
            return "LOW"

        high_count = sum(1 for f in findings if f.get("confidence") == "HIGH")
        if high_count >= len(findings) / 2 and high_count > 0:
            return "HIGH"

        return "MEDIUM"
