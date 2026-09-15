"""ORM models for Contract, Scope Commitment & Client Approval System."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Contract(BaseModel):
    """Central contract entity managing scope commitment, lifecycle status, and agreement tracking."""

    __tablename__ = "contracts"

    proposal_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("proposals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    estimate_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("project_estimates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    solution_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("solution_designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lead_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    contract_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str] = mapped_column(
        String(64), default="DRAFT", nullable=False, index=True
    )  # DRAFT, IN_REVIEW, READY_FOR_CLIENT, SENT, VIEWED, PENDING_CLIENT, CLIENT_APPROVED, SIGNATURE_REQUIRED, SIGNED, ACTIVE, REVISION_REQUIRED, REJECTED, EXPIRED, CANCELLED, VOIDED, SUPERSEDED

    pricing_status: Mapped[str] = mapped_column(
        String(64), default="PRICING_REQUIRES_HUMAN_REVIEW", nullable=False
    )
    risk_status: Mapped[str] = mapped_column(
        String(32), default="PENDING_REVIEW", nullable=False
    )

    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    total_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_stale: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    proposal = relationship("Proposal", foreign_keys=[proposal_id], lazy="joined")
    estimate = relationship("ProjectEstimate", foreign_keys=[estimate_id], lazy="joined")
    solution = relationship("SolutionDesign", foreign_keys=[solution_id], lazy="joined")
    business = relationship("Business", foreign_keys=[business_id], lazy="joined")
    lead = relationship("Lead", foreign_keys=[lead_id], lazy="joined")

    versions = relationship("ContractVersion", back_populates="contract", cascade="all, delete-orphan")
    sections = relationship("ContractSection", back_populates="contract", cascade="all, delete-orphan")
    approvals = relationship("ContractApproval", back_populates="contract", cascade="all, delete-orphan")
    acceptances = relationship("ContractClientAcceptance", back_populates="contract", cascade="all, delete-orphan")
    signatures = relationship("ContractSignature", back_populates="contract", cascade="all, delete-orphan")
    baselines = relationship("ContractBaseline", back_populates="contract", cascade="all, delete-orphan")
    discrepancies = relationship("ContractDiscrepancy", back_populates="contract", cascade="all, delete-orphan")


class ContractVersion(BaseModel):
    """Immutable historical snapshot version of a contract document."""

    __tablename__ = "contract_versions"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    sections_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    source_proposal_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    source_estimate_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    source_solution_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    source_requirements_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    contract = relationship("Contract", back_populates="versions")


class ContractTemplate(BaseModel):
    """Reusable versioned contract template."""

    __tablename__ = "contract_templates"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)  # DRAFT, ACTIVE, ARCHIVED
    sections_schema: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class ContractSection(BaseModel):
    """Individual clause or section within a contract."""

    __tablename__ = "contract_sections"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    section_type: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # PARTIES, OVERVIEW, SCOPE, DELIVERABLES, EXCLUSIONS, ASSUMPTIONS, DEPENDENCIES, COMMERCIAL, PAYMENT, RESPONSIBILITIES, PRIVACY, IP, TERMINATION, SIGNATURES
    content: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    contract = relationship("Contract", back_populates="sections")


class ContractApproval(BaseModel):
    """Internal operator approval record for contract content."""

    __tablename__ = "contract_approvals"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="APPROVED", nullable=False)  # PENDING, APPROVED, REJECTED, REVOKED
    approval_reason: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    approved_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    contract = relationship("Contract", back_populates="approvals")


class ContractClientAcceptance(BaseModel):
    """Immutable client explicit acceptance record."""

    __tablename__ = "contract_client_acceptances"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="APPROVED", nullable=False
    )  # PENDING, VIEWED, QUESTIONS_RAISED, REVISION_REQUESTED, APPROVED, REJECTED, EXPIRED, WITHDRAWN
    acceptance_statement: Mapped[str] = mapped_column(Text, nullable=False)
    client_email: Mapped[str] = mapped_column(String(255), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    contract = relationship("Contract", back_populates="acceptances")


class ContractSignature(BaseModel):
    """Signature tracking record with provider status."""

    __tablename__ = "contract_signatures"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider_name: Mapped[str] = mapped_column(String(64), default="mock", nullable=False)
    provider_request_id: Mapped[str] = mapped_column(String(128), nullable=False)
    signer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="PENDING", nullable=False
    )  # PENDING, SIGNATURE_REQUIRED, SIGNED, REJECTED, EXPIRED
    signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    contract = relationship("Contract", back_populates="signatures")


class ContractBaseline(BaseModel):
    """Immutable committed project baseline once contract is signed and locked."""

    __tablename__ = "contract_baselines"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    contract_version: Mapped[int] = mapped_column(Integer, nullable=False)
    requirements_version: Mapped[int] = mapped_column(Integer, nullable=False)
    solution_version: Mapped[int] = mapped_column(Integer, nullable=False)
    estimate_version: Mapped[int] = mapped_column(Integer, nullable=False)
    proposal_version: Mapped[int] = mapped_column(Integer, nullable=False)

    scope_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    commercial_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    contract_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    is_locked: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    locked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    contract = relationship("Contract", back_populates="baselines")


class ContractDiscrepancy(BaseModel):
    """Detected discrepancy between contract terms and approved baseline artifacts."""

    __tablename__ = "contract_discrepancies"

    contract_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    discrepancy_type: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # SCOPE_MISMATCH, COMMERCIAL_MISMATCH, REQUIREMENT_COVERAGE_WARNING, TIMELINE_MISMATCH
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(32), default="HIGH", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="DETECTED", nullable=False)  # DETECTED, RESOLVED, IGNORED

    contract = relationship("Contract", back_populates="discrepancies")
