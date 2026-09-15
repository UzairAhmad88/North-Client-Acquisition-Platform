"""add_unified_search_command_assistant_tables

Revision ID: 032
Revises: 031
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "032"
down_revision = "031"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Search Index Records
    op.create_table(
        "search_index_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("search_text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("priority", sa.String(length=50), nullable=True),
        sa.Column("action_url", sa.String(length=255), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_search_index_records_tenant_id", "search_index_records", ["tenant_id"])
    op.create_index("ix_search_index_records_entity_type", "search_index_records", ["entity_type"])
    op.create_index("ix_search_index_records_entity_id", "search_index_records", ["entity_id"])

    # 2. Search Index Version Records
    op.create_table(
        "search_index_version_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("total_documents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_search_index_version_records_tenant_id", "search_index_version_records", ["tenant_id"])

    # 3. Search Query Audit Records
    op.create_table(
        "search_query_audit_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("query_text", sa.String(length=500), nullable=False),
        sa.Column("search_type", sa.String(length=50), nullable=False, server_default="KEYWORD"),
        sa.Column("result_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("latency_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_search_query_audit_records_tenant_id", "search_query_audit_records", ["tenant_id"])
    op.create_index("ix_search_query_audit_records_user_id", "search_query_audit_records", ["user_id"])

    # 4. Search Saved Query Records
    op.create_table(
        "search_saved_query_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("query_text", sa.String(length=500), nullable=False),
        sa.Column("filters_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("is_pinned", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_search_saved_query_records_tenant_id", "search_saved_query_records", ["tenant_id"])
    op.create_index("ix_search_saved_query_records_user_id", "search_saved_query_records", ["user_id"])

    # 5. Search Pin Records
    op.create_table(
        "search_pin_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("action_url", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_search_pin_records_tenant_id", "search_pin_records", ["tenant_id"])
    op.create_index("ix_search_pin_records_user_id", "search_pin_records", ["user_id"])

    # 6. Command Definition Records
    op.create_table(
        "command_definition_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("command_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, server_default="NAVIGATION"),
        sa.Column("risk_level", sa.String(length=50), nullable=False, server_default="LOW"),
        sa.Column("required_permission", sa.String(length=100), nullable=True),
        sa.Column("requires_confirmation", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("requires_approval", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("parameters_schema", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_command_definition_records_command_id", "command_definition_records", ["command_id"], unique=True)

    # 7. Command Audit Event Records
    op.create_table(
        "command_audit_event_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("command_id", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="EXECUTED"),
        sa.Column("parameters_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("result_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_command_audit_event_records_tenant_id", "command_audit_event_records", ["tenant_id"])
    op.create_index("ix_command_audit_event_records_user_id", "command_audit_event_records", ["user_id"])

    # 8. Assistant Session & Message Records
    op.create_table(
        "assistant_session_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False, server_default="New Conversation"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assistant_session_records_tenant_id", "assistant_session_records", ["tenant_id"])
    op.create_index("ix_assistant_session_records_user_id", "assistant_session_records", ["user_id"])

    op.create_table(
        "assistant_message_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="USER"),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("answer_type", sa.String(length=50), nullable=False, server_default="FACT"),
        sa.Column("ai_trace_id", sa.String(length=100), nullable=True),
        sa.Column("sources_json", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["session_id"], ["assistant_session_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assistant_message_records_session_id", "assistant_message_records", ["session_id"])


def downgrade() -> None:
    op.drop_table("assistant_message_records")
    op.drop_table("assistant_session_records")
    op.drop_table("command_audit_event_records")
    op.drop_table("command_definition_records")
    op.drop_table("search_pin_records")
    op.drop_table("search_saved_query_records")
    op.drop_table("search_query_audit_records")
    op.drop_table("search_index_version_records")
    op.drop_table("search_index_records")
