"""Data Lineage Graph Engine & Transformation Traceability."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Union
import uuid

from app.data.base import LineageRelationship


@dataclass
class LineageNode:
    """Represents a data entity in the lineage graph."""

    entity_type: str
    entity_id: str
    tenant_id: str
    name: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class LineageEdge:
    """Directed connection from source entity to target entity."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default_tenant"
    source_type: str = ""
    source_id: str = ""
    target_type: str = ""
    target_id: str = ""
    relationship: LineageRelationship = LineageRelationship.DERIVED_FROM
    transformation: Optional[str] = None
    actor_id: Optional[str] = None
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class LineageGraphEngine:
    """Traverses and queries upstream sources and downstream derivations in memory or from database."""

    @staticmethod
    def _normalize_edge(e: Any) -> Dict[str, Any]:
        if isinstance(e, LineageEdge):
            return {
                "id": e.id,
                "source_type": e.source_type,
                "source_id": e.source_id,
                "target_type": e.target_type,
                "target_id": e.target_id,
                "relationship": e.relationship.value if hasattr(e.relationship, "value") else str(e.relationship),
                "transformation_name": e.transformation,
            }
        return e

    @staticmethod
    def trace_upstream(
        arg1: Any,
        arg2: Any = None,
        arg3: Any = None,
        max_depth: int = 10,
    ) -> List[Dict[str, Any]]:
        """Trace upstream origins. Supports:
        - trace_upstream(edges, target_id)
        - trace_upstream(target_type, target_id, edges)
        """
        if isinstance(arg1, list):
            raw_edges = arg1
            target_id = arg2
            target_type = None
        else:
            target_type = arg1
            target_id = arg2
            raw_edges = arg3 or []

        edges = [LineageGraphEngine._normalize_edge(e) for e in raw_edges]
        visited_ids: Set[str] = set()
        upstream_nodes: List[Dict[str, Any]] = []

        def _traverse(current_id: str, depth: int):
            if depth > max_depth or current_id in visited_ids:
                return
            visited_ids.add(current_id)

            incoming = [e for e in edges if e.get("target_id") == current_id]
            for edge in incoming:
                src_id = edge.get("source_id")
                if src_id:
                    upstream_nodes.append({
                        "id": src_id,
                        "type": edge.get("source_type", "UNKNOWN"),
                        "relationship": edge.get("relationship", "DERIVED_FROM"),
                        "transformation": edge.get("transformation_name") or edge.get("transformation"),
                        "confidence_score": edge.get("confidence_score", 1.0),
                    })
                    _traverse(src_id, depth + 1)

        _traverse(target_id, 0)
        return upstream_nodes

    @staticmethod
    def trace_downstream(
        arg1: Any,
        arg2: Any = None,
        arg3: Any = None,
        max_depth: int = 10,
    ) -> List[Dict[str, Any]]:
        """Trace downstream dependents. Supports:
        - trace_downstream(edges, source_id)
        - trace_downstream(source_type, source_id, edges)
        """
        if isinstance(arg1, list):
            raw_edges = arg1
            source_id = arg2
            source_type = None
        else:
            source_type = arg1
            source_id = arg2
            raw_edges = arg3 or []

        edges = [LineageGraphEngine._normalize_edge(e) for e in raw_edges]
        visited_ids: Set[str] = set()
        downstream_nodes: List[Dict[str, Any]] = []

        def _traverse(current_id: str, depth: int):
            if depth > max_depth or current_id in visited_ids:
                return
            visited_ids.add(current_id)

            outgoing = [e for e in edges if e.get("source_id") == current_id]
            for edge in outgoing:
                tgt_id = edge.get("target_id")
                if tgt_id:
                    downstream_nodes.append({
                        "id": tgt_id,
                        "type": edge.get("target_type", "UNKNOWN"),
                        "relationship": edge.get("relationship", "DERIVED_FROM"),
                        "transformation": edge.get("transformation_name") or edge.get("transformation"),
                        "confidence_score": edge.get("confidence_score", 1.0),
                    })
                    _traverse(tgt_id, depth + 1)

        _traverse(source_id, 0)
        return downstream_nodes
