"""Document & File Authorization and Access Control Layer."""

from typing import Any, Dict, List, Optional
from app.documents.base import DocumentVisibility, SensitivityLevel, SharePermission


class DocumentAuthorizer:
    """Enforces multi-tenant isolation, RBAC, client visibility boundaries, and sensitivity policies."""

    def authorize_read(
        self,
        tenant_id: str,
        user_tenant_id: str,
        user_role: str,
        visibility: str,
        sensitivity: str,
        is_client_user: bool = False,
    ) -> bool:
        """Check if user can view/read document."""
        # 1. Multi-tenant isolation
        if tenant_id != user_tenant_id:
            return False

        # 2. System administrators always have access within their tenant
        if user_role in ["ADMIN", "SYSTEM_ADMIN"]:
            return True

        # 3. Client user boundary
        if is_client_user:
            if visibility != DocumentVisibility.CLIENT_VISIBLE.value:
                return False
            if sensitivity in [SensitivityLevel.CONFIDENTIAL.value, SensitivityLevel.RESTRICTED.value]:
                return False
            return True

        # 4. Internal users
        if visibility == DocumentVisibility.RESTRICTED.value and user_role not in ["ADMIN", "MANAGER", "SECURITY_OFFICER"]:
            return False

        return True

    def authorize_action(
        self,
        action: SharePermission,
        user_role: str,
        is_client_user: bool = False,
        is_owner: bool = False,
    ) -> bool:
        """Check if user is authorized to perform specific action on document."""
        if user_role in ["ADMIN", "SYSTEM_ADMIN"]:
            return True

        if action == SharePermission.VIEW:
            return True

        if action == SharePermission.DOWNLOAD:
            return True

        if action == SharePermission.COMMENT:
            return True

        if action in [SharePermission.EDIT, SharePermission.SHARE]:
            return is_owner or user_role in ["OPERATOR", "MANAGER", "DEVELOPER"]

        if action == SharePermission.APPROVE:
            # Client users cannot approve internal documents; internal approvals require manager or admin
            if is_client_user:
                return False
            return user_role in ["ADMIN", "MANAGER", "APPROVER", "DIRECTOR"]

        return False

    def mask_sensitive_fields(self, metadata: Dict[str, Any], is_client_user: bool) -> Dict[str, Any]:
        """Strip internal margins, developer comments, and restricted cost details for client users."""
        if not is_client_user:
            return metadata

        masked = dict(metadata)
        for key in ["internal_notes", "margins", "cost_breakdown", "raw_ai_trace", "secret_references", "developer_remarks"]:
            masked.pop(key, None)
        return masked
