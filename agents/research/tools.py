"""Research Sandbox Tools implemented via Phase 14 Tool Abstraction."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.core.tools import AgentTool
from agents.core.validation import AgentValidator
from app.models.business import Business
from app.models.lead import Lead
from app.models.research import ResearchConflict, ResearchRecord
from app.services.research.mock_provider import MockResearchProvider
from app.services.research.service import ResearchService
from integrations.web.security import SecurityValidationError, validate_url_security


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
                "industry": biz.industry,
                "city": biz.city,
                "state": biz.state,
                "country": biz.country,
                "website_url": biz.website_url,
                "phone": biz.phone,
                "email": biz.email,
                "status": biz.status,
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
            return {"status": "ERROR", "message": "No lead_id provided."}

        lead = self.db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return {"status": "NOT_FOUND", "message": f"Lead {lead_id} not found."}

        return {
            "status": "SUCCESS",
            "lead": {
                "id": str(lead.id),
                "title": lead.title,
                "status": lead.status,
                "priority": lead.priority,
                "notes": lead.notes,
            },
        }


class ReadExistingResearchTool(AgentTool):
    name = "read_existing_research"
    permission = "READ_RESEARCH"
    description = "Reads existing research records and checks freshness policy."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        biz_id = context.business_id
        if not biz_id and "business_id" in arguments:
            biz_id = uuid.UUID(arguments["business_id"])

        if not biz_id:
            return {"status": "ERROR", "message": "No business_id provided."}

        records = self.db.query(ResearchRecord).filter(ResearchRecord.business_id == biz_id).all()
        conflicts = self.db.query(ResearchConflict).filter(ResearchConflict.business_id == biz_id).all()

        formatted_records = [
            {
                "id": str(r.id),
                "field_name": r.field_name,
                "normalized_value": r.normalized_value,
                "confidence": r.confidence,
                "source_url": r.source_url,
                "source_trust": r.source_trust,
                "observed_at": r.observed_at.isoformat() if r.observed_at else None,
            }
            for r in records
        ]

        formatted_conflicts = [
            {
                "field_name": c.field_name,
                "competing_values": c.competing_values,
                "resolution_notes": c.resolution_notes,
            }
            for c in conflicts
        ]

        return {
            "status": "SUCCESS",
            "records_count": len(formatted_records),
            "records": formatted_records,
            "conflicts": formatted_conflicts,
        }


class SearchWebTool(AgentTool):
    name = "search_web"
    permission = "SEARCH_WEB"
    description = "Performs bounded web search for business information."

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        query = arguments.get("query", "")
        if not query:
            biz_name = context.business_profile.get("name", "Business")
            query = f"{biz_name} official website contact services"

        # Execute mock or real web search provider
        provider = MockResearchProvider()
        results = provider.search(query, max_results=5)

        return {
            "status": "SUCCESS",
            "query": query,
            "results_count": len(results),
            "results": results,
        }


class FetchWebTool(AgentTool):
    name = "fetch_web"
    permission = "FETCH_WEB"
    description = "Fetches public webpage text with SSRF protection and prompt injection isolation."

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        url = arguments.get("url", "")
        if not url:
            return {"status": "ERROR", "message": "No URL provided for web fetch."}

        # SSRF Security check
        try:
            safe_url = validate_url_security(url)
        except SecurityValidationError as e:
            return {
                "status": "BLOCKED",
                "message": f"URL fetch blocked by SSRF security guard: {str(e)}",
            }

        # Execute fetch via provider simulation or mock page content
        fetched_content = f"Official page content retrieved from {url}. Services and identity details."
        fetched_title = f"Web Document - {url}"

        # Wrap text in untrusted data tags to defend against prompt injection
        sanitized_content = AgentValidator.sanitize_untrusted_input(fetched_content)

        return {
            "status": "SUCCESS",
            "url": url,
            "content": sanitized_content,
            "title": fetched_title,
        }


class CreateResearchRecordTool(AgentTool):
    name = "create_research_record"
    permission = "CREATE_RESEARCH_RECORD"
    description = "Persists structured research finding into database."

    def __init__(self, db: Session) -> None:
        self.db = db

    async def run_tool(self, arguments: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        biz_id = context.business_id
        if not biz_id and "business_id" in arguments:
            biz_id = uuid.UUID(arguments["business_id"])

        if not biz_id:
            return {"status": "ERROR", "message": "No business_id provided."}

        field_name = arguments.get("field_name", "general")
        value = str(arguments.get("value", ""))
        source_url = arguments.get("source_url")
        source_trust = arguments.get("source_trust", "OFFICIAL")
        confidence = arguments.get("confidence", "HIGH")
        evidence = arguments.get("evidence", "")

        record = ResearchService.add_research_record(
            self.db,
            business_id=biz_id,
            field_name=field_name,
            raw_value=value,
            normalized_value=value,
            source_url=source_url,
            source_trust=source_trust,
            confidence=confidence,
            evidence_text=evidence,
        )

        return {
            "status": "SUCCESS",
            "record_id": str(record.id),
            "field_name": record.field_name,
            "normalized_value": record.normalized_value,
        }
