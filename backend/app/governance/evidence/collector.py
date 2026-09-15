"""
Evidence Collector & Freshness Monitoring Engine (Section 14 & 46).
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import uuid

from backend.app.governance.base import (
    EvidenceFreshness,
    EvidenceType,
    GovernanceEvidence,
)
from backend.app.governance.evidence.integrity import EvidenceIntegrityManager


class EvidenceCollector:
    """Manages the lifecycle, storage, linking, and freshness auditing of GRC evidence items."""

    def __init__(self):
        self._evidence_store: Dict[str, GovernanceEvidence] = {}
        self._control_links: Dict[str, List[str]] = {}  # control_code -> list of evidence_id

    def ingest_evidence(
        self,
        evidence_type: EvidenceType,
        source_subsystem: str,
        source_record_id: str,
        provenance_uri: str,
        summary: str,
        data_payload: Dict[str, Any],
        control_codes: Optional[List[str]] = None,
        validity_days: int = 90
    ) -> GovernanceEvidence:
        """Ingests a verified evidence item with cryptographic SHA-256 fingerprinting."""
        now = datetime.now(timezone.utc)
        sha_hash = EvidenceIntegrityManager.calculate_evidence_hash(source_subsystem, source_record_id, data_payload)

        evidence = GovernanceEvidence(
            evidence_id=str(uuid.uuid4()),
            evidence_type=evidence_type,
            source_subsystem=source_subsystem,
            source_record_id=source_record_id,
            sha256_hash=sha_hash,
            provenance_uri=provenance_uri,
            summary=summary,
            data_payload=data_payload,
            collected_at=now,
            valid_until=now + timedelta(days=validity_days),
            freshness_status=EvidenceFreshness.FRESH
        )
        self._evidence_store[evidence.evidence_id] = evidence

        if control_codes:
            for c_code in control_codes:
                if c_code not in self._control_links:
                    self._control_links[c_code] = []
                self._control_links[c_code].append(evidence.evidence_id)

        return evidence

    def get_evidence(self, evidence_id: str) -> Optional[GovernanceEvidence]:
        return self._evidence_store.get(evidence_id)

    def get_evidence_for_control(self, control_code: str) -> List[GovernanceEvidence]:
        e_ids = self._control_links.get(control_code, [])
        return [self._evidence_store[eid] for eid in e_ids if eid in self._evidence_store]

    def audit_evidence_freshness(self) -> Dict[str, Any]:
        """Evaluates freshness states of all evidence items against age thresholds."""
        now = datetime.now(timezone.utc)
        fresh_count = 0
        aging_count = 0
        stale_count = 0

        for item in self._evidence_store.values():
            age_days = (now - item.collected_at).days
            if item.valid_until and now > item.valid_until:
                item.freshness_status = EvidenceFreshness.STALE
                stale_count += 1
            elif age_days > 90:
                item.freshness_status = EvidenceFreshness.STALE
                stale_count += 1
            elif age_days > 30:
                item.freshness_status = EvidenceFreshness.AGING
                aging_count += 1
            else:
                item.freshness_status = EvidenceFreshness.FRESH
                fresh_count += 1

        return {
            "total_evidence_items": len(self._evidence_store),
            "fresh_count": fresh_count,
            "aging_count": aging_count,
            "stale_count": stale_count,
            "audited_at": now.isoformat()
        }
