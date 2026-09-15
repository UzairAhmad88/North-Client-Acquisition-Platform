"""add_project_estimation_tables

Revision ID: 018
Revises: 017
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "018"
down_revision = "017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Project Estimates Table
    op.create_table(
        "project_estimates",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DRAFT"),
        sa.Column("complexity", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("estimated_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("minimum_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("maximum_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("risk_buffer_percent", sa.Float(), nullable=False, server_default="20.0"),
        sa.Column("internal_cost", sa.Float(), nullable=True),
        sa.Column("external_cost", sa.Float(), nullable=True),
        sa.Column("recommended_min", sa.Float(), nullable=True),
        sa.Column("recommended_max", sa.Float(), nullable=True),
        sa.Column("requirements_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("solution_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("pricing_policy_version", sa.String(length=32), nullable=False, server_default="v1.0"),
        sa.Column("cost_model_version", sa.String(length=32), nullable=False, server_default="v1.0"),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("approved_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["approved_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_estimates_solution_id"), "project_estimates", ["solution_id"], unique=False)
    op.create_index(op.f("ix_project_estimates_business_id"), "project_estimates", ["business_id"], unique=False)
    op.create_index(op.f("ix_project_estimates_lead_id"), "project_estimates", ["lead_id"], unique=False)
    op.create_index(op.f("ix_project_estimates_status"), "project_estimates", ["status"], unique=False)

    # 2. Estimate Work Items Table
    op.create_table(
        "estimate_work_items",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("estimate_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("requirement_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("feature_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="BACKEND"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("complexity", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("optimistic_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("most_likely_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("pessimistic_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("expected_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["estimate_id"], ["project_estimates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["feature_id"], ["solution_features.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_estimate_work_items_estimate_id"), "estimate_work_items", ["estimate_id"], unique=False)
    op.create_index(op.f("ix_estimate_work_items_category"), "estimate_work_items", ["category"], unique=False)

    # 3. Estimate Cost Items Table
    op.create_table(
        "estimate_cost_items",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("estimate_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("cost_type", sa.String(length=64), nullable=False, server_default="INTERNAL"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("source", sa.String(length=64), nullable=False, server_default="CONFIGURED_RATE"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["estimate_id"], ["project_estimates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_estimate_cost_items_estimate_id"), "estimate_cost_items", ["estimate_id"], unique=False)
    op.create_index(op.f("ix_estimate_cost_items_cost_type"), "estimate_cost_items", ["cost_type"], unique=False)

    # 4. Estimate Scenarios Table
    op.create_table(
        "estimate_scenarios",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("estimate_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("scope", sa.Text(), nullable=False),
        sa.Column("estimated_hours", sa.Float(), nullable=False),
        sa.Column("internal_cost", sa.Float(), nullable=True),
        sa.Column("external_cost", sa.Float(), nullable=True),
        sa.Column("recommended_min", sa.Float(), nullable=True),
        sa.Column("recommended_max", sa.Float(), nullable=True),
        sa.Column("risk_level", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PROPOSED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["estimate_id"], ["project_estimates.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_estimate_scenarios_estimate_id"), "estimate_scenarios", ["estimate_id"], unique=False)

    # 5. Estimate Versions Table
    op.create_table(
        "estimate_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("estimate_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["estimate_id"], ["project_estimates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_estimate_versions_estimate_id"), "estimate_versions", ["estimate_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_estimate_versions_estimate_id"), table_name="estimate_versions")
    op.drop_table("estimate_versions")
    op.drop_index(op.f("ix_estimate_scenarios_estimate_id"), table_name="estimate_scenarios")
    op.drop_table("estimate_scenarios")
    op.drop_index(op.f("ix_estimate_cost_items_cost_type"), table_name="estimate_cost_items")
    op.drop_index(op.f("ix_estimate_cost_items_estimate_id"), table_name="estimate_cost_items")
    op.drop_table("estimate_cost_items")
    op.drop_index(op.f("ix_estimate_work_items_category"), table_name="estimate_work_items")
    op.drop_index(op.f("ix_estimate_work_items_estimate_id"), table_name="estimate_work_items")
    op.drop_table("estimate_work_items")
    op.drop_index(op.f("ix_project_estimates_status"), table_name="project_estimates")
    op.drop_index(op.f("ix_project_estimates_lead_id"), table_name="project_estimates")
    op.drop_index(op.f("ix_project_estimates_business_id"), table_name="project_estimates")
    op.drop_index(op.f("ix_project_estimates_solution_id"), table_name="project_estimates")
    op.drop_table("project_estimates")
