"""
Process Event Log Store for Phase 49: Structured event ingestion, case linking, and tenant isolation.
"""

from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.process_intelligence.base import ActorType, ProcessCase, ProcessEvent
except ImportError:
    from app.process_intelligence.base import ActorType, ProcessCase, ProcessEvent


class ProcessEventLogStore:
    """Manages ingestion, retrieval, and case binding of process event logs."""

    def __init__(self):
        self._events: Dict[str, ProcessEvent] = {}
        self._cases: Dict[str, ProcessCase] = {}
        self._case_events: Dict[str, List[str]] = {}  # case_id -> list of event_ids

    def ingest_event(
        self,
        process_id: str,
        activity: str,
        tenant_id: str = "default_tenant",
        case_id: Optional[str] = None,
        actor: str = "system",
        actor_type: ActorType = ActorType.SYSTEM,
        resource: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        task_id: Optional[str] = None,
        status: str = "COMPLETED",
        duration_ms: int = 0,
        attributes: Optional[Dict[str, Any]] = None,
        source: str = "SYSTEM_TELEMETRY",
        anonymize_actor: bool = False,
    ) -> ProcessEvent:
        """Ingests and normalizes an event into the immutable event log."""
        event_id = str(uuid.uuid4())
        event_code = f"EVT-{uuid.uuid4().hex[:8].upper()}"

        # Privacy minimization: hash actor identifier if requested
        recorded_actor = actor
        if anonymize_actor and actor != "system":
            recorded_actor = f"actor_{hashlib.sha256(actor.encode()).hexdigest()[:10]}"

        event = ProcessEvent(
            id=event_id,
            tenant_id=tenant_id,
            event_code=event_code,
            case_id=case_id,
            process_id=process_id,
            activity=activity,
            timestamp=datetime.now(timezone.utc),
            actor=recorded_actor,
            actor_type=actor_type,
            resource=resource,
            entity_type=entity_type,
            entity_id=entity_id,
            workflow_id=workflow_id,
            task_id=task_id,
            status=status,
            duration_ms=duration_ms,
            attributes=attributes or {},
            source=source,
        )

        self._events[event_id] = event

        # Auto-link to case if case_id provided
        if case_id:
            if case_id not in self._case_events:
                self._case_events[case_id] = []
            self._case_events[case_id].append(event_id)

        return event

    def create_or_get_case(
        self,
        process_id: str,
        entity_type: str,
        entity_id: str,
        tenant_id: str = "default_tenant",
        owner_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> ProcessCase:
        """Creates or retrieves a case instance (e.g. Lead #104, Project #28)."""
        # Look for existing active case for this entity
        for case in self._cases.values():
            if (
                case.tenant_id == tenant_id
                and case.process_id == process_id
                and case.entity_type == entity_type
                and case.entity_id == entity_id
                and case.status == "ACTIVE"
            ):
                return case

        case_id = str(uuid.uuid4())
        case_code = f"CASE-{entity_type.upper()[:4]}-{uuid.uuid4().hex[:6].upper()}"
        case = ProcessCase(
            id=case_id,
            tenant_id=tenant_id,
            case_code=case_code,
            process_id=process_id,
            entity_type=entity_type,
            entity_id=entity_id,
            start_time=datetime.now(timezone.utc),
            status="ACTIVE",
            owner_id=owner_id,
            attributes=attributes or {},
        )
        self._cases[case_id] = case
        self._case_events[case_id] = []
        return case

    def complete_case(
        self,
        case_id: str,
        outcome: str = "COMPLETED",
        tenant_id: str = "default_tenant",
    ) -> Optional[ProcessCase]:
        """Completes a case and calculates total cycle, waiting, and processing time."""
        case = self._cases.get(case_id)
        if not case or case.tenant_id != tenant_id:
            return None

        case.end_time = datetime.now(timezone.utc)
        case.status = "COMPLETED"
        case.outcome = outcome

        # Calculate durations from linked events
        event_ids = self._case_events.get(case_id, [])
        linked_events = [self._events[eid] for eid in event_ids if eid in self._events]

        if linked_events:
            total_processing_ms = sum(e.duration_ms for e in linked_events)
            case.processing_time_seconds = total_processing_ms / 1000.0

            # End to end cycle time
            start_ts = linked_events[0].timestamp
            end_ts = linked_events[-1].timestamp
            total_seconds = max((end_ts - start_ts).total_seconds(), case.processing_time_seconds)
            case.cycle_time_seconds = total_seconds
            case.waiting_time_seconds = max(0.0, total_seconds - case.processing_time_seconds)
        else:
            case.cycle_time_seconds = 0.0
            case.waiting_time_seconds = 0.0
            case.processing_time_seconds = 0.0

        return case

    def get_events_for_case(self, case_id: str, tenant_id: str = "default_tenant") -> List[ProcessEvent]:
        """Returns sorted events for a given case ensuring tenant isolation."""
        event_ids = self._case_events.get(case_id, [])
        events = [self._events[eid] for eid in event_ids if eid in self._events and self._events[eid].tenant_id == tenant_id]
        return sorted(events, key=lambda e: e.timestamp)

    def get_events_for_process(self, process_id: str, tenant_id: str = "default_tenant") -> List[ProcessEvent]:
        """Returns all events for a given process definition."""
        return [e for e in self._events.values() if e.process_id == process_id and e.tenant_id == tenant_id]

    def get_cases_for_process(self, process_id: str, tenant_id: str = "default_tenant") -> List[ProcessCase]:
        """Returns all cases for a given process definition."""
        return [c for c in self._cases.values() if c.process_id == process_id and c.tenant_id == tenant_id]
