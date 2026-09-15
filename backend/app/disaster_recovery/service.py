"""Disaster Recovery & Business Continuity platform service."""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.disaster_recovery.backup import BackupManager
from app.disaster_recovery.drills import DisasterRecoveryDrillManager
from app.disaster_recovery.plans import DisasterRecoveryPlanRegistry
from app.disaster_recovery.restore import RestoreVerifier


class DisasterRecoveryService:
    """Coordinates backup registration, restore tests, DR plans, and game-day drills."""

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.backup_mgr = BackupManager()
        self.restore_verifier = RestoreVerifier()
        self.plan_registry = DisasterRecoveryPlanRegistry()
        self.drill_mgr = DisasterRecoveryDrillManager()

    def get_dr_plan(self) -> Dict[str, Any]:
        return self.plan_registry.get_standard_dr_plan()

    def run_restore_test(self, backup_id: str) -> Dict[str, Any]:
        return self.restore_verifier.execute_restore_test(backup_id=backup_id)

    def run_drill(self, scenario_name: str, simulated_failure: str, target_subsystem: str) -> Dict[str, Any]:
        return self.drill_mgr.execute_drill(
            scenario_name=scenario_name,
            simulated_failure=simulated_failure,
            target_subsystem=target_subsystem,
        )
