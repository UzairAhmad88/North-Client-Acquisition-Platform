"""ORM models for Phase 38: Unified Search, Global Command Center & Platform Assistant."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


# =============================================================================
# 1. Search Index & Versioning
# =============================================================================

class SearchIndexRecord(BaseModel):
    """Indexed searchable document record."""

    __tablename__ = "search_index_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    search_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    priority: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    action_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class SearchIndexVersionRecord(BaseModel):
    """Index build iteration and synchronization telemetry."""

    __tablename__ = "search_index_version_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    total_documents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)


# =============================================================================
# 2. Search History, Saved Searches & Pins
# =============================================================================

class SearchQueryAuditRecord(BaseModel):
    """Audit log of user search queries for observability and analytics."""

    __tablename__ = "search_query_audit_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    query_text: Mapped[str] = mapped_column(String(500), nullable=False)
    search_type: Mapped[str] = mapped_column(String(50), default="KEYWORD", nullable=False)
    result_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)


class SearchSavedQueryRecord(BaseModel):
    """User-saved search queries and filter views."""

    __tablename__ = "search_saved_query_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    query_text: Mapped[str] = mapped_column(String(500), nullable=False)
    filters_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class SearchPinRecord(BaseModel):
    """User-pinned entity shortcuts displayed in command center."""

    __tablename__ = "search_pin_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    action_url: Mapped[str] = mapped_column(String(255), nullable=False)


# =============================================================================
# 3. Command Palette Records
# =============================================================================

class CommandDefinitionRecord(BaseModel):
    """Registered command capabilities and safety policies."""

    __tablename__ = "command_definition_records"

    command_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="NAVIGATION", nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)
    required_permission: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    requires_confirmation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    parameters_schema: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class CommandAuditEventRecord(BaseModel):
    """Audit log of all command parse, validation, and execution events."""

    __tablename__ = "command_audit_event_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    command_id: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="EXECUTED", nullable=False)
    parameters_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    result_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


# =============================================================================
# 4. Platform Assistant Records
# =============================================================================

class AssistantSessionRecord(BaseModel):
    """Assistant conversational session envelope."""

    __tablename__ = "assistant_session_records"

    tenant_id: Mapped[str] = mapped_column(String(100), default="default_tenant", nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), default="New Conversation", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    messages: Mapped[List["AssistantMessageRecord"]] = relationship(
        "AssistantMessageRecord", back_populates="session", cascade="all, delete-orphan"
    )


class AssistantMessageRecord(BaseModel):
    """Message exchange in an assistant session."""

    __tablename__ = "assistant_message_records"

    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("assistant_session_records.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(50), default="USER", nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    answer_type: Mapped[str] = mapped_column(String(50), default="FACT", nullable=False)
    ai_trace_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sources_json: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    session: Mapped["AssistantSessionRecord"] = relationship("AssistantSessionRecord", back_populates="messages")
