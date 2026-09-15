"""Search Authorization, Tenant Isolation, and Field-Level Access Control."""

from typing import Any, Dict, List, Optional, Set

from app.search.base import SearchEntityType, SearchResultItem


class SearchAuthorizer:
    """Enforces multi-tenant isolation, role-based filters, and client boundaries on search operations."""

    # Entities completely restricted from client user accounts
    CLIENT_PROHIBITED_ENTITIES: Set[SearchEntityType] = {
        SearchEntityType.AI_TRACE,
        SearchEntityType.CHANGE_REQUEST,
        SearchEntityType.DEFECT,
        SearchEntityType.EVENT,
    }

    @classmethod
    def can_access_entity_type(
        cls, entity_type: SearchEntityType, is_client: bool = False, role: str = ""
    ) -> bool:
        """Check if principal has permission to search the specified entity category."""
        if is_client and entity_type in cls.CLIENT_PROHIBITED_ENTITIES:
            return False
        if entity_type == SearchEntityType.AI_TRACE and role not in ("ADMIN", "SECURITY_ADMIN", "DEVELOPER"):
            return False
        return True

    @classmethod
    def filter_authorized_results(
        cls,
        items: List[SearchResultItem],
        tenant_id: str,
        user_id: str,
        is_client: bool = False,
        role: str = "",
    ) -> List[SearchResultItem]:
        """Strictly filter search result items against tenant and client security boundaries."""
        authorized: List[SearchResultItem] = []

        for item in items:
            # 1. Enforce strict Tenant Isolation
            if item.tenant_id != tenant_id:
                continue

            # 2. Enforce Client Boundary
            if is_client:
                if item.entity_type in cls.CLIENT_PROHIBITED_ENTITIES:
                    continue
                if item.metadata.get("visibility") == "INTERNAL":
                    continue
                if item.metadata.get("classification") in ("RESTRICTED", "CONFIDENTIAL"):
                    continue

            # 3. Enforce AI Trace / System Audit role boundaries
            if item.entity_type == SearchEntityType.AI_TRACE and role not in ("ADMIN", "SECURITY_ADMIN", "DEVELOPER"):
                continue

            authorized.append(item)

        return authorized

    @classmethod
    def mask_sensitive_fields(
        cls, metadata: Dict[str, Any], is_client: bool = False
    ) -> Dict[str, Any]:
        """Strip internal cost, margin, and authentication tokens from result metadata."""
        cleaned = dict(metadata)
        if is_client:
            cleaned.pop("cost", None)
            cleaned.pop("internal_margin", None)
            cleaned.pop("risk_notes", None)
            cleaned.pop("private_notes", None)

        cleaned.pop("password", None)
        cleaned.pop("token", None)
        cleaned.pop("secret", None)
        return cleaned
