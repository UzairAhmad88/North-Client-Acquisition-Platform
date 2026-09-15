"""Service operations for Personalization Agent orchestration and Outreach Draft management."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.personalization import personalization_agent
from app.core.exceptions import AppError
from app.models.business import Business
from app.models.lead import Lead
from app.models.outreach import OutreachDraft
from app.models.qualification import LeadQualification
from app.models.recommendation import ServiceRecommendation
from app.models.research import ResearchRecord
from app.models.score import LeadScore
from app.repositories.outreach import OutreachDraftRepository


class OutreachDraftService:
    """Service layer orchestrating Personalization Agent and Outreach Draft persistence."""

    @staticmethod
    def get_latest_draft(db: Session, lead_id: uuid.UUID) -> Optional[OutreachDraft]:
        return OutreachDraftRepository.get_latest_by_lead(db, lead_id)

    @staticmethod
    def get_draft_by_id(db: Session, draft_id: uuid.UUID) -> Optional[OutreachDraft]:
        return OutreachDraftRepository.get_by_id(db, draft_id)

    @staticmethod
    def list_drafts(
        db: Session, limit: int = 20, offset: int = 0, approval_status: Optional[str] = None
    ) -> List[OutreachDraft]:
        return OutreachDraftRepository.list_all_drafts(
            db, limit=limit, offset=offset, approval_status=approval_status
        )

    @staticmethod
    async def run_personalization(
        db: Session,
        lead_id: uuid.UUID,
        channel: str = "EMAIL",
        tone: str = "PROFESSIONAL",
        language: str = "en",
        personalization_depth: str = "STANDARD",
        objective: str = "INTRODUCE_SERVICE",
        user_id: Optional[uuid.UUID] = None,
    ) -> OutreachDraft:
        # 1. Fetch Lead & Business
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise AppError(code="LEAD_NOT_FOUND", message="Lead not found", status_code=404)

        business = db.query(Business).filter(Business.id == lead.business_id).first()
        if not business:
            raise AppError(code="BUSINESS_NOT_FOUND", message="Associated Business not found", status_code=404)

        # 2. Fetch Research, Audit, Score, Recommendations, Qualification
        res_records = db.query(ResearchRecord).filter(ResearchRecord.business_id == business.id).all()
        research_data = {"records": [{"fact_summary": r.fact_summary, "confidence": r.confidence} for r in res_records]}

        audit_data: Dict[str, Any] = {"findings": []}
        if hasattr(business, "audits") and business.audits:
            latest_audit = business.audits[-1]
            audit_data["findings"] = [{"code": f.code, "title": f.title, "severity": f.severity, "description": f.description} for f in latest_audit.findings]

        score_rec = db.query(LeadScore).filter(LeadScore.lead_id == lead.id).order_by(LeadScore.created_at.desc()).first()
        score_data = {"score": score_rec.total_score, "band": score_rec.band} if score_rec else {}

        recs = db.query(ServiceRecommendation).filter(ServiceRecommendation.lead_id == lead.id).all()
        recommendations_data = [{"service_title": r.service_title, "relevance_band": r.relevance_band, "reason": r.reason} for r in recs]

        qual_rec = db.query(LeadQualification).filter(LeadQualification.lead_id == lead.id).order_by(LeadQualification.created_at.desc()).first()
        qualification_data = {
            "decision": qual_rec.human_override_decision or qual_rec.decision if qual_rec else "UNKNOWN",
            "outreach_readiness": qual_rec.outreach_readiness if qual_rec else "UNKNOWN",
        }

        # Check existing versions count for versioning
        existing_latest = OutreachDraftRepository.get_latest_by_lead(db, lead.id)
        next_version = (existing_latest.version + 1) if existing_latest else 1

        # 3. Build AgentContext
        context = AgentContext(
            workflow_id=f"wf-pers-{lead.id.hex[:8]}",
            task_id=f"task-pers-{lead.id.hex[:8]}",
            agent_run_id=str(uuid.uuid4()),
            lead_id=lead.id,
            business_id=business.id,
            business_profile={
                "name": business.name,
                "website_url": business.website_url,
                "phone": business.phone,
                "email": business.email,
            },
            lead_profile={
                "title": lead.title,
                "contact_name": lead.title,
                "email": business.email,
                "phone": business.phone,
            },
            research_data=research_data,
            audit_data=audit_data,
            score_data=score_data,
            service_recommendations=recommendations_data,
            metadata={
                "qualification_data": qualification_data,
                "is_dnc": False,
                "channel": channel,
                "tone": tone,
                "language": language,
                "personalization_depth": personalization_depth,
                "objective": objective,
            },
        )

        # 4. Execute PersonalizationAgent
        agent_result = await personalization_agent.run(context)
        res_payload = agent_result.result or {}

        draft_info = res_payload.get("draft", {})
        profile_info = res_payload.get("personalization_profile", {})

        # 5. Persist OutreachDraft
        draft_record_data = {
            "lead_id": lead.id,
            "business_id": business.id,
            "user_id": user_id,
            "channel": channel,
            "tone": tone,
            "language": language,
            "personalization_depth": personalization_depth,
            "objective": objective,
            "subject": draft_info.get("subject"),
            "body": draft_info.get("body", ""),
            "primary_angle": res_payload.get("primary_angle", {}),
            "personalization_profile": profile_info,
            "claims": draft_info.get("claims", []),
            "evidence": res_payload.get("evidence", []),
            "risk_level": draft_info.get("risk_level", "LOW"),
            "outreach_readiness": res_payload.get("outreach_readiness", "READY"),
            "approval_status": "PENDING_APPROVAL",
            "version": next_version,
            "content_hash": draft_info.get("content_hash"),
        }

        return OutreachDraftRepository.create_draft(db, draft_record_data)

    @staticmethod
    def update_draft(db: Session, draft_id: uuid.UUID, updates: Dict[str, Any]) -> OutreachDraft:
        draft = OutreachDraftRepository.get_by_id(db, draft_id)
        if not draft:
            raise AppError(code="DRAFT_NOT_FOUND", message="Outreach draft not found", status_code=404)
        return OutreachDraftRepository.update_draft(db, draft, updates)
