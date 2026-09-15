"""ORM models for Unified Identity, RBAC, Sessions, MFA, and Security Audit."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Tenant(BaseModel):
    """Multi-tenant isolation boundary entity."""

    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    tenant_type: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)  # INTERNAL, BUSINESS, CLIENT, DEMO, SYSTEM
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False, index=True)  # ACTIVE, SUSPENDED, DELETED
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class Organization(BaseModel):
    """Team or client company organization within a tenant."""

    __tablename__ = "organizations"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    org_type: Mapped[str] = mapped_column(String(50), default="INTERNAL", nullable=False)  # INTERNAL, CLIENT
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class OrganizationMember(BaseModel):
    """User membership in an organization."""

    __tablename__ = "organization_members"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(50), default="MEMBER", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class UserCredential(BaseModel):
    """Encrypted/hashed credentials and password history."""

    __tablename__ = "user_credentials"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    password_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class UserSession(BaseModel):
    """Durable active user session with revocation support."""

    __tablename__ = "user_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_mfa_authenticated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


class UserMFAMethod(BaseModel):
    """Configured MFA factor for a user."""

    __tablename__ = "user_mfa_methods"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    method_type: Mapped[str] = mapped_column(String(50), default="TOTP", nullable=False)  # TOTP, BACKUP_CODE, WEBAUTHN
    secret: Mapped[str] = mapped_column(String(255), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Role(BaseModel):
    """Role definition entity."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_system: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_internal: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Permission(BaseModel):
    """Granular permission descriptor."""

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)  # e.g. lead.read
    resource: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)


class RolePermission(BaseModel):
    """Association between roles and permissions."""

    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False, index=True
    )


class UserRole(BaseModel):
    """Assignment of a role to a user with optional scoping."""

    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scope_type: Mapped[str] = mapped_column(String(50), default="GLOBAL", nullable=False)  # GLOBAL, PROJECT, ORG
    scope_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), nullable=True)


class ProjectMembership(BaseModel):
    """Project-level access membership and role override."""

    __tablename__ = "project_memberships"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    project_role: Mapped[str] = mapped_column(String(50), default="DEVELOPER", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class ServiceAccount(BaseModel):
    """Non-human identity for workers and background infrastructure."""

    __tablename__ = "service_accounts"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class ServiceAccountPermission(BaseModel):
    """Permissions explicitly assigned to a service account."""

    __tablename__ = "service_account_permissions"

    service_account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("service_accounts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False, index=True
    )


class AgentIdentity(BaseModel):
    """Explicit identity record for an AI agent."""

    __tablename__ = "agent_identities"

    agent_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class AgentPermissionAssignment(BaseModel):
    """Permissions explicitly bound to an AI agent identity."""

    __tablename__ = "agent_permission_assignments"

    agent_identity_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("agent_identities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    permission: Mapped[str] = mapped_column(String(150), nullable=False)


class APIClient(BaseModel):
    """Registered external API integration client."""

    __tablename__ = "api_clients"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


class APIKey(BaseModel):
    """Scoped API key with hashed secret for machine access."""

    __tablename__ = "api_keys"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    api_client_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("api_clients.id", ondelete="CASCADE"), nullable=True, index=True
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    key_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    scopes: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)


class AuthorizationPolicy(BaseModel):
    """Versioned security policy specification."""

    __tablename__ = "authorization_policies"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    policy_type: Mapped[str] = mapped_column(String(50), default="RBAC", nullable=False)  # RBAC, ABAC, HIGH_RISK, CLIENT_ACCESS
    rules: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class SecurityEvent(BaseModel):
    """Immutable audit trail for all security, authentication, and authorization events."""

    __tablename__ = "security_events"

    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), default="INFO", nullable=False, index=True)
    principal_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    principal_type: Mapped[str] = mapped_column(String(50), default="USER", nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    action: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    resource: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    result: Mapped[str] = mapped_column(String(50), default="ALLOW", nullable=False)  # ALLOW, DENY, BLOCK
    reason_code: Mapped[str] = mapped_column(String(100), default="SUCCESS", nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
