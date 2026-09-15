"""Unified Search Package."""

from app.search.authorization import SearchAuthorizer
from app.search.base import (
    IndexFreshness,
    ParsedQuery,
    SearchEntityType,
    SearchFilter,
    SearchResultItem,
    SearchType,
)
from app.search.indexing import SearchIndexManager
from app.search.parser import QueryParser
from app.search.planner import QueryPlanner, StructuredQueryPlan
from app.search.ranking import SearchRanker
from app.search.service import GlobalSearchService
from app.search.snippets import SnippetGenerator
from app.search.suggestions import SuggestionEngine

__all__ = [
    "SearchEntityType",
    "SearchType",
    "IndexFreshness",
    "SearchFilter",
    "ParsedQuery",
    "SearchResultItem",
    "QueryParser",
    "QueryPlanner",
    "StructuredQueryPlan",
    "SearchRanker",
    "SearchAuthorizer",
    "SnippetGenerator",
    "SearchIndexManager",
    "SuggestionEngine",
    "GlobalSearchService",
]
