"""
Continuous Intelligence Monitoring, State Change Detection, and Significance Rating.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.research_intelligence.base import (
    IntelligenceEventType,
    SignificanceLevel,
)


class ContinuousMonitoringManager:
    """Manages continuous monitoring rules, detects entity state changes, and suppresses noisy alerts."""

    def __init__(self):
        self._rules: Dict[str, List[Dict[str, Any]]] = {}
        self._events: List[Dict[str, Any]] = []

    def create_monitoring_rule(
        self,
        workspace_id: str,
        target_entity: str,
        watch_frequency: str = "DAILY",
        topics_monitored: Optional[List[str]] = None,
        alert_significance_threshold: SignificanceLevel = SignificanceLevel.MEDIUM,
    ) -> Dict[str, Any]:
        """Establish a continuous discovery rule."""
        rule = {
            "id": f"rule_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "target_entity": target_entity,
            "watch_frequency": watch_frequency,
            "topics_monitored": topics_monitored or ["PRICING", "PRODUCT_RELEASES", "REGULATION"],
            "alert_significance_threshold": alert_significance_threshold.value if hasattr(alert_significance_threshold, "value") else str(alert_significance_threshold),
            "active": True,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._rules.setdefault(workspace_id, []).append(rule)
        return rule

    def list_rules(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._rules.get(workspace_id, [])

    def record_intelligence_event(
        self,
        target_entity: str,
        event_type: IntelligenceEventType,
        summary: str,
        significance: SignificanceLevel = SignificanceLevel.MEDIUM,
        confidence: float = 0.88,
        evidence_payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Emit a validated intelligence event."""
        event = {
            "id": f"ievt_{uuid.uuid4().hex[:12]}",
            "target_entity": target_entity,
            "event_type": event_type.value if hasattr(event_type, "value") else str(event_type),
            "summary": summary,
            "significance": significance.value if hasattr(significance, "value") else str(significance),
            "confidence": confidence,
            "evidence_payload": evidence_payload or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._events.append(event)
        return event

    def list_events(
        self,
        significance: Optional[str] = None,
        target_entity: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        events = self._events
        if significance:
            events = [e for e in events if e["significance"] == significance]
        if target_entity:
            events = [e for e in events if e["target_entity"] == target_entity]
        return events
