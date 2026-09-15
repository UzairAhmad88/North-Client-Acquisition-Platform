"""Initial foundation migration

Revision ID: 001_initial_foundation
Revises: None
Create Date: 2026-09-07

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_initial_foundation"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "system_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("level", sa.String(length=20), nullable=False),
        sa.Column("component", sa.String(length=50), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_system_logs")),
    )
    op.create_index(op.f("ix_system_logs_component"), "system_logs", ["component"], unique=False)
    op.create_index(op.f("ix_system_logs_level"), "system_logs", ["level"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_system_logs_level"), table_name="system_logs")
    op.drop_index(op.f("ix_system_logs_component"), table_name="system_logs")
    op.drop_table("system_logs")
