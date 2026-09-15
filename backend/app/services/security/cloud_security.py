"""Cloud Security Posture Management (CSPM) Service."""
from typing import List, Dict, Any

class CloudSecurityService:
    def assess_cloud_configuration(self, resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        misconfigs = []
        for r in resources:
            if r.get("public_access", False) and r.get("type") in ["S3_BUCKET", "DATABASE"]:
                misconfigs.append({"resource_id": r.get("id"), "issue": "PUBLIC_DATA_STORE_EXPOSURE", "severity": "CRITICAL"})
            if not r.get("encrypted", True):
                misconfigs.append({"resource_id": r.get("id"), "issue": "UNENCRYPTED_STORAGE_VOLUME", "severity": "HIGH"})
        return misconfigs
