from typing import Dict

from app.services.scoring.models import ComponentScoreResult


class ExplanationGenerator:
    @staticmethod
    def generate_explanation(
        total_score: float,
        band: str,
        component_scores: Dict[str, ComponentScoreResult],
    ) -> str:
        lines = [f"Lead Opportunity Score: {round(total_score)} — {band}"]

        top_drivers = []
        for comp_name, res in component_scores.items():
            if res.score >= 70.0 and res.reasons:
                top_drivers.append(f"- {res.reasons[0]} (+{res.weighted_contribution} pts)")

        if top_drivers:
            lines.append("Key Opportunity Drivers:")
            lines.extend(top_drivers[:4])

        return "\n".join(lines)
