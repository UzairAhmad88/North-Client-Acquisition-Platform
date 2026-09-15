"""Repository layer for persisting and querying Risk & Quality assessments."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.risk import QualityCheck, RiskAssessment, RiskFinding


class RiskRepository:
    """Database repository for risk assessments, findings, and quality checks."""

    @staticmethod
    def create_assessment(db: Session, data: Dict[str, Any]) -> RiskAssessment:
        assessment = RiskAssessment(
            artifact_id=data["artifact_id"],
            artifact_type=data.get("artifact_type", "OUTREACH"),
            business_id=data.get("business_id"),
            lead_id=data.get("lead_id"),
            decision=data.get("decision", "REVIEW"),
            risk_level=data.get("risk_level", "MEDIUM"),
            quality_score=data.get("quality_score", 100.0),
            evidence_coverage=data.get("evidence_coverage", 1.0),
            confidence=data.get("confidence", "HIGH"),
            engine_version=data.get("engine_version", "1.0.0"),
            policy_version=data.get("policy_version", "v1"),
            content_hash=data["content_hash"],
            artifact_version=data.get("artifact_version", 1),
            is_stale=data.get("is_stale", False),
            status=data.get("status", "COMPLETED"),
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)

        for f in data.get("findings", []):
            finding = RiskFinding(
                risk_assessment_id=assessment.id,
                rule_id=f.rule_id if hasattr(f, "rule_id") else f["rule_id"],
                category=f.category if hasattr(f, "category") else f["category"],
                severity=f.severity if hasattr(f, "severity") else f["severity"],
                message=f.message if hasattr(f, "message") else f["message"],
                evidence_reference=f.evidence_reference if hasattr(f, "evidence_reference") else f.get("evidence_reference"),
                remediation=f.remediation if hasattr(f, "remediation") else f.get("remediation"),
            )
            db.add(finding)

        for q in data.get("quality_checks", []):
            check = QualityCheck(
                risk_assessment_id=assessment.id,
                check_type=q.check_type if hasattr(q, "check_type") else q["check_type"],
                status=q.status if hasattr(q, "status") else q["status"],
                score=q.score if hasattr(q, "score") else q["score"],
                details=q.details if hasattr(q, "details") else q.get("details", {}),
            )
            db.add(check)

        db.commit()
        db.refresh(assessment)
        return assessment

    @staticmethod
    def get_latest_by_artifact(db: Session, artifact_id: str) -> Optional[RiskAssessment]:
        return (
            db.query(RiskAssessment)
            .filter(RiskAssessment.artifact_id == artifact_id)
            .order_by(RiskAssessment.created_at.desc())
            .first()
        )

    @staticmethod
    def get_by_id(db: Session, assessment_id: uuid.UUID) -> Optional[RiskAssessment]:
        return db.query(RiskAssessment).filter(RiskAssessment.id == assessment_id).first()

    @staticmethod
    def mark_stale_by_artifact(db: Session, artifact_id: str) -> None:
        db.query(RiskAssessment).filter(RiskAssessment.artifact_id == artifact_id).update({"is_stale": True})
        db.commit()

    @staticmethod
    def record_human_override(
        db: Session, assessment: RiskAssessment, user_id: uuid.UUID, decision: str, reason: str
    ) -> RiskAssessment:
        assessment.human_override_decision = decision.upper()
        assessment.human_override_reason = reason
        assessment.human_override_by_id = user_id
        assessment.human_override_at = datetime.utcnow()
        db.commit()
        db.refresh(assessment)
        return assessment
