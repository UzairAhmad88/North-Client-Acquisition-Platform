"""Scope Manager classifying scope items and detecting scope expansion."""

from typing import List, Tuple
from agents.requirements.models import ExtractedRequirementSchema, ScopeItemSchema


class ScopeManager:
    """Manages scope item classifications and scope expansion detection."""

    @classmethod
    def process_scope(
        cls,
        requirements: List[ExtractedRequirementSchema],
        existing_scope_items: List[ScopeItemSchema] = None,
    ) -> Tuple[List[ScopeItemSchema], bool]:
        """
        Returns (scope_items, scope_expansion_detected)
        """
        scope_items: List[ScopeItemSchema] = []
        existing_titles = {item.description for item in (existing_scope_items or [])}
        scope_expansion = False

        for req in requirements:
            status = "UNKNOWN"
            if req.explicit and req.priority in ("CRITICAL", "HIGH"):
                status = "IN_SCOPE"
            elif req.priority == "OPTIONAL" or not req.explicit:
                status = "OPTIONAL"

            scope_items.append(
                ScopeItemSchema(
                    description=req.title,
                    scope_status=status,
                    priority=req.priority,
                    confirmed=(req.status == "CONFIRMED"),
                )
            )

            if existing_scope_items and req.title not in existing_titles and req.category in ("MOBILE", "CRM", "INVENTORY"):
                scope_expansion = True

        return scope_items, scope_expansion
