"""Custom / Extensible Plugin Data Connector."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from backend.app.services.data.connectors.base import BaseConnector


class CustomConnector(BaseConnector):
    """Dynamic, user-defined or script-based connector."""

    def __init__(self, connector_id: str, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(connector_id, name, config)
        self.custom_protocol = self.config.get("protocol", "CUSTOM_HTTP")

    def connect(self) -> bool:
        self.is_connected = True
        return True

    def discover_schema(self) -> Dict[str, Any]:
        return {
            "source_id": self.connector_id,
            "protocol": self.custom_protocol,
            "custom_fields": self.config.get("declared_fields", ["id", "payload", "timestamp"]),
            "discovered_at": datetime.now(timezone.utc).isoformat(),
        }

    def extract(self, query_or_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        self.last_sync_time = datetime.now(timezone.utc)
        return [
            {"id": "cust_rec_1", "payload": {"k": "v1"}, "timestamp": datetime.now(timezone.utc).isoformat()},
            {"id": "cust_rec_2", "payload": {"k": "v2"}, "timestamp": datetime.now(timezone.utc).isoformat()},
        ]

    def validate(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"total_records": len(records), "valid_records": len(records), "passed": True}

    def load(self, records: List[Dict[str, Any]], target_destination: str) -> Dict[str, Any]:
        return {"target": target_destination, "loaded_count": len(records), "status": "SUCCESS"}

    def health_check(self) -> Dict[str, Any]:
        return {"connector_id": self.connector_id, "protocol": self.custom_protocol, "status": "HEALTHY", "latency_ms": 20.0}

    def disconnect(self) -> bool:
        self.is_connected = False
        return True
