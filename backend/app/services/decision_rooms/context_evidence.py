"""
Context and Evidence Board management with Fact / Inference classification.
"""

import uuid
from typing import Dict, Any, List, Optional
from backend.app.services.decision_rooms.base import (
    EvidenceType,
    StatementCategory,
    EvidenceItem,
)


class ContextEvidenceManager:
    """Manages Decision Context and Evidence items with strict fact/inference categorization."""

    def __init__(self):
        self._contexts: Dict[str, Dict[str, Any]] = {}
        self._evidence: Dict[str, List[Dict[str, Any]]] = {}

    def set_context(
        self,
        room_id: str,
        background: str,
        current_state: Optional[str] = None,
        constraints: Optional[List[str]] = None,
        entities_involved: Optional[List[str]] = None,
        policies_applicable: Optional[List[str]] = None,
        memory_references: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Set the background context for a decision room."""
        ctx_id = f"ctx_{uuid.uuid4().hex[:12]}"
        context = {
            "id": ctx_id,
            "room_id": room_id,
            "background": background,
            "current_state": current_state,
            "constraints": constraints or [],
            "entities_involved": entities_involved or [],
            "policies_applicable": policies_applicable or [],
            "memory_references": memory_references or [],
        }
        self._contexts[room_id] = context
        return context

    def get_context(self, room_id: str) -> Optional[Dict[str, Any]]:
        return self._contexts.get(room_id)

    def add_evidence(
        self,
        room_id: str,
        evidence_type: EvidenceType,
        source: str,
        claim: str,
        statement_category: StatementCategory = StatementCategory.FACT,
        provenance: Optional[str] = None,
        authority: str = "OFFICIAL",
        confidence: float = 1.0,
        freshness: str = "CURRENT",
        meta_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Add an evidence item with explicit provenance and statement category."""
        ev_id = f"ev_{uuid.uuid4().hex[:12]}"
        item = {
            "id": ev_id,
            "room_id": room_id,
            "evidence_type": evidence_type.value if hasattr(evidence_type, "value") else str(evidence_type),
            "source": source,
            "claim": claim,
            "provenance": provenance or source,
            "authority": authority,
            "statement_category": statement_category.value if hasattr(statement_category, "value") else str(statement_category),
            "confidence": max(0.0, min(1.0, confidence)),
            "freshness": freshness,
            "meta_info": meta_info or {},
        }
        self._evidence.setdefault(room_id, []).append(item)
        return item

    def list_evidence(
        self,
        room_id: str,
        statement_category: Optional[str] = None,
        evidence_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        items = self._evidence.get(room_id, [])
        if statement_category:
            items = [i for i in items if i["statement_category"] == statement_category]
        if evidence_type:
            items = [i for i in items if i["evidence_type"] == evidence_type]
        return items

    def classify_statement(self, statement: str, source_type: str) -> StatementCategory:
        """Categorize AI / human statements based on linguistic & source markers."""
        lower = statement.lower()
        if any(marker in lower for marker in ["recommend", "should", "suggest", "propose"]):
            return StatementCategory.RECOMMENDATION
        if any(marker in lower for marker in ["hypothesize", "if we assume", "could be", "might"]):
            return StatementCategory.HYPOTHESIS
        if any(marker in lower for marker in ["indicates", "suggests that", "likely", "inferred", "probably"]):
            return StatementCategory.INFERENCE
        if any(marker in lower for marker in ["unknown", "unclear", "unverified", "insufficient data"]):
            return StatementCategory.UNKNOWN
        if any(marker in lower for marker in ["contradicts", "conflict", "disputes"]):
            return StatementCategory.CONFLICTED
        if source_type in ["DATABASE", "AUDIT", "METRIC", "POLICY", "OFFICIAL"]:
            return StatementCategory.FACT
        return StatementCategory.INFERENCE
