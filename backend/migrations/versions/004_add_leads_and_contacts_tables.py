"""Add leads and contacts tables

Revision ID: 004_add_leads_and_contacts_tables
Revises: 003_add_businesses_table
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "004_add_leads_and_contacts_tables"
down_revision: Union[str, None] = "003_add_businesses_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "leads",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'NEW'"),
        ),
        sa.Column(
            "source",
            sa.String(length=100),
            nullable=False,
            server_default=sa.text("'MANUAL'"),
        ),
        sa.Column("source_detail", sa.String(length=255), nullable=True),
        sa.Column(
            "priority",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'MEDIUM'"),
        ),
        sa.Column("owner_user_id", sa.Uuid(), nullable=True),
        sa.Column(
            "qualification_status",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'UNQUALIFIED'"),
        ),
        sa.Column(
            "contactability_status",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'UNKNOWN'"),
        ),
        sa.Column("estimated_value", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column(
            "currency",
            sa.String(length=10),
            nullable=False,
            server_default=sa.text("'USD'"),
        ),
        sa.Column("next_action", sa.String(length=255), nullable=True),
        sa.Column("next_action_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_contacted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_contacted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("converted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("lost_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("loss_reason", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"],
            name=op.f("fk_leads_business_id_businesses"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["owner_user_id"],
            ["users.id"],
            name=op.f("fk_leads_owner_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leads")),
    )
    op.create_index(op.f("ix_leads_business_id"), "leads", ["business_id"], unique=False)
    op.create_index(op.f("ix_leads_title"), "leads", ["title"], unique=False)
    op.create_index(op.f("ix_leads_status"), "leads", ["status"], unique=False)
    op.create_index(op.f("ix_leads_source"), "leads", ["source"], unique=False)
    op.create_index(op.f("ix_leads_priority"), "leads", ["priority"], unique=False)
    op.create_index(op.f("ix_leads_owner_user_id"), "leads", ["owner_user_id"], unique=False)
    op.create_index(
        op.f("ix_leads_qualification_status"),
        "leads",
        ["qualification_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_leads_contactability_status"),
        "leads",
        ["contactability_status"],
        unique=False,
    )
    op.create_index(op.f("ix_leads_next_action_at"), "leads", ["next_action_at"], unique=False)
    op.create_index("ix_leads_status_priority", "leads", ["status", "priority"], unique=False)
    op.create_index("ix_leads_created_at", "leads", ["created_at"], unique=False)
    op.create_index("ix_leads_updated_at", "leads", ["updated_at"], unique=False)

    op.create_table(
        "contacts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("business_id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column(
            "is_primary",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"],
            name=op.f("fk_contacts_business_id_businesses"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"],
            ["leads.id"],
            name=op.f("fk_contacts_lead_id_leads"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contacts")),
    )
    op.create_index(op.f("ix_contacts_business_id"), "contacts", ["business_id"], unique=False)
    op.create_index(op.f("ix_contacts_lead_id"), "contacts", ["lead_id"], unique=False)
    op.create_index(op.f("ix_contacts_email"), "contacts", ["email"], unique=False)
    op.create_index(op.f("ix_contacts_phone"), "contacts", ["phone"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_contacts_phone"), table_name="contacts")
    op.drop_index(op.f("ix_contacts_email"), table_name="contacts")
    op.drop_index(op.f("ix_contacts_lead_id"), table_name="contacts")
    op.drop_index(op.f("ix_contacts_business_id"), table_name="contacts")
    op.drop_table("contacts")

    op.drop_index("ix_leads_updated_at", table_name="leads")
    op.drop_index("ix_leads_created_at", table_name="leads")
    op.drop_index("ix_leads_status_priority", table_name="leads")
    op.drop_index(op.f("ix_leads_next_action_at"), table_name="leads")
    op.drop_index(op.f("ix_leads_contactability_status"), table_name="leads")
    op.drop_index(op.f("ix_leads_qualification_status"), table_name="leads")
    op.drop_index(op.f("ix_leads_owner_user_id"), table_name="leads")
    op.drop_index(op.f("ix_leads_priority"), table_name="leads")
    op.drop_index(op.f("ix_leads_source"), table_name="leads")
    op.drop_index(op.f("ix_leads_status"), table_name="leads")
    op.drop_index(op.f("ix_leads_title"), table_name="leads")
    op.drop_index(op.f("ix_leads_business_id"), table_name="leads")
    op.drop_table("leads")
