"""AI Model Registry, Multi-Framework Artifact Storage, and Model Lineage Service for Phase 63."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

try:
    from backend.app.services.ai_model_factory.base import (
        AttrDict,
        FrameworkType,
        ModelStage,
        ModelType,
        generate_ai_id,
    )
except ImportError:
    from app.services.ai_model_factory.base import (
        AttrDict,
        FrameworkType,
        ModelStage,
        ModelType,
        generate_ai_id,
    )

logger = logging.getLogger(__name__)


class ModelRegistryArtifactsService:
    """Manages Central Model Registry, versioned immutable artifacts, and stage promotion gates."""

    def __init__(self):
        self._models: Dict[str, AttrDict] = {}
        self._model_versions: Dict[str, AttrDict] = {}

    def register_model(
        self,
        tenant_id: str,
        project_id: str,
        name: str,
        owner: str,
        model_type: str = ModelType.CLASSIFICATION.value,
        framework: str = FrameworkType.PYTORCH.value,
        steward: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> AttrDict:
        """Register a new top-level Model entity in the Model Registry."""
        model_id = generate_ai_id("aimodel")
        now = datetime.utcnow()
        model = AttrDict({
            "id": model_id,
            "tenant_id": tenant_id,
            "project_id": project_id,
            "name": name,
            "description": description or f"Production Model {name} ({framework})",
            "model_type": model_type,
            "framework": framework,
            "owner": owner,
            "steward": steward or owner,
            "current_stage": ModelStage.EXPERIMENTAL.value,
            "active_version": "1.0.0",
            "tags": tags or ["production-candidate", model_type.lower()],
            "created_at": now,
            "updated_at": now,
        })
        self._models[model_id] = model
        logger.info(f"Registered AI Model {model_id}: {name} ({framework})")
        return model

    def create_model_version(
        self,
        tenant_id: str,
        model_id: str,
        version: str,
        training_run_id: Optional[str] = None,
        dataset_version_id: Optional[str] = None,
        artifacts_manifest: Optional[Dict[str, Any]] = None,
        metrics_summary: Optional[Dict[str, float]] = None,
        supply_chain_sbom: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        """Create an immutable version artifact under a registered model."""
        version_id = generate_ai_id("aimv")
        now = datetime.utcnow()

        version_record = AttrDict({
            "id": version_id,
            "tenant_id": tenant_id,
            "model_id": model_id,
            "version": version,
            "stage": ModelStage.EXPERIMENTAL.value,
            "training_run_id": training_run_id or "airun_seed_01",
            "dataset_version_id": dataset_version_id or "aids_seed_01",
            "artifacts_manifest": artifacts_manifest or {
                "weights_uri": f"s3://uzaii-models/{model_id}/{version}/weights.pt",
                "onnx_uri": f"s3://uzaii-models/{model_id}/{version}/model.onnx",
                "config_uri": f"s3://uzaii-models/{model_id}/{version}/config.json",
                "checksum_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            },
            "metrics_summary": metrics_summary or {"accuracy": 0.942, "f1_score": 0.938, "latency_p95_ms": 32.5},
            "supply_chain_sbom": supply_chain_sbom or {
                "base_model": "none-scratch",
                "license": "Apache-2.0",
                "dependencies": ["torch>=2.1.0", "onnxruntime>=1.16.0", "numpy>=1.24.0"],
                "security_vulnerabilities_found": 0,
            },
            "is_signed": True,
            "quality_gate_passed": False,
            "security_scan_passed": False,
            "governance_approved": False,
            "created_at": now,
        })
        self._model_versions[version_id] = version_record

        # Update model active version
        model = self._models.get(model_id)
        if model:
            model.active_version = version
            model.updated_at = now

        logger.info(f"Created AI Model Version {version_id}: Model {model_id} v{version}")
        return version_record

    def evaluate_and_promote_stage(
        self,
        tenant_id: str,
        version_id: str,
        target_stage: str,
        approver: str,
    ) -> AttrDict:
        """Promote model version through stage gates (VALIDATION -> STAGING -> PRODUCTION)."""
        version = self._model_versions.get(version_id)
        if not version or version.tenant_id != tenant_id:
            raise ValueError(f"Model version {version_id} not found")

        # Mandatory checks for STAGING / PRODUCTION
        if target_stage in [ModelStage.STAGING.value, ModelStage.PRODUCTION.value]:
            if not version.quality_gate_passed:
                raise PermissionError("Cannot promote to STAGING/PRODUCTION: Quality gate has not passed.")
            if not version.security_scan_passed:
                raise PermissionError("Cannot promote to STAGING/PRODUCTION: Security scan has not passed.")
            if not version.governance_approved and target_stage == ModelStage.PRODUCTION.value:
                raise PermissionError("Cannot promote to PRODUCTION: Formal human Data/AI Steward governance sign-off required.")

        version.stage = target_stage
        model = self._models.get(version.model_id)
        if model:
            model.current_stage = target_stage
            model.updated_at = datetime.utcnow()

        logger.info(f"Promoted Model Version {version_id} to stage {target_stage} by {approver}")
        return version

    def list_models(self, tenant_id: str, project_id: Optional[str] = None) -> List[AttrDict]:
        """List models."""
        models = [m for m in self._models.values() if m.tenant_id == tenant_id]
        if project_id:
            models = [m for m in models if m.project_id == project_id]
        return models

    def list_model_versions(self, tenant_id: str, model_id: Optional[str] = None) -> List[AttrDict]:
        """List model versions."""
        versions = [v for v in self._model_versions.values() if v.tenant_id == tenant_id]
        if model_id:
            versions = [v for v in versions if v.model_id == model_id]
        return versions

    def get_model(self, model_id: str) -> Optional[AttrDict]:
        """Get model by ID."""
        return self._models.get(model_id)

    def get_model_version(self, version_id: str) -> Optional[AttrDict]:
        """Get model version by ID."""
        return self._model_versions.get(version_id)
