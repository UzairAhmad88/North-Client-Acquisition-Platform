"""
Strategic Risk Evaluation Subsystem for Phase 51.
Evaluates initiatives and portfolio vulnerabilities across 10 distinct strategic risk categories.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)


class StrategicRiskEngine:
    """Evaluates strategic, execution, security, compliance, and operational risks."""

    RISK_CATEGORIES = [
        "FINANCIAL",
        "OPERATIONAL",
        "SECURITY",
        "COMPLIANCE",
        "TECHNOLOGY",
        "CLIENT",
        "EXECUTION",
        "RESOURCE",
        "DEPENDENCY",
        "REPUTATIONAL",
    ]

    def evaluate_risk(
        self,
        title: str,
        category: str = "OPERATIONAL",
        likelihood: float = 0.3,
        impact: float = 0.6,
        mitigation_strategy: str = "Implement automated regression gating and weekly milestone reviews.",
        owner: str = "risk_lead",
    ) -> Dict[str, Any]:
        """Calculates normalized risk score (Likelihood x Impact) and returns mitigation structure."""
        l = max(0.0, min(1.0, likelihood))
        imp = max(0.0, min(1.0, impact))
        score = round(l * imp, 3)

        level = "LOW"
        if score >= 0.50:
            level = "CRITICAL"
        elif score >= 0.30:
            level = "HIGH"
        elif score >= 0.15:
            level = "MEDIUM"

        return {
            "risk_code": f"RISK-{uuid.uuid4().hex[:6].upper()}",
            "title": title,
            "category": category if category in self.RISK_CATEGORIES else "OPERATIONAL",
            "likelihood": l,
            "impact": imp,
            "risk_score": score,
            "risk_level": level,
            "mitigation_strategy": mitigation_strategy,
            "owner": owner,
        }

    def aggregate_portfolio_risk(
        self,
        risk_assessments: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Aggregates multiple risk assessments into a portfolio risk profile."""
        if not risk_assessments:
            return {
                "composite_risk_score": 0.05,
                "overall_risk_level": "LOW",
                "critical_risks_count": 0,
                "high_risks_count": 0,
            }

        avg_score = sum(r["risk_score"] for r in risk_assessments) / len(risk_assessments)
        critical_count = sum(1 for r in risk_assessments if r.get("risk_level") == "CRITICAL")
        high_count = sum(1 for r in risk_assessments if r.get("risk_level") == "HIGH")

        overall_level = "LOW"
        if critical_count > 0 or avg_score >= 0.40:
            overall_level = "CRITICAL"
        elif high_count > 0 or avg_score >= 0.25:
            overall_level = "HIGH"
        elif avg_score >= 0.12:
            overall_level = "MEDIUM"

        return {
            "composite_risk_score": round(avg_score, 3),
            "overall_risk_level": overall_level,
            "total_risks_evaluated": len(risk_assessments),
            "critical_risks_count": critical_count,
            "high_risks_count": high_count,
        }
