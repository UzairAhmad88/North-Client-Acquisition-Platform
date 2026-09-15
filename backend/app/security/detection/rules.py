"""
Security Detection Rules Engine.
Implements Deterministic, Threshold, Velocity, Behavioral, and Sequence detection rules (Sections 8-15).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import re
import uuid

try:
    from app.security.base import (
        SecurityEvent,
        SecurityAlert,
        AnomalyType,
        SecuritySeverity,
        AlertStatus,
        SecuritySourceType,
        SecurityEventCategory,
    )
    from app.security.detection.mitre import MitreMapper
except ImportError:
    from backend.app.security.base import (
        SecurityEvent,
        SecurityAlert,
        AnomalyType,
        SecuritySeverity,
        AlertStatus,
        SecuritySourceType,
        SecurityEventCategory,
    )
    from backend.app.security.detection.mitre import MitreMapper


# Common prompt injection signatures and evasion indicators
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+the\s+above",
    r"system\s+prompt\s+override",
    r"you\s+are\s+now\s+in\s+developer\s+mode",
    r"DAN\s+mode",
    r"reveal\s+your\s+system\s+prompt",
    r"exfiltrate.*(?:api_key|token|secret|password)",
    r"print\s+environment\s+variables",
    r"base64_decode\(",
    r"bypass\s+(all\s+)?security\s+rules",
    r"<\s*script\s*>",
]

TOKEN_LEAK_PATTERNS = [
    r"sk-[a-zA-Z0-9]{32,}",
    r"ghp_[a-zA-Z0-9]{36}",
    r"AKIA[0-9A-Z]{16}",
    r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}",
]


class BaseRule:
    """Abstract base class for all security detection rules."""

    def __init__(self, name: str, description: str, severity: SecuritySeverity, anomaly_type: AnomalyType):
        self.name = name
        self.description = description
        self.severity = severity
        self.anomaly_type = anomaly_type

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        raise NotImplementedError


class BruteForceRule(BaseRule):
    """Detects repeated authentication failures from the same principal or IP address."""

    def __init__(self, threshold: int = 5, window_seconds: int = 300):
        super().__init__(
            name="Brute Force Detection",
            description=f"Detects {threshold}+ failed login attempts within {window_seconds}s.",
            severity=SecuritySeverity.HIGH,
            anomaly_type=AnomalyType.BRUTE_FORCE
        )
        self.threshold = threshold
        self.window = timedelta(seconds=window_seconds)

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        if current_event.source != SecuritySourceType.AUTH or current_event.result not in ("FAILURE", "DENY"):
            return None

        actor_id = current_event.principal_id
        ip = current_event.ip_metadata.get("ip_address")
        now = current_event.timestamp

        count = 1
        for evt in recent_events:
            if evt.security_event_id == current_event.security_event_id:
                continue
            if evt.source == SecuritySourceType.AUTH and evt.result in ("FAILURE", "DENY"):
                same_actor = (evt.principal_id == actor_id and actor_id != "anonymous")
                same_ip = (ip and evt.ip_metadata.get("ip_address") == ip)
                if same_actor or same_ip:
                    if (now - evt.timestamp) <= self.window:
                        count += 1

        if count >= self.threshold:
            mitre_tech = MitreMapper.get_technique(self.anomaly_type)
            return SecurityAlert(
                alert_id=str(uuid.uuid4()),
                tenant_id=current_event.tenant_id,
                title=f"Potential Brute Force Attack ({count} failed logins)",
                description=f"Principal '{actor_id}' / IP '{ip}' encountered {count} failed login attempts in {self.window.total_seconds()}s.",
                severity=self.severity,
                status=AlertStatus.DETECTED,
                anomaly_type=self.anomaly_type,
                mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                risk_score=min(95.0, 50.0 + (count * 5.0)),
                confidence_score=min(1.0, 0.6 + (count * 0.05)),
                affected_actor_id=actor_id,
                affected_target_id=current_event.resource_id,
                evidence={
                    "failed_attempts": count,
                    "target_actor": actor_id,
                    "target_ip": ip,
                    "sample_event_id": current_event.security_event_id
                }
            )
        return None


class CredentialStuffingRule(BaseRule):
    """Detects multiple failed logins across different accounts from the same source IP."""

    def __init__(self, threshold_accounts: int = 3, window_seconds: int = 300):
        super().__init__(
            name="Credential Stuffing Detection",
            description=f"Detects failed attempts targeting {threshold_accounts}+ distinct accounts from same IP.",
            severity=SecuritySeverity.CRITICAL,
            anomaly_type=AnomalyType.CREDENTIAL_STUFFING
        )
        self.threshold_accounts = threshold_accounts
        self.window = timedelta(seconds=window_seconds)

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        ip = current_event.ip_metadata.get("ip_address")
        if not ip or current_event.source != SecuritySourceType.AUTH or current_event.result not in ("FAILURE", "DENY"):
            return None

        distinct_targets = {current_event.principal_id}
        now = current_event.timestamp

        for evt in recent_events:
            if evt.security_event_id == current_event.security_event_id:
                continue
            if evt.source == SecuritySourceType.AUTH and evt.result in ("FAILURE", "DENY"):
                if evt.ip_metadata.get("ip_address") == ip:
                    if (now - evt.timestamp) <= self.window:
                        distinct_targets.add(evt.principal_id)

        if len(distinct_targets) >= self.threshold_accounts:
            mitre_tech = MitreMapper.get_technique(self.anomaly_type)
            return SecurityAlert(
                alert_id=str(uuid.uuid4()),
                tenant_id=current_event.tenant_id,
                title=f"Credential Stuffing Detected ({len(distinct_targets)} target accounts from {ip})",
                description=f"Source IP '{ip}' targeted {len(distinct_targets)} distinct accounts with failed authentication within {self.window.total_seconds()}s.",
                severity=self.severity,
                status=AlertStatus.DETECTED,
                anomaly_type=self.anomaly_type,
                mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                risk_score=90.0,
                confidence_score=0.92,
                affected_actor_id=f"IP:{ip}",
                evidence={
                    "source_ip": ip,
                    "targeted_accounts": list(distinct_targets)[:10],
                    "count": len(distinct_targets)
                }
            )
        return None


class PromptInjectionRule(BaseRule):
    """Detects prompt injection or jailbreak patterns in AI agent interactions."""

    def __init__(self):
        super().__init__(
            name="LLM Prompt Injection Rule",
            description="Detects adversarial jailbreaks and system prompt extraction attacks against AI agents.",
            severity=SecuritySeverity.HIGH,
            anomaly_type=AnomalyType.AGENT_PROMPT_INJECTION
        )
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in PROMPT_INJECTION_PATTERNS]

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        text_content = ""
        if current_event.source == SecuritySourceType.AGENT or current_event.event_category == SecurityEventCategory.AI_SECURITY:
            text_content = f"{current_event.action} {current_event.metadata} {current_event.evidence}"
        else:
            text_content = f"{current_event.metadata.get('prompt', '')} {current_event.evidence.get('prompt_sample', '')}"

        for pattern in self.compiled_patterns:
            match = pattern.search(text_content)
            if match:
                mitre_tech = MitreMapper.get_technique(self.anomaly_type)
                return SecurityAlert(
                    alert_id=str(uuid.uuid4()),
                    tenant_id=current_event.tenant_id,
                    title="AI Agent Prompt Injection Pattern Intercepted",
                    description=f"Adversarial prompt injection pattern '{match.group(0)}' detected in agent payload.",
                    severity=self.severity,
                    status=AlertStatus.DETECTED,
                    anomaly_type=self.anomaly_type,
                    mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                    mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                    risk_score=85.0,
                    confidence_score=0.95,
                    affected_actor_id=current_event.principal_id,
                    affected_target_id=current_event.resource_id,
                    evidence={
                        "matched_signature": match.group(0),
                        "agent_id": current_event.agent_id or current_event.principal_id,
                        "sample_event_id": current_event.security_event_id
                    }
                )
        return None


class TokenLeakRule(BaseRule):
    """Detects raw API tokens, JWTs, or secrets in logged payloads or query params."""

    def __init__(self):
        super().__init__(
            name="Secret / Token Leakage Rule",
            description="Identifies raw API keys or tokens exposed in logged content.",
            severity=SecuritySeverity.HIGH,
            anomaly_type=AnomalyType.TOKEN_LEAK
        )
        self.compiled_patterns = [re.compile(p) for p in TOKEN_LEAK_PATTERNS]

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        payload_str = f"{current_event.metadata} {current_event.evidence}"
        for pattern in self.compiled_patterns:
            match = pattern.search(payload_str)
            if match:
                raw_token = match.group(0)
                masked = raw_token[:4] + "..." + raw_token[-4:]
                mitre_tech = MitreMapper.get_technique(self.anomaly_type)
                return SecurityAlert(
                    alert_id=str(uuid.uuid4()),
                    tenant_id=current_event.tenant_id,
                    title="Exposed Secret / Token Detected in Telemetry",
                    description=f"Sensitive token signature '{masked}' discovered in {current_event.source.value} telemetry.",
                    severity=self.severity,
                    status=AlertStatus.DETECTED,
                    anomaly_type=self.anomaly_type,
                    mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                    mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                    risk_score=80.0,
                    confidence_score=0.98,
                    affected_actor_id=current_event.principal_id,
                    affected_target_id=current_event.resource_id,
                    evidence={
                        "token_masked": masked,
                        "source": current_event.source.value,
                        "event_id": current_event.security_event_id
                    }
                )
        return None


class BulkDataExfiltrationRule(BaseRule):
    """Detects rapid excessive read/download actions across sensitive data resources."""

    def __init__(self, threshold_records: int = 1000, window_seconds: int = 60):
        super().__init__(
            name="Bulk Data Exfiltration Rule",
            description=f"Detects queries/exports accessing >{threshold_records} records in {window_seconds}s.",
            severity=SecuritySeverity.HIGH,
            anomaly_type=AnomalyType.DATA_EXFILTRATION
        )
        self.threshold_records = threshold_records
        self.window = timedelta(seconds=window_seconds)

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        if current_event.source != SecuritySourceType.DATA:
            return None

        records_accessed = current_event.evidence.get("records_accessed", 1)
        actor_id = current_event.principal_id
        now = current_event.timestamp

        total = records_accessed
        for evt in recent_events:
            if evt.security_event_id == current_event.security_event_id:
                continue
            if evt.source == SecuritySourceType.DATA and evt.principal_id == actor_id:
                if (now - evt.timestamp) <= self.window:
                    total += evt.evidence.get("records_accessed", 1)

        if total >= self.threshold_records:
            mitre_tech = MitreMapper.get_technique(self.anomaly_type)
            return SecurityAlert(
                alert_id=str(uuid.uuid4()),
                tenant_id=current_event.tenant_id,
                title=f"Potential Bulk Data Exfiltration ({total} records accessed)",
                description=f"Principal '{actor_id}' accessed {total} records within {self.window.total_seconds()}s.",
                severity=self.severity,
                status=AlertStatus.DETECTED,
                anomaly_type=self.anomaly_type,
                mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                risk_score=85.0,
                confidence_score=0.88,
                affected_actor_id=actor_id,
                affected_target_id=current_event.resource_id,
                evidence={
                    "records_accessed": total,
                    "target_resource": current_event.resource_id,
                    "window_seconds": self.window.total_seconds()
                }
            )
        return None


class PrivilegeEscalationRule(BaseRule):
    """Detects sudden role/permission changes or attempts to grant administrative rights."""

    def __init__(self):
        super().__init__(
            name="Privilege Escalation Rule",
            description="Detects unexpected role changes or administrative permission grants.",
            severity=SecuritySeverity.CRITICAL,
            anomaly_type=AnomalyType.PRIVILEGE_ESCALATION
        )

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        action_lower = (current_event.action or "").lower()
        type_lower = (current_event.event_type or "").lower()
        combined = f"{action_lower} {type_lower}"
        if (
            "role" in combined
            or "permission" in combined
            or "privilege" in combined
            or "admin" in combined
            or current_event.event_category in (SecurityEventCategory.PRIVILEGE, SecurityEventCategory.AUTHORIZATION)
        ):
            if any(term in combined for term in ["escalat", "grant_admin", "assign_admin", "promote", "elevat", "role_change"]):
                mitre_tech = MitreMapper.get_technique(self.anomaly_type)
                return SecurityAlert(
                    alert_id=str(uuid.uuid4()),
                    tenant_id=current_event.tenant_id,
                    title="Privilege Escalation Attempt Detected",
                    description=f"Principal '{current_event.principal_id}' initiated administrative privilege assignment '{current_event.action}'.",
                    severity=self.severity,
                    status=AlertStatus.DETECTED,
                    anomaly_type=self.anomaly_type,
                    mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                    mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                    risk_score=92.0,
                    confidence_score=0.90,
                    affected_actor_id=current_event.principal_id,
                    affected_target_id=current_event.resource_id,
                    evidence={
                        "action": current_event.action,
                        "resource": current_event.resource_id,
                        "event_id": current_event.security_event_id
                    }
                )
        return None


class CrossTenantAccessRule(BaseRule):
    """Detects unauthorized cross-tenant data requests (Section 15)."""

    def __init__(self):
        super().__init__(
            name="Cross-Tenant Boundary Violation Rule",
            description="Enforces strict tenant isolation and detects cross-tenant data requests.",
            severity=SecuritySeverity.CRITICAL,
            anomaly_type=AnomalyType.CROSS_TENANT_VIOLATION
        )

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        if current_event.evidence.get("cross_tenant_violation"):
            mitre_tech = MitreMapper.get_technique(self.anomaly_type)
            target_tenant = current_event.evidence.get("target_tenant", "unknown")
            return SecurityAlert(
                alert_id=str(uuid.uuid4()),
                tenant_id=current_event.tenant_id,
                title="Cross-Tenant Isolation Violation Detected",
                description=f"Principal from tenant '{current_event.tenant_id}' attempted to access resources in tenant '{target_tenant}'.",
                severity=self.severity,
                status=AlertStatus.DETECTED,
                anomaly_type=self.anomaly_type,
                mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                risk_score=98.0,
                confidence_score=0.99,
                affected_actor_id=current_event.principal_id,
                affected_target_id=f"Tenant:{target_tenant}",
                evidence={
                    "request_tenant": current_event.tenant_id,
                    "target_tenant": target_tenant,
                    "resource": current_event.resource_id
                }
            )
        return None


class APIAbuseRule(BaseRule):
    """Detects aggressive API bursts or endpoint enumeration."""

    def __init__(self, threshold_failures: int = 10, window_seconds: int = 60):
        super().__init__(
            name="API Rate & Abuse Rule",
            description=f"Detects {threshold_failures}+ authorization failures or rate limit hits in {window_seconds}s.",
            severity=SecuritySeverity.HIGH,
            anomaly_type=AnomalyType.API_RATE_ABUSE
        )
        self.threshold_failures = threshold_failures
        self.window = timedelta(seconds=window_seconds)

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        if current_event.source != SecuritySourceType.API:
            return None

        status_code = current_event.evidence.get("status_code", 200)
        if status_code not in (401, 403, 404, 429):
            return None

        actor_id = current_event.principal_id
        now = current_event.timestamp

        count = 1
        for evt in recent_events:
            if evt.security_event_id == current_event.security_event_id:
                continue
            if evt.source == SecuritySourceType.API and evt.principal_id == actor_id:
                if evt.evidence.get("status_code") in (401, 403, 404, 429):
                    if (now - evt.timestamp) <= self.window:
                        count += 1

        if count >= self.threshold_failures:
            mitre_tech = MitreMapper.get_technique(self.anomaly_type)
            return SecurityAlert(
                alert_id=str(uuid.uuid4()),
                tenant_id=current_event.tenant_id,
                title=f"API Abuse / Enumeration Detected ({count} client errors)",
                description=f"API Client '{actor_id}' incurred {count} authorization/rate limit errors in {self.window.total_seconds()}s.",
                severity=self.severity,
                status=AlertStatus.DETECTED,
                anomaly_type=self.anomaly_type,
                mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                risk_score=75.0,
                confidence_score=0.85,
                affected_actor_id=actor_id,
                affected_target_id=current_event.resource_id,
                evidence={
                    "error_count": count,
                    "last_status_code": status_code,
                    "endpoint": current_event.resource_id
                }
            )
        return None


class AgentRunawaySpendRule(BaseRule):
    """Detects runaway tool call loops or extreme token consumption by AI agents."""

    def __init__(self, threshold_calls: int = 15, window_seconds: int = 60):
        super().__init__(
            name="Agent Runaway Resource Consumption Rule",
            description=f"Detects {threshold_calls}+ rapid tool calls by a single agent within {window_seconds}s.",
            severity=SecuritySeverity.HIGH,
            anomaly_type=AnomalyType.AGENT_RUNAWAY_SPEND
        )
        self.threshold_calls = threshold_calls
        self.window = timedelta(seconds=window_seconds)

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        if current_event.source != SecuritySourceType.AGENT:
            return None

        agent_id = current_event.agent_id or current_event.principal_id
        now = current_event.timestamp

        count = 1
        for evt in recent_events:
            if evt.security_event_id == current_event.security_event_id:
                continue
            if evt.source == SecuritySourceType.AGENT and (evt.agent_id == agent_id or evt.principal_id == agent_id):
                if (now - evt.timestamp) <= self.window:
                    count += 1

        if count >= self.threshold_calls:
            mitre_tech = MitreMapper.get_technique(self.anomaly_type)
            return SecurityAlert(
                alert_id=str(uuid.uuid4()),
                tenant_id=current_event.tenant_id,
                title=f"Runaway Agent Activity ({count} tool calls in {self.window.total_seconds()}s)",
                description=f"AI Agent '{agent_id}' triggered {count} rapid tool invocations, indicating possible infinite loop or denial-of-wallet.",
                severity=self.severity,
                status=AlertStatus.DETECTED,
                anomaly_type=self.anomaly_type,
                mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                risk_score=80.0,
                confidence_score=0.90,
                affected_actor_id=agent_id,
                affected_target_id=current_event.resource_id,
                evidence={
                    "tool_calls_count": count,
                    "agent_id": agent_id,
                    "sample_tool": current_event.resource_id
                }
            )
        return None


class ConfigTamperingRule(BaseRule):
    """Detects unauthorized attempts to modify audit logging, policies, or kill switches."""

    def __init__(self):
        super().__init__(
            name="Security Config Tampering Rule",
            description="Detects attempts to disable audit logging, bypass RBAC policies, or alter compliance configurations.",
            severity=SecuritySeverity.CRITICAL,
            anomaly_type=AnomalyType.SENSITIVE_CONFIG_TAMPERING
        )

    def evaluate(self, current_event: SecurityEvent, recent_events: List[SecurityEvent]) -> Optional[SecurityAlert]:
        if current_event.source in (SecuritySourceType.ADMIN, SecuritySourceType.API, SecuritySourceType.SYSTEM):
            action_lower = current_event.action.lower()
            resource_lower = (current_event.resource_id or "").lower()
            if any(term in action_lower or term in resource_lower for term in [
                "disable_audit", "delete_audit", "bypass_rbac", "disable_guardrail", "disable_kill_switch"
            ]):
                mitre_tech = MitreMapper.get_technique(self.anomaly_type)
                return SecurityAlert(
                    alert_id=str(uuid.uuid4()),
                    tenant_id=current_event.tenant_id,
                    title="Critical Security Configuration Tampering Attempt",
                    description=f"Principal '{current_event.principal_id}' attempted destructive action '{current_event.action}' on security target '{current_event.resource_id}'.",
                    severity=self.severity,
                    status=AlertStatus.DETECTED,
                    anomaly_type=self.anomaly_type,
                    mitre_technique_id=mitre_tech.technique_id if mitre_tech else None,
                    mitre_tactic=mitre_tech.tactic.value if mitre_tech else None,
                    risk_score=99.0,
                    confidence_score=0.99,
                    affected_actor_id=current_event.principal_id,
                    affected_target_id=current_event.resource_id,
                    evidence={
                        "action": current_event.action,
                        "resource": current_event.resource_id,
                        "principal": current_event.principal_id
                    }
                )
        return None
