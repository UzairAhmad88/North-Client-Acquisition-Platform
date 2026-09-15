"""Resource Relationship Graph & Blast-Radius Traversal Service."""
from typing import Dict, Any, List, Optional

class ResourceRelationshipGraphService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._edges: List[Dict[str, Any]] = []

    def link_resources(self, source_id: str, target_id: str, relation: str = "DEPENDS_ON", tenant_id: str = "default_tenant") -> Dict[str, Any]:
        edge = {"source_id": source_id, "target_id": target_id, "relation": relation, "tenant_id": tenant_id}
        self._edges.append(edge)
        return edge

    def query_impact(self, resource_id: str) -> Dict[str, Any]:
        downstream = [e["target_id"] for e in self._edges if e["source_id"] == resource_id]
        return {"resource_id": resource_id, "blast_radius_count": len(downstream), "affected_downstream": downstream, "risk_level": "MEDIUM" if downstream else "LOW"}
