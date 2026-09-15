"""
Conflict Detector and Resolution Engine for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.

Enforces Rule 9 & 12: Knowledge conflicts must not be silently resolved.
Mutually contradictory claims or facts are registered as OPEN conflicts.
Never uses semantic similarity alone to resolve factual conflicts.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
import uuid

try:
    from backend.app.knowledge.base import (
        ConflictRecord,
        ConflictStatus,
        FactItem,
        KnowledgeAuthority,
        KnowledgeItem,
        KnowledgeLifecycle,
    )
except ImportError:
    from app.knowledge.base import (
        ConflictRecord,
        ConflictStatus,
        FactItem,
        KnowledgeAuthority,
        KnowledgeItem,
        KnowledgeLifecycle,
    )


class ConflictDetector:
    """
    Detects contradictions and conflicting claims across knowledge items and facts.
    """

    def __init__(self):
        self._conflicts: Dict[str, ConflictRecord] = {}

    def scan_fact_conflicts(self, facts: List[FactItem]) -> List[ConflictRecord]:
        """
        Scans a collection of facts for direct predicate contradictions:
        e.g., same subject and predicate but different target values.
        """
        detected: List[ConflictRecord] = []
        fact_map: Dict[Tuple[str, str, str], List[FactItem]] = {}

        for f in facts:
            key = (f.tenant_id, f.subject.strip().lower(), f.predicate.strip().lower())
            fact_map.setdefault(key, []).append(f)

        for (tenant_id, subject, predicate), group in fact_map.items():
            if len(group) > 1:
                # Check for disparate target values
                values = {item.target_value.strip().lower(): item for item in group}
                if len(values) > 1:
                    items_list = list(group)
                    for i in range(len(items_list)):
                        for j in range(i + 1, len(items_list)):
                            item_a = items_list[i]
                            item_b = items_list[j]
                            if item_a.target_value.strip().lower() != item_b.target_value.strip().lower():
                                c_code = f"CONF-{uuid.uuid4().hex[:8].upper()}"
                                desc = (
                                    f"Contradiction on subject '{item_a.subject}' for predicate '{item_a.predicate}': "
                                    f"Value A ('{item_a.target_value}') vs Value B ('{item_b.target_value}')"
                                )
                                record = ConflictRecord(
                                    conflict_code=c_code,
                                    tenant_id=tenant_id,
                                    source_a_code=item_a.fact_code,
                                    source_b_code=item_b.fact_code,
                                    description=desc,
                                    status=ConflictStatus.OPEN,
                                    detected_at=datetime.now(timezone.utc),
                                )
                                self._conflicts[c_code] = record
                                detected.append(record)
        return detected

    def detect_item_contradiction(
        self,
        item_a: KnowledgeItem,
        item_b: KnowledgeItem,
        contradiction_reason: str,
    ) -> ConflictRecord:
        """
        Explicitly flags a contradiction between two knowledge items.
        Marks both items or creates a conflict record without silently overwriting.
        """
        c_code = f"CONF-{uuid.uuid4().hex[:8].upper()}"
        desc = (
            f"Knowledge contradiction between [{item_a.knowledge_code}] '{item_a.title}' "
            f"and [{item_b.knowledge_code}] '{item_b.title}': {contradiction_reason}"
        )
        record = ConflictRecord(
            conflict_code=c_code,
            tenant_id=item_a.tenant_id,
            source_a_code=item_a.knowledge_code,
            source_b_code=item_b.knowledge_code,
            description=desc,
            status=ConflictStatus.OPEN,
            detected_at=datetime.now(timezone.utc),
        )
        self._conflicts[c_code] = record
        return record

    def evaluate_authority_resolution_recommendation(
        self,
        item_a: KnowledgeItem,
        item_b: KnowledgeItem,
    ) -> Dict[str, Any]:
        """
        Proposes a resolution recommendation based on the Phase 36 authority hierarchy:
        AUTHORITATIVE > VERIFIED > CONFIRMED > OBSERVED > DERIVED > INFERRED > UNVERIFIED
        
        Crucial Rule: This generates a recommendation for human review.
        It NEVER silently overwrites or auto-merges without human approval!
        """
        authority_rank = {
            KnowledgeAuthority.AUTHORITATIVE: 70,
            KnowledgeAuthority.VERIFIED: 60,
            KnowledgeAuthority.CONFIRMED: 50,
            KnowledgeAuthority.OBSERVED: 40,
            KnowledgeAuthority.DERIVED: 30,
            KnowledgeAuthority.INFERRED: 20,
            KnowledgeAuthority.UNVERIFIED: 10,
            KnowledgeAuthority.UNKNOWN: 0,
        }

        rank_a = authority_rank.get(item_a.authority, 0)
        rank_b = authority_rank.get(item_b.authority, 0)

        if rank_a > rank_b:
            rec = f"Prefer item {item_a.knowledge_code} due to higher authority ({item_a.authority.value} vs {item_b.authority.value}). Requires human verification."
            favored = item_a.knowledge_code
        elif rank_b > rank_a:
            rec = f"Prefer item {item_b.knowledge_code} due to higher authority ({item_b.authority.value} vs {item_a.authority.value}). Requires human verification."
            favored = item_b.knowledge_code
        else:
            # Same authority, check freshness
            time_a = item_a.updated_at or item_a.created_at
            time_b = item_b.updated_at or item_b.created_at
            if time_a > time_b:
                rec = f"Equal authority ({item_a.authority.value}). Item {item_a.knowledge_code} is fresher. Requires human sign-off."
                favored = item_a.knowledge_code
            else:
                rec = f"Equal authority ({item_b.authority.value}). Item {item_b.knowledge_code} is fresher. Requires human sign-off."
                favored = item_b.knowledge_code

        return {
            "item_a_code": item_a.knowledge_code,
            "item_b_code": item_b.knowledge_code,
            "favored_item": favored,
            "recommendation": rec,
            "auto_resolve_permitted": False,  # Non-negotiable: Human confirmation required!
        }

    def resolve_conflict(
        self,
        conflict_code: str,
        resolved_by: str,
        resolution_notes: str,
    ) -> Optional[ConflictRecord]:
        """
        Manually resolves a conflict with human provenance and audit notes.
        """
        conflict = self._conflicts.get(conflict_code)
        if not conflict:
            return None

        conflict.status = ConflictStatus.RESOLVED
        conflict.resolved_by = resolved_by
        conflict.resolved_at = datetime.now(timezone.utc)
        conflict.resolution_notes = resolution_notes
        return conflict

    def list_open_conflicts(self, tenant_id: Optional[str] = None) -> List[ConflictRecord]:
        results = [
            c for c in self._conflicts.values()
            if c.status == ConflictStatus.OPEN
        ]
        if tenant_id:
            results = [c for c in results if c.tenant_id == tenant_id]
        return results
