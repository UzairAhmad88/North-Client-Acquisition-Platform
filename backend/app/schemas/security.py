"""Pydantic schemas for Identity, RBAC, Sessions, MFA, API Keys, and Security Audit."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# 1. User & Identity Schemas
class UserInviteRequest(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "DEVELOPER"
    tenant_id: Optional[str] = None


class UserRoleAssignmentRequest(BaseModel):
    role_name: str
    scope_type: str = "GLOBAL"
    scope_id: Optional[str] = None


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    is_verified: bool
    role: str
    roles: List[str] = Field(default_factory=list)
    created_at: datetime
    last_login_at: Optional[datetime] = None


# 2. Session Schemas
class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    tenant_id: uuid.UUID
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_mfa_authenticated: bool
    expires_at: datetime
    last_seen_at: datetime
    is_revoked: bool


class RevokeSessionRequest(BaseModel):
    session_id: str
    reason: Optional[str] = "ADMIN_REVOCATION"


# 3. Roles & Permissions Schemas
class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    resource: str
    action: str
    description: str
    risk_level: str


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    is_internal: bool
    permissions: List[str] = Field(default_factory=list)


# 4. MFA Schemas
class MFASetupResponse(BaseModel):
    secret: str
    backup_codes: List[str]
    qr_code_uri: str


class MFAVerifyRequest(BaseModel):
    code: str


class StepUpAuthRequest(BaseModel):
    password: str
    totp_code: Optional[str] = None


class StepUpAuthResponse(BaseModel):
    step_up_token: str
    expires_in_minutes: int = 15


# 5. API Key Schemas
class APIKeyCreateRequest(BaseModel):
    name: str
    scopes: List[str]
    expires_in_days: Optional[int] = 90


class APIKeyCreatedResponse(BaseModel):
    id: uuid.UUID
    name: str
    key_prefix: str
    secret_key: str  # Displayed ONLY once
    scopes: List[str]
    expires_at: Optional[datetime] = None


class APIKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    key_prefix: str
    scopes: List[str]
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    is_revoked: bool
    created_at: datetime


# 6. Security Event Audit Schemas
class SecurityEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    event_type: str
    severity: str
    principal_id: str
    principal_type: str
    tenant_id: str
    action: Optional[str] = None
    resource: Optional[str] = None
    resource_id: Optional[str] = None
    result: str
    reason_code: str
    details: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    occurred_at: datetime


class SecurityMetricsResponse(BaseModel):
    active_sessions_count: int
    users_count: int
    security_events_last_24h: int
    failed_logins_last_24h: int
    mfa_enabled_users_count: int
    api_keys_active_count: int
