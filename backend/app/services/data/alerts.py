"""
Phase 65: Data Alerts & Anomaly Notification Service
Handles alert definitions, trigger evaluation, and active incident generation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import DataAlertModel, DataAnomalyModel


class DataAlertService:
    def __init__(self, db: Session):
        self.db = db

    def create_alert(
        self,
        tenant_id: str,
        name: str,
        alert_type: str,  # THRESHOLD, ANOMALY, FRESHNESS, QUALITY, PIPELINE
        target_resource: str,
        condition_expression: Dict[str, Any],
        severity: str = "HIGH",
        recipients: Optional[List[str]] = None
    ) -> DataAlertModel:
        alert = DataAlertModel(
            tenant_id=tenant_id,
            name=name,
            alert_type=alert_type,
            target_resource=target_resource,
            condition_expression=condition_expression,
            severity=severity,
            recipients=recipients or [],
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def record_anomaly(
        self,
        tenant_id: str,
        target_resource: str,
        metric_name: str,
        expected_value: float,
        actual_value: float,
        deviation_score: float,
        details: Optional[Dict[str, Any]] = None
    ) -> DataAnomalyModel:
        anomaly = DataAnomalyModel(
            tenant_id=tenant_id,
            target_resource=target_resource,
            metric_name=metric_name,
            expected_value=expected_value,
            actual_value=actual_value,
            deviation_score=deviation_score,
            details=details or {},
            status="OPEN",
            detected_at=datetime.now(timezone.utc)
        )
        self.db.add(anomaly)
        self.db.commit()
        self.db.refresh(anomaly)
        return anomaly

    def list_alerts(self, tenant_id: str) -> List[DataAlertModel]:
        return self.db.query(DataAlertModel).filter(
            DataAlertModel.tenant_id == tenant_id
        ).all()

    def list_anomalies(self, tenant_id: str, status: Optional[str] = None) -> List[DataAnomalyModel]:
        query = self.db.query(DataAnomalyModel).filter(DataAnomalyModel.tenant_id == tenant_id)
        if status:
            query = query.filter(DataAnomalyModel.status == status)
        return query.order_by(DataAnomalyModel.detected_at.desc()).all()
