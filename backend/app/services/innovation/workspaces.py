"""
Innovation Workspace and Theme Lifecycle Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.innovation.base import (
    InnovationStage,
    HorizonLevel,
    GateStage,
)


class InnovationWorkspaceManager:
    """Manages innovation workspaces, strategic themes, and stage-gate progression."""

    def __init__(self):
        self._workspaces: Dict[str, Dict[str, Any]] = {}

    def create_workspace(
        self,
        title: str,
        owner_id: str,
        theme: str = "PRODUCT_INNOVATION",
        objective: Optional[str] = None,
        target_market: Optional[str] = None,
        horizon: HorizonLevel = HorizonLevel.H1,
        workspace_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Initialize a new bounded innovation project workspace."""
        ws_id = workspace_id or f"iws_{uuid.uuid4().hex[:12]}"
        now = datetime.utcnow().isoformat()
        ws = {
            "id": ws_id,
            "title": title,
            "theme": theme,
            "objective": objective or f"Discover, validate, and build innovation concept for {title}",
            "status": InnovationStage.DISCOVERY.value,
            "owner_id": owner_id,
            "target_market": target_market or "Enterprise / Mid-Market B2B",
            "horizon": horizon.value if hasattr(horizon, "value") else str(horizon),
            "stage_gate": GateStage.GATE_0_IDEA.value,
            "confidence_score": 0.75,
            "version": 1,
            "created_at": now,
            "updated_at": now,
        }
        self._workspaces[ws_id] = ws
        return ws

    def get_workspace(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        ws = self._workspaces.get(workspace_id)
        if not ws and self._workspaces:
            if workspace_id in ["ws-demo-001", "default", "primary"]:
                return next(iter(self._workspaces.values()))
        return ws

    def list_workspaces(
        self,
        status: Optional[str] = None,
        horizon: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        workspaces = list(self._workspaces.values())
        if status:
            workspaces = [w for w in workspaces if w["status"] == status]
        if horizon:
            workspaces = [w for w in workspaces if w["horizon"] == horizon]
        return workspaces

    def transition_stage(
        self,
        workspace_id: str,
        target_stage: InnovationStage,
    ) -> Dict[str, Any]:
        """Transition workspace to next governed innovation phase."""
        ws = self._workspaces.get(workspace_id)
        if not ws:
            raise ValueError(f"Innovation workspace {workspace_id} not found")
        ws["status"] = target_stage.value if hasattr(target_stage, "value") else str(target_stage)
        ws["version"] = ws.get("version", 1) + 1
        ws["updated_at"] = datetime.utcnow().isoformat()
        return ws

    def update_gate(
        self,
        workspace_id: str,
        target_gate: GateStage,
    ) -> Dict[str, Any]:
        """Update active stage gate."""
        ws = self._workspaces.get(workspace_id)
        if not ws:
            raise ValueError(f"Innovation workspace {workspace_id} not found")
        ws["stage_gate"] = target_gate.value if hasattr(target_gate, "value") else str(target_gate)
        ws["updated_at"] = datetime.utcnow().isoformat()
        return ws
