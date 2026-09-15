"""Add agent_runs, agent_events, and ai_usage tables

Revision ID: 010_add_agent_runs_tables
Revises: 009_add_service_recommendations_tables
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "010_add_agent_runs_tables"
down_revision: Union[str, None] = "009_add_service_recommendations_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # agent_runs table
    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workflow_id", sa.String(length=100), nullable=False),
        sa.Column("task_id", sa.String(length=100), nullable=False),
        sa.Column("agent_run_id", sa.String(length=100), nullable=False),
        sa.Column("agent_name", sa.String(length=100), nullable=False),
        sa.Column("agent_version", sa.String(length=20), nullable=False, server_default="1.0"),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("lead_id", sa.Uuid(), nullable=True),
        sa.Column("business_id", sa.Uuid(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="CREATED"),
        sa.Column("input_summary", sa.JSON(), nullable=False),
        sa.Column("output_summary", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("tool_calls_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("steps_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("estimated_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_cost", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_runs_workflow_id"), "agent_runs", ["workflow_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_task_id"), "agent_runs", ["task_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_agent_run_id"), "agent_runs", ["agent_run_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_agent_name"), "agent_runs", ["agent_name"], unique=False)
    op.create_index(op.f("ix_agent_runs_user_id"), "agent_runs", ["user_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_lead_id"), "agent_runs", ["lead_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_business_id"), "agent_runs", ["business_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_status"), "agent_runs", ["status"], unique=False)

    # agent_events table
    op.create_table(
        "agent_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("agent_run_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["agent_run_id"], ["agent_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_events_agent_run_id"), "agent_events", ["agent_run_id"], unique=False)
    op.create_index(op.f("ix_agent_events_event_type"), "agent_events", ["event_type"], unique=False)

    # ai_usage table
    op.create_table(
        "ai_usage",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("agent_name", sa.String(length=100), nullable=False),
        sa.Column("agent_run_id", sa.Uuid(), nullable=True),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("output_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_cost", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("latency_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SUCCESS"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["agent_run_id"], ["agent_runs.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_usage_provider"), "ai_usage", ["provider"], unique=False)
    op.create_index(op.f("ix_ai_usage_model"), "ai_usage", ["model"], unique=False)
    op.create_index(op.f("ix_ai_usage_agent_name"), "ai_usage", ["agent_name"], unique=False)


def downgrade() -> None:
    op.drop_table("ai_usage")
    op.drop_table("agent_events")
    op.drop_table("agent_runs")
