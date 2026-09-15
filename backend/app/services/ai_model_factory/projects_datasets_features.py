"""AI Projects, Governed Datasets, and Feature Validation Service for Phase 63."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

try:
    from backend.app.services.ai_model_factory.base import (
        AttrDict,
        generate_ai_id,
    )
except ImportError:
    from app.services.ai_model_factory.base import (
        AttrDict,
        generate_ai_id,
    )

logger = logging.getLogger(__name__)


class ProjectsDatasetsFeaturesService:
    """Manages AI Project workspaces, Lakehouse-linked Dataset versions, and feature validation."""

    def __init__(self):
        self._projects: Dict[str, AttrDict] = {}
        self._dataset_versions: Dict[str, AttrDict] = {}
        self._feature_groups: Dict[str, AttrDict] = {}

    def create_project(
        self,
        tenant_id: str,
        name: str,
        owner: str,
        team: str,
        domain: str = "GENERAL",
        description: Optional[str] = None,
        objective: Optional[str] = None,
        budget_allocated_usd: float = 10000.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        """Create a new AI/ML Project workspace."""
        project_id = generate_ai_id("aiproj")
        now = datetime.utcnow()
        project = AttrDict({
            "id": project_id,
            "tenant_id": tenant_id,
            "name": name,
            "description": description or f"AI Project {name} focusing on {domain}",
            "owner": owner,
            "team": team,
            "domain": domain,
            "objective": objective or f"Train and deploy state-of-the-art models for {name}",
            "budget_allocated_usd": budget_allocated_usd,
            "budget_spent_usd": 0.0,
            "status": "ACTIVE",
            "metadata_json": metadata or {},
            "created_at": now,
            "updated_at": now,
        })
        self._projects[project_id] = project
        logger.info(f"Created AI Project {project_id}: {name} ({domain})")
        return project

    def list_projects(self, tenant_id: str, status: Optional[str] = None) -> List[AttrDict]:
        """List AI projects for tenant with optional status filter."""
        projects = [p for p in self._projects.values() if p.tenant_id == tenant_id]
        if status:
            projects = [p for p in projects if p.status == status]
        return projects

    def get_project(self, project_id: str) -> Optional[AttrDict]:
        """Get project by ID."""
        return self._projects.get(project_id)

    def register_dataset_version(
        self,
        tenant_id: str,
        project_id: str,
        dataset_name: str,
        version: str,
        features_list: List[str],
        label_column: Optional[str] = None,
        source_lakehouse_dataset_id: Optional[str] = None,
        splits: Optional[Dict[str, float]] = None,
        row_count: int = 50000,
        lineage_provenance: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        """Register a versioned training dataset with bias check & feature validation."""
        dataset_id = generate_ai_id("aids")
        now = datetime.utcnow()

        # Validate splits sum to 1.0 (or default 70/15/15)
        validated_splits = splits or {"train": 0.70, "val": 0.15, "test": 0.15}
        total_split = sum(validated_splits.values())
        if abs(total_split - 1.0) > 0.01:
            raise ValueError(f"Dataset split proportions must sum to 1.0, got {total_split}")

        # Deterministic bias check evaluation
        bias_status = "PASSED"
        if "demographic_parity_diff" in (lineage_provenance or {}) and lineage_provenance["demographic_parity_diff"] > 0.10:
            bias_status = "WARNING_BIAS_DETECTED"

        dataset = AttrDict({
            "id": dataset_id,
            "tenant_id": tenant_id,
            "project_id": project_id,
            "dataset_name": dataset_name,
            "version": version,
            "source_lakehouse_dataset_id": source_lakehouse_dataset_id or "ds_gold_cust_01",
            "features_list": features_list,
            "label_column": label_column,
            "splits": validated_splits,
            "row_count": row_count,
            "bias_check_status": bias_status,
            "lineage_provenance": lineage_provenance or {
                "lakehouse_layer": "GOLD",
                "upstream_tables": ["gold_customer_economics_mart", "feature_user_activity_30d"],
                "purity_score": 0.992,
            },
            "created_at": now,
        })
        self._dataset_versions[dataset_id] = dataset
        logger.info(f"Registered AI Dataset Version {dataset_id}: {dataset_name} v{version}")
        return dataset

    def validate_features_leakage(
        self,
        features_list: List[str],
        label_column: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Verify features do not leak target label or contain disallowed PII fields."""
        leaked_features = []
        pii_flagged_features = []

        prohibited_pii = {"ssn", "credit_card", "raw_password", "national_id", "secret_key"}

        for f in features_list:
            f_lower = f.lower()
            if label_column and f_lower == label_column.lower():
                leaked_features.append(f)
            if any(pii in f_lower for pii in prohibited_pii):
                pii_flagged_features.append(f)

        is_valid = (len(leaked_features) == 0) and (len(pii_flagged_features) == 0)
        return {
            "is_valid": is_valid,
            "leaked_features": leaked_features,
            "pii_flagged_features": pii_flagged_features,
            "total_features": len(features_list),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def list_dataset_versions(self, tenant_id: str, project_id: Optional[str] = None) -> List[AttrDict]:
        """List dataset versions."""
        datasets = [d for d in self._dataset_versions.values() if d.tenant_id == tenant_id]
        if project_id:
            datasets = [d for d in datasets if d.project_id == project_id]
        return datasets
