"""AI Memory System (Working, Episodic, Semantic, Organizational) for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class MemoryService:
    """Manages governed AI memory, provenance validation, classification, and conflict surfacing."""

    def __init__(self):
        self._memories: Dict[str, Dict[str, Any]] = {}
        self._seed_default_memory()

    def _seed_default_memory(self):
        self.store_memory(
            content="Acme Corporation requested custom column-level lineage reporting for compliance audit.",
            memory_type="EPISODIC",
            source="client-collaboration-agent",
            entity_ref="ent_cust_01",
            confidence=0.98,
            classification="OBSERVED",
        )
        self.store_memory(
            content="Enterprise Data Platform SLA requires 99.5% freshness availability on customer 360 data products.",
            memory_type="ORGANIZATIONAL",
            source="sla-policy-engine",
            entity_ref="prod_customer_360",
            confidence=1.0,
            classification="OBSERVED",
        )

    def store_memory(
        self,
        content: str,
        memory_type: str = "SEMANTIC",  # WORKING, EPISODIC, SEMANTIC, PROCEDURAL, ORGANIZATIONAL
        source: str = "autonomous-agent",
        entity_ref: Optional[str] = None,
        confidence: float = 0.9,
        classification: str = "OBSERVED",  # OBSERVED, DERIVED, INFERRED, HYPOTHESIS, USER_PROVIDED
        permissions: Optional[List[str]] = None,
        sensitivity: str = "INTERNAL",
        tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        mem_id = f"mem_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        record = {
            "id": mem_id,
            "tenant_id": tenant_id,
            "content": content,
            "memory_type": memory_type,
            "source": source,
            "entity_ref": entity_ref,
            "confidence": confidence,
            "classification": classification,
            "permissions": permissions or ["*"],
            "sensitivity": sensitivity,
            "version": "v1.0.0",
            "created_at": now.isoformat(),
        }
        self._memories[mem_id] = record
        return record

    def list_memories(
        self, memory_type: Optional[str] = None, entity_ref: Optional[str] = None, tenant_id: str = "default_tenant"
    ) -> List[Dict[str, Any]]:
        mems = [m for m in self._memories.values() if m.get("tenant_id") == tenant_id]
        if memory_type:
            mems = [m for m in mems if m.get("memory_type") == memory_type.upper()]
        if entity_ref:
            mems = [m for m in mems if m.get("entity_ref") == entity_ref]
        return mems

    def invalidate_memory(self, memory_id: str, tenant_id: str = "default_tenant") -> bool:
        if memory_id in self._memories and self._memories[memory_id].get("tenant_id") == tenant_id:
            del self._memories[memory_id]
            return True
        return False
