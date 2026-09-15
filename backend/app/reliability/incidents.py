"""Incident management lifecycle, event logging, actions tracking, and blameless postmortems."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.reliability.base import IncidentSeverity, IncidentStatus


class IncidentManager:
    """Manages operational incident declaration, mitigation tracking, recovery, and post-incident review."""

    VALID_TRANSITIONS = {
        IncidentStatus.DETECTED: [IncidentStatus.ACKNOWLEDGED, IncidentStatus.TRIAGED],
        IncidentStatus.ACKNOWLEDGED: [IncidentStatus.TRIAGED, IncidentStatus.INVESTIGATING],
        IncidentStatus.TRIAGED: [IncidentStatus.INVESTIGATING, IncidentStatus.MITIGATING],
        IncidentStatus.INVESTIGATING: [IncidentStatus.MITIGATING, IncidentStatus.RECOVERING],
        IncidentStatus.MITIGATING: [IncidentStatus.RECOVERING, IncidentStatus.RESOLVED],
        IncidentStatus.RECOVERING: [IncidentStatus.RESOLVED],
        IncidentStatus.RESOLVED: [IncidentStatus.VERIFIED, IncidentStatus.CLOSED],
        IncidentStatus.VERIFIED: [IncidentStatus.CLOSED],
        IncidentStatus.CLOSED: [],
    }

    @classmethod
    def can_transition(cls, current: IncidentStatus, next_state: IncidentStatus) -> bool:
        if current == next_state:
            return True
        return next_state in cls.VALID_TRANSITIONS.get(current, [])

    @classmethod
    def build_postmortem_draft(
        cls,
        incident_id: str,
        title: str,
        severity: IncidentSeverity,
        duration_minutes: int,
        affected_services: List[str],
        root_cause: str,
        prevention_actions: List[str],
    ) -> Dict[str, Any]:
        """Generates a structured, blameless postmortem report."""
        return {
            "incident_id": incident_id,
            "title": f"Postmortem: {title}",
            "severity": severity.value,
            "duration_minutes": duration_minutes,
            "affected_services": affected_services,
            "root_cause_summary": root_cause,
            "five_whys": [
                f"1. Why did the issue occur? -> {root_cause}",
                "2. Why did safeguards not prevent it? -> Safeguard threshold / edge case reached.",
                "3. Why was detection delayed? -> Initial telemetry threshold evaluation window.",
                "4. Why was recovery required? -> Automatic fallback completed, root cause mitigated.",
                "5. What systemic change prevents recurrence? -> Added automated tests and tighter alerts.",
            ],
            "action_items": [
                {"action": act, "status": "PLANNED", "owner": "Operations"}
                for act in prevention_actions
            ],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
