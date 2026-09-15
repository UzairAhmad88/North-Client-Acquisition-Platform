"""add_outreach_drafts_tables

Revision ID: 012_add_outreach_drafts_tables
Revises: 011_add_lead_qualifications_tables
Create Date: 2026-09-08 12:04:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "012_add_outreach_drafts_tables"
down_revision: Union[str, None] = "011_add_lead_qualifications_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "outreach_drafts",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), sa.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("agent_run_id", sa.Uuid(as_uuid=True), sa.ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="EMAIL"),
        sa.Column("tone", sa.String(length=32), nullable=False, server_default="PROFESSIONAL"),
        sa.Column("language", sa.String(length=8), nullable=False, server_default="en"),
        sa.Column("personalization_depth", sa.String(length=32), nullable=False, server_default="STANDARD"),
        sa.Column("objective", sa.String(length=64), nullable=False, server_default="INTRODUCE_SERVICE"),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("primary_angle", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("personalization_profile", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column("claims", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("evidence", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False),
        sa.Column("risk_level", sa.String(length=32), nullable=False, server_default="LOW"),
        sa.Column("outreach_readiness", sa.String(length=32), nullable=False, server_default="READY"),
        sa.Column("approval_status", sa.String(length=32), nullable=False, server_default="PENDING_APPROVAL"),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
        sa.Column("is_stale", sa.Boolean(), nullable=False, server_default="false"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_outreach_drafts_lead_id", "outreach_drafts", ["lead_id"])
    op.create_index("ix_outreach_drafts_business_id", "outreach_drafts", ["business_id"])
    op.create_index("ix_outreach_drafts_content_hash", "outreach_drafts", ["content_hash"])


def downgrade() -> None:
    op.drop_index("ix_outreach_drafts_content_hash", table_name="outreach_drafts")
    op.drop_index("ix_outreach_drafts_business_id", table_name="outreach_drafts")
    op.drop_index("ix_outreach_drafts_lead_id", table_name="outreach_drafts")
    op.drop_table("outreach_drafts")
