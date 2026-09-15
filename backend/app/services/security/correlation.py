"""Multi-Event & Attack Chain Correlation Service."""
from typing import List, Dict, Any, Optional

class EventCorrelationService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def correlate_attack_chain(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        failed_logins = [e for e in events if e.get("action") == "LOGIN" and e.get("status") == "FAILURE"]
        success_logins = [e for e in events if e.get("action") == "LOGIN" and e.get("status") == "SUCCESS"]
        data_exports = [e for e in events if "EXPORT" in e.get("action", "")]

        if len(failed_logins) >= 3 and len(success_logins) >= 1:
            findings.append({
                "pattern": "PASSWORD_SPRAY_OR_BRUTE_FORCE_SUCCESS",
                "severity": "CRITICAL",
                "evidence": f"{len(failed_logins)} failed logins followed by successful login",
                "confidence": 0.92,
            })
        if len(data_exports) >= 1 and len(success_logins) >= 1:
            findings.append({
                "pattern": "ANOMALOUS_DATA_ACCESS_AFTER_LOGIN",
                "severity": "HIGH",
                "evidence": "High-volume data export following recent login",
                "confidence": 0.88,
            })
        return findings
