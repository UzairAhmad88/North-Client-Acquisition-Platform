"""Knowledge RAG & Retrieval service for Phase 65."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from backend.app.services.data.documents import DocumentsService
from backend.app.services.data.knowledge_graph import KnowledgeGraphService
from backend.app.services.data.memory import MemoryService
from backend.app.services.data.metrics import MetricsService


class RetrievalService:
    """Combines documents, structured tables, knowledge graph, and AI memory into unified context."""

    def __init__(
        self,
        docs: Optional[DocumentsService] = None,
        kg: Optional[KnowledgeGraphService] = None,
        memory: Optional[MemoryService] = None,
        metrics: Optional[MetricsService] = None,
    ):
        self.docs = docs or DocumentsService()
        self.kg = kg or KnowledgeGraphService()
        self.memory = memory or MemoryService()
        self.metrics = metrics or MetricsService()

    def retrieve_context(self, prompt_or_topic: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        p_lower = prompt_or_topic.lower()

        # 1. Document chunks
        matched_docs = []
        for d in self.docs.list_documents(tenant_id=tenant_id):
            if any(word in d["title"].lower() or word in d.get("summary", "").lower() for word in p_lower.split()):
                chunks = self.docs.get_document_chunks(d["id"], tenant_id=tenant_id)
                matched_docs.extend([{"doc_title": d["title"], "content": c["content"]} for c in chunks[:2]])

        # 2. Graph entities
        graph_data = self.kg.query_graph(depth=1, tenant_id=tenant_id)
        matched_nodes = [
            n for n in graph_data["nodes"]
            if any(w in n["name"].lower() or w in n["label"].lower() for w in p_lower.split())
        ]

        # 3. AI Memory
        memories = self.memory.list_memories(tenant_id=tenant_id)
        matched_memories = [m for m in memories if any(w in m["content"].lower() for w in p_lower.split())]

        # 4. Certified metrics
        certified_metrics = [
            m for m in self.metrics.list_metrics(tenant_id=tenant_id)
            if any(w in m["name"].lower() for w in p_lower.split())
        ]

        return {
            "topic": prompt_or_topic,
            "document_passages": matched_docs[:3],
            "graph_entities": matched_nodes[:5],
            "memories": matched_memories[:3],
            "certified_metrics": certified_metrics[:2],
            "citations": [f"KnowledgeGraph: {n['name']}" for n in matched_nodes[:2]] + [f"Doc: {d.get('doc_title')}" for d in matched_docs[:2]],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
