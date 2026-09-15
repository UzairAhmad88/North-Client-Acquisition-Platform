"""Buying signal detector classifying prospect purchasing intent levels."""

import re
from typing import List
from agents.response.models import BuyingSignalDetail


class BuyingSignalDetector:
    """Detects buying signals in inbound messages."""

    STRONG_PATTERNS = [r"proposal", r"send\s+contract", r"schedule\s+a\s+call", r"when\s+can\s+we\s+start", r"pricing\s+options"]
    MODERATE_PATTERNS = [r"how\s+much", r"interested", r"case\s+studies?", r"portfolio", r"tell\s+me\s+more"]

    @staticmethod
    def detect(text: str) -> BuyingSignalDetail:
        clean = (text or "").lower()
        signals: List[str] = []

        for pat in BuyingSignalDetector.STRONG_PATTERNS:
            if re.search(pat, clean):
                signals.append(f"Strong signal match: '{pat}'")

        if signals:
            return BuyingSignalDetail(level="STRONG", signals=signals)

        for pat in BuyingSignalDetector.MODERATE_PATTERNS:
            if re.search(pat, clean):
                signals.append(f"Moderate signal match: '{pat}'")

        if signals:
            return BuyingSignalDetail(level="MODERATE", signals=signals)

        return BuyingSignalDetail(level="NONE", signals=[])
