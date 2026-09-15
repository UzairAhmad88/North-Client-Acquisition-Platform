"""Audit Sandbox Tools implemented via Phase 14 Tool Abstraction."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.core.tools import AgentTool
from agents.core.validation import AgentValidator
from app.models.audit import BusinessAudit
from app.models.business import Business
from app.models.lead import Lead
from app.repositories.audit import AuditRepository
from app.services.audit.service import AuditService
from integrations.web.security import SecurityValidationError, validate_url_security


class ReadBusinessTool(AgentTool):
    name = "read_business"
    permission = "READ_BUSINESS"
    description = "Reads business profile information."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        biz_id = context.business_id
        if not biz_id and "business_id" in arguments:
            biz_id = uuid.UUID(arguments["business_id"])

        if not biz_id:
            return {"status": "ERROR", "message": "No business_id provided in context or arguments."}

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
    description = "Reads lead opportunity context."

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
                "business_id": str(lead.business_id),
                "status": lead.status,
                "source": lead.source,
            },
        }


class ReadResearchTool(AgentTool):
    name = "read_research"
    permission = "READ_RESEARCH"
    description = "Reads existing research records for target business."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        records = context.research_data.get("records", [])
        return {"status": "SUCCESS", "records_count": len(records), "records": records}


class ReadExistingAuditTool(AgentTool):
    name = "read_existing_audit"
    permission = "READ_AUDIT"
    description = "Reads latest existing audit record for target business."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        biz_id = context.business_id
        if not biz_id:
            return {"status": "NOT_FOUND", "message": "No business_id provided."}

        audit = AuditRepository.get_latest_audit_by_business(self.db, biz_id)
        if not audit:
            return {"status": "NOT_FOUND", "message": "No existing audit found for this business."}

        return {
            "status": "SUCCESS",
            "audit": {
                "id": str(audit.id),
                "target_url": audit.target_url,
                "overall_health": audit.overall_health,
                "summary": audit.summary,
                "findings_count": len(audit.findings or []),
                "completed_at": audit.completed_at.isoformat() if audit.completed_at else None,
            },
        }


class ValidateAuditTargetTool(AgentTool):
    name = "validate_audit_target"
    permission = "READ_AUDIT"
    description = "Validates audit target URL using SSRF security guard."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        url = arguments.get("url", "")
        if not url:
            return {"status": "INVALID", "message": "No target URL provided."}

        try:
            safe_url = validate_url_security(url)
            return {"status": "VALID", "target_url": safe_url}
        except SecurityValidationError as e:
            return {"status": "BLOCKED", "message": str(e)}


class FetchAuditPageTool(AgentTool):
    name = "fetch_audit_page"
    permission = "FETCH_WEB"
    description = "Fetches a public web page for audit inspection (Read-Only GET)."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        url = arguments.get("url", "")
        if not url:
            return {"status": "ERROR", "message": "No URL provided."}

        try:
            safe_url = validate_url_security(url)
        except SecurityValidationError as e:
            return {"status": "BLOCKED", "message": f"URL fetch blocked by SSRF guard: {str(e)}"}

        content = f"Page document from {safe_url}. HTML tags, meta description, contact links."
        sanitized_content = AgentValidator.sanitize_untrusted_input(content)

        return {
            "status": "SUCCESS",
            "url": safe_url,
            "content": sanitized_content,
            "title": f"Document - {safe_url}",
        }


class RunWebsiteAuditTool(AgentTool):
    name = "run_website_audit"
    permission = "RUN_AUDIT"
    description = "Runs deterministic Phase 11 website audit runner for target URL."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        target_url = arguments.get("target_url")
        biz_id = context.business_id

        biz = self.db.query(Business).filter(Business.id == biz_id).first() if biz_id else None
        runner = AuditService.get_runner("MOCK")
        result = await runner.run_audit(biz, target_url=target_url, max_pages=10)

        findings_list = [f.to_dict() for f in result.findings]
        return {
            "status": "SUCCESS",
            "target_url": result.target_url,
            "overall_health": result.overall_health,
            "summary": result.summary,
            "findings": findings_list,
            "metrics": result.metrics,
            "warnings": result.warnings,
            "errors": result.errors,
        }


class CreateAuditRecordTool(AgentTool):
    name = "create_audit_record"
    permission = "CREATE_AUDIT_RECORD"
    description = "Persists verified BusinessAudit record."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        biz_id = context.business_id
        if not biz_id:
            return {"status": "ERROR", "message": "No business_id in context."}

        audit_data = {
            "business_id": biz_id,
            "target_url": arguments.get("target_url"),
            "audit_version": "1.0",
            "status": arguments.get("status", "AVAILABLE"),
            "overall_health": arguments.get("overall_health", "LIMITED_DATA"),
            "summary": arguments.get("summary", ""),
            "categories": arguments.get("categories", {}),
            "findings": arguments.get("findings", []),
            "metrics": arguments.get("metrics", {}),
            "warnings": arguments.get("warnings", []),
            "errors": arguments.get("errors", []),
        }

        audit = AuditRepository.create_audit(self.db, audit_data)
        return {"status": "SUCCESS", "audit_id": str(audit.id)}
