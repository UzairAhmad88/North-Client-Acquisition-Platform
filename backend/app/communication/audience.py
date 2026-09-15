"""Audience Resolution, Tenant Isolation, and Recipient Safety Filtering."""

from typing import Any, Dict, List, Optional, Set
from app.communication.base import CommunicationType, MessageVisibility


class AudienceResolver:
    """Resolves and filters notification and communication recipients safely."""

    @staticmethod
    def resolve_recipients(
        tenant_id: str,
        explicit_recipients: Optional[List[str]] = None,
        role_targets: Optional[List[str]] = None,
        project_members: Optional[List[Dict[str, Any]]] = None,
        client_users: Optional[List[Dict[str, Any]]] = None,
        visibility: MessageVisibility = MessageVisibility.INTERNAL,
    ) -> List[str]:
        """Resolve valid recipient user IDs within tenant and visibility boundaries."""
        resolved: Set[str] = set()

        if explicit_recipients:
            for r in explicit_recipients:
                resolved.add(r)

        if project_members:
            for m in project_members:
                # Ensure tenant matching
                if m.get("tenant_id") == tenant_id:
                    user_id = m.get("user_id") or m.get("id")
                    if user_id:
                        resolved.add(user_id)

        if client_users and visibility == MessageVisibility.CLIENT_VISIBLE:
            for c in client_users:
                if c.get("tenant_id") == tenant_id:
                    client_id = c.get("user_id") or c.get("id")
                    if client_id:
                        resolved.add(client_id)

        return list(resolved)

    @staticmethod
    def filter_by_tenant(
        recipients: List[Dict[str, Any]], expected_tenant_id: str
    ) -> List[Dict[str, Any]]:
        """Strictly filter out any recipient belonging to another tenant."""
        return [r for r in recipients if r.get("tenant_id") == expected_tenant_id]
