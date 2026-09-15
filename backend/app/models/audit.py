import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Index, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AuditJob(BaseModel):
    __tablename__ = "audit_jobs"

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
    target_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="PENDING", index=True)
    requested_categories: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    pages_requested: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    pages_analyzed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    findings_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    warnings_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    errors_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_audit_jobs_business_status", "business_id", "status"),
        Index("ix_audit_jobs_created_at", "created_at"),
    )


class BusinessAudit(BaseModel):
    __tablename__ = "business_audits"

    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    research_record_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("research_records.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    audit_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("audit_jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    target_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    audit_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="AVAILABLE", index=True)
    overall_health: Mapped[str] = mapped_column(
        String(50), nullable=False, default="LIMITED_DATA", index=True
    )
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    categories: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    findings: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    metrics: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    warnings: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    errors: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_business_audits_biz_created", "business_id", "created_at"),
    )


class AuditFinding(BaseModel):
    __tablename__ = "audit_findings"

    audit_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("business_audits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="INFO", index=True)
    confidence: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIUM", index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=False)
    evidence: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    affected_page: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        Index("ix_audit_findings_audit_cat", "audit_id", "category"),
    )



class AuditPage(BaseModel):
    __tablename__ = "audit_pages"

    audit_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("business_audits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, nullable=False, default=200)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_homepage: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_contact_form: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (Index("ix_audit_pages_audit_url", "audit_id", "url"),)
