"""Add services and lead_services tables

Revision ID: 005_add_services_and_lead_services_tables
Revises: 004_add_leads_and_contacts_tables
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "005_add_services_and_lead_services_tables"
down_revision: Union[str, None] = "004_add_leads_and_contacts_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "services",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("short_description", sa.String(length=500), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=False,
            server_default=sa.text("'WEB_DEVELOPMENT'"),
        ),
        sa.Column("subcategory", sa.String(length=100), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'ACTIVE'"),
        ),
        sa.Column(
            "delivery_model",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'FIXED_PROJECT'"),
        ),
        sa.Column(
            "pricing_model",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'CUSTOM'"),
        ),
        sa.Column("base_price", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("price_min", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("price_max", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column(
            "currency",
            sa.String(length=10),
            nullable=False,
            server_default=sa.text("'USD'"),
        ),
        sa.Column("estimated_duration_days", sa.Integer(), nullable=True),
        sa.Column(
            "is_featured",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column("features", sa.JSON(), nullable=True),
        sa.Column("requirements", sa.JSON(), nullable=True),
        sa.Column("target_business_types", sa.JSON(), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_services")),
        sa.UniqueConstraint("slug", name=op.f("uq_services_slug")),
    )
    op.create_index(op.f("ix_services_name"), "services", ["name"], unique=False)
    op.create_index(op.f("ix_services_slug"), "services", ["slug"], unique=True)
    op.create_index(op.f("ix_services_category"), "services", ["category"], unique=False)
    op.create_index(op.f("ix_services_status"), "services", ["status"], unique=False)
    op.create_index("ix_services_category_status", "services", ["category", "status"], unique=False)
    op.create_index("ix_services_created_at", "services", ["created_at"], unique=False)
    op.create_index("ix_services_updated_at", "services", ["updated_at"], unique=False)

    op.create_table(
        "lead_services",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("service_id", sa.Uuid(), nullable=False),
        sa.Column(
            "relationship_type",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'CONSIDERED'"),
        ),
        sa.Column(
            "source",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'HUMAN'"),
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["lead_id"],
            ["leads.id"],
            name=op.f("fk_lead_services_lead_id_leads"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            name=op.f("fk_lead_services_service_id_services"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lead_services")),
        sa.UniqueConstraint("lead_id", "service_id", name="uq_lead_services_lead_service"),
    )
    op.create_index(op.f("ix_lead_services_lead_id"), "lead_services", ["lead_id"], unique=False)
    op.create_index(
        op.f("ix_lead_services_service_id"), "lead_services", ["service_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_lead_services_service_id"), table_name="lead_services")
    op.drop_index(op.f("ix_lead_services_lead_id"), table_name="lead_services")
    op.drop_table("lead_services")

    op.drop_index("ix_services_updated_at", table_name="services")
    op.drop_index("ix_services_created_at", table_name="services")
    op.drop_index("ix_services_category_status", table_name="services")
    op.drop_index(op.f("ix_services_status"), table_name="services")
    op.drop_index(op.f("ix_services_category"), table_name="services")
    op.drop_index(op.f("ix_services_slug"), table_name="services")
    op.drop_index(op.f("ix_services_name"), table_name="services")
    op.drop_table("services")
