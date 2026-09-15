"""add_response_intelligence_tables

Revision ID: 015
Revises: 014
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "015"
down_revision = "014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add intelligence state columns to conversations table
    op.add_column("conversations", sa.Column("current_intent", sa.String(length=64), nullable=True))
    op.add_column("conversations", sa.Column("conversation_stage", sa.String(length=64), nullable=False, server_default="NEW_RESPONSE"))
    op.add_column("conversations", sa.Column("next_action", sa.String(length=64), nullable=True))
    op.add_column("conversations", sa.Column("priority", sa.String(length=32), nullable=False, server_default="NORMAL"))
    op.add_column("conversations", sa.Column("last_inbound_at", sa.DateTime(timezone=True), nullable=True))

    op.create_table(
        "conversation_analyses",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("conversation_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("latest_message_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("agent_run_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("primary_intent", sa.String(length=64), nullable=False),
        sa.Column("all_intents", sa.JSON(), nullable=False),
        sa.Column("intent_confidence", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("buying_signal_level", sa.String(length=32), nullable=False, server_default="NONE"),
        sa.Column("objection_type", sa.String(length=64), nullable=True),
        sa.Column("extracted_requirements", sa.JSON(), nullable=False),
        sa.Column("missing_information", sa.JSON(), nullable=False),
        sa.Column("conversation_stage", sa.String(length=64), nullable=False, server_default="NEW_RESPONSE"),
        sa.Column("recommended_next_action", sa.String(length=64), nullable=False),
        sa.Column("recommended_next_action_reason", sa.Text(), nullable=True),
        sa.Column("next_action_confidence", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("sentiment_signal", sa.String(length=32), nullable=False, server_default="NEUTRAL"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="NORMAL"),
        sa.Column("human_correction", sa.JSON(), nullable=True),
        sa.Column("human_correction_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("human_correction_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["latest_message_id"], ["messages.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["agent_run_id"], ["agent_runs.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["human_correction_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversation_analyses_conversation_id"), "conversation_analyses", ["conversation_id"], unique=False)
    op.create_index(op.f("ix_conversation_analyses_primary_intent"), "conversation_analyses", ["primary_intent"], unique=False)
    op.create_index(op.f("ix_conversation_analyses_conversation_stage"), "conversation_analyses", ["conversation_stage"], unique=False)
    op.create_index(op.f("ix_conversation_analyses_recommended_next_action"), "conversation_analyses", ["recommended_next_action"], unique=False)

    op.create_table(
        "inbound_event_logs",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("provider_event_id", sa.String(length=255), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False, server_default="EMAIL"),
        sa.Column("sender", sa.String(length=255), nullable=False),
        sa.Column("recipient", sa.String(length=255), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PROCESSED"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_inbound_event_logs_provider"), "inbound_event_logs", ["provider"], unique=False)
    op.create_index(op.f("ix_inbound_event_logs_provider_event_id"), "inbound_event_logs", ["provider_event_id"], unique=False)

    op.create_table(
        "conversation_facts",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("conversation_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("source_message_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("fact_key", sa.String(length=128), nullable=False),
        sa.Column("fact_value", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_message_id"], ["messages.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversation_facts_conversation_id"), "conversation_facts", ["conversation_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_conversation_facts_conversation_id"), table_name="conversation_facts")
    op.drop_table("conversation_facts")
    op.drop_index(op.f("ix_inbound_event_logs_provider_event_id"), table_name="inbound_event_logs")
    op.drop_index(op.f("ix_inbound_event_logs_provider"), table_name="inbound_event_logs")
    op.drop_table("inbound_event_logs")
    op.drop_index(op.f("ix_conversation_analyses_recommended_next_action"), table_name="conversation_analyses")
    op.drop_index(op.f("ix_conversation_analyses_conversation_stage"), table_name="conversation_analyses")
    op.drop_index(op.f("ix_conversation_analyses_primary_intent"), table_name="conversation_analyses")
    op.drop_index(op.f("ix_conversation_analyses_conversation_id"), table_name="conversation_analyses")
    op.drop_table("conversation_analyses")
    op.drop_column("conversations", "last_inbound_at")
    op.drop_column("conversations", "priority")
    op.drop_column("conversations", "next_action")
    op.drop_column("conversations", "conversation_stage")
    op.drop_column("conversations", "current_intent")
