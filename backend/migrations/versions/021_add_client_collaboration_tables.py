"""add_client_collaboration_tables

Revision ID: 021
Revises: 020
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "021"
down_revision = "020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Client Accounts Table
    op.create_table(
        "client_accounts",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_accounts_business_id"), "client_accounts", ["business_id"], unique=False)
    op.create_index(op.f("ix_client_accounts_status"), "client_accounts", ["status"], unique=False)

    # 2. Client Members Table
    op.create_table(
        "client_members",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("client_account_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False, server_default="CLIENT_MEMBER"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("invited_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["client_account_id"], ["client_accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_members_client_account_id"), "client_members", ["client_account_id"], unique=False)
    op.create_index(op.f("ix_client_members_user_id"), "client_members", ["user_id"], unique=False)

    # 3. Client Invitations Table
    op.create_table(
        "client_invitations",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("client_account_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False, server_default="CLIENT_MEMBER"),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["client_account_id"], ["client_accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index(op.f("ix_client_invitations_client_account_id"), "client_invitations", ["client_account_id"], unique=False)
    op.create_index(op.f("ix_client_invitations_email"), "client_invitations", ["email"], unique=False)
    op.create_index(op.f("ix_client_invitations_token_hash"), "client_invitations", ["token_hash"], unique=True)

    # 4. Client Project Access Table
    op.create_table(
        "client_project_access",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("client_account_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("access_level", sa.String(length=32), nullable=False, server_default="COLLABORATE"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["client_account_id"], ["client_accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_project_access_client_account_id"), "client_project_access", ["client_account_id"], unique=False)
    op.create_index(op.f("ix_client_project_access_project_id"), "client_project_access", ["project_id"], unique=False)

    # 5. Discussion Threads Table
    op.create_table(
        "discussion_threads",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("deliverable_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("type", sa.String(length=32), nullable=False, server_default="GENERAL"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="OPEN"),
        sa.Column("visibility", sa.String(length=32), nullable=False, server_default="CLIENT_VISIBLE"),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_discussion_threads_project_id"), "discussion_threads", ["project_id"], unique=False)
    op.create_index(op.f("ix_discussion_threads_deliverable_id"), "discussion_threads", ["deliverable_id"], unique=False)
    op.create_index(op.f("ix_discussion_threads_type"), "discussion_threads", ["type"], unique=False)
    op.create_index(op.f("ix_discussion_threads_status"), "discussion_threads", ["status"], unique=False)
    op.create_index(op.f("ix_discussion_threads_visibility"), "discussion_threads", ["visibility"], unique=False)

    # 6. Thread Messages Table
    op.create_table(
        "thread_messages",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("thread_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("sender_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("sender_type", sa.String(length=32), nullable=False, server_default="CLIENT"),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("visibility", sa.String(length=32), nullable=False, server_default="CLIENT_VISIBLE"),
        sa.Column("attachments", sa.JSON(), nullable=False),
        sa.Column("edited_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["thread_id"], ["discussion_threads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_thread_messages_thread_id"), "thread_messages", ["thread_id"], unique=False)
    op.create_index(op.f("ix_thread_messages_sender_id"), "thread_messages", ["sender_id"], unique=False)
    op.create_index(op.f("ix_thread_messages_visibility"), "thread_messages", ["visibility"], unique=False)

    # 7. Client Questions Table
    op.create_table(
        "client_questions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="OPEN"),
        sa.Column("answer", sa.Text(), nullable=True),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("answered_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["answered_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_questions_project_id"), "client_questions", ["project_id"], unique=False)
    op.create_index(op.f("ix_client_questions_status"), "client_questions", ["status"], unique=False)

    # 8. Client Requests Table
    op.create_table(
        "client_requests",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("client_account_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("classification", sa.String(length=64), nullable=False, server_default="NEEDS_REVIEW"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="SUBMITTED"),
        sa.Column("submitted_by_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["client_account_id"], ["client_accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["submitted_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_requests_project_id"), "client_requests", ["project_id"], unique=False)
    op.create_index(op.f("ix_client_requests_client_account_id"), "client_requests", ["client_account_id"], unique=False)
    op.create_index(op.f("ix_client_requests_classification"), "client_requests", ["classification"], unique=False)
    op.create_index(op.f("ix_client_requests_status"), "client_requests", ["status"], unique=False)

    # 9. Client Feedback Table
    op.create_table(
        "client_feedback",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("deliverable_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("category", sa.String(length=32), nullable=False, server_default="FUNCTIONALITY"),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="SUBMITTED"),
        sa.Column("submitted_by_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["submitted_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_feedback_project_id"), "client_feedback", ["project_id"], unique=False)
    op.create_index(op.f("ix_client_feedback_deliverable_id"), "client_feedback", ["deliverable_id"], unique=False)

    # 10. Deliverable Reviews Table
    op.create_table(
        "deliverable_reviews",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("deliverable_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PENDING_REVIEW"),
        sa.Column("feedback_notes", sa.Text(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reviewed_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deliverable_reviews_deliverable_id"), "deliverable_reviews", ["deliverable_id"], unique=False)
    op.create_index(op.f("ix_deliverable_reviews_status"), "deliverable_reviews", ["status"], unique=False)

    # 11. Deliverable Approvals Table
    op.create_table(
        "deliverable_approvals",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("deliverable_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("approval_statement", sa.Text(), nullable=False),
        sa.Column("signer_name", sa.String(length=255), nullable=False),
        sa.Column("signer_email", sa.String(length=255), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=False),
        sa.Column("user_agent", sa.String(length=255), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deliverable_approvals_deliverable_id"), "deliverable_approvals", ["deliverable_id"], unique=False)

    # 12. Project Files Table
    op.create_table(
        "project_files",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("uploaded_by_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("storage_key", sa.String(length=255), nullable=False),
        sa.Column("mime_type", sa.String(length=128), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("visibility", sa.String(length=32), nullable=False, server_default="INTERNAL_ONLY"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="READY"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["uploaded_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("storage_key"),
    )
    op.create_index(op.f("ix_project_files_project_id"), "project_files", ["project_id"], unique=False)
    op.create_index(op.f("ix_project_files_visibility"), "project_files", ["visibility"], unique=False)

    # 13. Client Action Items Table
    op.create_table(
        "client_action_items",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_action_items_project_id"), "client_action_items", ["project_id"], unique=False)
    op.create_index(op.f("ix_client_action_items_status"), "client_action_items", ["status"], unique=False)

    # 14. Project Announcements Table
    op.create_table(
        "project_announcements",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("published_by_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["published_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_announcements_project_id"), "project_announcements", ["project_id"], unique=False)

    # 15. Client Activities Table
    op.create_table(
        "client_activities",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("actor_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("visibility", sa.String(length=32), nullable=False, server_default="CLIENT_VISIBLE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["actor_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_activities_project_id"), "client_activities", ["project_id"], unique=False)
    op.create_index(op.f("ix_client_activities_event_type"), "client_activities", ["event_type"], unique=False)
    op.create_index(op.f("ix_client_activities_visibility"), "client_activities", ["visibility"], unique=False)


def downgrade() -> None:
    op.drop_table("client_activities")
    op.drop_table("project_announcements")
    op.drop_table("client_action_items")
    op.drop_table("project_files")
    op.drop_table("deliverable_approvals")
    op.drop_table("deliverable_reviews")
    op.drop_table("client_feedback")
    op.drop_table("client_requests")
    op.drop_table("client_questions")
    op.drop_table("thread_messages")
    op.drop_table("discussion_threads")
    op.drop_table("client_project_access")
    op.drop_table("client_invitations")
    op.drop_table("client_members")
    op.drop_table("client_accounts")
