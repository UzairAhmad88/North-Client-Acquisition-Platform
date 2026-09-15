"""Add lead_scores table

Revision ID: 008_add_lead_scores_tables
Revises: 007_add_audit_tables
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "008_add_lead_scores_tables"
down_revision: Union[str, None] = "007_add_audit_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lead_scores",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=True),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("audit_id", sa.Uuid(), nullable=True),
        sa.Column("score_version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("total_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("band", sa.String(length=20), nullable=False, server_default="VERY_LOW"),
        sa.Column("website_need_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("online_presence_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("lead_capture_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("automation_potential_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("business_activity_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("contactability_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("service_fit_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("breakdown", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("is_stale", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("calculated_by", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["audit_id"], ["business_audits.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["calculated_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_lead_scores_lead_id"), "lead_scores", ["lead_id"], unique=False)
    op.create_index(op.f("ix_lead_scores_business_id"), "lead_scores", ["business_id"], unique=False)
    op.create_index(op.f("ix_lead_scores_audit_id"), "lead_scores", ["audit_id"], unique=False)
    op.create_index(op.f("ix_lead_scores_score_version"), "lead_scores", ["score_version"], unique=False)
    op.create_index(op.f("ix_lead_scores_total_score"), "lead_scores", ["total_score"], unique=False)
    op.create_index(op.f("ix_lead_scores_band"), "lead_scores", ["band"], unique=False)
    op.create_index(op.f("ix_lead_scores_confidence"), "lead_scores", ["confidence"], unique=False)
    op.create_index(
        "ix_lead_scores_biz_calc", "lead_scores", ["business_id", "calculated_at"], unique=False
    )
    op.create_index(
        "ix_lead_scores_lead_calc", "lead_scores", ["lead_id", "calculated_at"], unique=False
    )


def downgrade() -> None:
    op.drop_table("lead_scores")
