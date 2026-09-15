"""Multi-Factor Search Ranking Engine."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from app.search.base import SearchEntityType, SearchResultItem


class SearchRanker:
    """Computes multi-factor relevance scores for search results."""

    # Configurable weighting weights
    WEIGHT_LEXICAL = 0.30
    WEIGHT_SEMANTIC = 0.20
    WEIGHT_EXACT = 0.15
    WEIGHT_RECENCY = 0.15
    WEIGHT_IMPORTANCE = 0.10
    WEIGHT_USER_CONTEXT = 0.10

    @classmethod
    def calculate_score(
        cls,
        item: SearchResultItem,
        query_terms: List[str],
        raw_query: str,
        user_recent_entity_ids: Optional[List[str]] = None,
        now: Optional[datetime] = None,
    ) -> float:
        """Calculate weighted score between 0.0 and 1.0."""
        if now is None:
            now = datetime.now(timezone.utc)

        title_lower = (item.title or "").lower()
        snippet_lower = (item.snippet or "").lower()
        combined_text = f"{title_lower} {snippet_lower}"

        # 1. Exact match score
        exact_score = 0.0
        clean_raw = raw_query.strip('"').lower()
        if clean_raw and clean_raw in title_lower:
            exact_score = 1.0
        elif clean_raw and clean_raw in snippet_lower:
            exact_score = 0.7

        # 2. Lexical term match score
        lexical_score = 0.0
        if query_terms:
            matched = sum(1 for term in query_terms if term in combined_text)
            lexical_score = min(1.0, matched / len(query_terms))
            # Title matches receive higher weight
            title_matched = sum(1 for term in query_terms if term in title_lower)
            if title_matched > 0:
                lexical_score = min(1.0, lexical_score + 0.2)

        # 3. Semantic similarity score (passed via metadata or calculated)
        semantic_score = item.metadata.get("semantic_score", 0.5)

        # 4. Recency score (decays over 30 days)
        recency_score = 0.5
        if item.updated_at:
            dt = item.updated_at
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            days_old = max(0, (now - dt).total_seconds() / 86400.0)
            recency_score = max(0.1, 1.0 - (days_old / 30.0))

        # 5. Entity importance
        importance_score = 0.5
        if item.priority in ("CRITICAL", "HIGH", "URGENT"):
            importance_score = 0.9
        elif item.status in ("QUALIFIED", "AT_RISK", "BLOCKED"):
            importance_score = 0.8
        elif item.entity_type in (SearchEntityType.PROJECT, SearchEntityType.CONTRACT):
            importance_score = 0.7

        # 6. User context score
        context_score = 0.0
        if user_recent_entity_ids and item.entity_id in user_recent_entity_ids:
            context_score = 1.0

        # Weighted combination
        total_score = (
            cls.WEIGHT_LEXICAL * lexical_score
            + cls.WEIGHT_SEMANTIC * semantic_score
            + cls.WEIGHT_EXACT * exact_score
            + cls.WEIGHT_RECENCY * recency_score
            + cls.WEIGHT_IMPORTANCE * importance_score
            + cls.WEIGHT_USER_CONTEXT * context_score
        )

        return round(min(1.0, max(0.0, total_score)), 4)

    @classmethod
    def rank_and_sort(
        cls,
        items: List[SearchResultItem],
        query_terms: List[str],
        raw_query: str,
        user_recent_entity_ids: Optional[List[str]] = None,
    ) -> List[SearchResultItem]:
        """Rank items and sort descending by score."""
        now = datetime.now(timezone.utc)
        for item in items:
            item.score = cls.calculate_score(
                item=item,
                query_terms=query_terms,
                raw_query=raw_query,
                user_recent_entity_ids=user_recent_entity_ids,
                now=now,
            )

        return sorted(items, key=lambda x: x.score, reverse=True)
