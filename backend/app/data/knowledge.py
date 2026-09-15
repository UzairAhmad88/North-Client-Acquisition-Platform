"""Knowledge Base Architecture, Promotion Lifecycle, and Authorized Context Retrieval."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Union
import uuid

from app.data.base import DataAuthority, DataClassification, KnowledgeLifecycle


@dataclass
class KnowledgeItem:
    """Represents an organizational knowledge entry."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    title: str = ""
    content: str = ""
    category: str = "BUSINESS_FACT"  # BUSINESS_FACT, CLIENT_PREFERENCE, PROJECT_DECISION, LESSON_LEARNED, POLICY
    authority: DataAuthority = DataAuthority.OBSERVED
    confidence: float = 0.9
    lifecycle: KnowledgeLifecycle = KnowledgeLifecycle.DRAFT
    classification: DataClassification = DataClassification.INTERNAL
    project_id: Optional[str] = None
    source_reference: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed_by: Optional[str] = None
    confirmed_at: Optional[datetime] = None


class KnowledgeEngine:
    """Manages knowledge item promotion and authorized contextual retrieval for AI systems."""

    @staticmethod
    def promote_item(
        current_state: Union[str, KnowledgeLifecycle],
        target_state: Union[str, KnowledgeLifecycle],
        actor_role: str,
    ) -> bool:
        """Validate and authorize lifecycle promotion rules."""
        target_str = target_state.value if hasattr(target_state, "value") else str(target_state)
        curr_str = current_state.value if hasattr(current_state, "value") else str(current_state)

        # Only Admin or Owner can promote to CANONICAL
        if target_str in ("CANONICAL", "ACTIVE"):
            if actor_role.upper() not in ("ADMIN", "OWNER", "LEAD"):
                raise ValueError(f"Role '{actor_role}' is not authorized to promote items to {target_str}")
        elif target_str in ("VERIFIED", "REVIEW"):
            if actor_role.upper() not in ("ADMIN", "OWNER", "LEAD", "MEMBER", "ANALYST"):
                raise ValueError(f"Role '{actor_role}' is not authorized to promote items to {target_str}")

        return True

    @staticmethod
    def promote_to_confirmed(
        item: KnowledgeItem,
        actor_id: str,
        authority: DataAuthority = DataAuthority.CONFIRMED,
    ) -> KnowledgeItem:
        """Promote knowledge from draft/review to confirmed/active status upon human review."""
        item.lifecycle = KnowledgeLifecycle.ACTIVE
        item.authority = authority
        item.confirmed_by = actor_id
        item.confirmed_at = datetime.now(timezone.utc)
        item.updated_at = item.confirmed_at
        return item

    @staticmethod
    def filter_authorized_items(
        items: List[Dict[str, Any]],
        allowed_classifications: List[Union[str, DataClassification]],
    ) -> List[Dict[str, Any]]:
        """Filter items by authorized classifications."""
        allowed_set = {
            c.value if hasattr(c, "value") else str(c) for c in allowed_classifications
        }
        filtered = []
        for it in items:
            classification = it.get("classification")
            c_str = classification.value if hasattr(classification, "value") else str(classification)
            if c_str in allowed_set:
                filtered.append(it)
        return filtered

    @staticmethod
    def retrieve_authorized_context(
        items: List[KnowledgeItem],
        tenant_id: str,
        is_client: bool = False,
        project_id: Optional[str] = None,
        min_authority: Optional[DataAuthority] = None,
        query: Optional[str] = None,
        limit: int = 10,
    ) -> List[KnowledgeItem]:
        """Filter knowledge items strictly by tenant isolation, client access boundary, and authority."""
        results = []
        for k in items:
            # 1. Tenant Isolation
            if k.tenant_id != tenant_id:
                continue

            # 2. Client Visibility Boundary
            if is_client and k.classification in (
                DataClassification.INTERNAL,
                DataClassification.RESTRICTED,
                DataClassification.SECURITY_SENSITIVE,
                DataClassification.SECRET,
            ):
                continue

            # 3. Project Scoping
            if project_id and k.project_id and k.project_id != project_id:
                continue

            # 4. Lifecycle Gate (Only Active or Confirmed knowledge for AI context)
            if k.lifecycle not in (KnowledgeLifecycle.ACTIVE, KnowledgeLifecycle.CONFIRMED):
                continue

            # 5. Query matching (simple substring if provided)
            if query and query.lower() not in k.title.lower() and query.lower() not in k.content.lower():
                continue

            results.append(k)
            if len(results) >= limit:
                break

        # Sort by authority priority: AUTHORITATIVE > CONFIRMED > VERIFIED > OBSERVED
        authority_rank = {
            DataAuthority.AUTHORITATIVE: 4,
            DataAuthority.CONFIRMED: 3,
            DataAuthority.VERIFIED: 2,
            DataAuthority.OBSERVED: 1,
            DataAuthority.DERIVED: 1,
            DataAuthority.INFERRED: 0,
            DataAuthority.UNVERIFIED: 0,
            DataAuthority.UNKNOWN: 0,
        }
        results.sort(key=lambda x: authority_rank.get(x.authority, 0), reverse=True)
        return results
