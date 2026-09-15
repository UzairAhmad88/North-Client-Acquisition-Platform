"""Core definitions, enums, and data models for Data Platform and Governance."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class DataAuthority(str, Enum):
    """Authority level of a data item or claim."""

    AUTHORITATIVE = "AUTHORITATIVE"
    VERIFIED = "VERIFIED"
    CONFIRMED = "CONFIRMED"
    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    INFERRED = "INFERRED"
    UNVERIFIED = "UNVERIFIED"
    UNKNOWN = "UNKNOWN"

    # Hierarchy Aliases
    RAW_DATA = "UNVERIFIED"
    NORMALIZED_DATA = "DERIVED"
    VERIFIED_DATA = "VERIFIED"
    HUMAN_CONFIRMATION = "CONFIRMED"
    CONTRACTUAL_COMMITMENT = "AUTHORITATIVE"
    AI_INFERENCE = "INFERRED"
    SYSTEM_INTEGRATION = "OBSERVED"


class ProvenanceType(str, Enum):
    """Origin classification for data facts and records."""

    OBSERVED = "OBSERVED"
    USER_PROVIDED = "USER_PROVIDED"
    CLIENT_PROVIDED = "CLIENT_PROVIDED"
    SYSTEM_GENERATED = "SYSTEM_GENERATED"
    AI_INFERRED = "AI_INFERRED"
    HUMAN_CONFIRMED = "HUMAN_CONFIRMED"
    IMPORTED = "IMPORTED"
    DERIVED = "DERIVED"
    CALCULATED = "CALCULATED"
    EXTERNAL_API = "EXTERNAL_API"


class DataClassification(str, Enum):
    """Security classification controlling data access and retention."""

    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    CLIENT_CONFIDENTIAL = "CLIENT_CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    SECURITY_SENSITIVE = "SECURITY_SENSITIVE"
    SECRET = "SECRET"


class KnowledgeLifecycle(str, Enum):
    """Lifecycle status of organizational knowledge items."""

    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"

    # Hierarchy Aliases
    INGESTED = "DRAFT"
    INDEXED = "REVIEW"
    VERIFIED = "CONFIRMED"
    CANONICAL = "ACTIVE"
    DEPRECATED = "SUPERSEDED"


class LineageRelationship(str, Enum):
    """Semantic relationship connecting source and target nodes in the lineage graph."""

    SOURCE_OF = "SOURCE_OF"
    DERIVED_FROM = "DERIVED_FROM"
    TRANSFORMED_FROM = "TRANSFORMED_FROM"
    GENERATED_FROM = "GENERATED_FROM"
    CONFIRMED_BY = "CONFIRMED_BY"
    SUPERSEDES = "SUPERSEDES"
    DEPENDS_ON = "DEPENDS_ON"
    IMPLEMENTED_BY = "IMPLEMENTED_BY"
    TESTED_BY = "TESTED_BY"
    DELIVERED_AS = "DELIVERED_AS"
    RESOLVED_BY = "RESOLVED_BY"
    COMPOSED_OF = "DERIVED_FROM"


@dataclass
class ProvenanceMetadata:
    """Standardized provenance envelope attached to facts and records."""

    source_type: ProvenanceType = ProvenanceType.SYSTEM_GENERATED
    source_reference: Optional[str] = None
    authority: DataAuthority = DataAuthority.DERIVED
    confidence: float = 1.0
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    actor_id: Optional[str] = None
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
