"""Generator for natural language recommendation reasons, evidence items, and objective limitations."""

from typing import Any, Dict, List, Tuple

from app.services.recommendations.components import (
    ComponentScoreResult,
    RecommendationContext,
    RecommendationSignal,
)


class ExplanationGenerator:
    """Generates explanations, collects evidence links, and determines confidence & limitations."""

    @staticmethod
    def generate_explanations_evidence_limitations(
        component_scores: Dict[str, ComponentScoreResult],
        context: RecommendationContext,
    ) -> Tuple[List[str], List[Dict[str, Any]], List[str], str]:
        """Produce reasons, evidence dicts, limitations list, and confidence rating.

        Returns:
            Tuple of (reasons, evidence, limitations, confidence)
        """
        reasons: List[str] = []
        evidence: List[Dict[str, Any]] = []
        limitations: List[str] = []

        all_signals: List[RecommendationSignal] = []
        for comp in component_scores.values():
            all_signals.extend(comp.signals)
            for r in comp.reasons:
                if r not in reasons:
                    reasons.append(r)

        # Build evidence list
        for sig in all_signals:
            ev_item = {
                "source": sig.source,
                "source_id": sig.source_id,
                "type": sig.signal,
                "description": sig.description,
                "strength": sig.strength,
                "confidence": sig.confidence,
            }
            if ev_item not in evidence:
                evidence.append(ev_item)

        # Determine confidence level
        high_conf_signals = [s for s in all_signals if s.confidence == "HIGH"]
        if len(high_conf_signals) >= 2 and context.audit and context.research_records:
            confidence = "HIGH"
        elif len(all_signals) >= 1 or (context.audit or context.research_records):
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        # Determine objective limitations
        if not context.audit:
            limitations.append("Technical website audit was not performed or is unavailable for this business.")
        else:
            limitations.append("Audit findings are based on publicly accessible web pages.")

        if not context.research_records:
            limitations.append("Public research data was not collected or is minimal.")

        limitations.append("Internal business operations, staff preferences, and budget constraints were not directly evaluated.")
        limitations.append("Customer demand and sales readiness for this service require human qualification.")

        if not reasons:
            reasons.append("General service catalog alignment based on business domain.")

        return reasons, evidence, limitations, confidence
