"""Executive Briefing Generation (Daily/Weekly/Monthly) and Strategic Business Calendar."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

from app.business_os.base import BriefingFrequency


class BusinessCalendarEvent(BaseModel):
    event_id: str
    title: str
    event_type: str  # RENEWAL, INVOICE_DUE, MILESTONE, UAT, STRATEGIC_REVIEW, SUPPORT_SLA
    event_date: str
    related_entity_id: str
    related_entity_name: str
    severity: str  # NORMAL, HIGH, CRITICAL
    owner: str
    is_completed: bool = False


class ExecutiveBriefingReport(BaseModel):
    briefing_id: str
    frequency: BriefingFrequency
    title: str
    summary_paragraph: str
    key_metrics_snapshot: Dict[str, Any] = Field(default_factory=dict)
    what_changed_summary: List[str] = Field(default_factory=list)
    top_decisions_required: List[Dict[str, Any]] = Field(default_factory=list)
    critical_risks: List[Dict[str, Any]] = Field(default_factory=list)
    upcoming_deadlines: List[BusinessCalendarEvent] = Field(default_factory=list)
    recommended_attention_areas: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExecutiveBriefingEngine:
    """Generates structured, executive-level briefings from across operational domains."""

    def __init__(self):
        pass

    def get_upcoming_calendar_events(self) -> List[BusinessCalendarEvent]:
        """Aggregates critical dates across all platform subsystems."""
        return [
            BusinessCalendarEvent(
                event_id="cal_1",
                title="Acme Global Retainer Contract Renewal",
                event_type="RENEWAL",
                event_date="2026-10-20",
                related_entity_id="client_acme",
                related_entity_name="Acme Global Logistics",
                severity="HIGH",
                owner="Head of Customer Success",
            ),
            BusinessCalendarEvent(
                event_id="cal_2",
                title="Zenith Retail Milestone M3 UAT Signoff",
                event_type="UAT",
                event_date="2026-10-15",
                related_entity_id="proj_beta",
                related_entity_name="Zenith Retail Corp",
                severity="HIGH",
                owner="Senior Tech Lead B",
            ),
            BusinessCalendarEvent(
                event_id="cal_3",
                title="Apex Financial Invoiced Milestone Payment Due (PKR 1.2M)",
                event_type="INVOICE_DUE",
                event_date="2026-09-15",
                related_entity_id="inv_apex_001",
                related_entity_name="Apex Financial",
                severity="NORMAL",
                owner="Finance",
            ),
            BusinessCalendarEvent(
                event_id="cal_4",
                title="Q4 Strategic OKR & Portfolio Alignment Review",
                event_type="STRATEGIC_REVIEW",
                event_date="2026-09-30",
                related_entity_id="strat_q4",
                related_entity_name="Uzaii Executive Board",
                severity="CRITICAL",
                owner="Executive Office",
            ),
        ]

    def generate_briefing(
        self,
        frequency: BriefingFrequency = BriefingFrequency.DAILY,
        executive_name: str = "Executive Leader",
    ) -> ExecutiveBriefingReport:
        briefing_id = f"brf_{uuid.uuid4().hex[:8]}"
        calendar_events = self.get_upcoming_calendar_events()

        if frequency == BriefingFrequency.DAILY:
            title = f"Daily Executive Briefing — {datetime.now(timezone.utc).strftime('%A, %B %d, %Y')}"
            summary = (
                f"Good morning, {executive_name}. Platform operations are stable with 99.95% uptime and a composite "
                "Business Health index of 81.6/100 (HEALTHY). Active pipeline stands at PKR 12.4M with 3 critical "
                "action items requiring executive prioritization."
            )
            what_changed = [
                "Apex Financial contract initiation phase completed successfully.",
                "AI inference token spend stabilized following semantic cache enablement.",
                "Zenith Retail milestone load testing identified potential 4-day schedule delay.",
            ]
        elif frequency == BriefingFrequency.WEEKLY:
            title = f"Weekly Business Review — Week {datetime.now(timezone.utc).strftime('%U, %Y')}"
            summary = (
                "Weekly operations overview: Revenue pacing on track at PKR 3.8M MRR towards the PKR 5.0M quarterly target. "
                "Engineering capacity utilization is tight at 95.8% across active client delivery squads."
            )
            what_changed = [
                "Converted 2 enterprise discovery sessions into active proposal reviews.",
                "Customer support SLA resolution achieved 98.2% (exceeding 95% target).",
                "Two lead engineers reached > 110% capacity utilization.",
            ]
        else:
            title = f"Monthly Strategic Intelligence Review — {datetime.now(timezone.utc).strftime('%B %Y')}"
            summary = (
                "Monthly strategic synthesis: 76% progress across active Q3/Q4 Strategic OKRs. "
                "Gross margins maintained at 65.4% with zero unmitigated SEV-1 operational incidents."
            )
            what_changed = [
                "Net client retention closed at 94.5% across the recurring retainer portfolio.",
                "Closed-loop decision learning recorded 92% accuracy on engineering contractor trade-offs.",
            ]

        metrics_snap = {
            "monthly_recurring_revenue": "PKR 3,800,000",
            "gross_profit_margin": "65.4%",
            "weighted_pipeline": "PKR 12,400,000",
            "active_client_retention": "94.5%",
            "platform_uptime": "99.95%",
            "composite_business_health": "81.6/100 (HEALTHY)",
        }

        decisions_req = [
            {
                "decision_id": "dec_cap_zenith",
                "title": "Q4 Engineering Capacity Reallocation vs Contractor Onboarding",
                "priority": "P1_HIGH",
                "summary": "Choose between shifting Acme ERP slack hours vs engaging external specialist contractor.",
            }
        ]

        risks = [
            {
                "risk_id": "risk_cap_zenith",
                "title": "Q4 Engineering Capacity Bottleneck",
                "severity": "HIGH",
                "mitigation": "Shift code review duties and evaluate contractor support.",
            },
            {
                "risk_id": "risk_acme_renewal",
                "title": "High-Value Client Renewal (Acme Logistics)",
                "severity": "HIGH",
                "mitigation": "Schedule Executive Business Review with new sponsor.",
            },
        ]

        attention = [
            "Review Decision Queue item regarding Zenith Retail engineering capacity reallocation.",
            "Confirm attendance for Acme Logistics Executive Business Review (EBR) briefing.",
            "Monitor outstanding accounts receivable overdue invoices (>= PKR 1.2M).",
        ]

        return ExecutiveBriefingReport(
            briefing_id=briefing_id,
            frequency=frequency,
            title=title,
            summary_paragraph=summary,
            key_metrics_snapshot=metrics_snap,
            what_changed_summary=what_changed,
            top_decisions_required=decisions_req,
            critical_risks=risks,
            upcoming_deadlines=calendar_events,
            recommended_attention_areas=attention,
        )
