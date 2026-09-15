"""Codebase Knowledge Graph & AST Search Service."""
from typing import Dict, Any, List, Optional

class CodeIntelligenceService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._graph: List[Dict[str, Any]] = []

    def add_relation(self, source: str, target: str, rel_type: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        edge = {"source": source, "target": target, "relation": rel_type, "tenant_id": tenant_id}
        self._graph.append(edge)
        return edge

    def query_relationships(self, entity_name: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        deps = [e["target"] for e in self._graph if e["source"] == entity_name and e["tenant_id"] == tenant_id]
        return {"entity": entity_name, "dependencies": deps, "total_dependencies": len(deps)}
