"""
Deployment Intelligence, Feature Flag Control, and Product Launch Workspace Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.product_management.base import FeatureFlagState


class DeploymentLaunchManager:
    """Manages continuous delivery feature flags, deployments, and launch readiness checklists."""

    def __init__(self):
        self._feature_flags: Dict[str, List[Dict[str, Any]]] = {}
        self._deployments: Dict[str, List[Dict[str, Any]]] = {}
        self._launches: Dict[str, List[Dict[str, Any]]] = {}

    # Feature Flags
    def create_feature_flag(
        self,
        product_id: str,
        flag_key: Optional[str] = None,
        description: Optional[str] = None,
        state: Any = FeatureFlagState.OFF,
        rollout_percentage: int = 0,
        target_segments: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a controlled rollout feature flag."""
        flag_id = f"flag_{uuid.uuid4().hex[:12]}"
        k = flag_key or kwargs.get("key", f"flag_{uuid.uuid4().hex[:8]}")
        st = state if state != FeatureFlagState.OFF else kwargs.get("state", FeatureFlagState.OFF)
        s_val = st.value if hasattr(st, "value") else str(st)
        pct = rollout_percentage or kwargs.get("rollout_percentage", 0)

        flag = {
            "id": flag_id,
            "product_id": product_id,
            "flag_key": k,
            "key": k,
            "description": description or kwargs.get("description", "Feature flag"),
            "state": s_val,
            "rollout_percentage": pct,
            "target_segments": target_segments or ["internal_qa", "beta_testers"],
            "created_at": datetime.utcnow().isoformat(),
        }
        self._feature_flags.setdefault(product_id, []).append(flag)
        return flag

    def create_flag(self, *args, **kwargs) -> Dict[str, Any]:
        """Alias for create_feature_flag."""
        return self.create_feature_flag(*args, **kwargs)

    def update_feature_flag(
        self,
        product_id: str,
        flag_key: str,
        state: Any,
        rollout_percentage: int = 100,
    ) -> Dict[str, Any]:
        s_val = state.value if hasattr(state, "value") else str(state)
        flags = self._feature_flags.get(product_id, [])
        for f in flags:
            if f["flag_key"] == flag_key or f.get("key") == flag_key:
                f["state"] = s_val
                f["rollout_percentage"] = rollout_percentage
                f["updated_at"] = datetime.utcnow().isoformat()
                return f
        # fallback create
        return self.create_feature_flag(product_id, flag_key, "Feature flag", state, rollout_percentage)

    def list_feature_flags(self, product_id: str) -> List[Dict[str, Any]]:
        return self._feature_flags.get(product_id, [])

    def list_flags(self, product_id: str) -> List[Dict[str, Any]]:
        return self.list_feature_flags(product_id)

    # Product Launches
    def create_launch_workspace(
        self,
        product_id: str,
        launch_name: Optional[str] = None,
        target_audience: Optional[str] = None,
        value_messaging: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Initialize product launch preparation workspace."""
        launch_id = f"launch_{uuid.uuid4().hex[:12]}"
        name = launch_name or kwargs.get("name", f"Launch {kwargs.get('target_release_version', 'v1.0.0')}")
        aud = target_audience or kwargs.get("target_audience", "Enterprise customers")
        msg = value_messaging or kwargs.get("positioning", "Continuous Delivery Intelligence OS")

        checklist = {
            "product_qa_passed": True,
            "security_attested": True,
            "infrastructure_scaled": True,
            "support_team_trained": True,
            "documentation_published": True,
            "analytics_telemetry_active": True,
            "billing_metering_ready": True,
            "rollback_tested": True,
            "human_executive_approval": False,
        }

        launch = {
            "id": launch_id,
            "product_id": product_id,
            "launch_name": name,
            "name": name,
            "target_release_version": kwargs.get("target_release_version", "v1.0.0"),
            "target_audience": aud,
            "value_messaging": msg,
            "positioning": msg,
            "checklist": checklist,
            "checklist_status": checklist,
            "is_launch_approved": False,
            "status": "PREPARING",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._launches.setdefault(product_id, []).append(launch)
        return launch

    def create_launch(self, *args, **kwargs) -> Dict[str, Any]:
        return self.create_launch_workspace(*args, **kwargs)

    def list_launches(self, product_id: str) -> List[Dict[str, Any]]:
        return self._launches.get(product_id, [])
