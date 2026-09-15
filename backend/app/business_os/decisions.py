"""Executive Decision Queue, Option Trade-Off Analysis & Strategic Learning Loop."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field

from app.business_os.base import DecisionOption, DecisionPriority, DecisionStatus


class DecisionRecord(BaseModel):
    decision_id: str
    title: str
    business_question: str
    context_summary: str
    priority: DecisionPriority
    status: DecisionStatus
    candidate_options: List[DecisionOption] = Field(default_factory=list)
    ai_recommendation: Optional[str] = None
    ai_recommendation_rationale: Optional[str] = None
    chosen_option_id: Optional[str] = None
    chosen_option_title: Optional[str] = None
    decision_rationale: Optional[str] = None
    decided_by: Optional[str] = None
    decided_at: Optional[datetime] = None
    evidence_signals: List[str] = Field(default_factory=list)
    expected_outcome: str = ""
    actual_outcome: Optional[str] = None
    outcome_variance_analysis: Optional[str] = None
    lessons_learned: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    review_due_date: Optional[str] = None


class DecisionIntelligenceEngine:
    """Manages strategic decision records, option generation, approvals, and post-outcome learning."""

    def __init__(self):
        self._decisions: Dict[str, DecisionRecord] = {}
        self._seed_default_decisions()

    def _seed_default_decisions(self) -> None:
        dec1 = self.create_decision_item(
            title="Q4 Engineering Capacity Reallocation vs Contractor Onboarding",
            business_question="How should we address the 118% lead engineer utilization on Zenith Retail without risking delivery dates?",
            context_summary="Committed project tasks exceed sprint capacity by ~16 hours/week across core backend and AI modules.",
            priority=DecisionPriority.P1_HIGH,
            evidence_signals=[
                "Lead engineer utilization: 118%",
                "Zenith milestone delivery deadline: 35 days remaining",
                "Acme ERP project on track with 15% slack capacity",
            ],
            expected_outcome="Milestone delivered within <= 3 days of baseline with zero regression defects and lead engineer utilization normalized to <= 95%.",
        )

        # Generate candidate options
        opt_a = DecisionOption(
            option_id="opt_contractor",
            title="Option A: Onboard Pre-Vetted Specialist Contractor",
            description="Engage dedicated senior contractor for 4 weeks to absorb UI/integration tasks.",
            expected_benefits=["Immediate relief of 20h/week for core leads", "Maintains original delivery date"],
            expected_costs=["Additional PKR 250,000 project expense (decreases project margin from 60% to 52%)"],
            risks=["2-3 day ramp-up time for codebase orientation"],
            dependencies=["Fast-track contractor NDA & access provisioning"],
            estimated_impact="High delivery certainty; minor margin reduction",
            confidence="HIGH",
            evidence_references=["Contractor rate card v2.1", "Workload snapshot week 36"],
        )
        opt_b = DecisionOption(
            option_id="opt_reallocate",
            title="Option B: Reallocate Internal Slack Capacity from Acme ERP",
            description="Temporarily shift 15h/week from Acme ERP non-critical polish sprint to Zenith Retail.",
            expected_benefits=["Zero incremental cash expense", "Zero external contractor onboarding overhead"],
            expected_costs=["Reduces contingency buffer on Acme ERP by 4 days"],
            risks=["Requires coordination across two client delivery leads"],
            dependencies=["Acme lead approval"],
            estimated_impact="Preserves gross margin; requires cross-project coordination",
            confidence="HIGH",
            evidence_references=["Acme ERP schedule buffer report", "Workload capacity matrix"],
        )
        opt_c = DecisionOption(
            option_id="opt_extend_milestone",
            title="Option C: Negotiate 1-Week Schedule Buffer Extension with Zenith",
            description="Discuss moving UAT signoff milestone by 7 calendar days to accommodate thorough load testing.",
            expected_benefits=["Avoids burnout and preserves maximum engineering quality", "Zero cost impact"],
            expected_costs=["Customer satisfaction risk if not communicated proactively"],
            risks=["Client project launch timeline sensitivity"],
            dependencies=["Customer Success partner alignment"],
            estimated_impact="Highest technical quality; slight client relationship friction",
            confidence="MEDIUM",
            evidence_references=["Zenith contract flexibility clause 4.2"],
        )

        dec1.candidate_options = [opt_a, opt_b, opt_c]
        dec1.ai_recommendation = "Option B (Reallocate Internal Slack Capacity)"
        dec1.ai_recommendation_rationale = "Preserves target 60% gross margin while delivering on time using internal vetted talent with zero onboarding lag."

    def create_decision_item(
        self,
        title: str,
        business_question: str,
        context_summary: str,
        priority: DecisionPriority = DecisionPriority.P1_HIGH,
        evidence_signals: Optional[List[str]] = None,
        expected_outcome: str = "",
        review_due_date: Optional[str] = None,
    ) -> DecisionRecord:
        decision_id = f"dec_{uuid.uuid4().hex[:8]}"
        record = DecisionRecord(
            decision_id=decision_id,
            title=title,
            business_question=business_question,
            context_summary=context_summary,
            priority=priority,
            status=DecisionStatus.DECISION_REQUIRED,
            evidence_signals=evidence_signals or [],
            expected_outcome=expected_outcome,
            review_due_date=review_due_date,
        )
        self._decisions[decision_id] = record
        return record

    def record_human_decision(
        self,
        decision_id: str,
        chosen_option_id: str,
        decision_rationale: str,
        decided_by: str,
    ) -> Optional[DecisionRecord]:
        """
        Records human executive authorization and selected course of action.
        Upholds the Business OS rule: Humans decide; AI provides decision support.
        """
        record = self._decisions.get(decision_id)
        if not record:
            return None

        chosen_title = ""
        for opt in record.candidate_options:
            if opt.option_id == chosen_option_id:
                chosen_title = opt.title
                break

        record.chosen_option_id = chosen_option_id
        record.chosen_option_title = chosen_title or chosen_option_id
        record.decision_rationale = decision_rationale
        record.decided_by = decided_by
        record.decided_at = datetime.now(timezone.utc)
        record.status = DecisionStatus.DECIDED
        return record

    def record_decision_outcome(
        self,
        decision_id: str,
        actual_outcome: str,
        outcome_variance_analysis: str,
        lessons_learned: List[str],
    ) -> Optional[DecisionRecord]:
        """
        Closes the Strategic Learning Loop by recording actual results versus expected targets.
        """
        record = self._decisions.get(decision_id)
        if not record:
            return None

        record.actual_outcome = actual_outcome
        record.outcome_variance_analysis = outcome_variance_analysis
        record.lessons_learned = lessons_learned
        record.status = DecisionStatus.COMPLETED
        return record

    def get_decision(self, decision_id: str) -> Optional[DecisionRecord]:
        return self._decisions.get(decision_id)

    def list_decisions(self, status: Optional[DecisionStatus] = None) -> List[DecisionRecord]:
        if status:
            return [d for d in self._decisions.values() if d.status == status]
        return list(self._decisions.values())
