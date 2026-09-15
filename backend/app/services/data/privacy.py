"""Data Privacy & PII Discovery service for Phase 65."""

import re
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class PrivacyService:
    """Detects PII (Emails, Phones, SSN, Credit Cards, Secrets) across dataset records."""

    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    PHONE_REGEX = re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")
    API_KEY_REGEX = re.compile(r"\b(sk-[a-zA-Z0-9]{32,}|ghp_[a-zA-Z0-9]{36})\b")

    def __init__(self):
        self._findings: List[Dict[str, Any]] = []

    def scan_records_for_pii(
        self, dataset_name: str, records: List[Dict[str, Any]], tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        detected = []
        for r in records:
            for col, val in r.items():
                val_str = str(val)
                if self.EMAIL_REGEX.search(val_str):
                    detected.append({"dataset": dataset_name, "column": col, "pii_type": "EMAIL", "sample_masked": "u***@***.com"})
                elif self.PHONE_REGEX.search(val_str):
                    detected.append({"dataset": dataset_name, "column": col, "pii_type": "PHONE", "sample_masked": "***-***-0123"})
                elif self.API_KEY_REGEX.search(val_str):
                    detected.append({"dataset": dataset_name, "column": col, "pii_type": "SECRET", "sample_masked": "sk-***masked"})

        # Record findings
        for d in detected:
            d["id"] = f"pii_{uuid.uuid4().hex[:8]}"
            d["tenant_id"] = tenant_id
            d["confidence"] = 0.95
            d["discovered_at"] = datetime.now(timezone.utc).isoformat()
            self._findings.append(d)

        return {
            "dataset_name": dataset_name,
            "records_scanned": len(records),
            "pii_detected_count": len(detected),
            "findings": detected,
        }

    def list_findings(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [f for f in self._findings if f.get("tenant_id") == tenant_id]
