"""System-Wide Emergency Kill Switches and Layered Disablement Engine."""

from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.administration.base import KillSwitchItem, KillSwitchLevel, KillSwitchState


class SystemControlManager:
    """Manages global and granular emergency kill switches across all platform tiers."""

    def __init__(self):
        self._switches: Dict[str, KillSwitchItem] = {}
        self._seed_default_kill_switches()

    def _seed_default_kill_switches(self):
        """Seed authoritative emergency system kill switches."""
        switches = [
            KillSwitchItem(
                switch_id="GLOBAL_AI_OFF",
                name="Global AI Agents & LLM Kill Switch",
                level=KillSwitchLevel.GLOBAL,
                target_identifier="AI_SUBSYSTEM",
            ),
            KillSwitchItem(
                switch_id="GLOBAL_COMMUNICATION_OFF",
                name="Global External Messaging Kill Switch",
                level=KillSwitchLevel.GLOBAL,
                target_identifier="COMMUNICATION_SUBSYSTEM",
            ),
            KillSwitchItem(
                switch_id="GLOBAL_PAYMENTS_OFF",
                name="Global Real-Time Payments Kill Switch",
                level=KillSwitchLevel.GLOBAL,
                target_identifier="PAYMENTS_SUBSYSTEM",
            ),
            KillSwitchItem(
                switch_id="GLOBAL_WORKFLOWS_OFF",
                name="Global Workflow Orchestration Kill Switch",
                level=KillSwitchLevel.GLOBAL,
                target_identifier="WORKFLOW_SUBSYSTEM",
            ),
            KillSwitchItem(
                switch_id="GLOBAL_AUTOMATIONS_OFF",
                name="Global Background Automations Kill Switch",
                level=KillSwitchLevel.GLOBAL,
                target_identifier="AUTOMATION_SUBSYSTEM",
            ),
            KillSwitchItem(
                switch_id="GLOBAL_SEARCH_OFF",
                name="Global Vector & Full-Text Search Kill Switch",
                level=KillSwitchLevel.GLOBAL,
                target_identifier="SEARCH_SUBSYSTEM",
            ),
            KillSwitchItem(
                switch_id="GLOBAL_EXTERNAL_INTEGRATIONS_OFF",
                name="Global Third-Party Webhook & Outbound Sync Kill Switch",
                level=KillSwitchLevel.GLOBAL,
                target_identifier="INTEGRATIONS_SUBSYSTEM",
            ),
        ]
        for s in switches:
            self._switches[s.switch_id] = s

    def list_switches(self) -> List[KillSwitchItem]:
        """List all registered kill switches."""
        return list(self._switches.values())

    def get_switch(self, switch_id: str) -> Optional[KillSwitchItem]:
        """Get kill switch by identifier."""
        return self._switches.get(switch_id)

    def is_kill_switch_active(self, switch_id: str) -> bool:
        """Check if a specific kill switch is engaged."""
        s = self.get_switch(switch_id)
        return s.state == KillSwitchState.ACTIVE if s else False

    def activate_kill_switch(self, switch_id: str, activated_by: str, reason: str) -> KillSwitchItem:
        """Activate an emergency kill switch with strict auditing."""
        s = self.get_switch(switch_id)
        if not s:
            raise KeyError(f"Kill switch '{switch_id}' not found.")
        s.state = KillSwitchState.ACTIVE
        s.activated_by = activated_by
        s.reason = reason
        s.activated_at = datetime.now(timezone.utc)
        return s

    def release_kill_switch(self, switch_id: str, released_by: str) -> KillSwitchItem:
        """Disarm an active kill switch and restore normal operations."""
        s = self.get_switch(switch_id)
        if not s:
            raise KeyError(f"Kill switch '{switch_id}' not found.")
        s.state = KillSwitchState.DISARMED
        s.reason = f"Disarmed by {released_by} at {datetime.now(timezone.utc).isoformat()}"
        return s
