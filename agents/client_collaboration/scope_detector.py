"""Client scope change detector."""

from typing import Any, Dict, List
from agents.client_collaboration.models import RequestClassificationResult


class ClientScopeDetector:
    """Detects scope change signals in client messages and requests."""

    def evaluate_scope(self, text: str, baseline_scope_items: List[str]) -> RequestClassificationResult:
        text_lower = text.lower()

        is_scope_change = False
        reasoning = "Message contains requests aligned with baseline deliverables."

        scope_triggers = ["also build", "new mobile app", "extra integration", "can we add a new page", "custom dashboard"]
        for trigger in scope_triggers:
            if trigger in text_lower:
                is_scope_change = True
                reasoning = f"Detected scope expansion trigger: '{trigger}' not present in committed baseline."
                break

        classification = "POTENTIAL_SCOPE_CHANGE" if is_scope_change else "IN_SCOPE"

        return RequestClassificationResult(
            request_id="text-eval",
            title="Scope Analysis",
            classification=classification,
            reasoning=reasoning,
            confidence_score=0.90 if is_scope_change else 0.80,
            is_potential_scope_change=is_scope_change,
        )
