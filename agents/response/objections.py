"""Objection detection subsystem classifying client reservations."""

import re
from typing import Optional
from agents.response.models import DetectedObjection


class ObjectionClassifier:
    """Classifies sales objections from inbound prospect responses."""

    OBJECTION_PATTERNS = {
        "PRICE": [r"too\s+expensive", r"cost\s+too\s+much", r"high\s+price", r"outside\s+our\s+budget"],
        "TIMING": [r"busy\s+right\s+now", r"bad\s+time", r"next\s+quarter", r"next\s+year", r"not\s+now"],
        "ALREADY_HAVE_PROVIDER": [r"already\s+have", r"current\s+vendor", r"existing\s+agency", r"in-house\s+team"],
        "NO_BUDGET": [r"no\s+budget", r"budget\s+frozen", r"cut\s+costs"],
        "AUTHORITY": [r"not\s+my\s+decision", r"need\s+boss\s+approval", r"speak\s+to\s+my\s+manager"],
    }

    @staticmethod
    def detect(text: str) -> Optional[DetectedObjection]:
        clean = (text or "").lower()
        for obj_type, regexes in ObjectionClassifier.OBJECTION_PATTERNS.items():
            for pat in regexes:
                if re.search(pat, clean):
                    return DetectedObjection(
                        type=obj_type,
                        confidence="HIGH",
                        detail=f"Detected objection keyword matching pattern '{pat}'",
                    )
        return None
