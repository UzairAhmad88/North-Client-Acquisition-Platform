"""Unit tests for Phase 35 — Unified Identity, RBAC, Sessions, MFA, and Security Control Plane."""

from datetime import datetime, timedelta, timezone
import uuid

import pytest

from app.security.audit import SecurityEventRecord, SecurityEventType, SecuritySeverity
from app.security.engine import AuthorizationDecision, AuthorizationEngine, ReasonCode
from app.security.mfa import MFAService
from app.security.password import hash_password, validate_password_policy, verify_password
from app.security.permissions import PERMISSION_REGISTRY, SystemPermissions, get_permission
from app.security.principals import (
    AuthorizationContext,
    Principal,
    PrincipalStatus,
    PrincipalType,
    SecurityContext,
)
from app.security.roles import ROLE_PERMISSIONS_MAP, SystemRole, get_role_permissions
from app.security.sessions import SessionManager


def test_password_hashing_and_complexity():
    """Test PBKDF2 hashing, verification, and policy enforcement."""
    password = "SuperSecretPassword123!"
    hashed = hash_password(password)

    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123!", hashed) is False

    # Policy validation: Valid password
    valid, msg = validate_password_policy(password)
    assert valid is True

    # Policy validation: Short password
    valid_short, msg_short = validate_password_policy("short")
    assert valid_short is False

    # Policy validation: Common weak password
    valid_weak, msg_weak = validate_password_policy("password123")
    assert valid_weak is False


def test_session_lifecycle_and_timeout():
    """Test token encoding/decoding and idle/absolute timeout detection."""
    user_id = str(uuid.uuid4())
    tenant_id = "tenant-001"
    session_id = str(uuid.uuid4())

    token = SessionManager.create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        session_id=session_id,
        roles=["DEVELOPER"],
    )
    decoded = SessionManager.decode_token(token)

    assert decoded["sub"] == user_id
    assert decoded["tenant_id"] == tenant_id
    assert decoded["session_id"] == session_id
    assert decoded["roles"] == ["DEVELOPER"]

    # Active session check
    now = datetime.now(timezone.utc)
    active, status = SessionManager.is_session_active(
        created_at=now - timedelta(hours=1),
        last_seen_at=now - timedelta(minutes=5),
        is_revoked=False,
    )
    assert active is True
    assert status == "SESSION_ACTIVE"

    # Idle timeout check (>60m)
    active_idle, status_idle = SessionManager.is_session_active(
        created_at=now - timedelta(hours=1),
        last_seen_at=now - timedelta(minutes=65),
        is_revoked=False,
    )
    assert active_idle is False
    assert status_idle == "IDLE_TIMEOUT_EXCEEDED"

    # Revoked session check
    active_revoked, status_revoked = SessionManager.is_session_active(
        created_at=now,
        last_seen_at=now,
        is_revoked=True,
    )
    assert active_revoked is False
    assert status_revoked == "SESSION_REVOKED"


def test_mfa_and_step_up_tokens():
    """Test TOTP secret generation and step-up authentication tokens."""
    secret = MFAService.generate_totp_secret()
    assert len(secret) >= 20

    backup_codes = MFAService.generate_backup_codes(count=8)
    assert len(backup_codes) == 8

    # Mock code verification
    assert MFAService.verify_totp_code(secret, "123456") is True
    assert MFAService.verify_totp_code(secret, "000000") is False
    assert MFAService.verify_totp_code(secret, "abc") is False

    # Step-up token
    user_id = str(uuid.uuid4())
    step_token = MFAService.create_step_up_token(user_id=user_id, tenant_id="tenant-1")
    assert MFAService.verify_step_up_token(step_token, user_id) is True
    assert MFAService.verify_step_up_token(step_token, "wrong-user") is False


def test_rbac_evaluation_default_deny():
    """Test default deny: Principal without assigned permission is blocked."""
    principal = Principal(
        id="user-1",
        type=PrincipalType.USER,
        tenant_id="tenant-1",
        status=PrincipalStatus.ACTIVE,
    )
    security_ctx = SecurityContext(
        principal=principal,
        tenant_id="tenant-1",
        roles=[],
        permissions=set(),
    )
    auth_ctx = AuthorizationContext(
        resource_type="lead",
        action=SystemPermissions.LEAD_READ,
        resource_tenant_id="tenant-1",
    )

    decision = AuthorizationEngine.evaluate(security_ctx, auth_ctx)
    assert decision.allowed is False
    assert decision.reason_code == ReasonCode.PERMISSION_DENIED


def test_rbac_role_hierarchy_permissions():
    """Test that roles inherit their mapped permissions."""
    principal = Principal(
        id="dev-1",
        type=PrincipalType.USER,
        tenant_id="tenant-1",
        status=PrincipalStatus.ACTIVE,
    )
    security_ctx = SecurityContext(
        principal=principal,
        tenant_id="tenant-1",
        roles=["DEVELOPER"],
        permissions=set(),
    )

    # Developer can read project
    auth_ctx = AuthorizationContext(
        resource_type="project",
        action=SystemPermissions.PROJECT_READ,
        resource_tenant_id="tenant-1",
    )
    decision = AuthorizationEngine.evaluate(security_ctx, auth_ctx)
    assert decision.allowed is True
    assert decision.reason_code == ReasonCode.ALLOWED

    # Developer cannot send outreach
    auth_ctx_outreach = AuthorizationContext(
        resource_type="outreach",
        action=SystemPermissions.OUTREACH_SEND,
        resource_tenant_id="tenant-1",
    )
    decision_outreach = AuthorizationEngine.evaluate(security_ctx, auth_ctx_outreach)
    assert decision_outreach.allowed is False
    assert decision_outreach.reason_code == ReasonCode.PERMISSION_DENIED


