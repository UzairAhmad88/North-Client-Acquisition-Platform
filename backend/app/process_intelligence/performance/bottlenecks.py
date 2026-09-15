"""
Performance, Bottleneck, Rework & Handoff Analytics Engine for Phase 49.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.process_intelligence.base import (
        BottleneckRecord,
        BottleneckType,
        HandoffRecord,
        ReworkDriver,
        ReworkRecord,
    )
    from backend.app.process_intelligence.event_log.store import ProcessEventLogStore
except ImportError:
    from app.process_intelligence.base import (
        BottleneckRecord,
        BottleneckType,
        HandoffRecord,
        ReworkDriver,
        ReworkRecord,
    )
    from app.process_intelligence.event_log.store import ProcessEventLogStore


class BottleneckDetector:
    """Identifies process bottlenecks, long wait queues, and high latency activities with attached evidence."""

    def __init__(self, event_store: ProcessEventLogStore):
        self.event_store = event_store

    def detect_bottlenecks(
        self,
        process_id: str,
        wait_threshold_seconds: float = 3600.0,  # 1 hour default
        tenant_id: str = "default_tenant",
    ) -> List[BottleneckRecord]:
        """Detects activities with excessive average wait time or high queue depth."""
        cases = self.event_store.get_cases_for_process(process_id, tenant_id)
        if not cases:
            return []

        activity_waits: Dict[str, List[float]] = defaultdict(list)
        activity_durations: Dict[str, List[float]] = defaultdict(list)
        affected_cases: Dict[str, set] = defaultdict(set)

        for case in cases:
            events = self.event_store.get_events_for_case(case.id or "", tenant_id)
            for i, event in enumerate(events):
                activity_durations[event.activity].append(event.duration_ms / 1000.0)

                # Wait time is time elapsed between previous event end and current event start
                if i > 0:
                    prev_event = events[i - 1]
                    wait_sec = max(0.0, (event.timestamp - prev_event.timestamp).total_seconds())
                    activity_waits[event.activity].append(wait_sec)
                    if wait_sec > wait_threshold_seconds:
                        affected_cases[event.activity].add(case.id)

        bottlenecks: List[BottleneckRecord] = []
        bottleneck_idx = 1

        for activity, waits in activity_waits.items():
            if not waits:
                continue

            avg_wait = sum(waits) / len(waits)
            durations = activity_durations.get(activity, [0.0])
            avg_proc = sum(durations) / len(durations) if durations else 0.0

            # If average wait exceeds threshold or wait/proc ratio is high
            if avg_wait >= wait_threshold_seconds or (avg_proc > 0 and (avg_wait / avg_proc) > 5.0):
                aff_count = len(affected_cases.get(activity, set()))
                severity = "CRITICAL" if avg_wait > (wait_threshold_seconds * 3) else ("HIGH" if avg_wait > wait_threshold_seconds else "MEDIUM")

                bottleneck = BottleneckRecord(
                    id=str(uuid.uuid4()),
                    tenant_id=tenant_id,
                    process_id=process_id,
                    bottleneck_code=f"BTN-{bottleneck_idx:03d}",
                    activity_name=activity,
                    bottleneck_type=BottleneckType.WAIT_TIME,
                    average_wait_seconds=round(avg_wait, 2),
                    average_processing_seconds=round(avg_proc, 2),
                    queue_depth=aff_count,
                    frequency=len(waits),
                    affected_cases_count=aff_count,
                    root_cause_summary=f"Activity '{activity}' exhibits an average wait time of {round(avg_wait, 1)}s vs processing time of {round(avg_proc, 1)}s.",
                    business_impact=f"Prolongs end-to-end case completion cycle time across {aff_count} active cases.",
                    severity=severity,
                    recommendation=f"Consider automating pre-validation tasks or introducing async notification hooks for '{activity}'.",
                    evidence_payload={
                        "avg_wait_seconds": avg_wait,
                        "avg_processing_seconds": avg_proc,
                        "sample_size": len(waits),
                        "affected_cases": list(affected_cases.get(activity, set())),
                    },
                )
                bottlenecks.append(bottleneck)
                bottleneck_idx += 1

        bottlenecks.sort(key=lambda b: b.average_wait_seconds, reverse=True)
        return bottlenecks


class CycleTimeAnalyzer:
    """Analyzes value-adding processing duration vs waiting / queue latency."""

    def __init__(self, event_store: ProcessEventLogStore):
        self.event_store = event_store

    def analyze_cycle_times(self, process_id: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        """Calculates aggregate cycle time statistics for a process."""
        cases = self.event_store.get_cases_for_process(process_id, tenant_id)
        if not cases:
            return {
                "total_cases": 0,
                "average_cycle_time_seconds": 0.0,
                "average_processing_time_seconds": 0.0,
                "average_waiting_time_seconds": 0.0,
                "flow_efficiency_percentage": 0.0,
            }

        cycle_times = [c.cycle_time_seconds or 0.0 for c in cases]
        proc_times = [c.processing_time_seconds or 0.0 for c in cases]
        wait_times = [c.waiting_time_seconds or 0.0 for c in cases]

        avg_cycle = sum(cycle_times) / len(cycle_times) if cycle_times else 0.0
        avg_proc = sum(proc_times) / len(proc_times) if proc_times else 0.0
        avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0.0

        # Flow efficiency = Value Add (Processing) / Total Cycle Time
        flow_efficiency = (avg_proc / avg_cycle * 100.0) if avg_cycle > 0 else 100.0

        return {
            "total_cases": len(cases),
            "average_cycle_time_seconds": round(avg_cycle, 2),
            "average_processing_time_seconds": round(avg_proc, 2),
            "average_waiting_time_seconds": round(avg_wait, 2),
            "flow_efficiency_percentage": round(flow_efficiency, 2),
        }


class ReworkAnalyzer:
    """Detects repeated/looping activities indicating rework friction."""

    def __init__(self, event_store: ProcessEventLogStore):
        self.event_store = event_store

    def detect_rework(self, process_id: str, tenant_id: str = "default_tenant") -> List[ReworkRecord]:
        """Scans case traces for repeated activities."""
        cases = self.event_store.get_cases_for_process(process_id, tenant_id)
        rework_records: List[ReworkRecord] = []

        for case in cases:
            events = self.event_store.get_events_for_case(case.id or "", tenant_id)
            activity_events: Dict[str, List[Any]] = defaultdict(list)
            for event in events:
                activity_events[event.activity].append(event)

            for activity, evts in activity_events.items():
                if len(evts) > 1:
                    # Rework detected: calculate wasted duration (sum of subsequent runs)
                    rework_durations = [e.duration_ms / 1000.0 for e in evts[1:]]
                    wasted_sec = sum(rework_durations)

                    record = ReworkRecord(
                        id=str(uuid.uuid4()),
                        tenant_id=tenant_id,
                        process_id=process_id,
                        case_id=case.id,
                        activity_name=activity,
                        repetition_count=len(evts),
                        wasted_duration_seconds=round(wasted_sec, 2),
                        probable_driver=ReworkDriver.SCOPE_INSTABILITY,
                        evidence_payload={
                            "case_id": case.id,
                            "activity": activity,
                            "occurrences": len(evts),
                            "event_timestamps": [e.timestamp.isoformat() for e in evts],
                        },
                    )
                    rework_records.append(record)

        return rework_records


class HandoffAnalyzer:
    """Evaluates cross-role and cross-team transitions and latency."""

    def __init__(self, event_store: ProcessEventLogStore):
        self.event_store = event_store

    def analyze_handoffs(self, process_id: str, tenant_id: str = "default_tenant") -> List[HandoffRecord]:
        """Calculates handoff friction and delay between different actor roles."""
        cases = self.event_store.get_cases_for_process(process_id, tenant_id)
        handoffs: Dict[tuple, List[float]] = defaultdict(list)

        for case in cases:
            events = self.event_store.get_events_for_case(case.id or "", tenant_id)
            for i in range(len(events) - 1):
                cur = events[i]
                nxt = events[i + 1]

                src_role = cur.attributes.get("role", cur.actor_type.value)
                tgt_role = nxt.attributes.get("role", nxt.actor_type.value)

                if src_role != tgt_role:
                    delay = max(0.0, (nxt.timestamp - cur.timestamp).total_seconds())
                    handoffs[(src_role, tgt_role)].append(delay)

        results: List[HandoffRecord] = []
        for (src_role, tgt_role), delays in handoffs.items():
            avg_delay = sum(delays) / len(delays) if delays else 0.0
            friction_score = min(1.0, avg_delay / 86400.0)  # normalized relative to 1 day

            results.append(
                HandoffRecord(
                    id=str(uuid.uuid4()),
                    tenant_id=tenant_id,
                    process_id=process_id,
                    source_role=src_role,
                    target_role=tgt_role,
                    handoff_type="ROLE_TRANSITION",
                    average_delay_seconds=round(avg_delay, 2),
                    handoff_count=len(delays),
                    friction_score=round(friction_score, 2),
                    common_issues=["Context transfer latency", "Queue wait time"],
                )
            )

        return results
