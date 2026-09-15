"""Audit confidence calculator determining measurement certainty and overall audit confidence."""

from typing import Any, Dict, List
from agents.audit.schemas import AuditFindingItem


class AuditConfidenceCalculator:
    """Calculates finding confidence and overall audit confidence score."""

    @staticmethod
    def calculate_finding_confidence(
        is_direct_observation: bool = True,
        is_fresh: bool = True,
        has_corroboration: bool = True,
    ) -> str:
        if is_direct_observation and is_fresh:
            return "HIGH"
        if is_direct_observation or (is_fresh and has_corroboration):
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def calculate_overall_confidence(
        findings: List[AuditFindingItem],
        pages_analyzed: int = 1,
    ) -> str:
        if pages_analyzed == 0:
            return "LOW"

        if not findings:
            return "HIGH"

        low_count = sum(1 for f in findings if f.confidence == "LOW")
        if low_count > len(findings) / 2:
            return "LOW"

        medium_count = sum(1 for f in findings if f.confidence == "MEDIUM")
        if (medium_count + low_count) > len(findings) / 2:
            return "MEDIUM"

        return "HIGH"
