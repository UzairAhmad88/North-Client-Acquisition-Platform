"""Add service_recommendations table

Revision ID: 009_add_service_recommendations_tables
Revises: 008_add_lead_scores_tables
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "009_add_service_recommendations_tables"
down_revision: Union[str, None] = "008_add_lead_scores_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "service_recommendations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("service_id", sa.Uuid(), nullable=False),
        sa.Column("recommendation_version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("relevance_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("band", sa.String(length=20), nullable=False, server_default="POSSIBLE"),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("confidence", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="SUGGESTED"),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("rejected_by", sa.Uuid(), nullable=True),
        sa.Column("rejected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("accepted_by", sa.Uuid(), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["rejected_by"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["accepted_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_service_recommendations_lead_id"), "service_recommendations", ["lead_id"], unique=False)
    op.create_index(op.f("ix_service_recommendations_business_id"), "service_recommendations", ["business_id"], unique=False)
    op.create_index(op.f("ix_service_recommendations_service_id"), "service_recommendations", ["service_id"], unique=False)
    op.create_index(op.f("ix_service_recommendations_recommendation_version"), "service_recommendations", ["recommendation_version"], unique=False)
    op.create_index(op.f("ix_service_recommendations_relevance_score"), "service_recommendations", ["relevance_score"], unique=False)
    op.create_index(op.f("ix_service_recommendations_band"), "service_recommendations", ["band"], unique=False)
    op.create_index(op.f("ix_service_recommendations_priority"), "service_recommendations", ["priority"], unique=False)
    op.create_index(op.f("ix_service_recommendations_confidence"), "service_recommendations", ["confidence"], unique=False)
    op.create_index(op.f("ix_service_recommendations_status"), "service_recommendations", ["status"], unique=False)
    op.create_index("ix_service_recommendations_lead_status", "service_recommendations", ["lead_id", "status"], unique=False)
    op.create_index("ix_service_recommendations_lead_service", "service_recommendations", ["lead_id", "service_id"], unique=False)


def downgrade() -> None:
    op.drop_table("service_recommendations")
