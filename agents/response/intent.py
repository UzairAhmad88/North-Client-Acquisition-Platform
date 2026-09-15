"""Intent classification engine for inbound response messages."""

import re
from typing import List, Tuple


class IntentClassifier:
    """Classifies client intent from message text using deterministic rules and pattern matching."""

    PATTERNS = {
        "OPT_OUT": [r"\bstop\b", r"\bunsubscribe\b", r"don'?t\s+contact", r"remove\s+me"],
        "REQUEST_FOR_PRICE": [r"how\s+much", r"cost", r"price", r"pricing", r"rate", r"quote"],
        "REQUEST_FOR_MEETING": [r"call", r"meeting", r"schedule", r"zoom", r"talk", r"discuss\s+on\s+phone"],
        "REQUEST_FOR_PORTFOLIO": [r"portfolio", r"case\s+study", r"examples?", r"previous\s+work", r"samples?"],
        "REQUEST_FOR_DETAILS": [r"more\s+info", r"details", r"tell\s+me\s+more", r"how\s+does\s+it\s+work"],
        "INTERESTED": [r"interested", r"sounds\s+good", r"would\s+love\s+to", r"let'?s\s+do\s+it", r"yes"],
        "NOT_INTERESTED": [r"not\s+interested", r"no\s+thanks", r"pass", r"not\s+at\s+this\s+time"],
        "WRONG_PERSON": [r"wrong\s+person", r"not\s+responsible", r"no\s+longer\s+here", r"contact\s+someone\s+else"],
    }

    @staticmethod
    def classify(text: str) -> Tuple[str, List[str], str]:
        """Classify message intent. Returns (primary_intent, all_intents, confidence)."""
        clean = (text or "").lower().strip()
        matched_intents: List[str] = []

        for intent, regexes in IntentClassifier.PATTERNS.items():
            for pat in regexes:
                if re.search(pat, clean):
                    if intent not in matched_intents:
                        matched_intents.append(intent)
                    break

        if not matched_intents:
            return "AMBIGUOUS", ["AMBIGUOUS"], "LOW"

        # Deterministic hierarchy for primary intent
        priority_order = [
            "OPT_OUT",
            "WRONG_PERSON",
            "REQUEST_FOR_MEETING",
            "REQUEST_FOR_PRICE",
            "REQUEST_FOR_PORTFOLIO",
            "REQUEST_FOR_DETAILS",
            "NOT_INTERESTED",
            "INTERESTED",
        ]
        for p in priority_order:
            if p in matched_intents:
                return p, matched_intents, "HIGH"

        return matched_intents[0], matched_intents, "MEDIUM"
