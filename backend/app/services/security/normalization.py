"""SIEM Telemetry Normalization Service."""
from typing import Dict, Any

class TelemetryNormalizationService:
    @staticmethod
    def normalize_event(raw_event: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "actor_id": raw_event.get("user") or raw_event.get("actor") or raw_event.get("principal", "UNKNOWN"),
            "action": (raw_event.get("event_type") or raw_event.get("action", "UNKNOWN")).upper(),
            "target_resource": raw_event.get("resource") or raw_event.get("target", "GLOBAL"),
            "source_ip": raw_event.get("ip") or raw_event.get("ip_address"),
            "status": "SUCCESS" if str(raw_event.get("status", "SUCCESS")).upper() in ["SUCCESS", "ALLOW", "200"] else "FAILURE",
        }
