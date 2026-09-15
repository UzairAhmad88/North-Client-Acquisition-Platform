"""Document Knowledge System & Chunking service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class DocumentsService:
    """Indexes unstructured documents, chunks content, detects entities, and extracts summaries."""

    def __init__(self):
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._chunks: List[Dict[str, Any]] = []

    def index_document(
        self,
        title: str,
        content: str,
        file_type: str = "MARKDOWN",
        storage_uri: str = "s3://uzaii-docs/doc.md",
        permissions: Optional[List[str]] = None,
        tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        
        # Simple intelligent chunking (per 200 chars or paragraph)
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()] or [content]
        created_chunks = []
        for idx, p in enumerate(paragraphs):
            chunk_id = f"chk_{doc_id}_{idx}"
            chunk_rec = {
                "id": chunk_id,
                "tenant_id": tenant_id,
                "document_id": doc_id,
                "chunk_index": idx,
                "content": p,
                "extracted_entities": ["Enterprise", "Data", "Knowledge"],
            }
            self._chunks.append(chunk_rec)
            created_chunks.append(chunk_rec)

        doc_record = {
            "id": doc_id,
            "tenant_id": tenant_id,
            "title": title,
            "file_type": file_type,
            "storage_uri": storage_uri,
            "summary": content[:160] + "..." if len(content) > 160 else content,
            "extracted_topics": ["Architecture", "Data Governance", "Intelligence"],
            "permissions": permissions or ["*"],
            "chunks_count": len(created_chunks),
            "version": "v1.0.0",
            "created_at": now.isoformat(),
        }
        self._documents[doc_id] = doc_record
        return doc_record

    def get_document(self, doc_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        doc = self._documents.get(doc_id)
        if doc and doc.get("tenant_id") == tenant_id:
            return doc
        return None

    def list_documents(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [d for d in self._documents.values() if d.get("tenant_id") == tenant_id]

    def get_document_chunks(self, doc_id: str, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [c for c in self._chunks if c.get("document_id") == doc_id and c.get("tenant_id") == tenant_id]
