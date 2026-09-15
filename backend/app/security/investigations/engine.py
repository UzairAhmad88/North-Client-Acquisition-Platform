"""
Security Investigations and Evidence Graph Engine (Sections 20, 21, 22).
Constructs chronological incident timelines and entity-relationship evidence graphs.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

try:
    from app.security.base import (
        SecurityIncident,
        SecurityEvent,
        SecurityAlert,
        AttackChainHypothesis,
    )
except ImportError:
    from backend.app.security.base import (
        SecurityIncident,
        SecurityEvent,
        SecurityAlert,
        AttackChainHypothesis,
    )


class InvestigationEngine:
    """
    Orchestrates investigation workspaces, produces timelines,
    and builds formal Evidence Graphs with provenance and edge relationships.
    """

    @classmethod
    def build_chronological_timeline(
        cls,
        events: List[SecurityEvent],
        alerts: Optional[List[SecurityAlert]] = None,
        incident: Optional[SecurityIncident] = None
    ) -> List[Dict[str, Any]]:
        """
        Synthesizes all related events, detections, and incident milestones into a unified timeline.
        """
        timeline_entries: List[Dict[str, Any]] = []

        for e in events:
            timeline_entries.append({
                "entry_id": str(uuid.uuid4()),
                "timestamp": e.timestamp.isoformat(),
                "type": "SECURITY_EVENT",
                "title": f"[{e.source.value.upper()}] {e.action} on {e.resource_id or e.resource_type}",
                "description": f"Result: {e.result}, Principal: {e.principal_id}",
                "severity": e.risk_level.value,
                "source_id": e.security_event_id,
                "category": e.event_category.value
            })

        for a in (alerts or []):
            timeline_entries.append({
                "entry_id": str(uuid.uuid4()),
                "timestamp": a.created_at.isoformat(),
                "type": "SECURITY_ALERT",
                "title": f"[ALERT] {a.title}",
                "description": a.description,
                "severity": a.severity.value,
                "source_id": a.alert_id,
                "category": "DETECTION"
            })

        if incident:
            timeline_entries.append({
                "entry_id": str(uuid.uuid4()),
                "timestamp": incident.created_at.isoformat(),
                "type": "INCIDENT_CREATED",
                "title": f"[INCIDENT] {incident.title}",
                "description": f"Declared with severity {incident.severity.value}",
                "severity": incident.severity.value,
                "source_id": incident.incident_id,
                "category": "INCIDENT"
            })

        # Sort chronologically
        timeline_entries.sort(key=lambda x: x["timestamp"])
        return timeline_entries

    @classmethod
    def construct_evidence_graph(
        cls,
        incident: SecurityIncident,
        events: List[SecurityEvent],
        alerts: Optional[List[SecurityAlert]] = None,
        attack_chain: Optional[AttackChainHypothesis] = None
    ) -> Dict[str, Any]:
        """
        Constructs Nodes and Edges representation of the Security Evidence Graph (Section 22).
        Nodes: Principals, Sessions, Resources, Events, Detections, Incidents.
        Edges: ACCESSES, MODIFIES, TRIGGERS, PRECEDES, SUPPORTS, CORRELATES_WITH.
        """
        nodes: Dict[str, Dict[str, Any]] = {}
        edges: List[Dict[str, Any]] = []

        # 1. Incident node
        inc_node_id = f"incident:{incident.incident_id}"
        nodes[inc_node_id] = {
            "id": inc_node_id,
            "label": incident.title,
            "type": "INCIDENT",
            "severity": incident.severity.value
        }

        # 2. Add alerts and events
        for alert in (alerts or []):
            alert_node_id = f"alert:{alert.alert_id}"
            nodes[alert_node_id] = {
                "id": alert_node_id,
                "label": alert.title,
                "type": "ALERT",
                "severity": alert.severity.value
            }
            edges.append({
                "source": alert_node_id,
                "target": inc_node_id,
                "relationship": "TRIGGERS"
            })

        for evt in events:
            evt_node_id = f"event:{evt.security_event_id}"
            nodes[evt_node_id] = {
                "id": evt_node_id,
                "label": f"{evt.action} ({evt.source.value})",
                "type": "EVENT",
                "severity": evt.risk_level.value
            }

            # Principal node
            if evt.principal_id:
                p_node_id = f"principal:{evt.principal_id}"
                if p_node_id not in nodes:
                    nodes[p_node_id] = {
                        "id": p_node_id,
                        "label": evt.principal_id,
                        "type": "PRINCIPAL",
                        "principal_type": evt.principal_type
                    }
                edges.append({
                    "source": p_node_id,
                    "target": evt_node_id,
                    "relationship": "PERFORMS"
                })

            # Resource node
            if evt.resource_id:
                res_node_id = f"resource:{evt.resource_id}"
                if res_node_id not in nodes:
                    nodes[res_node_id] = {
                        "id": res_node_id,
                        "label": evt.resource_id,
                        "type": "RESOURCE",
                        "resource_type": evt.resource_type or "resource"
                    }
                edges.append({
                    "source": evt_node_id,
                    "target": res_node_id,
                    "relationship": "ACCESSES" if "read" in evt.action.lower() else "MODIFIES"
                })

            edges.append({
                "source": evt_node_id,
                "target": inc_node_id,
                "relationship": "SUPPORTS"
            })

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
            "node_count": len(nodes),
            "edge_count": len(edges)
        }

    @classmethod
    def synthesize_hypotheses(
        cls,
        incident: SecurityIncident,
        events: List[SecurityEvent],
        attack_chain: Optional[AttackChainHypothesis] = None
    ) -> List[Dict[str, Any]]:
        """Synthesizes plausible root-cause hypotheses based on observed patterns."""
        hypotheses = []

        if attack_chain and len(attack_chain.stages) >= 2:
            hypotheses.append({
                "id": str(uuid.uuid4()),
                "title": "Compromised Credentials with Multi-Stage Lateral Movement",
                "confidence": attack_chain.confidence,
                "status": "MOST_LIKELY",
                "supporting_evidence": attack_chain.supporting_evidence,
                "contradicting_evidence": attack_chain.contradicting_evidence,
                "recommended_verification": "Check MFA logs and device footprint for initial login IP."
            })

        has_injection = any("injection" in e.action.lower() or e.event_category.value == "AI_SECURITY" for e in events)
        if has_injection:
            hypotheses.append({
                "id": str(uuid.uuid4()),
                "title": "Adversarial Prompt Injection against Autonomous AI Agent",
                "confidence": 0.88,
                "status": "LIKELY",
                "supporting_evidence": ["Prompt injection signatures intercepted in agent payload."],
                "contradicting_evidence": [],
                "recommended_verification": "Inspect context memory of affected agent."
            })

        if not hypotheses:
            hypotheses.append({
                "id": str(uuid.uuid4()),
                "title": "Isolated Policy Anomaly or Credential Misconfiguration",
                "confidence": 0.60,
                "status": "POSSIBLE",
                "supporting_evidence": ["Discrete authorization or authentication error events."],
                "contradicting_evidence": ["No sustained attack chain progression observed."],
                "recommended_verification": "Verify user credentials and permissions baseline."
            })

        return hypotheses
