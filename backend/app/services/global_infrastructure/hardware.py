"""Phase 69: HardwareInventoryService."""
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class HardwareInventoryService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def list_hardware_assets(self, rack_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return [
                    {"id": "hw_srv_01", "serial_number": "SN-DELL-94821", "asset_tag": "SRV-IAD-001", "model_name": "PowerEdge R760", "vendor": "Dell", "cpu_model": "Intel Xeon Platinum 8480+", "cpu_cores_total": 112, "memory_total_gb": 512.0, "storage_total_tb": 64.0, "nic_speed_gbps": 100.0, "firmware_version": "v2.18.4", "lifecycle_phase": "OPERATIONAL"},
                    {"id": "hw_srv_02", "serial_number": "SN-HPE-38291", "asset_tag": "SRV-IAD-002", "model_name": "ProLiant DL380 Gen11", "vendor": "HPE", "cpu_model": "AMD EPYC 9654", "cpu_cores_total": 96, "memory_total_gb": 768.0, "storage_total_tb": 128.0, "nic_speed_gbps": 200.0, "firmware_version": "v3.10.1", "lifecycle_phase": "OPERATIONAL"}
                ]

