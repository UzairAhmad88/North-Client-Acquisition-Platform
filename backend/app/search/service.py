"""Unified Search Service Orchestrator."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.search.authorization import SearchAuthorizer
from app.search.base import (
    IndexFreshness,
    ParsedQuery,
    SearchEntityType,
    SearchResultItem,
    SearchType,
)
from app.search.indexing import SearchIndexManager
from app.search.parser import QueryParser
from app.search.planner import QueryPlanner, StructuredQueryPlan
from app.search.ranking import SearchRanker
from app.search.snippets import SnippetGenerator
from app.search.suggestions import SuggestionEngine


class GlobalSearchService:
    """Core coordinator for unified search across all platform entities."""

    def __init__(self, index_manager: Optional[SearchIndexManager] = None):
        self.index_manager = index_manager or SearchIndexManager()
        self.parser = QueryParser()
        self.planner = QueryPlanner()
        self.ranker = SearchRanker()
        self.authorizer = SearchAuthorizer()
        self.snippet_gen = SnippetGenerator()
        self.suggestions = SuggestionEngine()

    def execute_search(
        self,
        raw_query: str,
        tenant_id: str,
        user_id: str,
        is_client: bool = False,
        role: str = "",
        entity_types: Optional[List[SearchEntityType]] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Execute complete search pipeline: Parse -> Plan -> Retrieve -> Authorize -> Rank -> Snippet."""
        start_time = datetime.now(timezone.utc)

        # 1. Parse Query
        parsed = self.parser.parse(raw_query)
        if entity_types and SearchEntityType.ALL not in entity_types:
            parsed.entity_types = entity_types
        if status:
            parsed.status = status
        if priority:
            parsed.priority = priority

        # 2. Generate Safe Query Plans
        plans = self.planner.plan(parsed, tenant_id=tenant_id, limit=limit, offset=offset)

        # 3. Retrieve Candidates from Search Index
        candidates: List[SearchResultItem] = []
        for plan in plans:
            # Check pre-retrieval permission
            if not self.authorizer.can_access_entity_type(plan.target_entity, is_client=is_client, role=role):
                continue

            results = self.index_manager.search(
                tenant_id=tenant_id,
                query_terms=plan.query_terms,
                entity_types=[plan.target_entity],
                status=parsed.status,
                priority=parsed.priority,
            )
            candidates.extend(results)

        # 4. Filter through Authorization & Tenant Boundaries
        authorized = self.authorizer.filter_authorized_results(
            items=candidates,
            tenant_id=tenant_id,
            user_id=user_id,
            is_client=is_client,
            role=role,
        )

        # 5. Multi-Factor Ranking & Sorting
        terms = parsed.normalized_query.split()
        ranked = self.ranker.rank_and_sort(
            items=authorized,
            query_terms=terms,
            raw_query=raw_query,
        )

        # 6. Generate Safe Snippets & Mask Metadata
        final_items: List[Dict[str, Any]] = []
        for item in ranked[offset : offset + limit]:
            safe_snippet = self.snippet_gen.generate(
                text=item.snippet,
                query_terms=terms,
                is_restricted=(is_client and item.metadata.get("visibility") == "INTERNAL"),
            )
            safe_meta = self.authorizer.mask_sensitive_fields(item.metadata, is_client=is_client)

            final_items.append({
                "id": item.id,
                "entity_type": item.entity_type.value,
                "entity_id": item.entity_id,
                "tenant_id": item.tenant_id,
                "title": item.title,
                "snippet": safe_snippet,
                "score": item.score,
                "status": item.status,
                "priority": item.priority,
                "action_url": item.action_url,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                "metadata": safe_meta,
            })

        latency_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000.0

        # Calculate Facet counts
        facets: Dict[str, int] = {}
        for it in authorized:
            facets[it.entity_type.value] = facets.get(it.entity_type.value, 0) + 1

        return {
            "query": raw_query,
            "parsed_query": {
                "search_type": parsed.search_type.value,
                "entity_types": [e.value for e in parsed.entity_types],
                "status": parsed.status,
                "priority": parsed.priority,
            },
            "total_count": len(authorized),
            "results": final_items,
            "facets": facets,
            "latency_ms": round(latency_ms, 2),
            "index_freshness": self.index_manager.freshness.value,
            "index_version": self.index_manager.version,
        }

    def get_suggestions(
        self, prefix: str, recent_queries: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Return autocomplete suggestions for the given prefix."""
        return self.suggestions.get_suggestions(prefix=prefix, recent_queries=recent_queries)
