"""add_discovery_requirements_tables

Revision ID: 016
Revises: 015
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "016"
down_revision = "015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Discovery Sessions Table
    op.create_table(
        "discovery_sessions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("conversation_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="OPEN"),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("readiness_stage", sa.String(length=64), nullable=False, server_default="NOT_READY"),
        sa.Column("readiness_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("completeness_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("scope_complexity", sa.String(length=32), nullable=False, server_default="UNKNOWN"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_discovery_sessions_business_id"), "discovery_sessions", ["business_id"], unique=False)
    op.create_index(op.f("ix_discovery_sessions_lead_id"), "discovery_sessions", ["lead_id"], unique=False)
    op.create_index(op.f("ix_discovery_sessions_conversation_id"), "discovery_sessions", ["conversation_id"], unique=False)
    op.create_index(op.f("ix_discovery_sessions_status"), "discovery_sessions", ["status"], unique=False)

    # 2. Client Requirements Table
    op.create_table(
        "requirements",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("discovery_session_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False, server_default="CLIENT_MESSAGE"),
        sa.Column("source_reference", sa.String(length=255), nullable=True),
        sa.Column("explicit", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="PROPOSED"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("confirmed_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["discovery_session_id"], ["discovery_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["confirmed_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_requirements_discovery_session_id"), "requirements", ["discovery_session_id"], unique=False)
    op.create_index(op.f("ix_requirements_business_id"), "requirements", ["business_id"], unique=False)
    op.create_index(op.f("ix_requirements_lead_id"), "requirements", ["lead_id"], unique=False)
    op.create_index(op.f("ix_requirements_category"), "requirements", ["category"], unique=False)
    op.create_index(op.f("ix_requirements_status"), "requirements", ["status"], unique=False)

    # 3. Requirement Evidence Table
    op.create_table(
        "requirement_evidence",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("requirement_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=True),
        sa.Column("evidence_text", sa.Text(), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_requirement_evidence_requirement_id"), "requirement_evidence", ["requirement_id"], unique=False)

    # 4. Requirement Dependency Table
    op.create_table(
        "requirement_dependencies",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("requirement_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("depends_on_requirement_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("dependency_type", sa.String(length=64), nullable=False, server_default="REQUIRES"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["depends_on_requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_requirement_dependencies_requirement_id"), "requirement_dependencies", ["requirement_id"], unique=False)
    op.create_index(op.f("ix_requirement_dependencies_depends_on_requirement_id"), "requirement_dependencies", ["depends_on_requirement_id"], unique=False)

    # 5. Requirement Questions Table
    op.create_table(
        "requirement_questions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("discovery_session_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("source_requirement_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="SCOPE"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PROPOSED"),
        sa.Column("answer_text", sa.Text(), nullable=True),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["discovery_session_id"], ["discovery_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_requirement_id"], ["requirements.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_requirement_questions_discovery_session_id"), "requirement_questions", ["discovery_session_id"], unique=False)
    op.create_index(op.f("ix_requirement_questions_status"), "requirement_questions", ["status"], unique=False)

    # 6. Scope Items Table
    op.create_table(
        "scope_items",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("discovery_session_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("requirement_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("scope_status", sa.String(length=32), nullable=False, server_default="UNKNOWN"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("confirmed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["discovery_session_id"], ["discovery_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scope_items_discovery_session_id"), "scope_items", ["discovery_session_id"], unique=False)
    op.create_index(op.f("ix_scope_items_scope_status"), "scope_items", ["scope_status"], unique=False)

    # 7. Discovery Events Table
    op.create_table(
        "discovery_events",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("discovery_session_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["discovery_session_id"], ["discovery_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_discovery_events_discovery_session_id"), "discovery_events", ["discovery_session_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_discovery_events_discovery_session_id"), table_name="discovery_events")
    op.drop_table("discovery_events")

    op.drop_index(op.f("ix_scope_items_scope_status"), table_name="scope_items")
    op.drop_index(op.f("ix_scope_items_discovery_session_id"), table_name="scope_items")
    op.drop_table("scope_items")

    op.drop_index(op.f("ix_requirement_questions_status"), table_name="requirement_questions")
    op.drop_index(op.f("ix_requirement_questions_discovery_session_id"), table_name="requirement_questions")
    op.drop_table("requirement_questions")

    op.drop_index(op.f("ix_requirement_dependencies_depends_on_requirement_id"), table_name="requirement_dependencies")
    op.drop_index(op.f("ix_requirement_dependencies_requirement_id"), table_name="requirement_dependencies")
    op.drop_table("requirement_dependencies")

    op.drop_index(op.f("ix_requirement_evidence_requirement_id"), table_name="requirement_evidence")
    op.drop_table("requirement_evidence")

    op.drop_index(op.f("ix_requirements_status"), table_name="requirements")
    op.drop_index(op.f("ix_requirements_category"), table_name="requirements")
    op.drop_index(op.f("ix_requirements_lead_id"), table_name="requirements")
    op.drop_index(op.f("ix_requirements_business_id"), table_name="requirements")
    op.drop_index(op.f("ix_requirements_discovery_session_id"), table_name="requirements")
    op.drop_table("requirements")

    op.drop_index(op.f("ix_discovery_sessions_status"), table_name="discovery_sessions")
    op.drop_index(op.f("ix_discovery_sessions_conversation_id"), table_name="discovery_sessions")
    op.drop_index(op.f("ix_discovery_sessions_lead_id"), table_name="discovery_sessions")
    op.drop_index(op.f("ix_discovery_sessions_business_id"), table_name="discovery_sessions")
    op.drop_table("discovery_sessions")
