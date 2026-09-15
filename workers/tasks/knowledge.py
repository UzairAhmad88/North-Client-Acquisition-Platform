"""
Celery Background Tasks for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform (Section 64).
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

try:
    from app.knowledge.service import KnowledgePlatformService
except ImportError:
    from backend.app.knowledge.service import KnowledgePlatformService

_knowledge_service = KnowledgePlatformService()


def task_chunk_and_embed_document(
    document_id: str,
    title: str,
    content: str,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Processes document into structural chunks, extracts candidate facts, and updates semantic vectors."""
    res = _knowledge_service.process_document(
        document_id=document_id,
        title=title,
        content=content,
        tenant_id=tenant_id,
    )
    return {
        "task": "chunk_and_embed_document",
        "status": "SUCCESS",
        "document_id": document_id,
        "chunks_count": res.get("chunks_count", 0),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_audit_knowledge_freshness(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Sweeps knowledge items to update freshness statuses (FRESH, AGING, STALE, EXPIRED)."""
    items = _knowledge_service.store.list_items(tenant_id=tenant_id)
    stale_items = []
    for it in items:
        status = _knowledge_service.evaluate_item_freshness(it)
        if status.value in ("STALE", "EXPIRED"):
            stale_items.append(it.knowledge_code)

    return {
        "task": "audit_knowledge_freshness",
        "status": "SUCCESS",
        "audited_count": len(items),
        "stale_count": len(stale_items),
        "stale_items": stale_items,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_detect_knowledge_conflicts(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Scans all facts and claims for active contradictions, flagging them for human review."""
    conflicts = _knowledge_service.detect_conflicts(tenant_id=tenant_id)
    return {
        "task": "detect_knowledge_conflicts",
        "status": "SUCCESS",
        "detected_conflicts_count": len(conflicts),
        "conflicts": [c.conflict_code for c in conflicts],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def task_rebuild_semantic_index(tenant_id: str = "default_tenant") -> Dict[str, Any]:
    """Rebuilds semantic vector embeddings from authoritative knowledge records (Rule 11 & 12)."""
    items = _knowledge_service.store.list_items(tenant_id=tenant_id)
    indexed = 0
    for it in items:
        _knowledge_service.semantic_engine.generate_embedding(
            source_id=it.knowledge_code,
            text=f"{it.title} {it.content}",
        )
        indexed += 1

    return {
        "task": "rebuild_semantic_index",
        "status": "SUCCESS",
        "indexed_count": indexed,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
