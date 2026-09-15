"""Customer Success Risk & Churn Detector."""

from decimal import Decimal
from typing import Any, Dict, List
from app.customer_success.base import RiskCategory


class CustomerSuccessRiskDetector:
    """Analyzes telemetry signals, engagement drops, payment latencies, and sentiment to detect risks."""

    def scan_for_risks(
        self,
        health_score: Decimal,
        unpaid_invoices_count: int = 0,
        days_since_last_contact: int = 0,
        critical_tickets_count: int = 0,
        negative_sentiment_ratio: float = 0.0,
        contract_days_remaining: int = 365,
    ) -> List[Dict[str, Any]]:
        """Identifies proactive risk warnings with recommended mitigation strategies."""
        detected_risks: List[Dict[str, Any]] = []

        if health_score < Decimal("50.00"):
            detected_risks.append({
                "category": RiskCategory.CHURN.value,
                "title": "Severe Health Score Degradation",
                "severity": "CRITICAL" if health_score < Decimal("35.00") else "HIGH",
                "description": f"Client composite health score is dangerously low at {health_score}%. Immediate CSM review required.",
                "mitigation_plan": "Schedule executive alignment session and conduct health audit across all active deliverables.",
            })

        if unpaid_invoices_count > 0:
            severity = "HIGH" if unpaid_invoices_count >= 2 else "MEDIUM"
            detected_risks.append({
                "category": RiskCategory.PAYMENT.value,
                "title": "Outstanding Unpaid Invoices",
                "severity": severity,
                "description": f"Client has {unpaid_invoices_count} overdue or unpaid invoice(s).",
                "mitigation_plan": "Coordinate with finance operations and schedule accounts payable check-in.",
            })

        if days_since_last_contact > 30:
            detected_risks.append({
                "category": RiskCategory.RELATIONSHIP.value,
                "title": "Extended Stakeholder Inactivity",
                "severity": "MEDIUM",
                "description": f"No recorded contact or collaboration activity in {days_since_last_contact} days.",
                "mitigation_plan": "CSM should initiate value-review check-in or share recent progress highlights.",
            })

        if critical_tickets_count > 0:
            detected_risks.append({
                "category": RiskCategory.DELIVERY.value,
                "title": "Active Critical Support Incidents",
                "severity": "CRITICAL" if critical_tickets_count > 1 else "HIGH",
                "description": f"Client currently has {critical_tickets_count} unresolved critical support incident(s).",
                "mitigation_plan": "Escalate to engineering lead and provide client with transparent resolution ETA updates.",
            })

        if negative_sentiment_ratio >= 0.4:
            detected_risks.append({
                "category": RiskCategory.SATISFACTION.value,
                "title": "Negative Sentiment Trend in Communications",
                "severity": "HIGH",
                "description": f"{int(negative_sentiment_ratio * 100)}% of recent communication messages exhibited negative sentiment.",
                "mitigation_plan": "Conduct structured CSAT / satisfaction interview to address root pain points.",
            })

        if 0 <= contract_days_remaining <= 60 and health_score < Decimal("70.00"):
            detected_risks.append({
                "category": RiskCategory.CONTRACT.value,
                "title": "Upcoming Renewal with Sub-Optimal Health",
                "severity": "HIGH",
                "description": f"Contract expires in {contract_days_remaining} days while health score is {health_score}%.",
                "mitigation_plan": "Draft targeted success plan resolving outstanding items before presenting renewal proposal.",
            })

        return detected_risks
