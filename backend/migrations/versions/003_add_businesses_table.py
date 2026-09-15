"""Add businesses table

Revision ID: 003_add_businesses_table
Revises: 002_add_users_table
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "003_add_businesses_table"
down_revision: Union[str, None] = "002_add_users_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "businesses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("normalized_name", sa.String(length=255), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "business_type",
            sa.String(length=100),
            nullable=False,
            server_default=sa.text("'OTHER'"),
        ),
        sa.Column(
            "industry", sa.String(length=100), nullable=False, server_default=sa.text("'OTHER'")
        ),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("subcategory", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("normalized_phone", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("normalized_email", sa.String(length=255), nullable=True),
        sa.Column("website_url", sa.String(length=500), nullable=True),
        sa.Column("normalized_website", sa.String(length=500), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column(
            "country", sa.String(length=100), nullable=True, server_default=sa.text("'Pakistan'")
        ),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("timezone", sa.String(length=50), nullable=True),
        sa.Column(
            "status", sa.String(length=50), nullable=False, server_default=sa.text("'ACTIVE'")
        ),
        sa.Column(
            "source", sa.String(length=100), nullable=False, server_default=sa.text("'MANUAL'")
        ),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name=op.f("fk_businesses_created_by_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_businesses")),
    )
    op.create_index(op.f("ix_businesses_name"), "businesses", ["name"], unique=False)
    op.create_index(
        op.f("ix_businesses_normalized_name"), "businesses", ["normalized_name"], unique=False
    )
    op.create_index(
        op.f("ix_businesses_business_type"), "businesses", ["business_type"], unique=False
    )
    op.create_index(op.f("ix_businesses_industry"), "businesses", ["industry"], unique=False)
    op.create_index(op.f("ix_businesses_phone"), "businesses", ["phone"], unique=False)
    op.create_index(
        op.f("ix_businesses_normalized_phone"), "businesses", ["normalized_phone"], unique=False
    )
    op.create_index(op.f("ix_businesses_email"), "businesses", ["email"], unique=False)
    op.create_index(
        op.f("ix_businesses_normalized_email"), "businesses", ["normalized_email"], unique=False
    )
    op.create_index(op.f("ix_businesses_website_url"), "businesses", ["website_url"], unique=False)
    op.create_index(
        op.f("ix_businesses_normalized_website"), "businesses", ["normalized_website"], unique=False
    )
    op.create_index(op.f("ix_businesses_city"), "businesses", ["city"], unique=False)
    op.create_index(op.f("ix_businesses_status"), "businesses", ["status"], unique=False)
    op.create_index(op.f("ix_businesses_source"), "businesses", ["source"], unique=False)
    op.create_index(op.f("ix_businesses_external_id"), "businesses", ["external_id"], unique=False)
    op.create_index(
        op.f("ix_businesses_created_by_user_id"), "businesses", ["created_by_user_id"], unique=False
    )
    op.create_index(
        "ix_businesses_source_external_id", "businesses", ["source", "external_id"], unique=False
    )
    op.create_index("ix_businesses_created_at", "businesses", ["created_at"], unique=False)
    op.create_index("ix_businesses_updated_at", "businesses", ["updated_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_businesses_updated_at", table_name="businesses")
    op.drop_index("ix_businesses_created_at", table_name="businesses")
    op.drop_index("ix_businesses_source_external_id", table_name="businesses")
    op.drop_index(op.f("ix_businesses_created_by_user_id"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_external_id"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_source"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_status"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_city"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_normalized_website"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_website_url"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_normalized_email"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_email"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_normalized_phone"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_phone"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_industry"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_business_type"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_normalized_name"), table_name="businesses")
    op.drop_index(op.f("ix_businesses_name"), table_name="businesses")
    op.drop_table("businesses")
