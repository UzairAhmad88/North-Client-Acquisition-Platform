"""Pipeline Orchestration DAG Execution service for Phase 65."""

from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone
from backend.app.services.data.pipelines import PipelinesService


class OrchestrationService:
    """Executes scheduled, dependency-based, and AI-triggered pipeline DAG runs."""

    def __init__(self, pipelines_service: Optional[PipelinesService] = None):
        self.pipelines_service = pipelines_service or PipelinesService()
        self._runs: Dict[str, Dict[str, Any]] = {}

    def run_pipeline(
        self,
        pipeline_id: str,
        parameters: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default_tenant"
    ) -> Dict[str, Any]:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        pipeline = self.pipelines_service.get_pipeline(pipeline_id, tenant_id)
        pipe_name = pipeline.get("name") if pipeline else f"Pipeline-{pipeline_id}"

        # Simulate execution of steps
        steps = pipeline.get("steps", []) if pipeline else []
        step_logs = []
        for s in steps:
            step_logs.append({
                "step": s.get("name"),
                "status": "COMPLETED",
                "duration_sec": 1.2,
            })

        run_record = {
            "id": run_id,
            "tenant_id": tenant_id,
            "pipeline_id": pipeline_id,
            "pipeline_name": pipe_name,
            "run_status": "COMPLETED",
            "records_transformed": 12500,
            "latency_seconds": 4.8,
            "step_logs": step_logs,
            "parameters": parameters or {},
            "started_at": now.isoformat(),
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        self._runs[run_id] = run_record
        return run_record

    def get_run(self, run_id: str, tenant_id: str = "default_tenant") -> Optional[Dict[str, Any]]:
        run = self._runs.get(run_id)
        if run and run.get("tenant_id") == tenant_id:
            return run
        return None

    def list_runs(self, pipeline_id: Optional[str] = None, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        runs = [r for r in self._runs.values() if r.get("tenant_id") == tenant_id]
        if pipeline_id:
            runs = [r for r in runs if r.get("pipeline_id") == pipeline_id]
        return runs
