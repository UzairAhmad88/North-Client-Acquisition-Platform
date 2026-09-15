"""add_qa_uat_handover_tables

Revision ID: 023
Revises: 022
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "023"
down_revision = "022"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Test Plans
    op.create_table(
        "test_plans",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("plan_type", sa.String(length=64), nullable=False, server_default="SYSTEM"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DRAFT"),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_plans_project_id"), "test_plans", ["project_id"], unique=False)
    op.create_index(op.f("ix_test_plans_status"), "test_plans", ["status"], unique=False)

    # 2. Test Cases
    op.create_table(
        "test_cases",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("test_plan_id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("requirement_id", sa.String(length=36), nullable=True),
        sa.Column("deliverable_id", sa.String(length=36), nullable=True),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="FUNCTIONAL"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("execution_type", sa.String(length=32), nullable=False, server_default="MANUAL"),
        sa.Column("preconditions", sa.Text(), nullable=True),
        sa.Column("steps", sa.JSON(), nullable=True),
        sa.Column("expected_results", sa.Text(), nullable=False),
        sa.Column("is_regression", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["test_plan_id"], ["test_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_test_cases_test_plan_id"), "test_cases", ["test_plan_id"], unique=False)
    op.create_index(op.f("ix_test_cases_code"), "test_cases", ["code"], unique=True)

    # 3. Test Runs
    op.create_table(
        "test_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("test_plan_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("environment", sa.String(length=64), nullable=False, server_default="STAGING"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="PLANNED"),
        sa.Column("executed_by", sa.String(length=255), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("passed_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("blocked_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("skipped_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["test_plan_id"], ["test_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_runs_project_id"), "test_runs", ["project_id"], unique=False)
    op.create_index(op.f("ix_test_runs_test_plan_id"), "test_runs", ["test_plan_id"], unique=False)

    # 4. Test Results
    op.create_table(
        "test_results",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("test_run_id", sa.String(length=36), nullable=False),
        sa.Column("test_case_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="UNTESTED"),
        sa.Column("actual_results", sa.Text(), nullable=True),
        sa.Column("execution_notes", sa.Text(), nullable=True),
        sa.Column("executed_by", sa.String(length=255), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["test_run_id"], ["test_runs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["test_case_id"], ["test_cases.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_test_results_test_run_id"), "test_results", ["test_run_id"], unique=False)

    # 5. Test Evidence
    op.create_table(
        "test_evidence",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("test_result_id", sa.String(length=36), nullable=False),
        sa.Column("evidence_type", sa.String(length=32), nullable=False, server_default="SCREENSHOT"),
        sa.Column("file_path", sa.String(length=512), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sha256_hash", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["test_result_id"], ["test_results.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 6. Defects
    op.create_table(
        "defects",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("defect_number", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("test_case_id", sa.String(length=36), nullable=True),
        sa.Column("test_run_id", sa.String(length=36), nullable=True),
        sa.Column("deliverable_id", sa.String(length=36), nullable=True),
        sa.Column("requirement_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="OPEN"),
        sa.Column("classification", sa.String(length=32), nullable=False, server_default="DEFECT"),
        sa.Column("reported_by", sa.String(length=255), nullable=False),
        sa.Column("assigned_to", sa.String(length=255), nullable=True),
        sa.Column("resolution_summary", sa.Text(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["test_case_id"], ["test_cases.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["test_run_id"], ["test_runs.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("defect_number"),
    )
    op.create_index(op.f("ix_defects_defect_number"), "defects", ["defect_number"], unique=True)
    op.create_index(op.f("ix_defects_project_id"), "defects", ["project_id"], unique=False)
    op.create_index(op.f("ix_defects_status"), "defects", ["status"], unique=False)

    # 7. UAT Sessions
    op.create_table(
        "uat_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("client_account_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("scope_description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PREPARING"),
        sa.Column("scheduled_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_by_client", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("client_signoff_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["client_account_id"], ["client_accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_uat_sessions_project_id"), "uat_sessions", ["project_id"], unique=False)

    # 8. UAT Feedback
    op.create_table(
        "uat_feedback",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("uat_session_id", sa.String(length=36), nullable=False),
        sa.Column("deliverable_id", sa.String(length=36), nullable=True),
        sa.Column("feedback_type", sa.String(length=32), nullable=False, server_default="COMMENT"),
        sa.Column("comments", sa.Text(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("submitted_by", sa.String(length=255), nullable=False),
        sa.Column("defect_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["uat_session_id"], ["uat_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["defect_id"], ["defects.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 9. Acceptance Criteria
    op.create_table(
        "acceptance_criteria",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("deliverable_id", sa.String(length=36), nullable=True),
        sa.Column("criterion_text", sa.Text(), nullable=False),
        sa.Column("is_met", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("verified_by", sa.String(length=255), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["project_deliverables.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 10. Release Versions
    op.create_table(
        "release_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("version_tag", sa.String(length=64), nullable=False),
        sa.Column("target_environment", sa.String(length=64), nullable=False, server_default="PRODUCTION"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="DRAFT"),
        sa.Column("release_notes", sa.Text(), nullable=True),
        sa.Column("qa_approval_status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("client_approval_status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("released_by", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_release_versions_project_id"), "release_versions", ["project_id"], unique=False)

    # 11. Delivery Packages
    op.create_table(
        "delivery_packages",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("release_version_id", sa.String(length=36), nullable=True),
        sa.Column("package_name", sa.String(length=255), nullable=False),
        sa.Column("storage_url", sa.String(length=512), nullable=False),
        sa.Column("sha256_hash", sa.String(length=64), nullable=False),
        sa.Column("file_size_bytes", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["release_version_id"], ["release_versions.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 12. Handover Checklists
    op.create_table(
        "handover_checklists",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("code_repository_transferred", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("documentation_delivered", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("credentials_transferred", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("training_completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("deployment_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="IN_PROGRESS"),
        sa.Column("signed_off_by_client", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("client_signoff_hash", sa.String(length=64), nullable=True),
        sa.Column("signed_off_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id"),
    )

    # 13. QA Events
    op.create_table(
        "qa_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=255), nullable=False),
        sa.Column("actor_type", sa.String(length=32), nullable=False, server_default="USER"),
        sa.Column("event_data", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_qa_events_project_id"), "qa_events", ["project_id"], unique=False)


def downgrade() -> None:
    op.drop_table("qa_events")
    op.drop_table("handover_checklists")
    op.drop_table("delivery_packages")
    op.drop_table("release_versions")
    op.drop_table("acceptance_criteria")
    op.drop_table("uat_feedback")
    op.drop_table("uat_sessions")
    op.drop_table("defects")
    op.drop_table("test_evidence")
    op.drop_table("test_results")
    op.drop_table("test_runs")
    op.drop_table("test_cases")
    op.drop_table("test_plans")
