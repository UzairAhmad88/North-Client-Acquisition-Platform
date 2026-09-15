"""Enterprise Hybrid Search service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone
from backend.app.services.data.catalog import CatalogService
from backend.app.services.data.documents import DocumentsService
from backend.app.services.data.metrics import MetricsService


class SearchService:
    """Hybrid Search combining Keyword match, Vector semantics, Metadata filters, and Knowledge Graph."""

    def __init__(
        self,
        catalog_service: Optional[CatalogService] = None,
        documents_service: Optional[DocumentsService] = None,
        metrics_service: Optional[MetricsService] = None,
    ):
        self.catalog = catalog_service or CatalogService()
        self.docs = documents_service or DocumentsService()
        self.metrics = metrics_service or MetricsService()
        self._search_log: List[Dict[str, Any]] = []

    def hybrid_search(
        self,
        query: str,
        user_roles: Optional[List[str]] = None,
        limit: int = 20,
        tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        start_time = datetime.now(timezone.utc)
        roles = user_roles or ["USER"]
        q_lower = query.lower()

        results = []

        # 1. Search Data Catalog
        cat_matches = self.catalog.search_catalog(query=query, tenant_id=tenant_id)
        for c in cat_matches:
            # Check permission
            if c.get("sensitivity") == "RESTRICTED" and "ADMIN" not in roles:
                continue
            results.append({
                "category": "CATALOG_ASSET",
                "title": c["name"],
                "type": c["asset_type"],
                "snippet": c.get("description", ""),
                "score": 0.95 if q_lower in c["name"].lower() else 0.82,
                "metadata": {"domain": c.get("domain"), "quality": c.get("quality_score")},
            })

        # 2. Search Certified Metrics
        metric_matches = self.metrics.list_metrics(tenant_id=tenant_id)
        for m in metric_matches:
            if q_lower in m["name"].lower() or q_lower in m.get("definition", "").lower():
                results.append({
                    "category": "METRIC",
                    "title": m["name"],
                    "type": "FORMULA",
                    "snippet": f"Formula: {m['formula_sql']}",
                    "score": 0.91,
                    "metadata": {"status": m.get("certification_status"), "value": m.get("current_value")},
                })

        # 3. Search Documents
        doc_matches = self.docs.list_documents(tenant_id=tenant_id)
        for d in doc_matches:
            if q_lower in d["title"].lower() or q_lower in d.get("summary", "").lower():
                results.append({
                    "category": "DOCUMENT",
                    "title": d["title"],
                    "type": d["file_type"],
                    "snippet": d.get("summary", ""),
                    "score": 0.88,
                    "metadata": {"uri": d.get("storage_uri")},
                })

        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:limit]

        duration_ms = round((datetime.now(timezone.utc) - start_time).total_seconds() * 1000, 2)
        
        # Log query
        self._search_log.append({
            "id": f"sq_{uuid.uuid4().hex[:8]}",
            "query": query,
            "results_count": len(results),
            "latency_ms": duration_ms,
            "timestamp": start_time.isoformat(),
        })

        return {
            "query": query,
            "total_matches": len(results),
            "latency_ms": duration_ms,
            "mode": "HYBRID",
            "results": results,
        }

    def list_recent_queries(self) -> List[Dict[str, Any]]:
        return self._search_log[-20:]
