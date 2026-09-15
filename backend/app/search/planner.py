"""Query Planner: Generates safe, parameterized query plans from ParsedQuery objects."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.search.base import ParsedQuery, SearchEntityType, SearchFilter, SearchType


@dataclass
class StructuredQueryPlan:
    """Safe, parameterized query execution plan."""

    tenant_id: str
    target_entity: SearchEntityType
    search_type: SearchType
    query_terms: List[str]
    parameters: Dict[str, Any]
    filters: List[SearchFilter]
    limit: int = 50
    offset: int = 0
    sort_by: str = "relevance"
    sort_desc: bool = True
    is_safe: bool = True
    explanation: Optional[str] = None


class QueryPlanner:
    """Constructs parameterized query plans without allowing dynamic raw SQL injection."""

    @classmethod
    def plan(
        cls,
        parsed_query: ParsedQuery,
        tenant_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[StructuredQueryPlan]:
        """Generate structured plans for each targeted entity type."""
        plans: List[StructuredQueryPlan] = []

        entity_targets = parsed_query.entity_types
        if SearchEntityType.ALL in entity_targets:
            # Expand to major searchable entity types
            entity_targets = [
                SearchEntityType.BUSINESS,
                SearchEntityType.LEAD,
                SearchEntityType.PROJECT,
                SearchEntityType.PROPOSAL,
                SearchEntityType.CONTRACT,
                SearchEntityType.DOCUMENT,
                SearchEntityType.TASK,
            ]

        # Tokenize query terms safely
        import re
        clean_text = re.sub(r"[^\w\s]", "", parsed_query.normalized_query)
        terms = [
            t.lower()
            for t in clean_text.split()
            if len(t) > 1 and not cls._is_stop_word(t.lower())
        ]

        for entity in entity_targets:
            params: Dict[str, Any] = {
                "tenant_id": tenant_id,
                "terms": terms,
            }
            if parsed_query.status:
                params["status"] = parsed_query.status
            if parsed_query.priority:
                params["priority"] = parsed_query.priority

            plan = StructuredQueryPlan(
                tenant_id=tenant_id,
                target_entity=entity,
                search_type=parsed_query.search_type,
                query_terms=terms,
                parameters=params,
                filters=parsed_query.filters,
                limit=limit,
                offset=offset,
                explanation=f"Safe structured search plan for {entity.value}",
            )
            plans.append(plan)

        return plans

    @staticmethod
    def _is_stop_word(word: str) -> bool:
        stop_words = {
            "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
            "with", "all", "is", "are", "of", "by", "from", "show", "find",
            "which", "what", "where", "me", "this", "that", "these", "those"
        }
        return word in stop_words
