"""Enterprise Organizational Risk Register, Severity Scoring & Mitigation Engine."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

from app.business_os.base import (
    RiskCategory,
    RiskImpact,
    RiskLifecycleStatus,
    RiskProbability,
    RiskSeverity,
)


class RiskRecord(BaseModel):
    risk_id: str
    title: str
    description: str
    category: RiskCategory
    probability: RiskProbability
    impact: RiskImpact
    risk_score: int  # Probability (1-5) * Impact (1-5)
    severity: RiskSeverity
    owner: str
    status: RiskLifecycleStatus
    identified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: Optional[str] = None
    evidence_signals: List[str] = Field(default_factory=list)
    mitigation_strategy: str = ""
    contingency_plan: str = ""
    last_reviewed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OrganizationalRiskRegister:
    """Manages enterprise-wide organizational risk matrix and mitigation workflows."""

    PROBABILITY_WEIGHTS = {
        RiskProbability.RARE: 1,
        RiskProbability.UNLIKELY: 2,
        RiskProbability.POSSIBLE: 3,
        RiskProbability.LIKELY: 4,
        RiskProbability.ALMOST_CERTAIN: 5,
    }

    IMPACT_WEIGHTS = {
        RiskImpact.MINOR: 1,
        RiskImpact.MODERATE: 2,
        RiskImpact.MAJOR: 3,
        RiskImpact.SEVERE: 4,
        RiskImpact.CRITICAL: 5,
    }

    def __init__(self):
        self._risks: Dict[str, RiskRecord] = {}
        self._seed_default_risks()

    def _calculate_score_and_severity(
        self, probability: RiskProbability, impact: RiskImpact
    ) -> tuple[int, RiskSeverity]:
        p_val = self.PROBABILITY_WEIGHTS.get(probability, 3)
        i_val = self.IMPACT_WEIGHTS.get(impact, 3)
        score = p_val * i_val

        if score >= 15:
            severity = RiskSeverity.CRITICAL
        elif score >= 10:
            severity = RiskSeverity.HIGH
        elif score >= 5:
            severity = RiskSeverity.MEDIUM
        else:
            severity = RiskSeverity.LOW

        return score, severity

    def _seed_default_risks(self) -> None:
        self.register_risk(
            title="Q4 Engineering Capacity Bottleneck",
            description="High committed project workload (118% lead engineer utilization) risks delivery delays on Zenith Retail milestone.",
            category=RiskCategory.RESOURCE,
            probability=RiskProbability.LIKELY,
            impact=RiskImpact.MAJOR,
            owner="VP Engineering",
            evidence_signals=[
                "Lead Fullstack Engineer assigned 46h/week",
                "Zenith Retail milestone due in 35 days with 2 pending dependencies",
            ],
            mitigation_strategy="Shift code review & testing responsibilities to dedicated QA engineer; reassign non-blocking task modules.",
            contingency_plan="Activate pre-qualified external contractor for frontend polish tasks.",
        )

        self.register_risk(
            title="High-Value Client Renewal Risk (Acme Logistics)",
            description="Recent stakeholder turnover at Acme Logistics could delay annual retainer contract renewal.",
            category=RiskCategory.CLIENT,
            probability=RiskProbability.POSSIBLE,
            impact=RiskImpact.SEVERE,
            owner="Head of Customer Success",
            evidence_signals=[
                "Primary sponsor moved to new role",
                "Contract renewal date in 45 days (PKR 3,500,000 value)",
            ],
            mitigation_strategy="Schedule Executive Business Review (EBR) with new incoming VP of Operations.",
            contingency_plan="Prepare flexible multi-year renewal concession package.",
        )

        self.register_risk(
            title="AI Model Inference Cost Spike",
            description="Unoptimized autonomous research loops increasing monthly token usage spend by 22%.",
            category=RiskCategory.AI,
            probability=RiskProbability.LIKELY,
            impact=RiskImpact.MODERATE,
            owner="Lead AI Architect",
            evidence_signals=[
                "AI spend reached PKR 240,000 this billing period (budget PKR 200,000)",
                "Research agent average token consumption per lead increased 30%",
            ],
            mitigation_strategy="Enable strict semantic cache and enforce smaller model routing for preliminary summarization tasks.",
            contingency_plan="Impose hard monthly spending quota on automated lead enrichment pipelines.",
        )

    def register_risk(
        self,
        title: str,
        description: str,
        category: RiskCategory,
        probability: RiskProbability,
        impact: RiskImpact,
        owner: str,
        evidence_signals: Optional[List[str]] = None,
        mitigation_strategy: str = "",
        contingency_plan: str = "",
        due_date: Optional[str] = None,
    ) -> RiskRecord:
        score, severity = self._calculate_score_and_severity(probability, impact)
        risk_id = f"risk_{uuid.uuid4().hex[:8]}"

        record = RiskRecord(
            risk_id=risk_id,
            title=title,
            description=description,
            category=category,
            probability=probability,
            impact=impact,
            risk_score=score,
            severity=severity,
            owner=owner,
            status=RiskLifecycleStatus.ASSESSED,
            evidence_signals=evidence_signals or [],
            mitigation_strategy=mitigation_strategy,
            contingency_plan=contingency_plan,
            due_date=due_date,
        )
        self._risks[risk_id] = record
        return record

    def get_risk(self, risk_id: str) -> Optional[RiskRecord]:
        return self._risks.get(risk_id)

    def list_risks(
        self,
        category: Optional[RiskCategory] = None,
        min_severity: Optional[RiskSeverity] = None,
    ) -> List[RiskRecord]:
        results = list(self._risks.values())
        if category:
            results = [r for r in results if r.category == category]
        if min_severity:
            sev_order = [RiskSeverity.LOW, RiskSeverity.MEDIUM, RiskSeverity.HIGH, RiskSeverity.CRITICAL]
            min_idx = sev_order.index(min_severity)
            results = [r for r in results if sev_order.index(r.severity) >= min_idx]

        # Sort by risk score descending
        return sorted(results, key=lambda r: r.risk_score, reverse=True)

    def update_risk_status(
        self, risk_id: str, new_status: RiskLifecycleStatus, mitigation_notes: Optional[str] = None
    ) -> Optional[RiskRecord]:
        record = self.get_risk(risk_id)
        if not record:
            return None
        record.status = new_status
        if mitigation_notes:
            record.mitigation_strategy += f" [Update: {mitigation_notes}]"
        record.last_reviewed_at = datetime.now(timezone.utc)
        return record
