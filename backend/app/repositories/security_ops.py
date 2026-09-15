"""
Database Repository for Phase 46 Security Operations and Threat Intelligence.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

try:
    from app.models.security_ops import (
        SecurityDetectionModel,
        SecurityAlertModel,
        SecurityIncidentModel,
        SecurityInvestigationModel,
        SecurityAttackChainModel,
        SecurityBlastRadiusModel,
        SecurityThreatIndicatorModel,
        SecurityRemediationRunModel,
        SecurityPostureSnapshotModel,
    )
except ImportError:
    from backend.app.models.security_ops import (
        SecurityDetectionModel,
        SecurityAlertModel,
        SecurityIncidentModel,
        SecurityInvestigationModel,
        SecurityAttackChainModel,
        SecurityBlastRadiusModel,
        SecurityThreatIndicatorModel,
        SecurityRemediationRunModel,
        SecurityPostureSnapshotModel,
    )


class SecurityOperationsRepository:
    """Repository handling SQL persistence for Security Operations."""

    def __init__(self, db: Session):
        self.db = db

    # --- Alerts ---
    def save_alert(self, alert_data: Dict[str, Any]) -> SecurityAlertModel:
        alert = SecurityAlertModel(
            tenant_id=alert_data.get("tenant_id", "default_tenant"),
            detection_id=alert_data.get("detection_id"),
            title=alert_data["title"],
            description=alert_data["description"],
            severity=alert_data.get("severity", "medium"),
            status=alert_data.get("status", "DETECTED"),
            anomaly_type=alert_data["anomaly_type"],
            mitre_technique_id=alert_data.get("mitre_technique_id"),
            mitre_tactic=alert_data.get("mitre_tactic"),
            risk_score=alert_data.get("risk_score", 50.0),
            confidence_score=alert_data.get("confidence_score", 0.8),
            affected_actor_id=alert_data.get("affected_actor_id"),
            affected_target_id=alert_data.get("affected_target_id"),
            evidence=alert_data.get("evidence", {}),
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def list_alerts(self, tenant_id: Optional[str] = None, limit: int = 50) -> List[SecurityAlertModel]:
        stmt = select(SecurityAlertModel).order_by(desc(SecurityAlertModel.created_at))
        if tenant_id:
            stmt = stmt.where(SecurityAlertModel.tenant_id == tenant_id)
        return list(self.db.scalars(stmt.limit(limit)).all())

    # --- Incidents ---
    def save_incident(self, incident_data: Dict[str, Any]) -> SecurityIncidentModel:
        incident = SecurityIncidentModel(
            tenant_id=incident_data.get("tenant_id", "default_tenant"),
            title=incident_data["title"],
            description=incident_data["description"],
            severity=incident_data.get("severity", "high"),
            status=incident_data.get("status", "detected"),
            category=incident_data.get("category", "INCIDENT"),
            detection_source=incident_data.get("detection_source", "detection_engine"),
            affected_tenants=incident_data.get("affected_tenants", []),
            affected_users=incident_data.get("affected_users", []),
            affected_services=incident_data.get("affected_services", []),
            affected_resources=incident_data.get("affected_resources", []),
            timeline=incident_data.get("timeline", []),
            evidence=incident_data.get("evidence", {}),
            root_cause=incident_data.get("root_cause"),
            containment_actions=incident_data.get("containment_actions", []),
            remediation_actions=incident_data.get("remediation_actions", []),
            owner=incident_data.get("owner"),
        )
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def list_incidents(self, tenant_id: Optional[str] = None, limit: int = 50) -> List[SecurityIncidentModel]:
        stmt = select(SecurityIncidentModel).order_by(desc(SecurityIncidentModel.created_at))
        if tenant_id:
            stmt = stmt.where(SecurityIncidentModel.tenant_id == tenant_id)
        return list(self.db.scalars(stmt.limit(limit)).all())

    # --- Threat Indicators ---
    def save_threat_indicator(self, ind_data: Dict[str, Any]) -> SecurityThreatIndicatorModel:
        ind = SecurityThreatIndicatorModel(
            tenant_id=ind_data.get("tenant_id", "default_tenant"),
            indicator_type=ind_data["indicator_type"],
            indicator_value=ind_data["indicator_value"],
            threat_category=ind_data["threat_category"],
            severity=ind_data.get("severity", "medium"),
            confidence=ind_data.get("confidence", 0.8),
            source=ind_data.get("source", "INTERNAL"),
            reputation=ind_data.get("reputation", 80),
            observed_at=ind_data.get("observed_at", datetime.now(timezone.utc)),
            metadata_payload=ind_data.get("metadata_payload", {}),
        )
        self.db.add(ind)
        self.db.commit()
        self.db.refresh(ind)
        return ind

    def list_threat_indicators(self, tenant_id: Optional[str] = None, limit: int = 100) -> List[SecurityThreatIndicatorModel]:
        stmt = select(SecurityThreatIndicatorModel).order_by(desc(SecurityThreatIndicatorModel.created_at))
        if tenant_id:
            stmt = stmt.where(SecurityThreatIndicatorModel.tenant_id == tenant_id)
        return list(self.db.scalars(stmt.limit(limit)).all())
