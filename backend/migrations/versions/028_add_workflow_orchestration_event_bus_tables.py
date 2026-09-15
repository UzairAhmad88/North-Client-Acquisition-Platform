"""add_workflow_orchestration_event_bus_tables

Revision ID: 028
Revises: 027
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "028"
down_revision = "027"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Event Registry & Versions
    op.create_table(
        "event_registry_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_name", sa.String(length=100), nullable=False),
        sa.Column("current_version", sa.String(length=20), nullable=False, server_default="v1"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("aggregate_type", sa.String(length=100), nullable=False),
        sa.Column("producer", sa.String(length=100), nullable=False),
        sa.Column("consumers", sa.JSON(), nullable=False),
        sa.Column("sensitivity", sa.String(length=50), nullable=False, server_default="INTERNAL"),
        sa.Column("retention_policy", sa.String(length=100), nullable=False, server_default="90_DAYS"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_name"),
    )
    op.create_index("ix_event_registry_items_event_name", "event_registry_items", ["event_name"])
    op.create_index("ix_event_registry_items_aggregate_type", "event_registry_items", ["aggregate_type"])

    op.create_table(
        "event_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("payload_schema", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["event_id"], ["event_registry_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_event_versions_event_id", "event_versions", ["event_id"])

    # 2. Event Outbox & Inbox
    op.create_table(
        "event_outbox",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_id", sa.String(length=100), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("event_version", sa.String(length=20), nullable=False, server_default="v1"),
        sa.Column("aggregate_type", sa.String(length=100), nullable=False),
        sa.Column("aggregate_id", sa.String(length=100), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("correlation_id", sa.String(length=100), nullable=False),
        sa.Column("causation_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("next_attempt_at", sa.DateTime(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )
    op.create_index("ix_event_outbox_event_id", "event_outbox", ["event_id"])
    op.create_index("ix_event_outbox_event_type", "event_outbox", ["event_type"])
    op.create_index("ix_event_outbox_aggregate_type", "event_outbox", ["aggregate_type"])
    op.create_index("ix_event_outbox_aggregate_id", "event_outbox", ["aggregate_id"])
    op.create_index("ix_event_outbox_tenant_id", "event_outbox", ["tenant_id"])
    op.create_index("ix_event_outbox_correlation_id", "event_outbox", ["correlation_id"])
    op.create_index("ix_event_outbox_status", "event_outbox", ["status"])
    op.create_index("ix_event_outbox_created_at", "event_outbox", ["created_at"])

    op.create_table(
        "event_inbox",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_id", sa.String(length=100), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("consumer_name", sa.String(length=100), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PROCESSED"),
        sa.Column("processed_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_event_inbox_event_id", "event_inbox", ["event_id"])
    op.create_index("ix_event_inbox_event_type", "event_inbox", ["event_type"])
    op.create_index("ix_event_inbox_consumer_name", "event_inbox", ["consumer_name"])
    op.create_index("ix_event_inbox_tenant_id", "event_inbox", ["tenant_id"])
    op.create_index("ix_event_inbox_dedup", "event_inbox", ["event_id", "consumer_name"], unique=True)

    op.create_table(
        "event_delivery_attempts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("outbox_id", sa.String(length=36), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SUCCESS"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("attempted_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["outbox_id"], ["event_outbox.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_event_delivery_attempts_outbox_id", "event_delivery_attempts", ["outbox_id"])

    op.create_table(
        "event_subscriptions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("handler_name", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_event_subscriptions_tenant_id", "event_subscriptions", ["tenant_id"])
    op.create_index("ix_event_subscriptions_event_type", "event_subscriptions", ["event_type"])

    op.create_table(
        "dead_letter_messages",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("event_id", sa.String(length=100), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("workflow_id", sa.String(length=100), nullable=True),
        sa.Column("consumer", sa.String(length=100), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("failure_type", sa.String(length=100), nullable=False),
        sa.Column("error_summary", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
        sa.Column("last_error_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_dead_letter_messages_event_id", "dead_letter_messages", ["event_id"])
    op.create_index("ix_dead_letter_messages_event_type", "dead_letter_messages", ["event_type"])
    op.create_index("ix_dead_letter_messages_workflow_id", "dead_letter_messages", ["workflow_id"])
    op.create_index("ix_dead_letter_messages_status", "dead_letter_messages", ["status"])
    op.create_index("ix_dead_letter_messages_created_at", "dead_letter_messages", ["created_at"])

    op.create_table(
        "event_replays",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("filter_criteria", sa.JSON(), nullable=False),
        sa.Column("replay_mode", sa.String(length=50), nullable=False, server_default="DRY_RUN"),
        sa.Column("events_replayed_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("triggered_by", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="COMPLETED"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_event_replays_tenant_id", "event_replays", ["tenant_id"])
    op.create_index("ix_event_replays_event_type", "event_replays", ["event_type"])

    # 3. Workflow Definitions & Versions
    op.create_table(
        "workflow_definitions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("current_version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_workflow_definitions_tenant_id", "workflow_definitions", ["tenant_id"])
    op.create_index("ix_workflow_definitions_name", "workflow_definitions", ["name"])
    op.create_index("ix_workflow_definitions_category", "workflow_definitions", ["category"])

    op.create_table(
        "workflow_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workflow_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("steps_config", sa.JSON(), nullable=False),
        sa.Column("transitions_config", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflow_definitions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_versions_workflow_id", "workflow_versions", ["workflow_id"])

    op.create_table(
        "workflow_steps",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workflow_version_id", sa.String(length=36), nullable=False),
        sa.Column("step_key", sa.String(length=100), nullable=False),
        sa.Column("step_type", sa.String(length=50), nullable=False, server_default="AGENT_TASK"),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("timeout_seconds", sa.Integer(), nullable=False, server_default="3600"),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["workflow_version_id"], ["workflow_versions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_steps_workflow_version_id", "workflow_steps", ["workflow_version_id"])

    op.create_table(
        "workflow_transitions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workflow_version_id", sa.String(length=36), nullable=False),
        sa.Column("from_step_key", sa.String(length=100), nullable=False),
        sa.Column("to_step_key", sa.String(length=100), nullable=False),
        sa.Column("condition", sa.String(length=255), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="true"),
        sa.ForeignKeyConstraint(["workflow_version_id"], ["workflow_versions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_transitions_workflow_version_id", "workflow_transitions", ["workflow_version_id"])

    # 4. Workflow Runs, Steps & Wait States
    op.create_table(
        "workflow_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_key", sa.String(length=100), nullable=False),
        sa.Column("workflow_version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("trigger_type", sa.String(length=50), nullable=False, server_default="EVENT"),
        sa.Column("trigger_reference", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="CREATED"),
        sa.Column("current_step", sa.String(length=100), nullable=True),
        sa.Column("correlation_id", sa.String(length=100), nullable=False),
        sa.Column("input_data", sa.JSON(), nullable=False),
        sa.Column("output_data", sa.JSON(), nullable=False),
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("paused_at", sa.DateTime(), nullable=True),
        sa.Column("failed_at", sa.DateTime(), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_runs_tenant_id", "workflow_runs", ["tenant_id"])
    op.create_index("ix_workflow_runs_workflow_key", "workflow_runs", ["workflow_key"])
    op.create_index("ix_workflow_runs_status", "workflow_runs", ["status"])
    op.create_index("ix_workflow_runs_correlation_id", "workflow_runs", ["correlation_id"])
    op.create_index("ix_workflow_runs_started_at", "workflow_runs", ["started_at"])

    op.create_table(
        "workflow_run_steps",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("step_key", sa.String(length=100), nullable=False),
        sa.Column("step_type", sa.String(length=50), nullable=False, server_default="AGENT_TASK"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("duration_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("input_data", sa.JSON(), nullable=False),
        sa.Column("output_data", sa.JSON(), nullable=False),
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_run_steps_workflow_run_id", "workflow_run_steps", ["workflow_run_id"])
    op.create_index("ix_workflow_run_steps_step_key", "workflow_run_steps", ["step_key"])
    op.create_index("ix_workflow_run_steps_status", "workflow_run_steps", ["status"])

    op.create_table(
        "workflow_run_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("event_id", sa.String(length=100), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("step_key", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_run_events_workflow_run_id", "workflow_run_events", ["workflow_run_id"])
    op.create_index("ix_workflow_run_events_event_id", "workflow_run_events", ["event_id"])
    op.create_index("ix_workflow_run_events_event_type", "workflow_run_events", ["event_type"])

    op.create_table(
        "workflow_wait_states",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("step_key", sa.String(length=100), nullable=False),
        sa.Column("wait_type", sa.String(length=50), nullable=False, server_default="HUMAN_APPROVAL"),
        sa.Column("condition_data", sa.JSON(), nullable=False),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="WAITING"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_wait_states_workflow_run_id", "workflow_wait_states", ["workflow_run_id"])

    # 5. Tasks, Locks, Human Queue & Approvals
    op.create_table(
        "workflow_tasks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("step_key", sa.String(length=100), nullable=False),
        sa.Column("task_type", sa.String(length=50), nullable=False, server_default="AGENT_TASK"),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="NORMAL"),
        sa.Column("queue_name", sa.String(length=100), nullable=False, server_default="default"),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="QUEUED"),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("current_attempt", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("scheduled_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_tasks_tenant_id", "workflow_tasks", ["tenant_id"])
    op.create_index("ix_workflow_tasks_workflow_run_id", "workflow_tasks", ["workflow_run_id"])
    op.create_index("ix_workflow_tasks_priority", "workflow_tasks", ["priority"])
    op.create_index("ix_workflow_tasks_status", "workflow_tasks", ["status"])
    op.create_index("ix_workflow_tasks_scheduled_at", "workflow_tasks", ["scheduled_at"])

    op.create_table(
        "workflow_task_attempts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("task_id", sa.String(length=36), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SUCCESS"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("attempted_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["task_id"], ["workflow_tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_task_attempts_task_id", "workflow_task_attempts", ["task_id"])

    op.create_table(
        "workflow_task_locks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("lock_key", sa.String(length=255), nullable=False),
        sa.Column("owner_id", sa.String(length=100), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("lock_key"),
    )
    op.create_index("ix_workflow_task_locks_lock_key", "workflow_task_locks", ["lock_key"])
    op.create_index("ix_workflow_task_locks_expires_at", "workflow_task_locks", ["expires_at"])

    op.create_table(
        "human_tasks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("step_key", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("task_type", sa.String(length=100), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="HIGH"),
        sa.Column("assigned_to", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PENDING"),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("input_data", sa.JSON(), nullable=False),
        sa.Column("decision", sa.String(length=50), nullable=True),
        sa.Column("decision_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_human_tasks_tenant_id", "human_tasks", ["tenant_id"])
    op.create_index("ix_human_tasks_workflow_run_id", "human_tasks", ["workflow_run_id"])
    op.create_index("ix_human_tasks_task_type", "human_tasks", ["task_type"])
    op.create_index("ix_human_tasks_priority", "human_tasks", ["priority"])
    op.create_index("ix_human_tasks_status", "human_tasks", ["status"])
    op.create_index("ix_human_tasks_created_at", "human_tasks", ["created_at"])

    op.create_table(
        "workflow_approvals",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("step_key", sa.String(length=100), nullable=False),
        sa.Column("approved_by", sa.String(length=100), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_approvals_tenant_id", "workflow_approvals", ["tenant_id"])
    op.create_index("ix_workflow_approvals_workflow_run_id", "workflow_approvals", ["workflow_run_id"])

    op.create_table(
        "workflow_cancellations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_run_id", sa.String(length=36), nullable=False),
        sa.Column("cancelled_by", sa.String(length=100), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_cancellations_tenant_id", "workflow_cancellations", ["tenant_id"])
    op.create_index("ix_workflow_cancellations_workflow_run_id", "workflow_cancellations", ["workflow_run_id"])

    # 6. Automation Rules & Schedules
    op.create_table(
        "automation_rules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("trigger_type", sa.String(length=50), nullable=False, server_default="EVENT"),
        sa.Column("trigger_config", sa.JSON(), nullable=False),
        sa.Column("condition_config", sa.JSON(), nullable=False),
        sa.Column("action_config", sa.JSON(), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False, server_default="NORMAL"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("requires_human_approval", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_automation_rules_tenant_id", "automation_rules", ["tenant_id"])
    op.create_index("ix_automation_rules_enabled", "automation_rules", ["enabled"])

    op.create_table(
        "automation_rule_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("rule_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("trigger_config", sa.JSON(), nullable=False),
        sa.Column("condition_config", sa.JSON(), nullable=False),
        sa.Column("action_config", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["rule_id"], ["automation_rules.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_automation_rule_versions_rule_id", "automation_rule_versions", ["rule_id"])

    op.create_table(
        "automation_rule_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("rule_id", sa.String(length=36), nullable=False),
        sa.Column("trigger_event_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SUCCESS"),
        sa.Column("result_summary", sa.Text(), nullable=False),
        sa.Column("executed_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["rule_id"], ["automation_rules.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_automation_rule_runs_tenant_id", "automation_rule_runs", ["tenant_id"])
    op.create_index("ix_automation_rule_runs_rule_id", "automation_rule_runs", ["rule_id"])
    op.create_index("ix_automation_rule_runs_trigger_event_id", "automation_rule_runs", ["trigger_event_id"])
    op.create_index("ix_automation_rule_runs_executed_at", "automation_rule_runs", ["executed_at"])

    op.create_table(
        "workflow_schedules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_key", sa.String(length=100), nullable=False),
        sa.Column("cron_expression", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("next_run_at", sa.DateTime(), nullable=True),
        sa.Column("last_run_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_schedules_tenant_id", "workflow_schedules", ["tenant_id"])
    op.create_index("ix_workflow_schedules_workflow_key", "workflow_schedules", ["workflow_key"])
    op.create_index("ix_workflow_schedules_is_active", "workflow_schedules", ["is_active"])
    op.create_index("ix_workflow_schedules_next_run_at", "workflow_schedules", ["next_run_at"])


def downgrade() -> None:
    op.drop_table("workflow_schedules")
    op.drop_table("automation_rule_runs")
    op.drop_table("automation_rule_versions")
    op.drop_table("automation_rules")
    op.drop_table("workflow_cancellations")
    op.drop_table("workflow_approvals")
    op.drop_table("human_tasks")
    op.drop_table("workflow_task_locks")
    op.drop_table("workflow_task_attempts")
    op.drop_table("workflow_tasks")
    op.drop_table("workflow_wait_states")
    op.drop_table("workflow_run_events")
    op.drop_table("workflow_run_steps")
    op.drop_table("workflow_runs")
    op.drop_table("workflow_transitions")
    op.drop_table("workflow_steps")
    op.drop_table("workflow_versions")
    op.drop_table("workflow_definitions")
    op.drop_table("event_replays")
    op.drop_table("dead_letter_messages")
    op.drop_table("event_subscriptions")
    op.drop_table("event_delivery_attempts")
    op.drop_table("event_inbox")
    op.drop_table("event_outbox")
    op.drop_table("event_versions")
    op.drop_table("event_registry_items")
