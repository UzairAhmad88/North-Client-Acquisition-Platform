import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Index, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class ResearchJob(BaseModel):
    __tablename__ = "research_jobs"

    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="PENDING", index=True)
    requested_sections: Mapped[Any] = mapped_column(JSON, nullable=False, default=list)
    source_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_validated: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    records_rejected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_research_jobs_business_status", "business_id", "status"),
        Index("ix_research_jobs_created_at", "created_at"),
    )


class ResearchRecord(BaseModel):
    __tablename__ = "research_records"

    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    research_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("research_jobs.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, index=True)
    source_trust: Mapped[str] = mapped_column(
        String(50), nullable=False, default="MEDIUM_TRUST", index=True
    )
    research_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="GENERAL", index=True
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    raw_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    normalized_value: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[str] = mapped_column(
        String(50), nullable=False, default="MEDIUM", index=True
    )
    evidence_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="VALIDATED", index=True)
    meta_info: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        Index("ix_research_records_biz_field", "business_id", "field_name"),
        Index("ix_research_records_biz_confidence", "business_id", "confidence"),
    )


class ResearchConflict(BaseModel):
    __tablename__ = "research_conflicts"

    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    competing_values: Mapped[Any] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="CONFLICT", index=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (Index("ix_research_conflicts_biz_field", "business_id", "field_name"),)
