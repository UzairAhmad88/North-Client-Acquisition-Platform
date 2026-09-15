"""Entity Resolution & Deduplication service for Phase 65."""

import difflib
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone
from backend.app.services.data.master_data import MasterDataService


class EntityResolutionService:
    """Fuzzy matching, entity deduplication, confidence estimation, and merge histories."""

    def __init__(self, master_data_service: Optional[MasterDataService] = None):
        self.mdm = master_data_service or MasterDataService()
        self._matches: List[Dict[str, Any]] = []
        self._merge_history: List[Dict[str, Any]] = []

    def resolve_entity(self, name: str, entity_type: str = "CUSTOMER", tenant_id: str = "default_tenant") -> Dict[str, Any]:
        res = self.resolve_candidate(candidate_name=name, entity_type=entity_type, tenant_id=tenant_id)
        res["matched"] = res.get("is_match", res.get("matched_entity_id") is not None)
        return res

    def resolve_candidate(
        self, candidate_name: str, entity_type: str = "CUSTOMER", threshold: float = 0.75, tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        entities = self.mdm.list_master_entities(entity_type, tenant_id)
        best_match = None
        highest_score = 0.0

        for ent in entities:
            # Check canonical name
            score = difflib.SequenceMatcher(None, candidate_name.lower(), ent["canonical_name"].lower()).ratio()
            if score > highest_score:
                highest_score = score
                best_match = ent
            
            # Check aliases
            for alias in ent.get("aliases", []):
                alias_score = difflib.SequenceMatcher(None, candidate_name.lower(), alias.lower()).ratio()
                if alias_score > highest_score:
                    highest_score = alias_score
                    best_match = ent

        is_match = highest_score >= threshold
        match_id = f"match_{uuid.uuid4().hex[:8]}"
        res = {
            "match_id": match_id,
            "candidate_name": candidate_name,
            "matched_entity_id": best_match["id"] if best_match and is_match else None,
            "matched_canonical_name": best_match["canonical_name"] if best_match and is_match else None,
            "confidence_score": round(highest_score, 3),
            "confidence": round(highest_score, 3),
            "matched": is_match,
            "status": "RESOLVED" if is_match else "UNCERTAIN_NEEDS_REVIEW",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._matches.append(res)
        return res

    def merge_entities(
        self, surviving_id: str, merged_id: str, merged_by: str = "data-steward", tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        surviving = self.mdm.get_master_entity(surviving_id, tenant_id)
        merged = self.mdm.get_master_entity(merged_id, tenant_id)
        
        if surviving and merged:
            aliases = surviving.get("aliases", [])
            aliases.append(merged.get("canonical_name"))
            aliases.extend(merged.get("aliases", []))
            self.mdm._aliases[surviving_id] = list(set(aliases))

        merge_record = {
            "surviving_entity_id": surviving_id,
            "merged_entity_id": merged_id,
            "merged_by": merged_by,
            "merged_at": datetime.now(timezone.utc).isoformat(),
            "status": "COMPLETED",
        }
        self._merge_history.append(merge_record)
        return merge_record

    def list_merges(self) -> List[Dict[str, Any]]:
        return self._merge_history
