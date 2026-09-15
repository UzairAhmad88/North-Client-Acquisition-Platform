"""Device Posture & Endpoint Security Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

class DeviceSecurityService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self._devices: List[Dict[str, Any]] = []

    def register_device(self, payload: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        dev_id = payload.get("id") or f"dev_{uuid.uuid4().hex[:12]}"
        record = {
            "id": dev_id,
            "tenant_id": tenant_id,
            "device_name": payload.get("device_name", "Workstation"),
            "owner_identity_id": payload.get("owner_identity_id", "admin"),
            "platform": payload.get("platform", "LINUX"),
            "os_version": payload.get("os_version", "Ubuntu 24.04"),
            "is_managed": payload.get("is_managed", True),
            "is_encrypted": payload.get("is_encrypted", True),
            "edr_installed": payload.get("edr_installed", True),
            "posture_status": payload.get("posture_status", "COMPLIANT"),
            "last_seen": datetime.now(timezone.utc).isoformat(),
        }
        self._devices.append(record)
        return record

    def assess_posture(self, device_id: str, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        for d in self._devices:
            if d["id"] == device_id and d["tenant_id"] == tenant_id:
                compliant = d.get("is_encrypted", False) and d.get("edr_installed", False)
                status = "COMPLIANT" if compliant else "NON_COMPLIANT"
                d["posture_status"] = status
                return {"device_id": device_id, "posture": status, "compliant": compliant}
        return {"device_id": device_id, "posture": "UNKNOWN", "compliant": False}
