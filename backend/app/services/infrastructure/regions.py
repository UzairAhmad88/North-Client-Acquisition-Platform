"""Multi-Cloud Region & Workload Placement Service."""
from typing import Dict, Any, List, Optional

class RegionAvailabilityService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def list_regions(self, provider: str = "AWS", tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [
            {"id": "reg_us_east_1", "provider": provider, "region_name": "us-east-1", "display_name": "N. Virginia", "availability_zones_count": 6, "latency_score_ms": 14.2, "health_status": "HEALTHY"},
            {"id": "reg_us_west_2", "provider": provider, "region_name": "us-west-2", "display_name": "Oregon", "availability_zones_count": 4, "latency_score_ms": 22.8, "health_status": "HEALTHY"},
            {"id": "reg_eu_central_1", "provider": provider, "region_name": "eu-central-1", "display_name": "Frankfurt", "availability_zones_count": 3, "latency_score_ms": 78.4, "health_status": "HEALTHY"},
        ]
