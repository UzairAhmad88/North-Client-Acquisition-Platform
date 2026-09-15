"""Service layer for Risk & Quality Engine orchestration and persistence."""

import uuid
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from agents.core.risk.engine import RiskEngine
from agents.core.risk.models import RiskArtifact
from app.core.exceptions import AppError
from app.models.business import Business
from app.models.lead import Lead
from app.models.outreach import OutreachDraft
from app.models.risk import RiskAssessment
from app.repositories.outreach import OutreachDraftRepository
from app.repositories.risk import RiskRepository


class RiskService:
    """Service layer orchestrating RiskEngine evaluation and database persistence."""

    @staticmethod
    async def evaluate_outreach_draft(
        db: Session, draft_id: uuid.UUID, context_override: Optional[Dict[str, Any]] = None
    ) -> RiskAssessment:
        draft = OutreachDraftRepository.get_by_id(db, draft_id)
        if not draft:
            raise AppError(code="DRAFT_NOT_FOUND", message="Outreach draft not found", status_code=404)

        lead = db.query(Lead).filter(Lead.id == draft.lead_id).first()
        business = db.query(Business).filter(Business.id == draft.business_id).first()

        recipient_email = business.email if business else (lead.notes if lead and "@" in str(lead.notes) else None)

        artifact = RiskArtifact(
            artifact_id=str(draft.id),
            artifact_type="OUTREACH",
            business_id=str(draft.business_id),
            lead_id=str(draft.lead_id),
            channel=draft.channel,
            content=draft.body,
            subject=draft.subject,
            claims=draft.claims or [],
            evidence=draft.evidence or [],
            metadata={
                "recipient_email": recipient_email or "",
                "tone": draft.tone,
                "language": draft.language,
                "objective": draft.objective,
            },
            version=draft.version,
            content_hash=draft.content_hash,
        )

        context = {
            "business_id": str(business.id) if business else None,
            "business_name": business.name if business else "Unknown",
            "business_email": business.email if business else None,
            "lead_id": str(lead.id) if lead else None,
        }
        if context_override:
            context.update(context_override)

        engine = RiskEngine()
        result = await engine.assess(artifact, context)

        # Mark previous assessment as stale
        RiskRepository.mark_stale_by_artifact(db, str(draft.id))

        assessment_data = {
            "artifact_id": str(draft.id),
            "artifact_type": "OUTREACH",
            "business_id": draft.business_id,
            "lead_id": draft.lead_id,
            "decision": result.decision,
            "risk_level": result.risk_level,
            "quality_score": result.quality_score,
            "evidence_coverage": result.evidence_coverage,
            "confidence": result.confidence,
            "engine_version": result.engine_version,
            "policy_version": result.policy_version,
            "content_hash": result.content_hash,
            "artifact_version": draft.version,
            "is_stale": False,
            "status": "COMPLETED",
            "findings": result.findings,
            "quality_checks": result.quality_checks,
        }

        assessment = RiskRepository.create_assessment(db, assessment_data)

        # Update risk_level on OutreachDraft
        OutreachDraftRepository.update_draft(db, draft, {"risk_level": result.risk_level})

        return assessment

    @staticmethod
    async def evaluate_artifact(
        db: Session,
        artifact_type: str,
        artifact_id: uuid.UUID,
        business_id: uuid.UUID,
        content: str,
        recipient_address: Optional[str] = None,
        lead_id: Optional[uuid.UUID] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> RiskAssessment:
        business = db.query(Business).filter(Business.id == business_id).first()
        artifact = RiskArtifact(
            artifact_id=str(artifact_id),
            artifact_type=artifact_type,
            business_id=str(business_id),
            lead_id=str(lead_id) if lead_id else None,
            channel="EMAIL",
            content=content,
            subject=f"{artifact_type} Evaluation",
            claims=[],
            evidence=[],
            metadata={
                "recipient_email": recipient_address or (business.email if business else ""),
                **(metadata or {}),
            },
            version=1,
            content_hash=str(uuid.uuid4())[:8],
        )

        context = {
            "business_id": str(business.id) if business else None,
            "business_name": business.name if business else "Unknown",
            "business_email": business.email if business else None,
        }

        engine = RiskEngine()
        result = await engine.assess(artifact, context)

        RiskRepository.mark_stale_by_artifact(db, str(artifact_id))

        assessment_data = {
            "artifact_id": str(artifact_id),
            "artifact_type": artifact_type,
            "business_id": business_id,
            "lead_id": lead_id,
            "decision": result.decision,
            "risk_level": result.risk_level,
            "quality_score": result.quality_score,
            "evidence_coverage": result.evidence_coverage,
            "confidence": result.confidence,
            "engine_version": result.engine_version,
            "policy_version": result.policy_version,
            "content_hash": result.content_hash,
            "artifact_version": 1,
            "is_stale": False,
            "status": "COMPLETED",
            "findings": result.findings,
            "quality_checks": result.quality_checks,
        }

        return RiskRepository.create_assessment(db, assessment_data)

    @staticmethod
    def get_latest_assessment(db: Session, artifact_id: str) -> Optional[RiskAssessment]:
        return RiskRepository.get_latest_by_artifact(db, artifact_id)

    @staticmethod
    def get_assessment_by_id(db: Session, assessment_id: uuid.UUID) -> Optional[RiskAssessment]:
        return RiskRepository.get_by_id(db, assessment_id)

    @staticmethod
    def record_override(
        db: Session, assessment_id: uuid.UUID, user_id: uuid.UUID, decision: str, reason: str
    ) -> RiskAssessment:
        assessment = RiskRepository.get_by_id(db, assessment_id)
        if not assessment:
            raise AppError(code="ASSESSMENT_NOT_FOUND", message="Risk assessment not found", status_code=404)
        return RiskRepository.record_human_override(db, assessment, user_id, decision, reason)
