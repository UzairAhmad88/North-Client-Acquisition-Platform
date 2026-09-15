"""Phase 64 — CI/CD Pipelines & Build Engine Service."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.services.autonomous_engineering_os.base import (
    BaseAutonomousEngineeringOsService,
    AttrDict,
    CiPipelineModel,
    CiBuildRunModel,
)


class CiCdBuildsArtifactsService(BaseAutonomousEngineeringOsService):
    """Service managing CI/CD pipeline definitions, execution runs, and build artifacts."""

    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)
        self._pipelines: Dict[str, Any] = {}
        self._build_runs: Dict[str, Any] = {}

    def create_pipeline(
        self,
        tenant_id: str,
        repository_id: str,
        pipeline_name: str,
        trigger_event: str = "PUSH",
        stages: Optional[List[str]] = None,
    ) -> Any:
        """Create CI/CD pipeline template."""
        pipe_id = self.generate_id("eng_pipe")
        now = datetime.utcnow()
        stages_list = stages or [
            "lint",
            "type_check",
            "unit_test",
            "integration_test",
            "security_scan",
            "build_container",
            "publish_artifact",
        ]

        if self.db is not None and CiPipelineModel is not None:
            pipeline = CiPipelineModel(
                id=pipe_id,
                tenant_id=tenant_id,
                repository_id=repository_id,
                pipeline_name=pipeline_name,
                trigger_event=trigger_event,
                stages_json=stages_list,
                status="ACTIVE",
                created_at=now,
            )
            self.db.add(pipeline)
            self.db.commit()
            self.db.refresh(pipeline)
            return pipeline
        else:
            pipeline = AttrDict({
                "id": pipe_id,
                "tenant_id": tenant_id,
                "repository_id": repository_id,
                "pipeline_name": pipeline_name,
                "trigger_event": trigger_event,
                "stages_json": stages_list,
                "status": "ACTIVE",
                "created_at": now,
            })
            self._pipelines[pipe_id] = pipeline
            return pipeline

    def list_pipelines(self, tenant_id: str, repository_id: Optional[str] = None) -> List[Any]:
        """List pipelines for repository."""
        if self.db is not None and CiPipelineModel is not None:
            q = self.db.query(CiPipelineModel).filter(CiPipelineModel.tenant_id == tenant_id)
            if repository_id:
                q = q.filter(CiPipelineModel.repository_id == repository_id)
            return q.all()
        results = [p for p in self._pipelines.values() if p.tenant_id == tenant_id]
        if repository_id:
            results = [p for p in results if p.repository_id == repository_id]
        return results

    def execute_build_run(
        self,
        tenant_id: str,
        pipeline_id: str,
        commit_sha: str,
        branch: str = "main",
        build_number: int = 1,
        duration_seconds: float = 38.5,
        status: str = "SUCCESS",
    ) -> Any:
        """Execute automated build run and record artifact provenance."""
        pipe_name = "build-pipeline"
        if self.db is not None and CiPipelineModel is not None:
            pipe = (
                self.db.query(CiPipelineModel)
                .filter(
                    CiPipelineModel.tenant_id == tenant_id,
                    CiPipelineModel.id == pipeline_id,
                )
                .first()
            )
            if pipe:
                pipe_name = pipe.pipeline_name
        else:
            pipe = self._pipelines.get(pipeline_id)
            if pipe:
                pipe_name = getattr(pipe, "pipeline_name", "build-pipeline")

        artifacts = [
            f"ghcr.io/uzaii-enterprise/{pipe_name.lower().replace(' ', '-')}:{commit_sha[:8]}",
            f"s3://uzaii-artifacts/builds/{commit_sha[:8]}/bundle.tar.gz",
        ]

        build_id = self.generate_id("eng_build")
        now = datetime.utcnow()

        if self.db is not None and CiBuildRunModel is not None:
            build = CiBuildRunModel(
                id=build_id,
                tenant_id=tenant_id,
                pipeline_id=pipeline_id,
                commit_sha=commit_sha,
                branch=branch,
                build_number=build_number,
                duration_seconds=duration_seconds,
                status=status,
                logs_uri=f"https://ci.uzaii.internal/logs/build/{pipeline_id}/{commit_sha[:8]}",
                artifacts_generated=artifacts,
                created_at=now,
            )
            self.db.add(build)
            self.db.commit()
            self.db.refresh(build)
            return build
        else:
            build = AttrDict({
                "id": build_id,
                "tenant_id": tenant_id,
                "pipeline_id": pipeline_id,
                "commit_sha": commit_sha,
                "branch": branch,
                "build_number": build_number,
                "duration_seconds": duration_seconds,
                "status": status,
                "logs_uri": f"https://ci.uzaii.internal/logs/build/{pipeline_id}/{commit_sha[:8]}",
                "artifacts_generated": artifacts,
                "created_at": now,
            })
            self._build_runs[build_id] = build
            return build

    def list_build_runs(self, tenant_id: str, pipeline_id: Optional[str] = None) -> List[Any]:
        """List build runs."""
        if self.db is not None and CiBuildRunModel is not None:
            q = self.db.query(CiBuildRunModel).filter(CiBuildRunModel.tenant_id == tenant_id)
            if pipeline_id:
                q = q.filter(CiBuildRunModel.pipeline_id == pipeline_id)
            return q.all()
        results = [b for b in self._build_runs.values() if b.tenant_id == tenant_id]
        if pipeline_id:
            results = [b for b in results if b.pipeline_id == pipeline_id]
        return results
