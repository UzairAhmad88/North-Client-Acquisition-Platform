"""
Telemetry normalizer for transforming heterogeneous platform logs into standard Canonical SecurityEvent format.
Strictly implements Data Minimization and Zero-Secret-Logging (Section 6 & 48).
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import re
import uuid

try:
    from app.security.base import (
        SecurityEvent,
        SecuritySourceType,
        SecuritySeverity,
        SecurityEventCategory,
    )
except ImportError:
    from backend.app.security.base import (
        SecurityEvent,
        SecuritySourceType,
        SecuritySeverity,
        SecurityEventCategory,
    )

# Keys that must never appear in security logs
SENSITIVE_FIELD_NAMES = {
    "password", "passwd", "secret", "api_key", "token", "access_token",
    "refresh_token", "jwt", "authorization", "auth_token", "private_key",
    "card_number", "cvv", "payment_secret", "client_secret"
}

# Regex patterns for accidental token leakage in free-text fields
TOKEN_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{32,}"),
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]+", re.IGNORECASE),
    re.compile(r"ey[A-Za-z0-9-_=]+\.ey[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*"),
]


def sanitize_payload(data: Any) -> Any:
    """Recursively redacts sensitive keys and secret patterns."""
    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            if any(sens in k.lower() for sens in SENSITIVE_FIELD_NAMES):
                cleaned[k] = "[REDACTED_SECRET]"
            else:
                cleaned[k] = sanitize_payload(v)
        return cleaned
    elif isinstance(data, list):
        return [sanitize_payload(item) for item in data]
    elif isinstance(data, str):
        sanitized_str = data
        for pattern in TOKEN_PATTERNS:
            sanitized_str = pattern.sub("[REDACTED_SECRET_PATTERN]", sanitized_str)
        return sanitized_str
    return data


class TelemetryNormalizer:
    """Transforms raw subsystem logs into sanitized Canonical SecurityEvent models."""

    @staticmethod
    def normalize(raw_data: Dict[str, Any], default_source: SecuritySourceType = SecuritySourceType.SYSTEM) -> SecurityEvent:
        """Generic normalizer routing to specialized normalizers or standardizing raw logs."""
        source_str = str(raw_data.get("source") or raw_data.get("source_type") or default_source.value).lower()
        if "auth" in source_str:
            return TelemetryNormalizer.normalize_auth_event(raw_data)
        elif "agent" in source_str:
            return TelemetryNormalizer.normalize_agent_event(raw_data)
        elif "api" in source_str:
            return TelemetryNormalizer.normalize_api_event(raw_data)
        elif "data" in source_str:
            return TelemetryNormalizer.normalize_data_event(raw_data)
        elif "admin" in source_str or "config" in source_str:
            return TelemetryNormalizer.normalize_admin_event(raw_data)
        elif "finan" in source_str:
            return TelemetryNormalizer.normalize_financial_event(raw_data)
        elif "integ" in source_str:
            return TelemetryNormalizer.normalize_integration_event(raw_data)
        elif "workflow" in source_str:
            return TelemetryNormalizer.normalize_workflow_event(raw_data)
        else:
            return TelemetryNormalizer.normalize_generic_event(raw_data, default_source)

    @staticmethod
    def normalize_auth_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        actor_id = cleaned.get("user_id") or cleaned.get("email") or cleaned.get("principal_id") or "anonymous"
        event_type = cleaned.get("event_type", "auth.login")
        status = cleaned.get("status", "success")
        is_failure = status in ("failure", "blocked", "failed")
        severity = SecuritySeverity.MEDIUM if is_failure else SecuritySeverity.INFO

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or cleaned.get("security_event_id") or str(uuid.uuid4()),
            event_type=event_type,
            event_category=SecurityEventCategory.AUTHENTICATION,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=actor_id,
            principal_type="USER",
            user_id=cleaned.get("user_id"),
            session_id=cleaned.get("session_id"),
            ip_metadata={"ip_address": cleaned.get("ip_address"), "country": cleaned.get("geo_country"), "city": cleaned.get("geo_city")},
            device_metadata={"user_agent": cleaned.get("user_agent")},
            resource_type="user_account",
            resource_id=cleaned.get("target_user_id") or actor_id,
            action=cleaned.get("action", "login"),
            result="FAILURE" if is_failure else "SUCCESS",
            risk_level=severity,
            source=SecuritySourceType.AUTH,
            metadata=cleaned.get("metadata", {}),
            evidence={"failed_attempts": cleaned.get("failed_attempts", 1 if is_failure else 0)}
        )

    @staticmethod
    def normalize_agent_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        agent_id = cleaned.get("agent_id", "unknown_agent")
        action = cleaned.get("action", "agent_invocation")
        is_anomalous = bool(cleaned.get("is_anomalous") or cleaned.get("injection_detected"))
        severity = SecuritySeverity.HIGH if is_anomalous else SecuritySeverity.LOW

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=cleaned.get("event_type", "agent.tool_execution"),
            event_category=SecurityEventCategory.AI_SECURITY if is_anomalous else SecurityEventCategory.AGENT_SECURITY,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=agent_id,
            principal_type="AGENT",
            agent_id=agent_id,
            session_id=cleaned.get("session_id"),
            ip_metadata={"ip_address": cleaned.get("ip_address")},
            device_metadata={},
            resource_type="agent_tool",
            resource_id=cleaned.get("target_tool") or cleaned.get("tool_name"),
            action=action,
            result="BLOCK" if cleaned.get("blocked") else ("SUCCESS" if not is_anomalous else "FAILURE"),
            risk_level=severity,
            source=SecuritySourceType.AGENT,
            metadata=cleaned.get("metadata", {}),
            evidence={"prompt_sample": cleaned.get("prompt_sample"), "injection_pattern": cleaned.get("injection_pattern")}
        )

    @staticmethod
    def normalize_api_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        actor_id = cleaned.get("actor_id") or cleaned.get("user_id") or "api_client"
        status_code = cleaned.get("status_code", 200)
        status = "SUCCESS" if status_code < 400 else "FAILURE"
        severity = SecuritySeverity.INFO
        if status_code in (401, 403):
            severity = SecuritySeverity.MEDIUM
        elif status_code == 429:
            severity = SecuritySeverity.HIGH

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=f"api.{cleaned.get('method', 'GET').lower()}",
            event_category=SecurityEventCategory.API,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=actor_id,
            principal_type="API_TOKEN" if cleaned.get("is_service") else "USER",
            request_id=cleaned.get("request_id"),
            ip_metadata={"ip_address": cleaned.get("ip_address")},
            device_metadata={"user_agent": cleaned.get("user_agent")},
            resource_type="endpoint",
            resource_id=cleaned.get("endpoint") or cleaned.get("path"),
            action=cleaned.get("method", "GET"),
            result=status,
            risk_level=severity,
            source=SecuritySourceType.API,
            metadata=cleaned.get("metadata", {}),
            evidence={"status_code": status_code, "query_params": cleaned.get("query_params")}
        )

    @staticmethod
    def normalize_data_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        target_tenant = cleaned.get("resource_tenant_id") or tenant_id
        actor_id = cleaned.get("user_id") or cleaned.get("principal_id") or "system"
        action = cleaned.get("action", "read")
        
        # Cross-tenant violation check
        is_cross_tenant = (target_tenant != tenant_id and target_tenant != "global")
        is_bulk = bool(cleaned.get("is_bulk_export") or cleaned.get("records_count", 0) > 1000)
        
        severity = SecuritySeverity.INFO
        category = SecurityEventCategory.DATA_ACCESS
        if is_cross_tenant:
            severity = SecuritySeverity.CRITICAL
            category = SecurityEventCategory.AUTHORIZATION
        elif is_bulk:
            severity = SecuritySeverity.HIGH

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=f"data.{action}",
            event_category=category,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=actor_id,
            principal_type="USER",
            user_id=cleaned.get("user_id"),
            ip_metadata={"ip_address": cleaned.get("ip_address")},
            device_metadata={},
            resource_type="table",
            resource_id=cleaned.get("table_name") or cleaned.get("resource_id"),
            action=action,
            result="DENY" if is_cross_tenant else ("SUCCESS" if cleaned.get("status") != "failure" else "FAILURE"),
            risk_level=severity,
            source=SecuritySourceType.DATA,
            metadata=cleaned.get("metadata", {}),
            evidence={
                "cross_tenant_violation": is_cross_tenant,
                "target_tenant": target_tenant,
                "records_accessed": cleaned.get("records_count", 1)
            }
        )

    @staticmethod
    def normalize_admin_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        actor_id = cleaned.get("user_id") or cleaned.get("admin_id") or "admin"
        action = cleaned.get("action", "config_update")
        is_high_risk = bool(cleaned.get("is_high_risk") or cleaned.get("kill_switch_engaged"))
        severity = SecuritySeverity.HIGH if is_high_risk else SecuritySeverity.MEDIUM

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=f"admin.{action}",
            event_category=SecurityEventCategory.ADMINISTRATION,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=actor_id,
            principal_type="USER",
            ip_metadata={"ip_address": cleaned.get("ip_address")},
            resource_type="configuration",
            resource_id=cleaned.get("config_key"),
            action=action,
            result="SUCCESS" if cleaned.get("status") != "failure" else "FAILURE",
            risk_level=severity,
            source=SecuritySourceType.ADMIN,
            metadata=cleaned.get("metadata", {}),
            evidence={"previous_value": cleaned.get("previous_value"), "new_value": cleaned.get("new_value")}
        )

    @staticmethod
    def normalize_financial_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        actor_id = cleaned.get("user_id") or "finance_system"
        action = cleaned.get("action", "payment_attempt")
        is_anomalous = bool(cleaned.get("is_duplicate") or cleaned.get("amount", 0) > 50000)
        severity = SecuritySeverity.HIGH if is_anomalous else SecuritySeverity.LOW

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=f"financial.{action}",
            event_category=SecurityEventCategory.FINANCIAL_SECURITY,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=actor_id,
            principal_type="USER",
            resource_type="invoice" if "invoice" in action else "payment",
            resource_id=cleaned.get("resource_id"),
            action=action,
            result="SUCCESS" if cleaned.get("status") != "failure" else "FAILURE",
            risk_level=severity,
            source=SecuritySourceType.FINANCE,
            metadata=cleaned.get("metadata", {}),
            evidence={"amount": cleaned.get("amount"), "is_duplicate": cleaned.get("is_duplicate", False)}
        )

    @staticmethod
    def normalize_integration_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        provider = cleaned.get("provider", "unknown_provider")
        action = cleaned.get("action", "webhook_received")

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=f"integration.{action}",
            event_category=SecurityEventCategory.INTEGRATION_SECURITY,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=provider,
            principal_type="SERVICE_ACCOUNT",
            resource_type="integration",
            resource_id=provider,
            action=action,
            result="SUCCESS" if cleaned.get("status") != "failure" else "FAILURE",
            risk_level=SecuritySeverity.LOW,
            source=SecuritySourceType.INTEGRATION,
            metadata=cleaned.get("metadata", {}),
            evidence={"provider": provider}
        )

    @staticmethod
    def normalize_workflow_event(raw_data: Dict[str, Any]) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        tenant_id = cleaned.get("tenant_id", "default_tenant")
        workflow_id = cleaned.get("workflow_id", "unknown_workflow")
        action = cleaned.get("action", "step_execution")

        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=f"workflow.{action}",
            event_category=SecurityEventCategory.WORKFLOW_SECURITY,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=tenant_id,
            principal_id=workflow_id,
            principal_type="SERVICE_ACCOUNT",
            workflow_id=workflow_id,
            resource_type="workflow",
            resource_id=workflow_id,
            action=action,
            result="SUCCESS" if cleaned.get("status") != "failure" else "FAILURE",
            risk_level=SecuritySeverity.LOW,
            source=SecuritySourceType.SYSTEM,
            metadata=cleaned.get("metadata", {}),
            evidence={"workflow_id": workflow_id}
        )

    @staticmethod
    def normalize_generic_event(raw_data: Dict[str, Any], default_source: SecuritySourceType) -> SecurityEvent:
        cleaned = sanitize_payload(raw_data)
        return SecurityEvent(
            security_event_id=cleaned.get("event_id") or str(uuid.uuid4()),
            event_type=cleaned.get("event_type", "generic.event"),
            event_category=SecurityEventCategory.INFRASTRUCTURE,
            timestamp=cleaned.get("timestamp") or datetime.now(timezone.utc),
            tenant_id=cleaned.get("tenant_id", "default_tenant"),
            principal_id=cleaned.get("principal_id") or cleaned.get("user_id") or "system",
            principal_type=cleaned.get("principal_type", "USER"),
            resource_type=cleaned.get("resource_type"),
            resource_id=cleaned.get("resource_id"),
            action=cleaned.get("action", "execute"),
            result=cleaned.get("result", "SUCCESS"),
            risk_level=SecuritySeverity.INFO,
            source=default_source,
            metadata=cleaned.get("metadata", {}),
            evidence=cleaned.get("evidence", {})
        )
