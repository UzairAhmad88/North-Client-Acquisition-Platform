"""Maintenance Windows & Scheduled Tasks Service."""
from typing import Dict, Any, List, Optional

class MaintenanceWindowService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def get_active_windows(self) -> List[Dict[str, Any]]:
        return [{"id": "mw_01", "name": "EKS Worker Node Rolling Patch", "status": "SCHEDULED", "window_utc": "Sun 02:00-04:00"}]
