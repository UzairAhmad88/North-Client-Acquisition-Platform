"""
Knowledge Extraction Agent (Section 21, 22, 63).
Extracts candidate entities, facts, and chunks from raw documents and conversations.
Enforces Rule 1 & 2: Candidate facts are created strictly as INFERRED drafts, never Authoritative.
"""

from typing import Any, Dict, List, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.knowledge.extraction.engine import DocumentIntelligenceEngine
except ImportError:
    from app.knowledge.extraction.engine import DocumentIntelligenceEngine


class KnowledgeExtractionAgent(BaseAgent):
    """
    Agent responsible for extracting candidate knowledge from documents and client interactions.
    Produces DRAFT knowledge with INFERRED authority.
    """

    agent_id = "knowledge_extraction_agent"
    name = "Knowledge Extraction Agent"
    version = "1.0"
    description = "Parses documents and interactions into chunks, extracting candidate entities and unverified inferred facts."

    def __init__(self):
        super().__init__()
        self.engine = DocumentIntelligenceEngine()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_DOCUMENTS,
            AgentPermission.CREATE_KNOWLEDGE_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        doc_id = str(params.get("document_id") or "doc_sample")
        content = str(params.get("content") or "")
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")

        if not content:
            return {
                "status": "ERROR",
                "message": "Document content is empty or missing.",
                "chunks": [],
                "entities": [],
                "candidate_facts": [],
            }

        chunks = self.engine.chunk_document(doc_id, content, tenant_id=tenant_id)
        entities = self.engine.extract_entities(doc_id, content, tenant_id=tenant_id)
        candidate_facts = self.engine.extract_candidate_facts(doc_id, content, tenant_id=tenant_id)

        return {
            "status": "SUCCESS",
            "document_id": doc_id,
            "chunks_count": len(chunks),
            "chunks": [c.model_dump() for c in chunks],
            "entities": [e.model_dump() for e in entities],
            "candidate_facts": [f.model_dump() for f in candidate_facts],
            "authority_notice": "Candidate facts are INFERRED drafts and require human confirmation.",
        }
