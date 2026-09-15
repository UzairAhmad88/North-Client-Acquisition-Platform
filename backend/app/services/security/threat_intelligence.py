"""Threat Intelligence Ingestion & Indicator Matching Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class ThreatIntelligenceService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._indicators: List[Dict[str, Any]] = [
            {"id": "ioc_1", "indicator_type": "IP", "value": "198.51.100.44", "threat_actor": "APT29", "severity": "CRITICAL"},
            {"id": "ioc_2", "indicator_type": "DOMAIN", "value": "malicious-c2-node.example", "threat_actor": "FIN7", "severity": "HIGH"},
        ]

    def add_indicator(self, indicator_type: str, value: str, threat_actor: Optional[str] = None, severity: str = "HIGH") -> Dict[str, Any]:
        ioc = {
            "id": f"ioc_{uuid.uuid4().hex[:8]}",
            "indicator_type": indicator_type,
            "value": value,
            "threat_actor": threat_actor or "UNKNOWN",
            "severity": severity,
            "first_seen": datetime.now(timezone.utc).isoformat(),
        }
        self._indicators.append(ioc)
        return ioc

    def check_indicator(self, query_value: str) -> Optional[Dict[str, Any]]:
        for ioc in self._indicators:
            if ioc["value"].lower() == query_value.lower():
                return ioc
        return None
