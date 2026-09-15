"""
Semantic Intelligence & Vector Retrieval Engine (Section 18 & 19).
Computes deterministic embeddings, measures cosine similarity, and manages versioned vector indices.
"""

from datetime import datetime, timezone
import hashlib
import math
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    from backend.app.knowledge.base import KnowledgeChunk
except ImportError:
    from app.knowledge.base import KnowledgeChunk


class EmbeddingResult:
    def __init__(self, vector: List[float], source_id: str):
        self.vector = vector
        self.source_id = source_id


class SemanticIntelligenceEngine:
    """Computes dense vector representations and performs vector similarity search."""

    def __init__(self, dimensions: int = 256, model_version: str = "1.0"):
        self.dimensions = dimensions
        self.model_version = model_version
        self.model_name = "text-embedding-3-small"
        # chunk_code -> (embedding_vector, chunk_object)
        self._vector_index: Dict[str, Tuple[List[float], KnowledgeChunk]] = {}

    def generate_embedding(self, source_id: str, text: str) -> EmbeddingResult:
        vec = self.compute_embedding(text)
        return EmbeddingResult(vector=vec, source_id=source_id)

    STOPWORDS = {
        "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with",
        "is", "are", "was", "were", "of", "by", "as", "be", "this", "that", "it"
    }

    def compute_embedding(self, text: str) -> List[float]:
        """
        Generates deterministic, unit-normalized dense embedding vector based on word token hashing.
        Allows instantaneous vector retrieval operations without external API dependencies or GPU requirements.
        """
        if not text:
            return [0.0] * self.dimensions

        vector = [0.0] * self.dimensions
        clean_text = text.lower()
        raw_tokens = re.findall(r"[a-z0-9_\-]+", clean_text)

        for token in raw_tokens:
            if not token or token in self.STOPWORDS:
                continue
            token_hash = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
            dim_idx = token_hash % self.dimensions
            vector[dim_idx] += 1.0

        # L2 Unit Normalization
        norm = math.sqrt(sum(x * x for x in vector))
        if norm > 0.0:
            vector = [round(x / norm, 6) for x in vector]

        return vector

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Calculates exact cosine similarity between two normalized vectors."""
        if len(vec_a) != len(vec_b) or not vec_a or not vec_b:
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        sim = dot_product / (norm_a * norm_b)
        return max(0.0, min(1.0, round(sim, 4)))

    def index_chunk(self, chunk: KnowledgeChunk) -> List[float]:
        """Generates embedding for a chunk and indexes it in the vector store."""
        vector = self.compute_embedding(chunk.content)
        self._vector_index[chunk.chunk_code] = (vector, chunk)
        return vector

    def search_similar_chunks(
        self,
        query: str,
        top_k: int = 5,
        min_similarity: float = 0.1,
        tenant_id: str = "default_tenant",
    ) -> List[Dict[str, Any]]:
        """Performs vector similarity search against indexed document chunks."""
        query_vector = self.compute_embedding(query)
        scored_results: List[Dict[str, Any]] = []

        for chunk_code, (chunk_vector, chunk) in self._vector_index.items():
            # Rule 5: Tenant isolation enforced on vector retrieval
            if chunk.tenant_id != tenant_id:
                continue

            similarity = self.cosine_similarity(query_vector, chunk_vector)
            if similarity >= min_similarity:
                scored_results.append(
                    {
                        "chunk_code": chunk_code,
                        "document_id": chunk.document_id,
                        "section_heading": chunk.section_heading,
                        "content": chunk.content,
                        "similarity_score": similarity,
                        "access_scope": chunk.access_scope,
                    }
                )

        scored_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_results[:top_k]

    def total_indexed_chunks(self) -> int:
        return len(self._vector_index)

    def rebuild_index(self, chunks: List[KnowledgeChunk]) -> int:
        """Rebuilds the entire vector index from authoritative chunk records (Rule 12: Index != Source of Truth)."""
        self._vector_index.clear()
        for c in chunks:
            self.index_chunk(c)
        return len(self._vector_index)
