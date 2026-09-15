"""Master Data Management (MDM) service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class MasterDataService:
    """Manages canonical golden record master entities (Customer, Company, Employee, Product)."""

    def __init__(self):
        self._entities: Dict[str, Dict[str, Any]] = {}
        self._aliases: Dict[str, List[str]] = {}
        self._seed_default_master_data()

    def _seed_default_master_data(self):
        seeds = [
            ("ent_cust_01", "CUSTOMER", "Acme Corporation", {"industry": "SaaS", "tier": "Enterprise", "ltv": 350000.0}, ["Acme Corp", "Acme Inc", "Acme"]),
            ("ent_cust_02", "CUSTOMER", "Omni Health Systems", {"industry": "Healthcare", "tier": "Strategic", "ltv": 820000.0}, ["OmniHealth", "Omni Systems"]),
            ("ent_prod_01", "PRODUCT", "Uzaii Autonomous Platform", {"category": "Enterprise AI OS", "version": "2.0"}, ["Uzaii Core", "Uzaii Platform"]),
        ]
        for eid, e_type, name, attrs, aliases in seeds:
            self._entities[eid] = {
                "id": eid,
                "tenant_id": "default_tenant",
                "entity_type": e_type,
                "canonical_name": name,
                "attributes": attrs,
                "confidence": 1.0,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            self._aliases[eid] = aliases

    def create_entity(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        return self.create_master_entity(data, tenant_id=tenant_id)

    def create_master_entity(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        eid = data.get("id") or f"ent_{uuid.uuid4().hex[:12]}"
        record = {
            "id": eid,
            "tenant_id": tenant_id,
            "entity_type": data.get("entity_type", "CUSTOMER"),
            "canonical_name": data.get("canonical_name", "Unnamed Master Entity"),
            "attributes": data.get("attributes", {}),
            "confidence": data.get("confidence", 1.0),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._entities[eid] = record
        self._aliases[eid] = data.get("aliases", [])
        return record

    def get_master_entity(self, entity_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        ent = self._entities.get(entity_id)
        if ent and ent.get("tenant_id") == tenant_id:
            res = dict(ent)
            res["aliases"] = self._aliases.get(entity_id, [])
            return res
        return None

    def list_master_entities(self, entity_type: Optional[str] = None, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        results = []
        for eid, ent in self._entities.items():
            if ent.get("tenant_id") == tenant_id:
                if not entity_type or ent.get("entity_type") == entity_type.upper():
                    item = dict(ent)
                    item["aliases"] = self._aliases.get(eid, [])
                    results.append(item)
        return results
