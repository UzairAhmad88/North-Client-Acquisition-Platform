WEIGHTS = {
    "website_need": 0.25,
    "online_presence": 0.15,
    "lead_capture": 0.15,
    "automation_potential": 0.20,
    "business_activity": 0.10,
    "contactability": 0.10,
    "service_fit": 0.05,
}


def score(features: dict[str, float]) -> float:
    return round(sum(features.get(k, 0) * w for k, w in WEIGHTS.items()), 2)
