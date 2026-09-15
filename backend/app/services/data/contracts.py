"""Data Contracts service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class ContractsService:
    """Manages formal interface contracts between data producers and consumers."""

    def __init__(self):
        self._contracts: Dict[str, Dict[str, Any]] = {}

    def create_contract(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        contract_id = data.get("id") or f"contract_{uuid.uuid4().hex[:12]}"
        name = data.get("name") or data.get("dataset_name", "orders_stream")
        record = {
            "id": contract_id,
            "name": name,
            "tenant_id": tenant_id,
            "dataset_name": data.get("dataset_name", name),
            "owner": data.get("owner", "data-producer@uzaii.com"),
            "schema_rules": data.get("schema_rules", {"required_fields": ["id", "timestamp"]}),
            "constraints": data.get("constraints", [{"field": "id", "rule": "NOT_NULL"}]),
            "freshness_sla_minutes": data.get("freshness_sla_minutes", 60),
            "quality_threshold_pct": data.get("quality_threshold_pct", 98.0),
            "compatibility_mode": data.get("compatibility_mode", "BACKWARD"),
            "version": data.get("version", "v1.0.0"),
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._contracts[contract_id] = record
        return record

    def list_contracts(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [c for c in self._contracts.values() if c.get("tenant_id") == tenant_id]

    def validate_payload_against_contract(self, contract_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        contract = self._contracts.get(contract_id)
        if not contract:
            return {"valid": True, "note": "No active contract enforcement found for this ID"}
        
        required_fields = contract.get("schema_rules", {}).get("required_fields", [])
        missing = [f for f in required_fields if f not in payload]
        return {
            "contract_id": contract_id,
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "status": "PASSED" if len(missing) == 0 else "VIOLATION_DETECTED"
        }
