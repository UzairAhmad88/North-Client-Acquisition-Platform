"""Search Suggestions and Query Autocompletion Engine."""

from typing import Any, Dict, List, Optional
from app.search.base import SearchEntityType


class SuggestionEngine:
    """Generates entity completions, query suggestions, and spelling corrections."""

    DEFAULT_SUGGESTIONS = [
        {"title": "High Priority Leads", "type": "SAVED_QUERY", "query": "high priority leads"},
        {"title": "Projects At Risk", "type": "SAVED_QUERY", "query": "projects at risk"},
        {"title": "Pending Contract Approvals", "type": "SAVED_QUERY", "query": "pending contract approvals"},
        {"title": "Open Support Incidents", "type": "SAVED_QUERY", "query": "open support incidents"},
        {"title": "Unconfirmed Requirements", "type": "SAVED_QUERY", "query": "unconfirmed requirements"},
    ]

    @classmethod
    def get_suggestions(
        cls,
        prefix: str,
        recent_queries: Optional[List[str]] = None,
        entity_titles: Optional[List[Dict[str, Any]]] = None,
        limit: int = 8,
    ) -> List[Dict[str, Any]]:
        """Return autocomplete and suggestion items based on query prefix."""
        results: List[Dict[str, Any]] = []
        clean_prefix = (prefix or "").strip().lower()

        # 1. Matching recent queries
        if recent_queries:
            for q in recent_queries:
                if not clean_prefix or clean_prefix in q.lower():
                    results.append({"text": q, "type": "RECENT_SEARCH", "category": "history"})
                    if len(results) >= limit:
                        return results

        # 2. Matching entity titles
        if entity_titles:
            for item in entity_titles:
                title = item.get("title", "")
                if not clean_prefix or clean_prefix in title.lower():
                    results.append({
                        "text": title,
                        "type": "ENTITY_MATCH",
                        "entity_type": item.get("entity_type"),
                        "entity_id": item.get("entity_id"),
                        "category": "entity",
                    })
                    if len(results) >= limit:
                        return results

        # 3. Fallback to default popular suggestions if prefix matches or prefix is empty
        for item in cls.DEFAULT_SUGGESTIONS:
            if not clean_prefix or clean_prefix in item["title"].lower():
                results.append({
                    "text": item["title"],
                    "type": item["type"],
                    "query": item["query"],
                    "category": "suggested",
                })
                if len(results) >= limit:
                    return results

        return results
