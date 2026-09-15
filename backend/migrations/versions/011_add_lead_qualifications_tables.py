"""add_lead_qualifications_tables

Revision ID: 011_add_lead_qualifications_tables
Revises: 010_add_agent_runs_tables
Create Date: 2026-09-08 11:43:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "011_add_lead_qualifications_tables"
down_revision: Union[str, None] = "010_add_agent_runs_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lead_qualifications",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), sa.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("agent_run_id", sa.Uuid(as_uuid=True), sa.ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("decision", sa.String(length=50), nullable=False, server_default="INSUFFICIENT_DATA"),
        sa.Column("confidence", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("factors", sa.JSON(), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("risks", sa.JSON(), nullable=False),
        sa.Column("missing_information", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("outreach_readiness", sa.String(length=50), nullable=False, server_default="NOT_READY"),
        sa.Column("recommended_internal_action", sa.String(length=100), nullable=True),
        sa.Column("qualification_version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("is_stale", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("human_override_decision", sa.String(length=50), nullable=True),
        sa.Column("human_override_reason", sa.Text(), nullable=True),
        sa.Column("overridden_by_user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("overridden_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_lead_qualifications_lead_id", "lead_qualifications", ["lead_id"])
    op.create_index("ix_lead_qualifications_business_id", "lead_qualifications", ["business_id"])
    op.create_index("ix_lead_qualifications_user_id", "lead_qualifications", ["user_id"])
    op.create_index("ix_lead_qualifications_agent_run_id", "lead_qualifications", ["agent_run_id"])
    op.create_index("ix_lead_qualifications_decision", "lead_qualifications", ["decision"])
    op.create_index("ix_lead_qualifications_confidence", "lead_qualifications", ["confidence"])
    op.create_index("ix_lead_qualifications_outreach_readiness", "lead_qualifications", ["outreach_readiness"])
    op.create_index("ix_lead_qualifications_is_stale", "lead_qualifications", ["is_stale"])
    op.create_index("ix_lead_qualifications_lead_created", "lead_qualifications", ["lead_id", "created_at"])
    op.create_index("ix_lead_qualifications_biz_created", "lead_qualifications", ["business_id", "created_at"])


def downgrade() -> None:
    op.drop_table("lead_qualifications")
