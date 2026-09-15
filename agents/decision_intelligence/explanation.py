"""Prediction Explanation & Calibrated Driver Extraction Engine."""

from typing import Any, Dict, List
import re


class ExplanationEngine:
    """Generates transparent, human-readable explanations using calibrated, non-presumptuous language."""

    FORBIDDEN_CERTAINTY_WORDS = [
        r"\bdefinitely\b",
        r"\bguaranteed\b",
        r"\bcertainly\b",
        r"\bwill happen\b",
        r"\bimpossible\b",
        r"\b100% sure\b",
    ]

    def sanitize_explanation_text(self, text: str) -> str:
        """Enforce calibrated, probabilistic phrasing by stripping inappropriate certainty claims."""
        sanitized = text
        for pattern in self.FORBIDDEN_CERTAINTY_WORDS:
            sanitized = re.sub(pattern, "probabilistically estimated to", sanitized, flags=re.IGNORECASE)
        return sanitized

    def format_driver_summary(
        self,
        prediction_type: str,
        probability: float,
        drivers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Construct calibrated feature attribution summary."""
        ranked_drivers = sorted(drivers, key=lambda d: abs(float(str(d.get("impact", "0")).replace("+", ""))), reverse=True)

        driver_bullets = [
            f"• {d['feature']}: observed value '{d['value']}' (estimated contribution {d['impact']})"
            for d in ranked_drivers[:4]
        ]

        summary = (
            f"Model estimates a {int(probability * 100)}% probability for {prediction_type.replace('_', ' ').lower()}. "
            f"Primary contributing indicators:\n" + "\n".join(driver_bullets)
        )

        return {
            "summary_text": self.sanitize_explanation_text(summary),
            "ranked_drivers": ranked_drivers,
            "safety_disclaimer": "Probabilistic estimate derived from historical operational signals. Requires human review.",
        }
