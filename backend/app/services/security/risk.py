"""Explainable Multi-Factor Risk Scoring Service."""
from typing import Dict, Any

class SecurityRiskScoringService:
    def calculate_risk_score(self, identity_risk: float, asset_criticality_weight: float, vuln_score: float) -> Dict[str, Any]:
        composite = round((identity_risk * 0.3) + (asset_criticality_weight * 0.3) + (vuln_score * 0.04), 2)
        return {
            "composite_risk_score": min(1.0, composite),
            "level": "CRITICAL" if composite >= 0.8 else "HIGH" if composite >= 0.6 else "MEDIUM" if composite >= 0.3 else "LOW",
            "breakdown": {
                "identity_risk_contribution": identity_risk * 0.3,
                "asset_criticality_contribution": asset_criticality_weight * 0.3,
                "vulnerability_contribution": vuln_score * 0.04,
            }
        }
