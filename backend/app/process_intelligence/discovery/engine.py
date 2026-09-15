"""
Process Discovery Engine for Phase 49: Reconstructs observed process flows, discovers variants, and builds directly-follows graphs.
"""

from collections import defaultdict
import hashlib
from typing import Any, Dict, List, Optional, Tuple
import uuid

try:
    from backend.app.process_intelligence.base import ProcessCase, ProcessEvent, ProcessMap, ProcessVariant, TransitionEdge
    from backend.app.process_intelligence.event_log.store import ProcessEventLogStore
except ImportError:
    from app.process_intelligence.base import ProcessCase, ProcessEvent, ProcessMap, ProcessVariant, TransitionEdge
    from app.process_intelligence.event_log.store import ProcessEventLogStore


class ProcessDiscoveryEngine:
    """Discovers process graph structures, transition matrices, and execution variants from event logs."""

    def __init__(self, event_store: ProcessEventLogStore):
        self.event_store = event_store

    def discover_variants(self, process_id: str, tenant_id: str = "default_tenant") -> List[ProcessVariant]:
        """Groups cases into distinct sequential variants and calculates metrics for each variant."""
        cases = self.event_store.get_cases_for_process(process_id, tenant_id)
        if not cases:
            return []

        variant_groups: Dict[str, List[ProcessCase]] = defaultdict(list)
        variant_sequences: Dict[str, List[str]] = {}

        for case in cases:
            events = self.event_store.get_events_for_case(case.id or "", tenant_id)
            if not events:
                continue

            sequence = [e.activity for e in events]
            seq_str = " -> ".join(sequence)
            seq_hash = hashlib.sha256(seq_str.encode()).hexdigest()[:16]

            variant_groups[seq_hash].append(case)
            variant_sequences[seq_hash] = sequence

        total_cases = sum(len(c_list) for c_list in variant_groups.values())
        if total_cases == 0:
            return []

        variants: List[ProcessVariant] = []
        variant_idx = 1

        for seq_hash, grouped_cases in variant_groups.items():
            freq = len(grouped_cases)
            percentage = round((freq / total_cases) * 100.0, 2)
            sequence = variant_sequences[seq_hash]

            # Calculate average cycle time for cases in this variant
            cycle_times = [c.cycle_time_seconds for c in grouped_cases if c.cycle_time_seconds is not None]
            avg_cycle = round(sum(cycle_times) / len(cycle_times), 2) if cycle_times else 0.0

            # Conversion rate & failure rate
            success_count = sum(1 for c in grouped_cases if c.outcome in ("WON", "COMPLETED", "DELIVERED", "RESOLVED"))
            failure_count = sum(1 for c in grouped_cases if c.outcome in ("LOST", "FAILED", "ABANDONED", "CANCELLED"))
            conversion_rate = round((success_count / freq) * 100.0, 2) if freq > 0 else 0.0
            failure_rate = round((failure_count / freq) * 100.0, 2) if freq > 0 else 0.0

            # Rework detection in sequence
            activity_counts = defaultdict(int)
            for act in sequence:
                activity_counts[act] += 1
            has_rework = any(cnt > 1 for cnt in activity_counts.values())
            rework_rate = 100.0 if has_rework else 0.0

            variant = ProcessVariant(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                process_id=process_id,
                variant_code=f"VAR-{variant_idx:03d}",
                event_sequence=sequence,
                sequence_hash=seq_hash,
                frequency=freq,
                percentage=percentage,
                average_cycle_time_seconds=avg_cycle,
                conversion_rate=conversion_rate,
                failure_rate=failure_rate,
                rework_rate=rework_rate,
                is_conforming=True,
            )
            variants.append(variant)
            variant_idx += 1

        # Sort variants by frequency descending
        variants.sort(key=lambda v: v.frequency, reverse=True)
        return variants

    def build_process_map(
        self,
        process_id: str,
        map_type: str = "OBSERVED",
        tenant_id: str = "default_tenant",
    ) -> ProcessMap:
        """Constructs a graph of activity nodes and directly-follows transition edges."""
        cases = self.event_store.get_cases_for_process(process_id, tenant_id)

        transitions_count: Dict[Tuple[str, str], int] = defaultdict(int)
        transitions_latencies: Dict[Tuple[str, str], List[float]] = defaultdict(list)
        activity_durations: Dict[str, List[int]] = defaultdict(list)
        activity_occurrences: Dict[str, int] = defaultdict(int)

        for case in cases:
            events = self.event_store.get_events_for_case(case.id or "", tenant_id)
            for i, event in enumerate(events):
                activity_occurrences[event.activity] += 1
                activity_durations[event.activity].append(event.duration_ms)

                if i < len(events) - 1:
                    next_event = events[i + 1]
                    edge_key = (event.activity, next_event.activity)
                    transitions_count[edge_key] += 1
                    latency = max(0.0, (next_event.timestamp - event.timestamp).total_seconds())
                    transitions_latencies[edge_key].append(latency)

        # Build nodes
        nodes: List[Dict[str, Any]] = []
        for activity, count in activity_occurrences.items():
            durations = activity_durations.get(activity, [0])
            avg_duration_ms = sum(durations) / len(durations) if durations else 0
            nodes.append({
                "id": activity,
                "label": activity,
                "frequency": count,
                "average_duration_ms": round(avg_duration_ms, 2),
            })

        # Build transition edges
        edges: List[TransitionEdge] = []
        for (src, tgt), count in transitions_count.items():
            latencies = transitions_latencies.get((src, tgt), [0.0])
            avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
            sorted_lat = sorted(latencies)
            med_lat = sorted_lat[len(sorted_lat) // 2] if sorted_lat else 0.0

            edges.append(
                TransitionEdge(
                    source_activity=src,
                    target_activity=tgt,
                    transition_frequency=count,
                    average_latency_seconds=round(avg_lat, 2),
                    median_latency_seconds=round(med_lat, 2),
                    failure_count=0,
                )
            )

        return ProcessMap(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            process_id=process_id,
            map_type=map_type,
            version_number=1,
            nodes=nodes,
            edges=edges,
            metrics_summary={
                "total_cases_analyzed": len(cases),
                "total_unique_activities": len(nodes),
                "total_transitions": len(edges),
            },
        )
