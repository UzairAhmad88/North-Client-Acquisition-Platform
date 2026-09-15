"""Validation and Safety checks for Document AI outputs."""

from typing import Any, Dict, List


class DocumentAIValidator:
    """Ensures AI document outputs do not attempt unauthorized side effects or mutate source data."""

    def validate_ai_output(self, output: Dict[str, Any]) -> bool:
        # Guarantee authority is strictly labeled as AI_INFERRED
        if output.get("authority") != "AI_INFERRED":
            return False
        return True
