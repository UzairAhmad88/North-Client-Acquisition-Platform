"""Confidence calculator rating personalization groundedness."""

from typing import Any, Dict, List


class PersonalizationConfidenceCalculator:
    """Calculates evidence-backed confidence for personalization profiles."""

    @staticmethod
    def calculate_confidence(
        evidence_list: List[Dict[str, Any]],
        qualification_data: Dict[str, Any],
    ) -> str:
        qual_decision = qualification_data.get("decision") or qualification_data.get("human_override_decision")
        evidence_count = len(evidence_list)

        if qual_decision == "QUALIFIED" and evidence_count >= 2:
            return "HIGH"
        elif qual_decision in ("QUALIFIED", "POTENTIALLY_QUALIFIED") and evidence_count >= 1:
            return "MEDIUM"
        else:
            return "LOW"
