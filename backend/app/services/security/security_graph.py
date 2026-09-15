"""Multi-Hop Security Relationship Graph Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional

class SecurityGraphService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, entity_type: str, name: str, risk_score: float = 0.0) -> Dict[str, Any]:
        node = {"id": node_id, "entity_type": entity_type, "name": name, "risk_score": risk_score}
        self._nodes[node_id] = node
        return node

    def add_edge(self, source_id: str, target_id: str, relationship_type: str) -> Dict[str, Any]:
        edge = {"source": source_id, "target": target_id, "relationship": relationship_type}
        self._edges.append(edge)
        return edge

    def query_blast_radius(self, entity_id: str) -> Dict[str, Any]:
        connected = [e["target"] for e in self._edges if e["source"] == entity_id]
        return {
            "origin_entity": entity_id,
            "direct_dependencies_count": len(connected),
            "affected_entities": connected,
        }
