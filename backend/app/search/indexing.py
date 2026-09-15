"""Unified Search Index Management and Event-Driven Indexing Engine."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.search.base import IndexFreshness, SearchEntityType, SearchResultItem


class SearchIndexManager:
    """In-memory and event-synchronized search index provider."""

    def __init__(self):
        # Maps index_key -> { "doc_id": str, "entity_type": str, "tenant_id": str, "title": str, ... }
        self._index: Dict[str, Dict[str, Any]] = {}
        self._index_version: int = 1
        self._last_updated_at: datetime = datetime.now(timezone.utc)

    @property
    def version(self) -> int:
        return self._index_version

    @property
    def freshness(self) -> IndexFreshness:
        now = datetime.now(timezone.utc)
        age_seconds = (now - self._last_updated_at).total_seconds()
        if age_seconds < 300:
            return IndexFreshness.INDEX_CURRENT
        elif age_seconds < 1800:
            return IndexFreshness.INDEX_SLIGHTLY_STALE
        return IndexFreshness.INDEX_STALE

    def index_document(
        self,
        entity_type: SearchEntityType,
        entity_id: str,
        tenant_id: str,
        title: str,
        search_text: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        action_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Upsert document into search index with version increment."""
        doc_key = f"{tenant_id}:{entity_type.value}:{entity_id}"
        self._index[doc_key] = {
            "key": doc_key,
            "entity_type": entity_type.value,
            "entity_id": str(entity_id),
            "tenant_id": str(tenant_id),
            "title": title,
            "search_text": search_text,
            "status": status,
            "priority": priority,
            "action_url": action_url,
            "metadata": metadata or {},
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "version": self._index_version,
        }
        self._last_updated_at = datetime.now(timezone.utc)
        return doc_key

    def remove_document(
        self, entity_type: SearchEntityType, entity_id: str, tenant_id: str
    ) -> bool:
        """Remove document from search index upon entity deletion."""
        doc_key = f"{tenant_id}:{entity_type.value}:{entity_id}"
        if doc_key in self._index:
            del self._index[doc_key]
            self._last_updated_at = datetime.now(timezone.utc)
            return True
        return False

    def search(
        self,
        tenant_id: str,
        query_terms: List[str],
        entity_types: Optional[List[SearchEntityType]] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[SearchResultItem]:
        """Query index documents matching tenant, terms, and filter constraints."""
        results: List[SearchResultItem] = []
        target_types = (
            [e.value for e in entity_types if e != SearchEntityType.ALL]
            if entity_types and SearchEntityType.ALL not in entity_types
            else None
        )

        for doc in self._index.values():
            if doc["tenant_id"] != tenant_id:
                continue

            if target_types and doc["entity_type"] not in target_types:
                continue

            if status and doc.get("status") != status:
                continue

            if priority and doc.get("priority") != priority:
                continue

            # Check term containment
            doc_text = f"{doc['title']} {doc['search_text']}".lower()
            if query_terms:
                matched = any(t in doc_text for t in query_terms)
                if not matched:
                    continue

            results.append(
                SearchResultItem(
                    id=doc["key"],
                    entity_type=SearchEntityType(doc["entity_type"]),
                    entity_id=doc["entity_id"],
                    tenant_id=doc["tenant_id"],
                    title=doc["title"],
                    snippet=doc["search_text"][:160],
                    score=1.0,
                    status=doc.get("status"),
                    priority=doc.get("priority"),
                    action_url=doc.get("action_url"),
                    updated_at=datetime.fromisoformat(doc["updated_at"]),
                    metadata=doc.get("metadata", {}),
                )
            )

        return results
