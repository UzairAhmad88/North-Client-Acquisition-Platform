"""Software Artifact Registry Service."""
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class ArtifactRegistryService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._artifacts: List[Dict[str, Any]] = []

    def register_artifact(self, name: str, version: str, sha256_checksum: str, artifact_type: str = "CONTAINER_IMAGE", tenant_id: str = "default_tenant") -> Dict[str, Any]:
        art_id = f"art_{uuid.uuid4().hex[:12]}"
        rec = {
            "id": art_id,
            "tenant_id": tenant_id,
            "name": name,
            "version": version,
            "artifact_type": artifact_type,
            "sha256_checksum": sha256_checksum,
            "signature_verified": True,
            "sbom_scanned": True,
            "critical_vulnerabilities": 0,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._artifacts.append(rec)
        return rec
