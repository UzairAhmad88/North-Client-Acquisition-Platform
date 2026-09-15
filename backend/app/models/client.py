"""ORM models for Client Collaboration, Communication & Delivery Workspace."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ClientAccount(BaseModel):
    """Client organization entity linked to business."""

    __tablename__ = "client_accounts"

    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="ACTIVE", nullable=False, index=True
    )  # ACTIVE, SUSPENDED, ARCHIVED

    members = relationship("ClientMember", back_populates="account", cascade="all, delete-orphan")
    project_accesses = relationship("ClientProjectAccess", back_populates="account", cascade="all, delete-orphan")


class ClientMember(BaseModel):
    """Client user membership in a ClientAccount with RBAC role."""

    __tablename__ = "client_members"

    client_account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("client_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(64), default="CLIENT_MEMBER", nullable=False
    )  # CLIENT_OWNER, CLIENT_ADMIN, CLIENT_MEMBER, CLIENT_REVIEWER, CLIENT_VIEWER
    status: Mapped[str] = mapped_column(
        String(32), default="ACTIVE", nullable=False
    )  # ACTIVE, INVITED, SUSPENDED

    invited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    joined_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    account = relationship("ClientAccount", back_populates="members")
    user = relationship("User")


class ClientInvitation(BaseModel):
    """Secure single-use client portal invitation token."""

    __tablename__ = "client_invitations"

    client_account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("client_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(64), default="CLIENT_MEMBER", nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )


class ClientProjectAccess(BaseModel):
    """Granular project access permission grant for client organization."""

    __tablename__ = "client_project_access"

    client_account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("client_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    access_level: Mapped[str] = mapped_column(
        String(32), default="COLLABORATE", nullable=False
    )  # VIEW, COLLABORATE, REVIEW, APPROVE
    status: Mapped[str] = mapped_column(
        String(32), default="ACTIVE", nullable=False
    )  # ACTIVE, SUSPENDED

    account = relationship("ClientAccount", back_populates="project_accesses")
    project = relationship("Project")


class DiscussionThread(BaseModel):
    """Context-bound discussion thread linked to a project or deliverable."""

    __tablename__ = "discussion_threads"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    deliverable_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_deliverables.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    type: Mapped[str] = mapped_column(
        String(32), default="GENERAL", nullable=False, index=True
    )  # GENERAL, DELIVERABLE, QUESTION, FEEDBACK, REQUEST, ANNOUNCEMENT
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="OPEN", nullable=False, index=True
    )  # OPEN, RESOLVED, CLOSED
    visibility: Mapped[str] = mapped_column(
        String(32), default="CLIENT_VISIBLE", nullable=False, index=True
    )  # INTERNAL_ONLY, CLIENT_VISIBLE

    created_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    messages = relationship("ThreadMessage", back_populates="thread", cascade="all, delete-orphan")


class ThreadMessage(BaseModel):
    """Individual message within a discussion thread."""

    __tablename__ = "thread_messages"

    thread_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("discussion_threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender_type: Mapped[str] = mapped_column(
        String(32), default="CLIENT", nullable=False
    )  # INTERNAL, CLIENT, SYSTEM
    content: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[str] = mapped_column(
        String(32), default="CLIENT_VISIBLE", nullable=False, index=True
    )  # INTERNAL_ONLY, CLIENT_VISIBLE
    attachments: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)

    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    thread = relationship("DiscussionThread", back_populates="messages")
    sender = relationship("User")


class ClientQuestion(BaseModel):
    """Structured question asked to or by the client."""

    __tablename__ = "client_questions"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="OPEN", nullable=False, index=True
    )  # OPEN, WAITING_FOR_CLIENT, ANSWERED, RESOLVED, CANCELLED
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    answered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    answered_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    project = relationship("Project")


class ClientRequest(BaseModel):
    """Client request intake for changes or additions."""

    __tablename__ = "client_requests"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_account_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("client_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    classification: Mapped[str] = mapped_column(
        String(64), default="NEEDS_REVIEW", nullable=False, index=True
    )  # IN_SCOPE, POTENTIAL_SCOPE_CHANGE, SUPPORT, BUG, CONTENT, NEEDS_REVIEW
    status: Mapped[str] = mapped_column(
        String(32), default="SUBMITTED", nullable=False, index=True
    )  # SUBMITTED, UNDER_REVIEW, APPROVED_SCOPE, REJECTED, CONVERTED_TO_CHANGE_ORDER

    submitted_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    project = relationship("Project")


class ClientFeedback(BaseModel):
    """Categorized feedback provided by client on deliverables or project."""

    __tablename__ = "client_feedback"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    deliverable_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_deliverables.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    category: Mapped[str] = mapped_column(
        String(32), default="FUNCTIONALITY", nullable=False
    )  # DESIGN, FUNCTIONALITY, CONTENT, PERFORMANCE, BUG, USABILITY, OTHER
    content: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1 to 5
    status: Mapped[str] = mapped_column(
        String(32), default="SUBMITTED", nullable=False
    )  # SUBMITTED, ACKNOWLEDGED, RESOLVED

    submitted_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    project = relationship("Project")


class DeliverableReview(BaseModel):
    """Versioned client review record for a project deliverable."""

    __tablename__ = "deliverable_reviews"

    deliverable_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_deliverables.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="PENDING_REVIEW", nullable=False, index=True
    )  # PENDING_REVIEW, IN_REVIEW, CHANGES_REQUESTED, APPROVED, REJECTED
    feedback_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reviewed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    deliverable = relationship("ProjectDeliverable")


class DeliverableApproval(BaseModel):
    """Explicit formal client approval record with canonical SHA-256 content hash."""

    __tablename__ = "deliverable_approvals"

    deliverable_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_deliverables.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    approval_statement: Mapped[str] = mapped_column(Text, nullable=False)
    signer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    signer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(64), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    deliverable = relationship("ProjectDeliverable")


class ProjectFile(BaseModel):
    """Secure project file asset record."""

    __tablename__ = "project_files"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    visibility: Mapped[str] = mapped_column(
        String(32), default="INTERNAL_ONLY", nullable=False, index=True
    )  # INTERNAL_ONLY, CLIENT_VISIBLE
    status: Mapped[str] = mapped_column(
        String(32), default="READY", nullable=False
    )  # UPLOADED, SCANNING, READY, REJECTED, QUARANTINED

    project = relationship("Project")


class ClientActionItem(BaseModel):
    """Outstanding action item required from the client."""

    __tablename__ = "client_action_items"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="PENDING", nullable=False, index=True
    )  # PENDING, IN_PROGRESS, COMPLETED, OVERDUE, CANCELLED
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project")


class ProjectAnnouncement(BaseModel):
    """Published client-visible project announcement."""

    __tablename__ = "project_announcements"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    published_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    project = relationship("Project")


class ClientActivity(BaseModel):
    """Client-safe audit activity log (`visibility = CLIENT_VISIBLE`)."""

    __tablename__ = "client_activities"

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    actor_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    visibility: Mapped[str] = mapped_column(
        String(32), default="CLIENT_VISIBLE", nullable=False, index=True
    )  # CLIENT_VISIBLE

    project = relationship("Project")
