"""
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform Package.
Phase 48.
"""

from backend.app.knowledge.base import (
    ConflictRecord,
    ConflictStatus,
    ContextBundle,
    DecisionRecord,
    FactItem,
    FreshnessStatus,
    GraphRelationshipType,
    KnowledgeAuthority,
    KnowledgeChunk,
    KnowledgeDomain,
    KnowledgeEntity,
    KnowledgeItem,
    KnowledgeLifecycle,
    KnowledgeProvenance,
    KnowledgeRelationship,
    KnowledgeType,
    LessonItem,
    SearchResultItem,
    SearchStrategy,
)
from backend.app.knowledge.service import KnowledgePlatformService

__all__ = [
    "ConflictRecord",
    "ConflictStatus",
    "ContextBundle",
    "DecisionRecord",
    "FactItem",
    "FreshnessStatus",
    "GraphRelationshipType",
    "KnowledgeAuthority",
    "KnowledgeChunk",
    "KnowledgeDomain",
    "KnowledgeEntity",
    "KnowledgeItem",
    "KnowledgeLifecycle",
    "KnowledgePlatformService",
    "KnowledgeProvenance",
    "KnowledgeRelationship",
    "KnowledgeType",
    "LessonItem",
    "SearchResultItem",
    "SearchStrategy",
]
