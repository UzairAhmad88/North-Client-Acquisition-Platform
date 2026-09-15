"""Data Security & Exfiltration Monitoring Service (Phase 65 Integration)."""
from typing import Dict, Any, List, Optional, Optional, List
from datetime import datetime, timezone

class DataSecurityDefenseService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._exfiltration_alerts: List[Dict[str, Any]] = []

    def check_exfiltration_anomaly(self, actor_id: str, dataset_name: str, records_exported: int, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        is_anomalous = records_exported > 5000
        alert = None
        if is_anomalous:
            alert = {
                "tenant_id": tenant_id,
                "actor_id": actor_id,
                "dataset_name": dataset_name,
                "records_exported": records_exported,
                "severity": "CRITICAL",
                "reason": f"Export volume ({records_exported}) exceeds safe threshold (5000).",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self._exfiltration_alerts.append(alert)

        return {
            "anomalous": is_anomalous,
            "alert": alert,
            "action_recommended": "QUARANTINE_CREDENTIAL" if is_anomalous else "ALLOW",
        }
