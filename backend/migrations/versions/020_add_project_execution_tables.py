"""add_project_execution_tables

Revision ID: 020
Revises: 019
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "020"
down_revision = "019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Projects Table
    op.create_table(
        "projects",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_number", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("client_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("baseline_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("owner_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="INITIATED"),
        sa.Column("health", sa.String(length=32), nullable=False, server_default="HEALTHY"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("planned_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("planned_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("progress_percent", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_estimated_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("total_actual_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["client_id"], ["leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["baseline_id"], ["contract_baselines.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_number"),
    )
    op.create_index(op.f("ix_projects_business_id"), "projects", ["business_id"], unique=False)
    op.create_index(op.f("ix_projects_client_id"), "projects", ["client_id"], unique=False)
    op.create_index(op.f("ix_projects_contract_id"), "projects", ["contract_id"], unique=False)
    op.create_index(op.f("ix_projects_baseline_id"), "projects", ["baseline_id"], unique=False)
    op.create_index(op.f("ix_projects_owner_id"), "projects", ["owner_id"], unique=False)
    op.create_index(op.f("ix_projects_project_number"), "projects", ["project_number"], unique=True)
    op.create_index(op.f("ix_projects_status"), "projects", ["status"], unique=False)
    op.create_index(op.f("ix_projects_health"), "projects", ["health"], unique=False)

    # 2. Project Members Table
    op.create_table(
        "project_members",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False, server_default="DEVELOPER"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_members_project_id"), "project_members", ["project_id"], unique=False)
    op.create_index(op.f("ix_project_members_user_id"), "project_members", ["user_id"], unique=False)

    # 3. Project Milestones Table
    op.create_table(
        "project_milestones",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("target_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="UPCOMING"),
        sa.Column("progress_percent", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("owner_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_milestones_project_id"), "project_milestones", ["project_id"], unique=False)
    op.create_index(op.f("ix_project_milestones_status"), "project_milestones", ["status"], unique=False)

    # 4. Project Deliverables Table
    op.create_table(
        "project_deliverables",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source_baseline_item", sa.String(length=255), nullable=False),
        sa.Column("acceptance_criteria", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("owner_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("target_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_deliverables_project_id"), "project_deliverables", ["project_id"], unique=False)
    op.create_index(op.f("ix_project_deliverables_status"), "project_deliverables", ["status"], unique=False)

    # 5. Project Tasks Table
    op.create_table(
        "project_tasks",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("parent_task_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("deliverable_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("milestone_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("task_number", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="TODO"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("assignee_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("planned_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("planned_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("estimated_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("actual_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("progress_percent", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("dependency_status", sa.String(length=32), nullable=False, server_default="CLEAR"),
        sa.Column("blocked_reason", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_task_id"], ["project_tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["milestone_id"], ["project_milestones.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["assignee_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_tasks_project_id"), "project_tasks", ["project_id"], unique=False)
    op.create_index(op.f("ix_project_tasks_parent_task_id"), "project_tasks", ["parent_task_id"], unique=False)
    op.create_index(op.f("ix_project_tasks_deliverable_id"), "project_tasks", ["deliverable_id"], unique=False)
    op.create_index(op.f("ix_project_tasks_milestone_id"), "project_tasks", ["milestone_id"], unique=False)
    op.create_index(op.f("ix_project_tasks_assignee_id"), "project_tasks", ["assignee_id"], unique=False)
    op.create_index(op.f("ix_project_tasks_task_number"), "project_tasks", ["task_number"], unique=False)
    op.create_index(op.f("ix_project_tasks_status"), "project_tasks", ["status"], unique=False)

    # 6. Task Dependencies Table
    op.create_table(
        "task_dependencies",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("predecessor_task_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("successor_task_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("dependency_type", sa.String(length=32), nullable=False, server_default="FINISH_TO_START"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["predecessor_task_id"], ["project_tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["successor_task_id"], ["project_tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_task_dependencies_project_id"), "task_dependencies", ["project_id"], unique=False)
    op.create_index(op.f("ix_task_dependencies_predecessor_task_id"), "task_dependencies", ["predecessor_task_id"], unique=False)
    op.create_index(op.f("ix_task_dependencies_successor_task_id"), "task_dependencies", ["successor_task_id"], unique=False)

    # 7. Project Risks Table
    op.create_table(
        "project_risks",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("probability", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("impact", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("mitigation_plan", sa.Text(), nullable=False),
        sa.Column("owner_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="IDENTIFIED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_risks_project_id"), "project_risks", ["project_id"], unique=False)

    # 8. Project Blockers Table
    op.create_table(
        "project_blockers",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("task_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("owner_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="OPEN"),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task_id"], ["project_tasks.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_blockers_project_id"), "project_blockers", ["project_id"], unique=False)

    # 9. Client Dependencies Table
    op.create_table(
        "client_dependencies",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("required_by_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="REQUESTED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_dependencies_project_id"), "client_dependencies", ["project_id"], unique=False)
    op.create_index(op.f("ix_client_dependencies_status"), "client_dependencies", ["status"], unique=False)

    # 10. Project Assumptions Table
    op.create_table(
        "project_assumptions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("statement", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="VALID"),
        sa.Column("invalidation_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_assumptions_project_id"), "project_assumptions", ["project_id"], unique=False)

    # 11. Project Scope Signals Table
    op.create_table(
        "project_scope_signals",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("signal_type", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="DETECTED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_scope_signals_project_id"), "project_scope_signals", ["project_id"], unique=False)

    # 12. Effort Entries Table
    op.create_table(
        "effort_entries",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("task_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("log_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("hours", sa.Float(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False, server_default="MANUAL"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task_id"], ["project_tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_effort_entries_project_id"), "effort_entries", ["project_id"], unique=False)
    op.create_index(op.f("ix_effort_entries_task_id"), "effort_entries", ["task_id"], unique=False)
    op.create_index(op.f("ix_effort_entries_user_id"), "effort_entries", ["user_id"], unique=False)

    # 13. Project Health Snapshots Table
    op.create_table(
        "project_health_snapshots",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("project_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("health", sa.String(length=32), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("schedule_variance_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("effort_variance_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("overdue_task_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("blocked_task_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unresolved_blocker_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_health_snapshots_project_id"), "project_health_snapshots", ["project_id"], unique=False)


def downgrade() -> None:
    op.drop_table("project_health_snapshots")
    op.drop_table("effort_entries")
    op.drop_table("project_scope_signals")
    op.drop_table("project_assumptions")
    op.drop_table("client_dependencies")
    op.drop_table("project_blockers")
    op.drop_table("project_risks")
    op.drop_table("task_dependencies")
    op.drop_table("project_tasks")
    op.drop_table("project_deliverables")
    op.drop_table("project_milestones")
    op.drop_table("project_members")
    op.drop_table("projects")
