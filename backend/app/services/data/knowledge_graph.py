"""Knowledge Graph & Semantic Reasoning service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class KnowledgeGraphService:
    """Manages enterprise knowledge graph nodes, edges, multi-hop traversals, and conflict detection."""

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._edges: List[Dict[str, Any]] = []
        self._conflicts: List[Dict[str, Any]] = []
        self._seed_default_graph()

    def _seed_default_graph(self):
        # Nodes: Customer, Company, Project, Requirement, Service, Dataset, Metric, Model
        nodes = [
            ("node_cust_1", "Customer", "Acme Corporation", {"industry": "SaaS", "mrr": 24000}),
            ("node_proj_1", "Project", "Enterprise Data Platform Implementation", {"budget": 180000}),
            ("node_req_1", "Requirement", "Column-Level Lineage & Governance", {"priority": "P0"}),
            ("node_srv_1", "Service", "Lineage Graph Microservice", {"runtime": "Python/FastAPI"}),
            ("node_dset_1", "Dataset", "lakehouse_gold_lineage_edges", {"storage": "s3"}),
            ("node_metric_1", "Metric", "Governance Audit Pass Rate", {"formula": "pass / total"}),
            ("node_model_1", "Model", "Data Drift Predictor", {"accuracy": 0.94}),
        ]
        for nid, lbl, name, props in nodes:
            self._nodes[nid] = {
                "id": nid,
                "tenant_id": "default_tenant",
                "label": lbl,
                "name": name,
                "properties": props,
                "confidence": 1.0,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

        # Edges
        edges = [
            ("node_cust_1", "node_proj_1", "OWNS", {"relationship": "sponsor"}),
            ("node_proj_1", "node_req_1", "CONTAINS", {"scope": "core"}),
            ("node_req_1", "node_srv_1", "IMPLEMENTED_BY", {"version": "v1.2"}),
            ("node_srv_1", "node_dset_1", "PRODUCES", {"rate": "continuous"}),
            ("node_dset_1", "node_metric_1", "FEEDS", {"metric_type": "operational"}),
            ("node_dset_1", "node_model_1", "TRAINS", {"dataset_split": "train_80"}),
        ]
        for src, tgt, rel, props in edges:
            self._edges.append({
                "id": f"kedge_{uuid.uuid4().hex[:8]}",
                "tenant_id": "default_tenant",
                "from_node_id": src,
                "to_node_id": tgt,
                "relationship_type": rel,
                "properties": props,
                "confidence": 1.0,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })

    def add_node(
        self,
        label: Any = None,
        name: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default_tenant",
        **kwargs
    ) -> Dict[str, Any]:
        if isinstance(label, dict):
            d = dict(label)
            lbl = d.get("label") or d.get("node_type", "Entity")
            nm = d.get("name", "Node")
            props = d.get("properties", {})
            tid = d.get("tenant_id", tenant_id)
        else:
            lbl = label or kwargs.get("node_type", "Entity")
            nm = name or kwargs.get("name", "Node")
            props = properties or kwargs.get("properties", {})
            tid = kwargs.get("tenant_id", tenant_id)

        nid = f"knode_{uuid.uuid4().hex[:10]}"
        record = {
            "id": nid,
            "tenant_id": tid,
            "label": lbl,
            "name": nm,
            "properties": props or {},
            "confidence": 1.0,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._nodes[nid] = record
        return record

    def add_edge(
        self, from_node_id: str, to_node_id: str, relationship_type: str, properties: Optional[Dict[str, Any]] = None, tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        eid = f"kedge_{uuid.uuid4().hex[:10]}"
        record = {
            "id": eid,
            "tenant_id": tenant_id,
            "from_node_id": from_node_id,
            "to_node_id": to_node_id,
            "relationship_type": relationship_type,
            "properties": properties or {},
            "confidence": 1.0,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._edges.append(record)
        return record

    def get_stats(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        return {
            "nodes_count": len([n for n in self._nodes.values() if n.get("tenant_id") == tenant_id]),
            "edges_count": len([e for e in self._edges if e.get("tenant_id") == tenant_id])
        }

    def query_subgraph(self, start_node_id: Optional[str] = None, max_depth: int = 2, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        return self.query_graph(start_node_id=start_node_id, depth=max_depth, tenant_id=tenant_id)

    def query_graph(
        self, start_node_id: Optional[str] = None, depth: int = 2, tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        nodes = [n for n in self._nodes.values() if n.get("tenant_id") == tenant_id]
        edges = [e for e in self._edges if e.get("tenant_id") == tenant_id]

        if start_node_id:
            # Multi-hop traversal
            visited_nodes = {start_node_id}
            traversed_edges = []
            current_level = {start_node_id}

            for _ in range(depth):
                next_level = set()
                for e in edges:
                    if e["from_node_id"] in current_level:
                        next_level.add(e["to_node_id"])
                        traversed_edges.append(e)
                    elif e["to_node_id"] in current_level:
                        next_level.add(e["from_node_id"])
                        traversed_edges.append(e)
                visited_nodes.update(next_level)
                current_level = next_level

            filtered_nodes = [n for n in nodes if n["id"] in visited_nodes]
            return {"nodes": filtered_nodes, "edges": traversed_edges, "node_count": len(filtered_nodes), "edge_count": len(traversed_edges)}

        return {"nodes": nodes, "edges": edges, "node_count": len(nodes), "edge_count": len(edges)}

    def detect_conflicts(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return self._conflicts
