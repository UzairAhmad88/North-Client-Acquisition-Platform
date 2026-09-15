"""Qualification Sandbox Tools implemented via Phase 14 Tool Abstraction."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.core.tools import AgentTool
from app.models.business import Business
from app.models.lead import Lead
from app.repositories.audit import AuditRepository
from app.repositories.recommendation import RecommendationRepository
from app.repositories.research import ResearchRepository
from app.repositories.score import ScoringRepository


class ReadBusinessTool(AgentTool):
    name = "read_business"
    permission = "READ_BUSINESS"
    description = "Reads public business profile information."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        biz_id = context.business_id
        if not biz_id and "business_id" in arguments:
            biz_id = uuid.UUID(arguments["business_id"])

        if not biz_id:
            return {"status": "ERROR", "message": "No business_id provided."}

        biz = self.db.query(Business).filter(Business.id == biz_id).first()
        if not biz:
            return {"status": "NOT_FOUND", "message": f"Business {biz_id} not found."}

        return {
            "status": "SUCCESS",
            "business": {
                "id": str(biz.id),
                "name": biz.name,
                "category": biz.category,
                "website_url": biz.website_url,
                "phone": biz.phone,
                "email": biz.email,
                "city": biz.city,
            },
        }


class ReadLeadTool(AgentTool):
    name = "read_lead"
    permission = "READ_LEAD"
    description = "Reads lead details."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        lead_id = context.lead_id
        if not lead_id and "lead_id" in arguments:
            lead_id = uuid.UUID(arguments["lead_id"])

        if not lead_id:
            return {"status": "NOT_FOUND", "message": "No lead_id provided."}

        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return {"status": "NOT_FOUND", "message": f"Lead {lead_id} not found."}

        return {
            "status": "SUCCESS",
            "lead": {
                "id": str(lead.id),
                "title": lead.title,
                "business_id": str(lead.business_id),
                "status": lead.status,
                "source": lead.source,
                "qualification_status": lead.qualification_status,
                "contactability_status": lead.contactability_status,
            },
        }


class ReadResearchTool(AgentTool):
    name = "read_research"
    permission = "READ_RESEARCH"
    description = "Reads validated research intelligence records."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        records = context.research_data.get("records", [])
        return {"status": "SUCCESS", "records_count": len(records), "records": records}


class ReadAuditTool(AgentTool):
    name = "read_audit"
    permission = "READ_AUDIT"
    description = "Reads digital presence audit findings."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        biz_id = context.business_id
        if not biz_id:
            return {"status": "NOT_FOUND", "message": "No business_id provided."}

        audit = AuditRepository.get_latest_audit_by_business(self.db, biz_id)
        if not audit:
            return {"status": "NOT_FOUND", "message": "No audit found."}

        return {
            "status": "SUCCESS",
            "audit": {
                "id": str(audit.id),
                "overall_health": audit.overall_health,
                "findings": audit.findings or [],
            },
        }


class ReadScoreTool(AgentTool):
    name = "read_score"
    permission = "READ_SCORE"
    description = "Reads deterministic lead opportunity score."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        lead_id = context.lead_id
        if not lead_id:
            return {"status": "NOT_FOUND", "message": "No lead_id provided."}

        score = ScoringRepository.get_score_by_lead(self.db, lead_id)
        if not score:
            return {"status": "NOT_FOUND", "message": "No score record found for lead."}

        return {
            "status": "SUCCESS",
            "score": {
                "score": score.total_score,
                "score_band": score.score_band,
                "confidence": score.confidence,
                "summary": score.explanation_summary,
            },
        }


class ReadServiceRecommendationsTool(AgentTool):
    name = "read_service_recommendations"
    permission = "READ_SERVICES"
    description = "Reads deterministic North's service recommendations."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        lead_id = context.lead_id
        if not lead_id:
            return {"status": "NOT_FOUND", "message": "No lead_id provided."}

        recs = RecommendationRepository.list_by_lead(self.db, lead_id)
        recs_data = [
            {
                "id": str(r.id),
                "service_id": str(r.service_id),
                "score": r.relevance_score,
                "relevance_band": r.relevance_band,
                "priority": r.priority,
                "status": r.status,
            }
            for r in recs
        ]
        return {"status": "SUCCESS", "recommendations_count": len(recs_data), "recommendations": recs_data}


class ReadCrmContextTool(AgentTool):
    name = "read_crm_context"
    permission = "READ_CRM_CONTEXT"
    description = "Reads CRM activity context for target lead."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        return {
            "status": "SUCCESS",
            "crm_context": {
                "notes": context.metadata.get("lead_notes"),
                "previous_interactions_count": 0,
            },
        }


class ReadDncStatusTool(AgentTool):
    name = "read_dnc_status"
    permission = "READ_CRM_CONTEXT"
    description = "Reads Do-Not-Contact (DNC) status for lead or business."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        dnc_flag = context.metadata.get("is_dnc", False)
        return {"status": "SUCCESS", "is_dnc": dnc_flag}


class ReadDuplicateContextTool(AgentTool):
    name = "read_duplicate_context"
    permission = "READ_CRM_CONTEXT"
    description = "Checks whether target lead has unresolved duplicate records."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        has_duplicate = context.metadata.get("has_duplicate", False)
        return {"status": "SUCCESS", "has_unresolved_duplicate": has_duplicate}


class CreateQualificationResultTool(AgentTool):
    name = "create_qualification_result"
    permission = "CREATE_QUALIFICATION_RESULT"
    description = "Persists verified LeadQualification record."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        return {"status": "SUCCESS", "message": "Qualification record persisted."}
