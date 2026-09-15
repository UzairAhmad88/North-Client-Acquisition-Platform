"""Query Parser for Global Unified Platform Search."""

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set

from app.search.base import ParsedQuery, SearchEntityType, SearchFilter, SearchType


class QueryParser:
    """Parses raw text queries into structured search specifications."""

    ENTITY_KEYWORDS = {
        "lead": SearchEntityType.LEAD,
        "leads": SearchEntityType.LEAD,
        "business": SearchEntityType.BUSINESS,
        "businesses": SearchEntityType.BUSINESS,
        "contact": SearchEntityType.CONTACT,
        "contacts": SearchEntityType.CONTACT,
        "project": SearchEntityType.PROJECT,
        "projects": SearchEntityType.PROJECT,
        "proposal": SearchEntityType.PROPOSAL,
        "proposals": SearchEntityType.PROPOSAL,
        "contract": SearchEntityType.CONTRACT,
        "contracts": SearchEntityType.CONTRACT,
        "requirement": SearchEntityType.REQUIREMENT,
        "requirements": SearchEntityType.REQUIREMENT,
        "solution": SearchEntityType.SOLUTION,
        "solutions": SearchEntityType.SOLUTION,
        "task": SearchEntityType.TASK,
        "tasks": SearchEntityType.TASK,
        "defect": SearchEntityType.DEFECT,
        "defects": SearchEntityType.DEFECT,
        "document": SearchEntityType.DOCUMENT,
        "documents": SearchEntityType.DOCUMENT,
        "knowledge": SearchEntityType.KNOWLEDGE_ITEM,
        "workflow": SearchEntityType.WORKFLOW,
        "workflows": SearchEntityType.WORKFLOW,
        "conversation": SearchEntityType.CONVERSATION,
        "conversations": SearchEntityType.CONVERSATION,
        "support": SearchEntityType.SUPPORT_REQUEST,
    }

    PRIORITY_KEYWORDS = {
        "high": "HIGH",
        "urgent": "URGENT",
        "critical": "CRITICAL",
        "medium": "MEDIUM",
        "normal": "NORMAL",
        "low": "LOW",
    }

    STATUS_KEYWORDS = {
        "qualified": "QUALIFIED",
        "at risk": "AT_RISK",
        "risk": "AT_RISK",
        "blocked": "BLOCKED",
        "completed": "COMPLETED",
        "in progress": "IN_PROGRESS",
        "open": "OPEN",
        "active": "ACTIVE",
        "pending": "PENDING",
        "draft": "DRAFT",
    }

    @classmethod
    def parse(cls, raw_query: str) -> ParsedQuery:
        """Analyze raw query text and extract entities, filters, and search type."""
        query = (raw_query or "").strip()
        if not query:
            return ParsedQuery(raw_query="", normalized_query="")

        lower_query = query.lower()
        extracted_entities: List[str] = []
        target_entity_types: List[SearchEntityType] = []
        filters: List[SearchFilter] = []
        priority: Optional[str] = None
        status: Optional[str] = None
        date_from: Optional[datetime] = None
        date_to: Optional[datetime] = None

        # 1. Detect Exact Query (quoted string)
        is_exact = query.startswith('"') and query.endswith('"') and len(query) > 2
        search_type = SearchType.EXACT if is_exact else SearchType.KEYWORD

        normalized_text = query.strip('"') if is_exact else re.sub(r"[^\w\s]", "", query).strip()

        # 2. Extract Entity Types
        for keyword, entity_type in cls.ENTITY_KEYWORDS.items():
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, lower_query):
                if entity_type not in target_entity_types:
                    target_entity_types.append(entity_type)

        if not target_entity_types:
            target_entity_types = [SearchEntityType.ALL]

        # 3. Extract Priority
        for keyword, prio_val in cls.PRIORITY_KEYWORDS.items():
            pattern = r"\b" + re.escape(keyword) + r"(\s+priority)?\b"
            if re.search(pattern, lower_query):
                priority = prio_val
                filters.append(SearchFilter(field="priority", operator="eq", value=prio_val))
                break

        # 4. Extract Status
        for keyword, status_val in cls.STATUS_KEYWORDS.items():
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, lower_query):
                status = status_val
                filters.append(SearchFilter(field="status", operator="eq", value=status_val))
                break

        # 5. Extract Date References
        now = datetime.now(timezone.utc)
        if "this month" in lower_query or "current month" in lower_query:
            date_from = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
            filters.append(SearchFilter(field="created_at", operator="gte", value=date_from))
        elif "this week" in lower_query:
            date_from = now - timedelta(days=now.weekday())
            filters.append(SearchFilter(field="created_at", operator="gte", value=date_from))
        elif "today" in lower_query:
            date_from = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
            filters.append(SearchFilter(field="created_at", operator="gte", value=date_from))

        # 6. Detect Natural Language intent markers
        nl_markers = ["find", "show", "what", "which", "list", "where", "how many", "tell me"]
        if any(lower_query.startswith(marker) for marker in nl_markers) and not is_exact:
            search_type = SearchType.NATURAL_LANGUAGE

        return ParsedQuery(
            raw_query=raw_query,
            normalized_query=normalized_text,
            search_type=search_type,
            entity_types=target_entity_types,
            filters=filters,
            date_from=date_from,
            date_to=date_to,
            priority=priority,
            status=status,
            extracted_entities=extracted_entities,
        )
