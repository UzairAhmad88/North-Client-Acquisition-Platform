"""
Knowledge Graph & Relationship Traversal Engine (Section 23 & 24).
Maintains multi-hop organizational entity relationships and dependency path traversal.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Set

try:
    from backend.app.knowledge.base import (
        GraphRelationshipType,
        KnowledgeEntity,
        KnowledgeRelationship,
    )
except ImportError:
    from app.knowledge.base import (
        GraphRelationshipType,
        KnowledgeEntity,
        KnowledgeRelationship,
    )


class KnowledgeGraphEngine:
    """Graph engine modeling inter-entity relationships across the entire enterprise."""

    def __init__(self):
        self._entities: Dict[str, KnowledgeEntity] = {}
        self._adjacency: Dict[str, List[KnowledgeRelationship]] = {}  # source_code -> list of outgoing edges
        self._reverse_adjacency: Dict[str, List[KnowledgeRelationship]] = {}  # target_code -> list of incoming edges
        self._seed_default_graph()

    def _seed_default_graph(self) -> None:
        """Seeds canonical cross-system relationships representing platform architecture."""
        # Entities
        self.add_entity(KnowledgeEntity(entity_code="ENT-CLI-ACME", entity_type="CLIENT", name="Acme Logistics Corp", domain="CLIENT"))
        self.add_entity(KnowledgeEntity(entity_code="ENT-PRJ-PORTAL", entity_type="PROJECT", name="Carrier Dispatch Portal", domain="PROJECT"))
        self.add_entity(KnowledgeEntity(entity_code="ENT-REQ-MFA", entity_type="REQUIREMENT", name="Privileged Dispatcher MFA", domain="REQUIREMENTS"))
        self.add_entity(KnowledgeEntity(entity_code="ENT-DEC-POSTGRES", entity_type="DECISION", name="PostgreSQL Schema per Tenant", domain="DECISIONS"))
        self.add_entity(KnowledgeEntity(entity_code="ENT-CTL-MFA", entity_type="CONTROL", name="CTL_SEC_MFA", domain="SECURITY"))
        self.add_entity(KnowledgeEntity(entity_code="ENT-EVD-AUTH", entity_type="EVIDENCE", name="EVD-AUTH-DAILY-001", domain="GOVERNANCE"))

        # Edges
        self.add_relationship(KnowledgeRelationship(
            source_entity_code="ENT-CLI-ACME",
            target_entity_code="ENT-PRJ-PORTAL",
            relationship_type=GraphRelationshipType.OWNED_BY,
        ))
        self.add_relationship(KnowledgeRelationship(
            source_entity_code="ENT-PRJ-PORTAL",
            target_entity_code="ENT-REQ-MFA",
            relationship_type=GraphRelationshipType.REQUIRES,
        ))
        self.add_relationship(KnowledgeRelationship(
            source_entity_code="ENT-REQ-MFA",
            target_entity_code="ENT-DEC-POSTGRES",
            relationship_type=GraphRelationshipType.DEPENDS_ON,
        ))
        self.add_relationship(KnowledgeRelationship(
            source_entity_code="ENT-REQ-MFA",
            target_entity_code="ENT-CTL-MFA",
            relationship_type=GraphRelationshipType.IMPLEMENTS,
        ))
        self.add_relationship(KnowledgeRelationship(
            source_entity_code="ENT-CTL-MFA",
            target_entity_code="ENT-EVD-AUTH",
            relationship_type=GraphRelationshipType.SUPPORTED_BY,
        ))

    def add_entity(self, entity: KnowledgeEntity) -> None:
        self._entities[entity.entity_code] = entity
        if entity.entity_code not in self._adjacency:
            self._adjacency[entity.entity_code] = []
        if entity.entity_code not in self._reverse_adjacency:
            self._reverse_adjacency[entity.entity_code] = []

    def get_entity(self, entity_code: str) -> Optional[KnowledgeEntity]:
        return self._entities.get(entity_code)

    def list_entities(self, entity_type: Optional[str] = None) -> List[KnowledgeEntity]:
        entities = list(self._entities.values())
        if entity_type:
            entities = [e for e in entities if e.entity_type == entity_type]
        return entities

    def add_relationship(self, rel: KnowledgeRelationship) -> None:
        # Ensure endpoints exist
        if rel.source_entity_code not in self._adjacency:
            self._adjacency[rel.source_entity_code] = []
        if rel.target_entity_code not in self._reverse_adjacency:
            self._reverse_adjacency[rel.target_entity_code] = []

        self._adjacency[rel.source_entity_code].append(rel)
        self._reverse_adjacency[rel.target_entity_code].append(rel)

    def get_neighbors(
        self,
        entity_code: str,
        direction: str = "OUTGOING",  # OUTGOING, INCOMING, BOTH
    ) -> List[KnowledgeRelationship]:
        """Returns direct graph relationships for an entity node."""
        if direction == "OUTGOING":
            return self._adjacency.get(entity_code, [])
        elif direction == "INCOMING":
            return self._reverse_adjacency.get(entity_code, [])
        else:
            return self._adjacency.get(entity_code, []) + self._reverse_adjacency.get(entity_code, [])

    def find_path(
        self,
        start_code: Optional[str] = None,
        end_code: Optional[str] = None,
        max_depth: int = 5,
        source_code: Optional[str] = None,
        target_code: Optional[str] = None,
        max_hops: Optional[int] = None,
    ) -> Optional[List[str]]:
        """Finds shortest entity relationship path between two knowledge nodes via BFS."""
        start = start_code or source_code
        end = end_code or target_code
        depth = max_hops if max_hops is not None else max_depth

        if not start or not end or start not in self._entities or end not in self._entities:
            return None
        if start == end:
            return [start]

        queue: deque = deque([(start, [start])])
        visited: Set[str] = {start}

        while queue:
            current, path = queue.popleft()
            if len(path) > depth:
                continue

            for edge in self._adjacency.get(current, []):
                neighbor = edge.target_entity_code
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def get_subgraph(self, root_code: str, depth: int = 2) -> Dict[str, Any]:
        """Extracts an entity subgraph for visual rendering in KnowledgeGraph UI."""
        nodes: Dict[str, KnowledgeEntity] = {}
        edges: List[KnowledgeRelationship] = []
        visited: Set[str] = set()

        queue = deque([(root_code, 0)])
        visited.add(root_code)

        while queue:
            curr, curr_depth = queue.popleft()
            ent = self._entities.get(curr)
            if ent:
                nodes[curr] = ent

            if curr_depth >= depth:
                continue

            for edge in self._adjacency.get(curr, []):
                edges.append(edge)
                target = edge.target_entity_code
                if target not in visited:
                    visited.add(target)
                    queue.append((target, curr_depth + 1))

        return {
            "root_code": root_code,
            "nodes": list(nodes.values()),
            "edges": edges,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
        }

    def get_graph_visualization_data(
        self,
        root_code: Optional[str] = None,
        max_hops: int = 2,
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        if root_code:
            sub = self.get_subgraph(root_code, depth=max_hops)
            return {
                "nodes": [{"id": n.entity_code, "name": n.name, "type": n.entity_type, "domain": n.domain} for n in sub["nodes"]],
                "edges": [{"source": e.source_entity_code, "target": e.target_entity_code, "type": e.relationship_type.value if hasattr(e.relationship_type, "value") else str(e.relationship_type), "confidence": e.confidence} for e in sub["edges"]],
            }

        all_nodes = [
            {"id": e.entity_code, "name": e.name, "type": e.entity_type, "domain": e.domain}
            for e in self._entities.values()
            if e.tenant_id == tenant_id
        ]
        all_edges = []
        for edge_list in self._adjacency.values():
            for e in edge_list:
                if e.tenant_id == tenant_id:
                    all_edges.append({
                        "source": e.source_entity_code,
                        "target": e.target_entity_code,
                        "type": e.relationship_type.value if hasattr(e.relationship_type, "value") else str(e.relationship_type),
                        "confidence": e.confidence,
                    })
        return {
            "nodes": all_nodes,
            "edges": all_edges,
        }
