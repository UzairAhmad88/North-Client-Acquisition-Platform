from typing import Dict

CURRENT_SCORE_VERSION = "1.0"

# Formula weights summing to 1.0 (100%)
WEIGHT_CONFIG_V1: Dict[str, float] = {
    "website_need": 0.25,
    "online_presence": 0.15,
    "lead_capture": 0.15,
    "automation_potential": 0.20,
    "business_activity": 0.10,
    "contactability": 0.10,
    "service_fit": 0.05,
}


def get_band_for_score(score: float) -> str:
    """
    Explicit score bands:
    80–100 -> HIGH
    60–79  -> MEDIUM
    40–59  -> LOW
    0–39   -> VERY_LOW
    """
    r_score = round(score)
    if r_score >= 80:
        return "HIGH"
    elif r_score >= 60:
        return "MEDIUM"
    elif r_score >= 40:
        return "LOW"
    else:
        return "VERY_LOW"
