"""
Phase 65: Data Classification Service
Classifies datasets, tables, columns, and unstructured assets into sensitivity tiers
(PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, HIGHLY_RESTRICTED).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import (
    DataClassificationModel,
    DataSensitivityRuleModel
)


class DataClassificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_classification(
        self,
        tenant_id: str,
        asset_id: str,
        classification_level: str,
        detected_categories: Optional[List[str]] = None,
        confidence_score: float = 0.95,
        policy_tags: Optional[List[str]] = None,
        steward_verified: bool = False,
        verified_by: Optional[str] = None
    ) -> DataClassificationModel:
        record = DataClassificationModel(
            tenant_id=tenant_id,
            asset_id=asset_id,
            classification_level=classification_level,
            detected_categories=detected_categories or [],
            confidence_score=confidence_score,
            policy_tags=policy_tags or [],
            steward_verified=steward_verified,
            verified_by=verified_by,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_classifications(self, tenant_id: str, level: Optional[str] = None) -> List[DataClassificationModel]:
        query = self.db.query(DataClassificationModel).filter(DataClassificationModel.tenant_id == tenant_id)
        if level:
            query = query.filter(DataClassificationModel.classification_level == level)
        return query.order_by(DataClassificationModel.created_at.desc()).all()

    def create_sensitivity_rule(
        self,
        tenant_id: str,
        rule_name: str,
        pattern_regex: str,
        target_classification: str,
        is_active: bool = True
    ) -> DataSensitivityRuleModel:
        rule = DataSensitivityRuleModel(
            tenant_id=tenant_id,
            rule_name=rule_name,
            pattern_regex=pattern_regex,
            target_classification=target_classification,
            is_active=is_active,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def list_sensitivity_rules(self, tenant_id: str) -> List[DataSensitivityRuleModel]:
        return self.db.query(DataSensitivityRuleModel).filter(
            DataSensitivityRuleModel.tenant_id == tenant_id
        ).all()
