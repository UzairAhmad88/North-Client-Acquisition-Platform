"""Compute Instances & Bare-Metal Fleet Service."""
from typing import Dict, Any, List, Optional

class ComputeManagementService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def get_compute_metrics(self, instance_id: str) -> Dict[str, Any]:
        return {"instance_id": instance_id, "cpu_utilization_pct": 38.4, "memory_utilization_pct": 52.1, "network_in_mbps": 84.5, "status": "HEALTHY"}
