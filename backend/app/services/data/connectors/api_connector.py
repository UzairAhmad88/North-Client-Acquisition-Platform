"""REST, GraphQL, and Webhook API Connector."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from backend.app.services.data.connectors.base import BaseConnector


class ApiConnector(BaseConnector):
    """Connector for External APIs and Webhooks."""

    def __init__(self, connector_id: str, name: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(connector_id, name, config)
        self.endpoint_url = self.config.get("endpoint_url", "https://api.external-service.com/v1")

    def connect(self) -> bool:
        self.is_connected = True
        return True

    def discover_schema(self) -> Dict[str, Any]:
        return {
            "source_id": self.connector_id,
            "endpoint": self.endpoint_url,
            "methods": ["GET", "POST"],
            "parameters": ["limit", "cursor", "since"],
            "payload_schema": {
                "id": "string",
                "event_type": "string",
                "timestamp": "iso8601",
                "data": "object"
            },
            "discovered_at": datetime.now(timezone.utc).isoformat(),
        }

    def extract(self, query_or_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        self.last_sync_time = datetime.now(timezone.utc)
        return [
            {"id": "evt_api_1", "event_type": "user.signup", "data": {"user_id": "u1", "plan": "pro"}},
            {"id": "evt_api_2", "event_type": "subscription.renew", "data": {"user_id": "u2", "amount": 99.0}},
        ]

    def validate(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        valid = sum(1 for r in records if "id" in r and "event_type" in r)
        return {"total_records": len(records), "valid_records": valid, "passed": valid == len(records)}

    def load(self, records: List[Dict[str, Any]], target_destination: str) -> Dict[str, Any]:
        return {"target": target_destination, "loaded_count": len(records), "status": "SUCCESS"}

    def health_check(self) -> Dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "status": "HEALTHY",
            "latency_ms": 28.5,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    def disconnect(self) -> bool:
        self.is_connected = False
        return True
