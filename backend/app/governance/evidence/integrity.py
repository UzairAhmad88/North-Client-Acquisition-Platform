"""
Evidence Integrity, Cryptographic Hashing & Provenance (Section 15).
"""

import hashlib
import json
from typing import Any, Dict


class EvidenceIntegrityManager:
    """Verifies evidence authenticity via deterministic SHA-256 cryptographic digests."""

    @staticmethod
    def calculate_evidence_hash(source_subsystem: str, source_record_id: str, data_payload: Dict[str, Any]) -> str:
        """Calculates canonical SHA-256 digest of an evidence payload."""
        canonical_str = json.dumps(
            {
                "subsystem": source_subsystem,
                "record_id": source_record_id,
                "payload": data_payload
            },
            sort_keys=True,
            default=str
        )
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_evidence_hash(evidence_hash: str, source_subsystem: str, source_record_id: str, data_payload: Dict[str, Any]) -> bool:
        """Verifies if an evidence payload matches its recorded SHA-256 signature."""
        computed = EvidenceIntegrityManager.calculate_evidence_hash(source_subsystem, source_record_id, data_payload)
        return computed == evidence_hash
