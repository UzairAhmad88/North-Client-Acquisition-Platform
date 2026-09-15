"""Assistant Retrieval Coordinator connecting Search, Knowledge, and Analytics."""

from typing import Any, Dict, List, Optional
from app.search.base import SearchEntityType
from app.search.service import GlobalSearchService


class AssistantRetriever:
    """Retrieves context records from Search, Knowledge, and Domain services under tenant authorization."""

    def __init__(self, search_service: Optional[GlobalSearchService] = None):
        self.search_service = search_service or GlobalSearchService()

    def retrieve_context(
        self,
        query: str,
        tenant_id: str,
        user_id: str,
        is_client: bool = False,
        role: str = "",
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Retrieve authorized records for assistant question answering."""
        search_res = self.search_service.execute_search(
            raw_query=query,
            tenant_id=tenant_id,
            user_id=user_id,
            is_client=is_client,
            role=role,
            limit=limit,
        )
        return search_res.get("results", [])
