"""
Hybrid Search & Multi-Factor Relevance Ranking Engine (Section 14-17, 43).
Fuses keyword lexical search, semantic vector similarity, authority tiers, and freshness decay.
"""

from datetime import datetime, timezone
import re
from typing import Any, Dict, List, Optional

try:
    from backend.app.knowledge.base import (
        FreshnessStatus,
        KnowledgeAuthority,
        KnowledgeDomain,
        KnowledgeItem,
        SearchResultItem,
    )
    from backend.app.knowledge.items.store import KnowledgeStore
    from backend.app.knowledge.semantic.engine import SemanticIntelligenceEngine
except ImportError:
    from app.knowledge.base import (
        FreshnessStatus,
        KnowledgeAuthority,
        KnowledgeDomain,
        KnowledgeItem,
        SearchResultItem,
    )
    from app.knowledge.items.store import KnowledgeStore
    from app.knowledge.semantic.engine import SemanticIntelligenceEngine


class HybridSearchEngine:
    """Multi-strategy search engine evaluating exact lexical match, semantic vectors, authority, and freshness."""

    AUTHORITY_WEIGHTS: Dict[KnowledgeAuthority, float] = {
        KnowledgeAuthority.AUTHORITATIVE: 1.0,
        KnowledgeAuthority.VERIFIED: 0.9,
        KnowledgeAuthority.CONFIRMED: 0.85,
        KnowledgeAuthority.OBSERVED: 0.70,
        KnowledgeAuthority.DERIVED: 0.65,
        KnowledgeAuthority.INFERRED: 0.50,
        KnowledgeAuthority.UNVERIFIED: 0.30,
        KnowledgeAuthority.UNKNOWN: 0.20,
    }

    FRESHNESS_WEIGHTS: Dict[FreshnessStatus, float] = {
        FreshnessStatus.FRESH: 1.0,
        FreshnessStatus.AGING: 0.8,
        FreshnessStatus.STALE: 0.4,
        FreshnessStatus.EXPIRED: 0.1,
        FreshnessStatus.UNKNOWN: 0.5,
    }

    def __init__(self, store: KnowledgeStore, semantic_engine: SemanticIntelligenceEngine):
        self.store = store
        self.semantic_engine = semantic_engine

    def search(
        self,
        query: str,
        domain: Optional[KnowledgeDomain] = None,
        strategy: str = "HYBRID",  # KEYWORD, SEMANTIC, HYBRID
        top_k: int = 10,
        tenant_id: str = "default_tenant",
        user_role: str = "INTERNAL_USER",
    ) -> List[SearchResultItem]:
        """
        Executes permission-aware hybrid search across governed organizational knowledge.
        Enforces Rule 4-6: Tenant isolation and resource access scopes are strictly evaluated before ranking.
        """
        if not query or not query.strip():
            return []

        all_items = self.store.list_items(domain=domain, tenant_id=tenant_id)
        # Role-based confidentiality filtering
        if user_role == "CLIENT_USER":
            all_items = [i for i in all_items if i.classification == "PUBLIC"]
        elif user_role == "INTERNAL_USER":
            all_items = [i for i in all_items if i.classification in ["PUBLIC", "INTERNAL", "CONFIDENTIAL"]]
        # PRIVILEGED_ADMIN sees RESTRICTED as well

        raw_query_tokens = set(re.findall(r"\w+", query.lower()))
        query_tokens = raw_query_tokens - self.semantic_engine.STOPWORDS
        if not query_tokens:
            query_tokens = raw_query_tokens

        query_vector = self.semantic_engine.compute_embedding(query)
        scored_results: List[SearchResultItem] = []

        for item in all_items:
            # 1. Lexical Exact & Keyword Match Score
            item_text = f"{item.knowledge_code} {item.title} {item.content}".lower()
            item_tokens = set(re.findall(r"\w+", item_text))
            token_intersection = query_tokens.intersection(item_tokens)
            keyword_score = (len(token_intersection) / max(len(query_tokens), 1)) if query_tokens else 0.0

            # Exact phrase bonus
            if query.lower() in item_text:
                keyword_score = min(1.0, keyword_score + 0.3)

            # 2. Semantic Similarity Score
            item_vector = self.semantic_engine.compute_embedding(f"{item.title} {item.content}")
            semantic_score = self.semantic_engine.cosine_similarity(query_vector, item_vector)

            # Skip items with zero keyword overlap and negligible semantic similarity
            if keyword_score == 0.0 and semantic_score < 0.20:
                continue

            # 3. Authority Weight
            authority_weight = self.AUTHORITY_WEIGHTS.get(item.authority, 0.5)

            # 4. Freshness Weight
            freshness_weight = self.FRESHNESS_WEIGHTS.get(item.freshness_status, 0.5)

            # 5. Composite Ranking Formula (Section 43)
            if strategy == "KEYWORD":
                composite_score = keyword_score
            elif strategy == "SEMANTIC":
                composite_score = semantic_score
            else:  # HYBRID
                composite_score = (
                    (0.35 * semantic_score)
                    + (0.25 * keyword_score)
                    + (0.20 * authority_weight)
                    + (0.10 * freshness_weight)
                    + (0.10 * (1.0 if token_intersection else 0.0))
                )

            composite_score = round(composite_score, 4)

            # Highlight snippet
            snippet = self._generate_snippet(item.content, query_tokens)

            scored_results.append(
                SearchResultItem(
                    knowledge_code=item.knowledge_code,
                    title=item.title,
                    snippet=snippet,
                    domain=item.domain.value if hasattr(item.domain, "value") else str(item.domain),
                    item_type=item.item_type.value if hasattr(item.item_type, "value") else str(item.item_type),
                    authority=item.authority.value if hasattr(item.authority, "value") else str(item.authority),
                    provenance=item.provenance.value if hasattr(item.provenance, "value") else str(item.provenance),
                    freshness=item.freshness_status.value if hasattr(item.freshness_status, "value") else str(item.freshness_status),
                    score=composite_score,
                    relevance_factors={
                        "semantic_score": semantic_score,
                        "keyword_score": keyword_score,
                        "authority_weight": authority_weight,
                        "freshness_weight": freshness_weight,
                        "authority": authority_weight,
                        "freshness": freshness_weight,
                    },
                )
            )

        scored_results.sort(key=lambda x: x.score, reverse=True)
        return scored_results[:top_k]

    @staticmethod
    def _generate_snippet(content: str, query_tokens: set, max_len: int = 200) -> str:
        """Generates dynamic snippet highlighting query token occurrences."""
        if not content:
            return ""
        words = content.split()
        if len(content) <= max_len:
            return content

        # Find first matching word
        match_idx = 0
        for idx, word in enumerate(words):
            clean_word = re.sub(r"\W+", "", word.lower())
            if clean_word in query_tokens:
                match_idx = idx
                break

        start = max(0, match_idx - 10)
        end = min(len(words), start + 30)
        snippet = " ".join(words[start:end])
        if start > 0:
            snippet = "... " + snippet
        if end < len(words):
            snippet = snippet + " ..."
        return snippet
