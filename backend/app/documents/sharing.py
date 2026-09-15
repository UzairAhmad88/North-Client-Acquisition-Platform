"""Document and file sharing manager with secure expiring links."""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.documents.base import SharePermission, ShareType


class DocumentShareManager:
    """Manages document shares, collaborator access, and secure expiring link generation."""

    def create_share(
        self,
        tenant_id: str,
        document_id: str,
        shared_by: str,
        share_type: ShareType,
        target_id: str,  # user_id, team_id, project_id, or client_id
        permissions: List[SharePermission],
    ) -> Dict[str, Any]:
        return {
            "share_id": str(uuid4()),
            "tenant_id": tenant_id,
            "document_id": document_id,
            "shared_by": shared_by,
            "share_type": share_type.value,
            "target_id": target_id,
            "permissions": [p.value for p in permissions],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def generate_secure_share_link(
        self,
        tenant_id: str,
        document_id: str,
        created_by: str,
        expires_in_hours: int = 24,
        allow_download: bool = False,
        passcode: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate high-entropy expiring share link token."""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=expires_in_hours)

        return {
            "link_id": str(uuid4()),
            "tenant_id": tenant_id,
            "document_id": document_id,
            "token": token,
            "permissions": [SharePermission.VIEW.value] + ([SharePermission.DOWNLOAD.value] if allow_download else []),
            "expires_at": expires_at.isoformat(),
            "created_by": created_by,
            "revoked_at": None,
            "access_count": 0,
            "has_passcode": bool(passcode),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def validate_share_link(self, link_data: Dict[str, Any]) -> bool:
        """Validate if link is active, unexpired, and unrevoked."""
        if link_data.get("revoked_at"):
            return False

        expires_at_str = link_data.get("expires_at")
        if expires_at_str:
            expires_at = datetime.fromisoformat(expires_at_str)
            if datetime.now(timezone.utc) > expires_at:
                return False

        return True
