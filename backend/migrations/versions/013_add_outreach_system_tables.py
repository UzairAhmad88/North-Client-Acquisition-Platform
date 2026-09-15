"""add_outreach_system_tables

Revision ID: 013_add_outreach_system_tables
Revises: 012_add_outreach_drafts_tables
Create Date: 2026-09-08 12:27:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "013_add_outreach_system_tables"
down_revision: Union[str, None] = "012_add_outreach_drafts_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. do_not_contact
    op.create_table(
        "do_not_contact",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("scope", sa.String(length=32), nullable=False, server_default="EMAIL"),
        sa.Column("target_value", sa.String(length=255), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_by_user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_do_not_contact_target_value", "do_not_contact", ["target_value"])
    op.create_index("ix_do_not_contact_scope", "do_not_contact", ["scope"])

    # 2. communication_policies
    op.create_table(
        "communication_policies",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("max_per_contact_per_day", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("max_per_business_per_day", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("cooldown_hours", sa.Integer(), nullable=False, server_default="24"),
        sa.Column("allowed_channels", sa.JSON(), nullable=False, server_default='["EMAIL", "WHATSAPP", "SMS", "LINKEDIN"]'),
        sa.Column("require_approval", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    # 3. outreach_events
    op.create_table(
        "outreach_events",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("outreach_id", sa.Uuid(as_uuid=True), sa.ForeignKey("outreach_drafts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), sa.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False, server_default='{}'),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_outreach_events_outreach_id", "outreach_events", ["outreach_id"])
    op.create_index("ix_outreach_events_event_type", "outreach_events", ["event_type"])

    # 4. conversations
    op.create_table(
        "conversations",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), sa.ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("contact_id", sa.Uuid(as_uuid=True), sa.ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="EMAIL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversations_lead_id", "conversations", ["lead_id"])

    # 5. messages
    op.create_table(
        "messages",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("conversation_id", sa.Uuid(as_uuid=True), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("outreach_id", sa.Uuid(as_uuid=True), sa.ForeignKey("outreach_drafts.id", ondelete="SET NULL"), nullable=True),
        sa.Column("direction", sa.String(length=16), nullable=False, server_default="OUTBOUND"),
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="EMAIL"),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="SENT"),
        sa.Column("provider_message_id", sa.String(length=128), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"])


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("outreach_events")
    op.drop_table("communication_policies")
    op.drop_table("do_not_contact")
