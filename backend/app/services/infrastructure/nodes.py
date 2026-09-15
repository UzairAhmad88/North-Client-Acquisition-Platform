"""Kubernetes Node Management & Capacity Service."""
from typing import Dict, Any, List, Optional

class NodeManagementService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def list_nodes(self, cluster_id: str) -> List[Dict[str, Any]]:
        return [
            {"id": "node_01", "cluster_id": cluster_id, "node_name": "ip-10-0-12-42.ec2.internal", "instance_type": "m6i.4xlarge", "ready": True, "cpu_allocatable_cores": 16.0, "memory_allocatable_gb": 64.0, "pods_running": 42},
            {"id": "node_02", "cluster_id": cluster_id, "node_name": "ip-10-0-12-89.ec2.internal", "instance_type": "m6i.4xlarge", "ready": True, "cpu_allocatable_cores": 16.0, "memory_allocatable_gb": 64.0, "pods_running": 38},
        ]
