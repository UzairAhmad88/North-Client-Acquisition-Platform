"""Add audit_jobs, business_audits, audit_findings, and audit_pages tables

Revision ID: 007_add_audit_tables
Revises: 006_add_research_tables
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "007_add_audit_tables"
down_revision: Union[str, None] = "006_add_research_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. create audit_jobs
    op.create_table(
        "audit_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("target_url", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
        sa.Column("requested_categories", sa.JSON(), nullable=False),
        sa.Column("pages_requested", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("pages_analyzed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("findings_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("warnings_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("errors_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_jobs_business_id"), "audit_jobs", ["business_id"], unique=False)
    op.create_index(op.f("ix_audit_jobs_user_id"), "audit_jobs", ["user_id"], unique=False)
    op.create_index(op.f("ix_audit_jobs_status"), "audit_jobs", ["status"], unique=False)
    op.create_index(
        "ix_audit_jobs_business_status", "audit_jobs", ["business_id", "status"], unique=False
    )
    op.create_index("ix_audit_jobs_created_at", "audit_jobs", ["created_at"], unique=False)

    # 2. create business_audits
    op.create_table(
        "business_audits",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("research_record_id", sa.Uuid(), nullable=True),
        sa.Column("audit_job_id", sa.Uuid(), nullable=True),
        sa.Column("target_url", sa.String(length=500), nullable=True),
        sa.Column("audit_version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="AVAILABLE"),
        sa.Column(
            "overall_health", sa.String(length=50), nullable=False, server_default="LIMITED_DATA"
        ),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("categories", sa.JSON(), nullable=False),
        sa.Column("findings", sa.JSON(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("warnings", sa.JSON(), nullable=False),
        sa.Column("errors", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["research_record_id"], ["research_records.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["audit_job_id"], ["audit_jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_business_audits_business_id"), "business_audits", ["business_id"], unique=False
    )
    op.create_index(
        op.f("ix_business_audits_status"), "business_audits", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_business_audits_overall_health"),
        "business_audits",
        ["overall_health"],
        unique=False,
    )
    op.create_index(
        "ix_business_audits_biz_created",
        "business_audits",
        ["business_id", "created_at"],
        unique=False,
    )

    # 3. create audit_findings
    op.create_table(
        "audit_findings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("audit_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="INFO"),
        sa.Column("confidence", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("affected_page", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["audit_id"], ["business_audits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_findings_audit_id"), "audit_findings", ["audit_id"], unique=False)
    op.create_index(op.f("ix_audit_findings_code"), "audit_findings", ["code"], unique=False)
    op.create_index(op.f("ix_audit_findings_category"), "audit_findings", ["category"], unique=False)
    op.create_index(op.f("ix_audit_findings_severity"), "audit_findings", ["severity"], unique=False)
    op.create_index(
        "ix_audit_findings_audit_cat", "audit_findings", ["audit_id", "category"], unique=False
    )

    # 4. create audit_pages
    op.create_table(
        "audit_pages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("audit_id", sa.Uuid(), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False, server_default="200"),
        sa.Column("response_time_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("content_type", sa.String(length=100), nullable=True),
        sa.Column("meta_description", sa.Text(), nullable=True),
        sa.Column("is_homepage", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_contact_form", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["audit_id"], ["business_audits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_pages_audit_id"), "audit_pages", ["audit_id"], unique=False)
    op.create_index("ix_audit_pages_audit_url", "audit_pages", ["audit_id", "url"], unique=False)


def downgrade() -> None:
    op.drop_table("audit_pages")
    op.drop_table("audit_findings")
    op.drop_table("business_audits")
    op.drop_table("audit_jobs")
