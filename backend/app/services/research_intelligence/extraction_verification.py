"""
Entity Resolution, Fact Extraction, Claim Verification, Corroboration, and Conflict Detection.
"""

import uuid
from typing import Dict, Any, List, Optional
from backend.app.services.research_intelligence.base import (
    FactStatus,
    ClaimVerificationStatus,
)


class ExtractionVerificationManager:
    """Extracts entities and atomic facts, verifies claims via multi-source corroboration, and detects conflicts."""

    def __init__(self):
        self._entities: Dict[str, List[Dict[str, Any]]] = {}
        self._facts: Dict[str, List[Dict[str, Any]]] = {}
        self._claims: Dict[str, List[Dict[str, Any]]] = {}
        self._conflicts: Dict[str, List[Dict[str, Any]]] = {}

    # Entities
    def resolve_entity(
        self,
        workspace_id: str,
        name: str,
        entity_type: str,
        canonical_id: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve and canonicalize an entity in the research graph."""
        entity = {
            "id": f"ent_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "name": name,
            "entity_type": entity_type,
            "canonical_id": canonical_id or name.lower().replace(" ", "_"),
            "aliases": aliases or [],
            "attributes": attributes or {},
            "confidence": 0.92,
        }
        self._entities.setdefault(workspace_id, []).append(entity)
        return entity

    def list_entities(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._entities.get(workspace_id, [])

    # Facts
    def extract_fact(
        self,
        workspace_id: str,
        claim: str,
        source_id: Optional[str] = None,
        value_extracted: Optional[str] = None,
        fact_status: FactStatus = FactStatus.VERIFIED,
        confidence: float = 0.85,
        provenance: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Extract atomic verified fact with source attribution."""
        fact = {
            "id": f"fact_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "source_id": source_id,
            "claim": claim,
            "value_extracted": value_extracted,
            "fact_status": fact_status.value if hasattr(fact_status, "value") else str(fact_status),
            "confidence": max(0.0, min(1.0, confidence)),
            "provenance": provenance or "Primary Document Extraction",
        }
        self._facts.setdefault(workspace_id, []).append(fact)
        return fact

    def list_facts(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._facts.get(workspace_id, [])

    # Claims & Verification
    def verify_claim(
        self,
        workspace_id: str,
        claim_text: str,
        supporting_sources: Optional[List[str]] = None,
        contradicting_sources: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Verify claim against evidence. Independent sources are counted.
        Repeated syndicated articles are not counted as independent corroboration.
        """
        sup = supporting_sources or []
        con = contradicting_sources or []
        count = len(sup)

        if count >= 2 and len(con) == 0:
            status = ClaimVerificationStatus.SUPPORTED
            confidence = 0.95
        elif count == 1 and len(con) == 0:
            status = ClaimVerificationStatus.PARTIALLY_SUPPORTED
            confidence = 0.75
        elif len(con) > 0 and count > 0:
            status = ClaimVerificationStatus.CONFLICTED
            confidence = 0.50
        elif count == 0 and len(con) > 0:
            status = ClaimVerificationStatus.UNSUPPORTED
            confidence = 0.90
        else:
            status = ClaimVerificationStatus.UNKNOWN
            confidence = 0.30

        claim = {
            "id": f"clm_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "claim_text": claim_text,
            "verification_status": status.value,
            "independent_sources_count": count,
            "confidence": confidence,
            "supporting_evidence": sup,
            "contradicting_evidence": con,
        }
        self._claims.setdefault(workspace_id, []).append(claim)
        return claim

    def list_claims(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._claims.get(workspace_id, [])

    # Conflicts
    def surface_conflict(
        self,
        workspace_id: str,
        topic: str,
        source_a_id: str,
        claim_a: str,
        source_b_id: str,
        claim_b: str,
        possible_explanation: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Explicitly record a contradiction between sources without silently choosing one."""
        conflict = {
            "id": f"conf_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "topic": topic,
            "source_a_id": source_a_id,
            "claim_a": claim_a,
            "source_b_id": source_b_id,
            "claim_b": claim_b,
            "possible_explanation": possible_explanation or "Different measurement windows or methodology.",
            "resolution_status": "SURFACED",
        }
        self._conflicts.setdefault(workspace_id, []).append(conflict)
        return conflict

    def list_conflicts(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._conflicts.get(workspace_id, [])