def test_tenant_isolation_cross_tenant_denial():
    """Test IDOR defense: Cross-tenant access is strictly rejected."""
    principal = Principal(
        id="user-tenant-a",
        type=PrincipalType.USER,
        tenant_id="tenant-a",
        status=PrincipalStatus.ACTIVE,
    )
    security_ctx = SecurityContext(
        principal=principal,
        tenant_id="tenant-a",
        roles=["ADMIN"],
    )
    auth_ctx = AuthorizationContext(
        resource_type="project",
        action=SystemPermissions.PROJECT_READ,
        resource_tenant_id="tenant-b",  # Target belongs to Tenant B!
    )

    decision = AuthorizationEngine.evaluate(security_ctx, auth_ctx)
    assert decision.allowed is False
    assert decision.reason_code == ReasonCode.TENANT_MISMATCH


def test_project_membership_abac():
    """Test ABAC: Developer assigned only to Project A cannot modify Project B."""
    principal = Principal(
        id="dev-1",
        type=PrincipalType.USER,
        tenant_id="tenant-1",
        status=PrincipalStatus.ACTIVE,
    )
    security_ctx = SecurityContext(
        principal=principal,
        tenant_id="tenant-1",
        roles=["DEVELOPER"],
    )

    # Trying to update project-B while only assigned to project-A
    auth_ctx = AuthorizationContext(
        resource_type="project",
        resource_id="project-b",
        action=SystemPermissions.PROJECT_UPDATE,
        project_id="project-b",
        resource_tenant_id="tenant-1",
        attributes={"assigned_project_ids": ["project-a"]},
    )

    decision = AuthorizationEngine.evaluate(security_ctx, auth_ctx)
    assert decision.allowed is False
    assert decision.reason_code == ReasonCode.PROJECT_MEMBERSHIP_REQUIRED


def test_client_vs_internal_boundary():
    """Test Client Boundary: Client users cannot access internal AI traces."""
    client_principal = Principal(
        id="client-user-1",
        type=PrincipalType.CLIENT,
        tenant_id="tenant-1",
        status=PrincipalStatus.ACTIVE,
    )
    security_ctx = SecurityContext(
        principal=client_principal,
        tenant_id="tenant-1",
        roles=["CLIENT_ADMIN"],
    )
    auth_ctx = AuthorizationContext(
        resource_type="ai_trace",
        action=SystemPermissions.AI_TRACE_READ,
        resource_tenant_id="tenant-1",
        is_client_visible=False,
    )

    decision = AuthorizationEngine.evaluate(security_ctx, auth_ctx)
    assert decision.allowed is False
    assert decision.reason_code == ReasonCode.CLIENT_ACCESS_BOUNDARY_VIOLATION


def test_agent_identity_prohibited_permissions():
    """Test Agent Boundary: Agents are strictly prohibited from external side-effects."""
    agent_principal = Principal(
        id="research_agent_v1",
        type=PrincipalType.AGENT,
        tenant_id="tenant-1",
        status=PrincipalStatus.ACTIVE,
    )
    security_ctx = SecurityContext(
        principal=agent_principal,
        tenant_id="tenant-1",
        roles=[],
        permissions={SystemPermissions.OUTREACH_SEND},  # Even if mistakenly granted
    )
    auth_ctx = AuthorizationContext(
        resource_type="outreach",
        action=SystemPermissions.OUTREACH_SEND,
        resource_tenant_id="tenant-1",
    )

    decision = AuthorizationEngine.evaluate(security_ctx, auth_ctx)
    assert decision.allowed is False
    assert decision.reason_code == ReasonCode.AGENT_PROHIBITED_ACTION


def test_high_risk_mfa_step_up_evaluation():
    """Test that high risk permissions require MFA and Step-Up authentication."""
    principal = Principal(
        id="owner-1",
        type=PrincipalType.USER,
        tenant_id="tenant-1",
        status=PrincipalStatus.ACTIVE,
    )
    security_ctx_no_mfa = SecurityContext(
        principal=principal,
        tenant_id="tenant-1",
        roles=["OWNER"],
        is_mfa_authenticated=False,
    )

    # Contract signing requires MFA
    auth_ctx = AuthorizationContext(
        resource_type="contract",
        action=SystemPermissions.CONTRACT_SIGN,
        resource_tenant_id="tenant-1",
    )

    decision_no_mfa = AuthorizationEngine.evaluate(security_ctx_no_mfa, auth_ctx)
    assert decision_no_mfa.allowed is False
    assert decision_no_mfa.reason_code == ReasonCode.MFA_REQUIRED

    # Now with MFA
    security_ctx_mfa = SecurityContext(
        principal=principal,
        tenant_id="tenant-1",
        roles=["OWNER"],
        is_mfa_authenticated=True,
    )
    decision_mfa = AuthorizationEngine.evaluate(security_ctx_mfa, auth_ctx)
    assert decision_mfa.allowed is True
    assert "STEP_UP" in decision_mfa.required_gates


def test_security_audit_events_recording():
    """Test SecurityEventRecord creation with immutable timestamp and severity."""
    event = SecurityEventRecord(
        event_type=SecurityEventType.LOGIN_FAILURE,
        severity=SecuritySeverity.MEDIUM,
        principal_id="user-bad-login",
        result="DENY",
        reason_code="INVALID_CREDENTIALS",
        details={"attempt": 3},
    )

    assert event.event_type == SecurityEventType.LOGIN_FAILURE
    assert event.severity == SecuritySeverity.MEDIUM
    assert event.result == "DENY"
    assert event.details["attempt"] == 3
    assert isinstance(event.occurred_at, datetime)
