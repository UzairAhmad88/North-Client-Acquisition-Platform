"""Data Pipelines service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone


class PipelinesService:
    """Manages Transformation, ETL/ELT DAG pipelines and step dependencies."""

    def __init__(self):
        self._pipelines: Dict[str, Dict[str, Any]] = {}

    def create_pipeline(self, data: Dict[str, Any], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        pipeline_id = data.get("id") or f"pipe_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()
        record = {
            "id": pipeline_id,
            "tenant_id": tenant_id,
            "name": data.get("name", "Unnamed Pipeline"),
            "description": data.get("description", ""),
            "trigger_type": data.get("trigger_type", "SCHEDULED"),
            "schedule_cron": data.get("schedule_cron", "0 * * * *"),
            "owner": data.get("owner", "data-eng@uzaii.com"),
            "sla_minutes": data.get("sla_minutes", 60),
            "dependencies": data.get("dependencies", []),
            "steps": data.get("steps", [
                {"step_order": 1, "name": "Extract Raw", "step_type": "EXTRACT"},
                {"step_order": 2, "name": "Validate Cleanse", "step_type": "VALIDATE"},
                {"step_order": 3, "name": "Transform Normalize", "step_type": "TRANSFORM"},
                {"step_order": 4, "name": "Load Lakehouse Gold", "step_type": "LOAD"},
            ]),
            "status": "ACTIVE",
            "version": data.get("version", "v1.0.0"),
            "created_at": now_iso,
        }
        self._pipelines[pipeline_id] = record
        return record

    def get_pipeline(self, pipeline_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        pipe = self._pipelines.get(pipeline_id)
        if pipe and pipe.get("tenant_id") == tenant_id:
            return pipe
        return None

    def list_pipelines(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [p for p in self._pipelines.values() if p.get("tenant_id") == tenant_id]
