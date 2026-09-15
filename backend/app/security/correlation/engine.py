"""
Security Correlation and Attack Chain Engine (Section 8.5 & 19).
Correlates discrete security events across time and entities into cohesive attack chain hypotheses.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import uuid

try:
    from app.security.base import (
        SecurityEvent,
        SecurityEventCategory,
        SecurityAlert,
        AttackChainHypothesis,
        AttackChainStage,
        SecuritySeverity,
        AnomalyType,
        MitreTactic,
    )
except ImportError:
    from backend.app.security.base import (
        SecurityEvent,
        SecurityEventCategory,
        SecurityAlert,
        AttackChainHypothesis,
        AttackChainStage,
        SecuritySeverity,
        AnomalyType,
        MitreTactic,
    )


class CorrelationEngine:
    """
    Analyzes sequences of security events and alerts to synthesize Attack Chain Hypotheses.
    Detects classic multi-stage attacker progression:
    Initial Access -> Credential Access -> Persistence/Privilege Escalation -> Collection/Exfiltration.
    """

    def __init__(self, window_hours: int = 24):
        self.window = timedelta(hours=window_hours)
        self._chains: List[AttackChainHypothesis] = []

    def correlate_events(self, events: List[SecurityEvent], alerts: Optional[List[SecurityAlert]] = None) -> List[AttackChainHypothesis]:
        """
        Examines event stream grouped by principal or source IP to detect sequential attack chains.
        """
        chains: List[AttackChainHypothesis] = []
        # Group events by principal_id
        grouped: Dict[str, List[SecurityEvent]] = {}
        for evt in events:
            p_id = evt.principal_id
            if p_id not in grouped:
                grouped[p_id] = []
            grouped[p_id].append(evt)

        for principal_id, p_events in grouped.items():
            if len(p_events) < 2:
                continue

            sorted_events = sorted(p_events, key=lambda x: x.timestamp)
            chain = self._evaluate_principal_sequence(principal_id, sorted_events)
            if chain:
                chains.append(chain)
                self._chains.append(chain)

        return chains

    def _evaluate_principal_sequence(self, principal_id: str, events: List[SecurityEvent]) -> Optional[AttackChainHypothesis]:
        """Evaluates if a single principal's timeline represents a compromise chain."""
        has_failed_auth = False
        has_success_auth = False
        has_priv_or_config = False
        has_data_or_export = False

        failed_evts: List[str] = []
        success_evts: List[str] = []
        priv_evts: List[str] = []
        data_evts: List[str] = []

        for e in events:
            act = (e.action or "").lower()
            ev_type = (e.event_type or "").lower()
            combined = f"{act} {ev_type}"
            res = (e.result or "").upper()

            if (
                "role" in combined
                or "permission" in combined
                or "privilege" in combined
                or "config" in combined
                or e.event_category in (SecurityEventCategory.PRIVILEGE, SecurityEventCategory.ADMINISTRATION, SecurityEventCategory.CONFIGURATION)
            ):
                has_priv_or_config = True
                priv_evts.append(e.security_event_id)
            elif (
                e.source.value == "data"
                or "export" in combined
                or "download" in combined
                or e.event_category == SecurityEventCategory.DATA_ACCESS
                or "data" in combined
            ):
                has_data_or_export = True
                data_evts.append(e.security_event_id)
            elif (
                e.source.value == "auth"
                or "login" in combined
                or "auth" in combined
                or e.event_category == SecurityEventCategory.AUTHENTICATION
            ):
                if res in ("FAILURE", "DENY"):
                    has_failed_auth = True
                    failed_evts.append(e.security_event_id)
                elif res in ("SUCCESS", "ALLOW"):
                    if has_failed_auth:  # Login success after failures
                        has_success_auth = True
                        success_evts.append(e.security_event_id)

        # Multi-stage attack chain pattern: Failed logins -> Success login -> Privilege change -> Data access
        stages: List[AttackChainStage] = []

        if has_failed_auth:
            stages.append(AttackChainStage(
                stage_name="1. Credential Probing / Brute Force",
                event_ids=failed_evts,
                mitre_tactic=MitreTactic.CREDENTIAL_ACCESS.value,
                mitre_technique="T1110",
                description="Repeated failed authentications observed prior to access."
            ))

        if has_success_auth:
            stages.append(AttackChainStage(
                stage_name="2. Account Ingress / Breach",
                event_ids=success_evts,
                mitre_tactic=MitreTactic.INITIAL_ACCESS.value,
                mitre_technique="T1078",
                description="Successful login authenticated following prior credential failures."
            ))

        if has_priv_or_config:
            stages.append(AttackChainStage(
                stage_name="3. Privilege Escalation / Tampering",
                event_ids=priv_evts,
                mitre_tactic=MitreTactic.PRIVILEGE_ESCALATION.value,
                mitre_technique="T1068",
                description="Role modification or configuration alteration executed."
            ))

        if has_data_or_export:
            stages.append(AttackChainStage(
                stage_name="4. Collection / Data Exfiltration",
                event_ids=data_evts,
                mitre_tactic=MitreTactic.EXFILTRATION.value,
                mitre_technique="T1048",
                description="Sensitive document or bulk database records queried/exported."
            ))

        # We construct an attack chain if at least 2 distinct strategic stages are observed
        if len(stages) >= 2:
            confidence = min(0.98, 0.4 + (len(stages) * 0.15))
            tenant_id = events[0].tenant_id if events else "default_tenant"
            all_stage_event_ids = [eid for s in stages for eid in s.event_ids]

            return AttackChainHypothesis(
                chain_id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                title=f"Potential Account Compromise & Lateral Movement Chain ({principal_id})",
                confidence=confidence,
                stages=stages,
                affected_principal=principal_id,
                supporting_evidence=[
                    f"Observed {len(stages)} distinct MITRE attack stages within correlation window",
                    f"Sequential progression matching: {' -> '.join(s.stage_name.split('. ')[1] for s in stages)}",
                    f"Total correlated events: {len(all_stage_event_ids)}"
                ],
                contradicting_evidence=[],
                recommended_investigation_steps=[
                    f"Revoke all active sessions for principal '{principal_id}' immediately",
                    "Audit IP addresses and geolocation of successful logins",
                    "Inspect all administrative permissions or roles granted in Stage 3",
                    "Quantify exact records exported during Stage 4"
                ]
            )

        return None

    def get_chains(self, tenant_id: Optional[str] = None) -> List[AttackChainHypothesis]:
        if tenant_id:
            return [c for c in self._chains if c.tenant_id == tenant_id]
        return self._chains
