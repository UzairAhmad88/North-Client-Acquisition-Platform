"""Add research_jobs, research_records, and research_conflicts tables

Revision ID: 006_add_research_tables
Revises: 005_add_services_and_lead_services_tables
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "006_add_research_tables"
down_revision: Union[str, None] = "005_add_services_and_lead_services_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. create research_jobs
    op.create_table(
        "research_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
        sa.Column("requested_sections", sa.JSON(), nullable=False),
        sa.Column("source_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_found", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_validated", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_rejected", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_research_jobs_business_id"), "research_jobs", ["business_id"], unique=False
    )
    op.create_index(op.f("ix_research_jobs_user_id"), "research_jobs", ["user_id"], unique=False)
    op.create_index(op.f("ix_research_jobs_status"), "research_jobs", ["status"], unique=False)
    op.create_index(
        "ix_research_jobs_business_status", "research_jobs", ["business_id", "status"], unique=False
    )
    op.create_index("ix_research_jobs_created_at", "research_jobs", ["created_at"], unique=False)

    # 2. create research_records
    op.create_table(
        "research_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("research_job_id", sa.Uuid(), nullable=True),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column(
            "source_trust", sa.String(length=50), nullable=False, server_default="MEDIUM_TRUST"
        ),
        sa.Column("research_type", sa.String(length=50), nullable=False, server_default="GENERAL"),
        sa.Column("field_name", sa.String(length=100), nullable=False),
        sa.Column("raw_value", sa.Text(), nullable=True),
        sa.Column("normalized_value", sa.Text(), nullable=False),
        sa.Column("confidence", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("evidence_text", sa.Text(), nullable=True),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="VALIDATED"),
        sa.Column("meta_info", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["research_job_id"], ["research_jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_research_records_business_id"), "research_records", ["business_id"], unique=False
    )
    op.create_index(
        op.f("ix_research_records_research_job_id"),
        "research_records",
        ["research_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_research_records_source_url"), "research_records", ["source_url"], unique=False
    )
    op.create_index(
        op.f("ix_research_records_source_trust"), "research_records", ["source_trust"], unique=False
    )
    op.create_index(
        op.f("ix_research_records_research_type"),
        "research_records",
        ["research_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_research_records_field_name"), "research_records", ["field_name"], unique=False
    )
    op.create_index(
        op.f("ix_research_records_confidence"), "research_records", ["confidence"], unique=False
    )
    op.create_index(
        op.f("ix_research_records_status"), "research_records", ["status"], unique=False
    )
    op.create_index(
        "ix_research_records_biz_field",
        "research_records",
        ["business_id", "field_name"],
        unique=False,
    )
    op.create_index(
        "ix_research_records_biz_confidence",
        "research_records",
        ["business_id", "confidence"],
        unique=False,
    )

    # 3. create research_conflicts
    op.create_table(
        "research_conflicts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("field_name", sa.String(length=100), nullable=False),
        sa.Column("competing_values", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="CONFLICT"),
        sa.Column("resolution_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_research_conflicts_business_id"),
        "research_conflicts",
        ["business_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_research_conflicts_field_name"), "research_conflicts", ["field_name"], unique=False
    )
    op.create_index(
        op.f("ix_research_conflicts_status"), "research_conflicts", ["status"], unique=False
    )
    op.create_index(
        "ix_research_conflicts_biz_field",
        "research_conflicts",
        ["business_id", "field_name"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("research_conflicts")
    op.drop_table("research_records")
    op.drop_table("research_jobs")
