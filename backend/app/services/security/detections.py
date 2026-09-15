"""Detection Engine & Configurable Rule Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional

class DetectionEngineService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._rules: List[Dict[str, Any]] = [
            {"id": "rule_brute_force", "name": "Brute Force Detection", "severity": "HIGH", "threshold": 5, "mitre": "T1110"},
            {"id": "rule_exfiltration", "name": "Mass Data Exfiltration", "severity": "CRITICAL", "threshold": 1000, "mitre": "T1048"},
            {"id": "rule_priv_esc", "name": "Privilege Escalation Spike", "severity": "HIGH", "threshold": 2, "mitre": "T1078"},
        ]

    def list_rules(self) -> List[Dict[str, Any]]:
        return self._rules

    def add_rule(self, name: str, severity: str, threshold: int, mitre: str = "T1078") -> Dict[str, Any]:
        r = {"id": f"rule_{uuid.uuid4().hex[:8]}", "name": name, "severity": severity, "threshold": threshold, "mitre": mitre}
        self._rules.append(r)
        return r
