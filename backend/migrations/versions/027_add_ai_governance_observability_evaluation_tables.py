"""add_ai_governance_observability_evaluation_tables

Revision ID: 027
Revises: 026
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "027"
down_revision = "026"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Tracing & Spans
    op.create_table(
        "ai_traces",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("workflow_id", sa.String(length=100), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=True),
        sa.Column("lead_id", sa.String(length=36), nullable=True),
        sa.Column("agent_id", sa.String(length=100), nullable=False),
        sa.Column("agent_version", sa.String(length=20), nullable=False),
        sa.Column("model_id", sa.String(length=100), nullable=False),
        sa.Column("model_version", sa.String(length=20), nullable=False),
        sa.Column("prompt_version", sa.String(length=20), nullable=False),
        sa.Column("total_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_cost", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_duration_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="RUNNING"),
        sa.Column("started_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_traces_tenant_id", "ai_traces", ["tenant_id"])
    op.create_index("ix_ai_traces_workflow_id", "ai_traces", ["workflow_id"])
    op.create_index("ix_ai_traces_project_id", "ai_traces", ["project_id"])
    op.create_index("ix_ai_traces_lead_id", "ai_traces", ["lead_id"])
    op.create_index("ix_ai_traces_agent_id", "ai_traces", ["agent_id"])
    op.create_index("ix_ai_traces_status", "ai_traces", ["status"])
    op.create_index("ix_ai_traces_started_at", "ai_traces", ["started_at"])

    op.create_table(
        "ai_trace_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("trace_id", sa.String(length=36), nullable=False),
        sa.Column("span_type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("input_summary", sa.JSON(), nullable=False),
        sa.Column("output_summary", sa.JSON(), nullable=False),
        sa.Column("tokens_consumed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("duration_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SUCCESS"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["trace_id"], ["ai_traces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_trace_events_tenant_id", "ai_trace_events", ["tenant_id"])
    op.create_index("ix_ai_trace_events_trace_id", "ai_trace_events", ["trace_id"])

    # 2. Agent Versions & Deployments
    op.create_table(
        "agent_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("agent_key", sa.String(length=100), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("model_key", sa.String(length=100), nullable=False),
        sa.Column("prompt_version", sa.String(length=20), nullable=False),
        sa.Column("allowed_tools", sa.JSON(), nullable=False),
        sa.Column("permissions", sa.JSON(), nullable=False),
        sa.Column("configuration", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_versions_tenant_id", "agent_versions", ["tenant_id"])
    op.create_index("ix_agent_versions_agent_key", "agent_versions", ["agent_key"])

    op.create_table(
        "agent_deployments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("agent_key", sa.String(length=100), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DESIGN"),
        sa.Column("rollout_percentage", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("deployed_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("retired_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_deployments_tenant_id", "agent_deployments", ["tenant_id"])
    op.create_index("ix_agent_deployments_agent_key", "agent_deployments", ["agent_key"])
    op.create_index("ix_agent_deployments_status", "agent_deployments", ["status"])

    # 3. Prompt Registry & Versions
    op.create_table(
        "prompt_registry_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("prompt_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("agent_target", sa.String(length=100), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("current_version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("prompt_key"),
    )
    op.create_index("ix_prompt_registry_items_tenant_id", "prompt_registry_items", ["tenant_id"])
    op.create_index("ix_prompt_registry_items_prompt_key", "prompt_registry_items", ["prompt_key"])

    op.create_table(
        "prompt_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("prompt_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DRAFT"),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["prompt_id"], ["prompt_registry_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_prompt_versions_tenant_id", "prompt_versions", ["tenant_id"])
    op.create_index("ix_prompt_versions_prompt_id", "prompt_versions", ["prompt_id"])
    op.create_index("ix_prompt_versions_status", "prompt_versions", ["status"])

    # 4. Usage Records
    op.create_table(
        "model_usage_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("trace_id", sa.String(length=36), nullable=False),
        sa.Column("provider", sa.String(length=100), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("prompt_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("completion_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("estimated_cost", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("latency_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_usage_records_tenant_id", "model_usage_records", ["tenant_id"])
    op.create_index("ix_model_usage_records_trace_id", "model_usage_records", ["trace_id"])
    op.create_index("ix_model_usage_records_created_at", "model_usage_records", ["created_at"])

    op.create_table(
        "tool_usage_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("trace_id", sa.String(length=36), nullable=False),
        sa.Column("agent_id", sa.String(length=100), nullable=False),
        sa.Column("tool_name", sa.String(length=100), nullable=False),
        sa.Column("is_authorized", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("denial_reason", sa.String(length=255), nullable=True),
        sa.Column("latency_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="SUCCESS"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tool_usage_records_tenant_id", "tool_usage_records", ["tenant_id"])
    op.create_index("ix_tool_usage_records_trace_id", "tool_usage_records", ["trace_id"])
    op.create_index("ix_tool_usage_records_agent_id", "tool_usage_records", ["agent_id"])
    op.create_index("ix_tool_usage_records_tool_name", "tool_usage_records", ["tool_name"])
    op.create_index("ix_tool_usage_records_created_at", "tool_usage_records", ["created_at"])

    # 5. Evaluation Datasets, Cases & Runs
    op.create_table(
        "evaluation_datasets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("dataset_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("task_type", sa.String(length=100), nullable=False),
        sa.Column("is_golden", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dataset_key"),
    )
    op.create_index("ix_evaluation_datasets_tenant_id", "evaluation_datasets", ["tenant_id"])
    op.create_index("ix_evaluation_datasets_dataset_key", "evaluation_datasets", ["dataset_key"])
    op.create_index("ix_evaluation_datasets_task_type", "evaluation_datasets", ["task_type"])

    op.create_table(
        "evaluation_cases",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("dataset_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("input_context", sa.JSON(), nullable=False),
        sa.Column("expected_output", sa.JSON(), nullable=False),
        sa.Column("evaluation_criteria", sa.JSON(), nullable=False),
        sa.Column("difficulty", sa.String(length=50), nullable=False, server_default="MEDIUM"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["dataset_id"], ["evaluation_datasets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evaluation_cases_tenant_id", "evaluation_cases", ["tenant_id"])
    op.create_index("ix_evaluation_cases_dataset_id", "evaluation_cases", ["dataset_id"])

    op.create_table(
        "evaluation_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("dataset_id", sa.String(length=36), nullable=False),
        sa.Column("agent_key", sa.String(length=100), nullable=False),
        sa.Column("agent_version", sa.String(length=20), nullable=False),
        sa.Column("prompt_version", sa.String(length=20), nullable=False),
        sa.Column("model_version", sa.String(length=20), nullable=False),
        sa.Column("evaluation_type", sa.String(length=50), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("passed_cases_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_cases_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("regression_detected", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("regression_details", sa.JSON(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["dataset_id"], ["evaluation_datasets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evaluation_runs_tenant_id", "evaluation_runs", ["tenant_id"])
    op.create_index("ix_evaluation_runs_dataset_id", "evaluation_runs", ["dataset_id"])
    op.create_index("ix_evaluation_runs_agent_key", "evaluation_runs", ["agent_key"])

    # 6. Human Evaluation & Revisions
    op.create_table(
        "human_evaluations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("trace_id", sa.String(length=36), nullable=False),
        sa.Column("reviewer", sa.String(length=100), nullable=False),
        sa.Column("correctness_score", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("completeness_score", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("evidence_score", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("safety_score", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("usefulness_score", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_human_evaluations_tenant_id", "human_evaluations", ["tenant_id"])
    op.create_index("ix_human_evaluations_trace_id", "human_evaluations", ["trace_id"])

    op.create_table(
        "human_revision_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("trace_id", sa.String(length=36), nullable=False),
        sa.Column("agent_key", sa.String(length=100), nullable=False),
        sa.Column("edit_magnitude", sa.String(length=50), nullable=False),
        sa.Column("levenshtein_distance", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("similarity_score", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("operator", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_human_revision_records_tenant_id", "human_revision_records", ["tenant_id"])
    op.create_index("ix_human_revision_records_trace_id", "human_revision_records", ["trace_id"])
    op.create_index("ix_human_revision_records_agent_key", "human_revision_records", ["agent_key"])

    # 7. Failures, Incidents & Security
    op.create_table(
        "ai_failure_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("trace_id", sa.String(length=36), nullable=False),
        sa.Column("agent_key", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=False),
        sa.Column("context_data", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_failure_records_tenant_id", "ai_failure_records", ["tenant_id"])
    op.create_index("ix_ai_failure_records_trace_id", "ai_failure_records", ["trace_id"])
    op.create_index("ix_ai_failure_records_agent_key", "ai_failure_records", ["agent_key"])
    op.create_index("ix_ai_failure_records_created_at", "ai_failure_records", ["created_at"])

    op.create_table(
        "ai_incidents",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("incident_number", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="HIGH"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="DETECTED"),
        sa.Column("affected_agent", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("containment_action", sa.Text(), nullable=True),
        sa.Column("root_cause", sa.Text(), nullable=True),
        sa.Column("resolved_by", sa.String(length=100), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("incident_number"),
    )
    op.create_index("ix_ai_incidents_tenant_id", "ai_incidents", ["tenant_id"])
    op.create_index("ix_ai_incidents_incident_number", "ai_incidents", ["incident_number"])
    op.create_index("ix_ai_incidents_status", "ai_incidents", ["status"])
    op.create_index("ix_ai_incidents_created_at", "ai_incidents", ["created_at"])

    op.create_table(
        "ai_security_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("agent_key", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="HIGH"),
        sa.Column("action_taken", sa.String(length=50), nullable=False, server_default="BLOCKED"),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_security_events_tenant_id", "ai_security_events", ["tenant_id"])
    op.create_index("ix_ai_security_events_event_type", "ai_security_events", ["event_type"])
    op.create_index("ix_ai_security_events_created_at", "ai_security_events", ["created_at"])

    # 8. Budget Policies, Health Snapshots & Kill Switch
    op.create_table(
        "ai_budget_policies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("scope", sa.String(length=50), nullable=False, server_default="GLOBAL"),
        sa.Column("scope_key", sa.String(length=100), nullable=False, server_default="all"),
        sa.Column("daily_cost_limit", sa.Float(), nullable=False, server_default="50.0"),
        sa.Column("monthly_cost_limit", sa.Float(), nullable=False, server_default="500.0"),
        sa.Column("enforcement_action", sa.String(length=50), nullable=False, server_default="BLOCK"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_budget_policies_tenant_id", "ai_budget_policies", ["tenant_id"])

    op.create_table(
        "ai_health_snapshots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("agent_key", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="HEALTHY"),
        sa.Column("success_rate_pct", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("avg_latency_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("human_acceptance_pct", sa.Float(), nullable=False, server_default="100.0"),
        sa.Column("daily_cost_consumed", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("captured_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_health_snapshots_tenant_id", "ai_health_snapshots", ["tenant_id"])
    op.create_index("ix_ai_health_snapshots_agent_key", "ai_health_snapshots", ["agent_key"])
    op.create_index("ix_ai_health_snapshots_captured_at", "ai_health_snapshots", ["captured_at"])

    op.create_table(
        "ai_kill_switch_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("level", sa.String(length=50), nullable=False),
        sa.Column("target_key", sa.String(length=100), nullable=False, server_default="GLOBAL"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("activated_by", sa.String(length=100), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_kill_switch_events_tenant_id", "ai_kill_switch_events", ["tenant_id"])
    op.create_index("ix_ai_kill_switch_events_created_at", "ai_kill_switch_events", ["created_at"])

    # 9. Improvement Items & Technical Debt
    op.create_table(
        "ai_improvement_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("item_type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("evidence_reference", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="BACKLOG"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_improvement_items_tenant_id", "ai_improvement_items", ["tenant_id"])

    op.create_table(
        "ai_technical_debt_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("component", sa.String(length=100), nullable=False),
        sa.Column("debt_type", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="MEDIUM"),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_technical_debt_items_tenant_id", "ai_technical_debt_items", ["tenant_id"])


def downgrade() -> None:
    op.drop_table("ai_technical_debt_items")
    op.drop_table("ai_improvement_items")
    op.drop_table("ai_kill_switch_events")
    op.drop_table("ai_health_snapshots")
    op.drop_table("ai_budget_policies")
    op.drop_table("ai_security_events")
    op.drop_table("ai_incidents")
    op.drop_table("ai_failure_records")
    op.drop_table("human_revision_records")
    op.drop_table("human_evaluations")
    op.drop_table("evaluation_runs")
    op.drop_table("evaluation_cases")
    op.drop_table("evaluation_datasets")
    op.drop_table("tool_usage_records")
    op.drop_table("model_usage_records")
    op.drop_table("prompt_versions")
    op.drop_table("prompt_registry_items")
    op.drop_table("agent_deployments")
    op.drop_table("agent_versions")
    op.drop_table("ai_trace_events")
    op.drop_table("ai_traces")
