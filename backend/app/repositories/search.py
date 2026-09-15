"""Repository for search index, history, saved queries, pins, commands, and assistant sessions."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import delete, desc, select, update
from sqlalchemy.orm import Session

from app.models.search import (
    AssistantMessageRecord,
    AssistantSessionRecord,
    CommandAuditEventRecord,
    CommandDefinitionRecord,
    SearchIndexRecord,
    SearchIndexVersionRecord,
    SearchPinRecord,
    SearchQueryAuditRecord,
    SearchSavedQueryRecord,
)


class SearchRepository:
    """Database repository for Phase 38 search, command, and assistant entities."""

    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------------------------------
    # Search Query Audit & History
    # -------------------------------------------------------------------------

    def log_query(
        self,
        tenant_id: str,
        user_id: str,
        query_text: str,
        search_type: str,
        result_count: int,
        latency_ms: float,
    ) -> SearchQueryAuditRecord:
        """Record search audit telemetry."""
        record = SearchQueryAuditRecord(
            tenant_id=tenant_id,
            user_id=user_id,
            query_text=query_text,
            search_type=search_type,
            result_count=result_count,
            latency_ms=latency_ms,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_recent_queries(
        self, tenant_id: str, user_id: str, limit: int = 10
    ) -> List[SearchQueryAuditRecord]:
        """Fetch user's recent search queries."""
        return (
            self.db.query(SearchQueryAuditRecord)
            .filter(
                SearchQueryAuditRecord.tenant_id == tenant_id,
                SearchQueryAuditRecord.user_id == user_id,
            )
            .order_by(SearchQueryAuditRecord.created_at.desc())
            .limit(limit)
            .all()
        )

    # -------------------------------------------------------------------------
    # Saved Searches
    # -------------------------------------------------------------------------

    def create_saved_query(
        self,
        tenant_id: str,
        user_id: str,
        name: str,
        query_text: str,
        filters_json: Optional[Dict[str, Any]] = None,
        is_pinned: bool = False,
    ) -> SearchSavedQueryRecord:
        """Create a user-saved search specification."""
        record = SearchSavedQueryRecord(
            tenant_id=tenant_id,
            user_id=user_id,
            name=name,
            query_text=query_text,
            filters_json=filters_json or {},
            is_pinned=is_pinned,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_saved_queries(
        self, tenant_id: str, user_id: str
    ) -> List[SearchSavedQueryRecord]:
        """Retrieve user's saved searches."""
        return (
            self.db.query(SearchSavedQueryRecord)
            .filter(
                SearchSavedQueryRecord.tenant_id == tenant_id,
                SearchSavedQueryRecord.user_id == user_id,
            )
            .order_by(SearchSavedQueryRecord.created_at.desc())
            .all()
        )

    def delete_saved_query(
        self, tenant_id: str, user_id: str, saved_id: str
    ) -> bool:
        """Remove a saved search."""
        item = (
            self.db.query(SearchSavedQueryRecord)
            .filter(
                SearchSavedQueryRecord.id == saved_id,
                SearchSavedQueryRecord.tenant_id == tenant_id,
                SearchSavedQueryRecord.user_id == user_id,
            )
            .first()
        )
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

    # -------------------------------------------------------------------------
    # Search Pins
    # -------------------------------------------------------------------------

    def create_pin(
        self,
        tenant_id: str,
        user_id: str,
        entity_type: str,
        entity_id: str,
        title: str,
        action_url: str,
    ) -> SearchPinRecord:
        """Pin a record shortcut for quick command center access."""
        pin = SearchPinRecord(
            tenant_id=tenant_id,
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            title=title,
            action_url=action_url,
        )
        self.db.add(pin)
        self.db.commit()
        self.db.refresh(pin)
        return pin

    def list_pins(self, tenant_id: str, user_id: str) -> List[SearchPinRecord]:
        """Retrieve user pins."""
        return (
            self.db.query(SearchPinRecord)
            .filter(
                SearchPinRecord.tenant_id == tenant_id,
                SearchPinRecord.user_id == user_id,
            )
            .order_by(SearchPinRecord.created_at.desc())
            .all()
        )

    def remove_pin(self, tenant_id: str, user_id: str, pin_id: str) -> bool:
        """Remove pin."""
        pin = (
            self.db.query(SearchPinRecord)
            .filter(
                SearchPinRecord.id == pin_id,
                SearchPinRecord.tenant_id == tenant_id,
                SearchPinRecord.user_id == user_id,
            )
            .first()
        )
        if pin:
            self.db.delete(pin)
            self.db.commit()
            return True
        return False

    # -------------------------------------------------------------------------
    # Command Audit Events
    # -------------------------------------------------------------------------

    def log_command_execution(
        self,
        tenant_id: str,
        user_id: str,
        command_id: str,
        category: str,
        risk_level: str,
        status: str,
        parameters_json: Dict[str, Any],
        result_json: Dict[str, Any],
    ) -> CommandAuditEventRecord:
        """Record command execution audit."""
        rec = CommandAuditEventRecord(
            tenant_id=tenant_id,
            user_id=user_id,
            command_id=command_id,
            category=category,
            risk_level=risk_level,
            status=status,
            parameters_json=parameters_json,
            result_json=result_json,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec
