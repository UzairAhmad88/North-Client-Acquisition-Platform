"""
Security Detection Engine orchestrator.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import logging

try:
    from app.security.base import SecurityEvent, SecurityAlert, SecurityDetection
    from app.security.detection.rules import (
        BaseRule,
        BruteForceRule,
        CredentialStuffingRule,
        PromptInjectionRule,
        TokenLeakRule,
        BulkDataExfiltrationRule,
        PrivilegeEscalationRule,
        CrossTenantAccessRule,
        APIAbuseRule,
        AgentRunawaySpendRule,
        ConfigTamperingRule,
    )
except ImportError:
    from backend.app.security.base import SecurityEvent, SecurityAlert, SecurityDetection
    from backend.app.security.detection.rules import (
        BaseRule,
        BruteForceRule,
        CredentialStuffingRule,
        PromptInjectionRule,
        TokenLeakRule,
        BulkDataExfiltrationRule,
        PrivilegeEscalationRule,
        CrossTenantAccessRule,
        APIAbuseRule,
        AgentRunawaySpendRule,
        ConfigTamperingRule,
    )

logger = logging.getLogger(__name__)


class DetectionEngine:
    """
    Real-time security detection engine that evaluates normalized events
    against deterministic, threshold, behavioral, and sequence rules.
    """

    def __init__(self, max_buffer_size: int = 1000):
        self.rules: List[BaseRule] = [
            BruteForceRule(),
            CredentialStuffingRule(),
            PromptInjectionRule(),
            TokenLeakRule(),
            BulkDataExfiltrationRule(),
            PrivilegeEscalationRule(),
            CrossTenantAccessRule(),
            APIAbuseRule(),
            AgentRunawaySpendRule(),
            ConfigTamperingRule(),
        ]
        self._event_buffer: List[SecurityEvent] = []
        self._max_buffer_size = max_buffer_size
        self._detections_history: List[SecurityDetection] = []
        self._alerts_history: List[SecurityAlert] = []

    def register_rule(self, rule: BaseRule) -> None:
        """Register a custom detection rule."""
        self.rules.append(rule)
        logger.info(f"Registered custom security rule: {rule.name}")

    def ingest_event(self, event: SecurityEvent) -> List[SecurityAlert]:
        """
        Ingests a normalized security event, appends it to memory buffer,
        runs all detection rules against it, and returns any triggered alerts.
        """
        self._event_buffer.append(event)
        if len(self._event_buffer) > self._max_buffer_size:
            self._event_buffer.pop(0)

        alerts_triggered: List[SecurityAlert] = []

        for rule in self.rules:
            try:
                alert = rule.evaluate(current_event=event, recent_events=self._event_buffer)
                if alert:
                    # Create corresponding detection record
                    detection = SecurityDetection(
                        detection_id=alert.alert_id,
                        tenant_id=alert.tenant_id,
                        rule_id=rule.name.lower().replace(" ", "_"),
                        rule_name=rule.name,
                        anomaly_type=alert.anomaly_type,
                        severity=alert.severity,
                        risk_score=alert.risk_score,
                        confidence=alert.confidence_score,
                        mitre_technique_id=alert.mitre_technique_id,
                        mitre_tactic=alert.mitre_tactic,
                        description=alert.description,
                        evidence_events=[event.security_event_id],
                        metadata=alert.evidence
                    )
                    alert.detection_id = detection.detection_id

                    self._detections_history.append(detection)
                    self._alerts_history.append(alert)
                    alerts_triggered.append(alert)

                    logger.warning(
                        f"Security Alert Triggered: [{alert.severity.value}] {alert.title} "
                        f"(Tenant: {alert.tenant_id}, MITRE: {alert.mitre_technique_id})"
                    )
            except Exception as e:
                logger.error(f"Error evaluating rule '{rule.name}': {str(e)}", exc_info=True)

        return alerts_triggered

    def get_recent_events(self, limit: int = 50, tenant_id: Optional[str] = None) -> List[SecurityEvent]:
        """Retrieve recent events from the in-memory buffer."""
        events = self._event_buffer
        if tenant_id:
            events = [e for e in events if e.tenant_id == tenant_id]
        return events[-limit:]

    def get_recent_detections(self, limit: int = 50, tenant_id: Optional[str] = None) -> List[SecurityDetection]:
        """Retrieve recent detections."""
        dets = self._detections_history
        if tenant_id:
            dets = [d for d in dets if d.tenant_id == tenant_id]
        return dets[-limit:]

    def get_recent_alerts(self, limit: int = 50, tenant_id: Optional[str] = None) -> List[SecurityAlert]:
        """Retrieve recent alerts."""
        alts = self._alerts_history
        if tenant_id:
            alts = [a for a in alts if a.tenant_id == tenant_id]
        return alts[-limit:]
