"""Session Lifecycle, Revocation, and Token Management."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple
import uuid

import jwt

from app.core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
IDLE_TIMEOUT_MINUTES = 60
ABSOLUTE_TIMEOUT_HOURS = 24


@dataclass
class SessionInfo:
    """Active session metadata."""

    session_id: str
    user_id: str
    tenant_id: str
    created_at: datetime
    expires_at: datetime
    last_seen_at: datetime
    is_revoked: bool = False
    revoked_at: Optional[datetime] = None
    revocation_reason: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_mfa_authenticated: bool = False


class SessionManager:
    """Manages short-lived JWT tokens, session lifecycle, and timeout enforcement."""

    @staticmethod
    def create_access_token(
        user_id: str,
        tenant_id: str,
        session_id: str,
        roles: list,
        is_mfa: bool = False,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        expires = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        payload = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "session_id": session_id,
            "roles": roles,
            "is_mfa": is_mfa,
            "iat": now,
            "exp": expires,
            "type": "access",
        }
        return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

    @staticmethod
    def create_refresh_token(
        user_id: str,
        session_id: str,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        expires = now + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        payload = {
            "sub": user_id,
            "session_id": session_id,
            "iat": now,
            "exp": expires,
            "type": "refresh",
        }
        return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])

    @staticmethod
    def is_session_active(
        created_at: datetime,
        last_seen_at: datetime,
        is_revoked: bool,
    ) -> Tuple[bool, str]:
        now = datetime.now(timezone.utc)
        if is_revoked:
            return False, "SESSION_REVOKED"

        # Absolute timeout
        if (now - created_at) > timedelta(hours=ABSOLUTE_TIMEOUT_HOURS):
            return False, "ABSOLUTE_TIMEOUT_EXCEEDED"

        # Idle timeout
        if (now - last_seen_at) > timedelta(minutes=IDLE_TIMEOUT_MINUTES):
            return False, "IDLE_TIMEOUT_EXCEEDED"

        return True, "SESSION_ACTIVE"

