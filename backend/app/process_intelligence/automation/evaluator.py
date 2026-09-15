"""
Automation Candidate Evaluator for Phase 49: Computes 8-factor suitability scores for workflow automation candidates.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.process_intelligence.base import AutomationCandidate, AutomationSuitability
    from backend.app.process_intelligence.event_log.store import ProcessEventLogStore
except ImportError:
    from app.process_intelligence.base import AutomationCandidate, AutomationSuitability
    from app.process_intelligence.event_log.store import ProcessEventLogStore


class AutomationCandidateEvaluator:
    """Evaluates repetitive, deterministic manual tasks for safe workflow automation."""

    def __init__(self, event_store: ProcessEventLogStore):
        self.event_store = event_store

    def evaluate_task(
        self,
        process_id: str,
        task_name: str,
        frequency_per_month: int,
        average_duration_minutes: float,
        error_rate: float,  # 0.0 to 1.0
        determinism_score: float = 0.8,  # 0.0 to 1.0
        data_availability_score: float = 0.9,  # 0.0 to 1.0
        business_value_score: float = 0.7,  # 0.0 to 1.0
        risk_score: float = 0.2,  # 0.0 (safe) to 1.0 (dangerous)
        reversibility: str = "HIGH",  # HIGH, MODERATE, LOW, IRREVERSIBLE
        tenant_id: str = "default_tenant",
    ) -> AutomationCandidate:
        """Computes the 8-factor Automation Suitability Score and risk classification."""
        # Normalize factors
        freq_norm = min(1.0, frequency_per_month / 100.0)
        reversibility_multiplier = {"HIGH": 1.0, "MODERATE": 0.75, "LOW": 0.4, "IRREVERSIBLE": 0.1}.get(reversibility, 0.5)

        # Composite Suitability Formula:
        # High frequency, high determinism, high data availability, high error reduction value, high reversibility, minus risk
        positive_factors = (
            0.20 * freq_norm
            + 0.20 * determinism_score
            + 0.15 * data_availability_score
            + 0.15 * error_rate
            + 0.15 * business_value_score
            + 0.15 * reversibility_multiplier
        )
        suitability_score = max(0.0, min(1.0, round(positive_factors - (0.30 * risk_score), 2)))

        # Expected monthly savings in hours
        savings_hours = round((frequency_per_month * average_duration_minutes) / 60.0, 1)

        # Classification gating
        if risk_score >= 0.7 or reversibility == "IRREVERSIBLE":
            classification = AutomationSuitability.NOT_SUITABLE
        elif risk_score >= 0.4 or suitability_score < 0.55:
            classification = AutomationSuitability.HIGH_RISK_AUTOMATION
        elif suitability_score >= 0.70 and risk_score <= 0.25 and reversibility == "HIGH":
            classification = AutomationSuitability.LOW_RISK_AUTOMATION
        else:
            classification = AutomationSuitability.REVIEW_REQUIRED

        return AutomationCandidate(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            candidate_code=f"AUTO-{uuid.uuid4().hex[:6].upper()}",
            process_id=process_id,
            task_name=task_name,
            frequency_per_month=frequency_per_month,
            average_duration_minutes=average_duration_minutes,
            error_rate=error_rate,
            reversibility=reversibility,
            suitability_score=suitability_score,
            classification=classification,
            expected_savings_hours_month=savings_hours,
            status="IDENTIFIED",
        )

    def scan_for_candidates(self, process_id: str, tenant_id: str = "default_tenant") -> List[AutomationCandidate]:
        """Scans process event history for repetitive human tasks with high frequency."""
        events = self.event_store.get_events_for_process(process_id, tenant_id)
        human_events = [e for e in events if e.actor_type.value in ("USER", "SYSTEM")]

        activity_counts = defaultdict(int)
        activity_durations = defaultdict(list)

        for event in human_events:
            activity_counts[event.activity] += 1
            activity_durations[event.activity].append(event.duration_ms / 60000.0)  # to minutes

        candidates: List[AutomationCandidate] = []
        for activity, count in activity_counts.items():
            if count >= 3:  # candidate threshold
                durations = activity_durations[activity]
                avg_min = sum(durations) / len(durations) if durations else 5.0
                candidate = self.evaluate_task(
                    process_id=process_id,
                    task_name=activity,
                    frequency_per_month=count * 10,
                    average_duration_minutes=round(avg_min, 1),
                    error_rate=0.05,
                    determinism_score=0.85,
                    data_availability_score=0.9,
                    risk_score=0.2,
                    reversibility="HIGH",
                    tenant_id=tenant_id,
                )
                candidates.append(candidate)

        return candidates
