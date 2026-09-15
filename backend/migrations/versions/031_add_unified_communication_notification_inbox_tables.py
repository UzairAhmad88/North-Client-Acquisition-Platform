"""add_unified_communication_notification_inbox_tables

Revision ID: 031
Revises: 030
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "031"
down_revision = "030"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Notifications & Templates
    op.create_table(
        "notification_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("recipient_id", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, server_default="OPERATIONAL"),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="NORMAL"),
        sa.Column("action_url", sa.String(length=255), nullable=True),
        sa.Column("action_type", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DELIVERED"),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notification_records_tenant_id", "notification_records", ["tenant_id"])
    op.create_index("ix_notification_records_recipient_id", "notification_records", ["recipient_id"])
    op.create_index("ix_notification_records_category", "notification_records", ["category"])

    op.create_table(
        "notification_template_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False, server_default="IN_APP"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("subject_template", sa.String(length=255), nullable=False),
        sa.Column("body_template", sa.Text(), nullable=False),
        sa.Column("required_variables", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notification_template_records_event_type", "notification_template_records", ["event_type"])

    op.create_table(
        "notification_preference_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("in_app_enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("email_enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("push_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("quiet_hours_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("quiet_hours_start", sa.Integer(), nullable=False, server_default="22"),
        sa.Column("quiet_hours_end", sa.Integer(), nullable=False, server_default="7"),
        sa.Column("category_preferences", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_notification_preference_records_tenant_id", "notification_preference_records", ["tenant_id"])
    op.create_index("ix_notification_preference_records_user_id", "notification_preference_records", ["user_id"])

    # 2. Unified Inbox
    op.create_table(
        "inbox_item_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("recipient_id", sa.String(length=100), nullable=False),
        sa.Column("notification_id", sa.String(length=100), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, server_default="OPERATIONAL"),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="NORMAL"),
        sa.Column("state", sa.String(length=50), nullable=False, server_default="UNREAD"),
        sa.Column("source_type", sa.String(length=100), nullable=True),
        sa.Column("source_id", sa.String(length=100), nullable=True),
        sa.Column("action_url", sa.String(length=255), nullable=True),
        sa.Column("action_type", sa.String(length=50), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("snoozed_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_inbox_item_records_tenant_id", "inbox_item_records", ["tenant_id"])
    op.create_index("ix_inbox_item_records_recipient_id", "inbox_item_records", ["recipient_id"])
    op.create_index("ix_inbox_item_records_category", "inbox_item_records", ["category"])
    op.create_index("ix_inbox_item_records_state", "inbox_item_records", ["state"])

    # 3. Conversations & Messages
    op.create_table(
        "conversation_records",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("conversation_type", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("project_id", sa.String(length=100), nullable=True),
        sa.Column("client_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_records_tenant_id", "conversation_records", ["tenant_id"])
    op.create_index("ix_conversation_records_type", "conversation_records", ["conversation_type"])
    op.create_index("ix_conversation_records_project_id", "conversation_records", ["project_id"])
    op.create_index("ix_conversation_records_client_id", "conversation_records", ["client_id"])

    op.create_table(
        "conversation_member_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("conversation_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="MEMBER"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversation_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_member_records_conversation_id", "conversation_member_records", ["conversation_id"])
    op.create_index("ix_conversation_member_records_user_id", "conversation_member_records", ["user_id"])

    op.create_table(
        "conversation_message_records",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("conversation_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("sender_id", sa.String(length=100), nullable=False),
        sa.Column("sender_type", sa.String(length=50), nullable=False, server_default="USER"),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("visibility", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("reply_to_id", sa.String(length=100), nullable=True),
        sa.Column("edited_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversation_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_message_records_conversation_id", "conversation_message_records", ["conversation_id"])
    op.create_index("ix_conversation_message_records_sender_id", "conversation_message_records", ["sender_id"])
    op.create_index("ix_conversation_message_records_visibility", "conversation_message_records", ["visibility"])

    op.create_table(
        "conversation_message_version_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("message_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("editor_id", sa.String(length=100), nullable=False),
        sa.Column("edited_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["message_id"], ["conversation_message_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_message_version_records_message_id", "conversation_message_version_records", ["message_id"])

    op.create_table(
        "conversation_attachment_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("message_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mime_type", sa.String(length=100), nullable=False, server_default="application/pdf"),
        sa.Column("storage_path", sa.String(length=500), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["message_id"], ["conversation_message_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_conversation_attachment_records_message_id", "conversation_attachment_records", ["message_id"])

    # 4. Deliveries & Audits
    op.create_table(
        "communication_delivery_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("recipient_id", sa.String(length=100), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False, server_default="IN_APP"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DELIVERED"),
        sa.Column("provider", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_communication_delivery_records_tenant_id", "communication_delivery_records", ["tenant_id"])
    op.create_index("ix_communication_delivery_records_status", "communication_delivery_records", ["status"])

    op.create_table(
        "communication_audit_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("actor_id", sa.String(length=100), nullable=True),
        sa.Column("target_recipient", sa.String(length=100), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("outcome", sa.String(length=50), nullable=False, server_default="SUCCESS"),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_communication_audit_records_tenant_id", "communication_audit_records", ["tenant_id"])
    op.create_index("ix_communication_audit_records_event_type", "communication_audit_records", ["event_type"])

    op.create_table(
        "realtime_subscription_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False, server_default="default_tenant"),
        sa.Column("user_id", sa.String(length=100), nullable=False),
        sa.Column("channel_name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_realtime_subscription_records_user_id", "realtime_subscription_records", ["user_id"])
    op.create_index("ix_realtime_subscription_records_channel_name", "realtime_subscription_records", ["channel_name"])


def downgrade() -> None:
    op.drop_table("realtime_subscription_records")
    op.drop_table("communication_audit_records")
    op.drop_table("communication_delivery_records")
    op.drop_table("conversation_attachment_records")
    op.drop_table("conversation_message_version_records")
    op.drop_table("conversation_message_records")
    op.drop_table("conversation_member_records")
    op.drop_table("conversation_records")
    op.drop_table("inbox_item_records")
    op.drop_table("notification_preference_records")
    op.drop_table("notification_template_records")
    op.drop_table("notification_records")
