"""add_change_management_tables

Revision ID: 022
Revises: 021
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "022"
down_revision = "021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Change Requests
    op.create_table(
        "change_requests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_number", sa.String(length=32), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("business_id", sa.String(length=36), nullable=True),
        sa.Column("client_id", sa.String(length=36), nullable=True),
        sa.Column("contract_id", sa.String(length=36), nullable=True),
        sa.Column("baseline_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="SCOPE"),
        sa.Column("classification", sa.String(length=64), nullable=False, server_default="UNKNOWN"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="REQUESTED"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("source", sa.String(length=64), nullable=False, server_default="CLIENT_PORTAL"),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("requested_by", sa.String(length=255), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("impact_status", sa.String(length=64), nullable=False, server_default="NOT_STARTED"),
        sa.Column("approval_status", sa.String(length=64), nullable=False, server_default="PENDING"),
        sa.Column("client_approval_status", sa.String(length=64), nullable=False, server_default="PENDING"),
        sa.Column("implementation_status", sa.String(length=64), nullable=False, server_default="NOT_STARTED"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["client_id"], ["client_accounts.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["baseline_id"], ["contract_baselines.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("change_number"),
    )
    op.create_index(op.f("ix_change_requests_change_number"), "change_requests", ["change_number"], unique=True)
    op.create_index(op.f("ix_change_requests_project_id"), "change_requests", ["project_id"], unique=False)
    op.create_index(op.f("ix_change_requests_status"), "change_requests", ["status"], unique=False)

    # 2. Change Request Versions
    op.create_table(
        "change_request_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("scope_summary", sa.Text(), nullable=True),
        sa.Column("commercial_summary", sa.Text(), nullable=True),
        sa.Column("schedule_summary", sa.Text(), nullable=True),
        sa.Column("impact_summary", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_id"], ["change_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_change_request_versions_change_request_id"), "change_request_versions", ["change_request_id"], unique=False)

    # 3. Change Evidence
    op.create_table(
        "change_evidence",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_id", sa.String(length=36), nullable=False),
        sa.Column("source_type", sa.String(length=64), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=False),
        sa.Column("source_version", sa.String(length=64), nullable=True),
        sa.Column("evidence_excerpt", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_id"], ["change_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_change_evidence_change_request_id"), "change_evidence", ["change_request_id"], unique=False)

    # 4. Change Impacts
    op.create_table(
        "change_impacts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_version_id", sa.String(length=36), nullable=False),
        sa.Column("impact_type", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=True),
        sa.Column("entity_id", sa.String(length=255), nullable=True),
        sa.Column("impact_action", sa.String(length=32), nullable=False, server_default="AFFECTED"),
        sa.Column("impact_description", sa.Text(), nullable=False),
        sa.Column("confidence", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("evidence_reference", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_version_id"], ["change_request_versions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_change_impacts_change_request_version_id"), "change_impacts", ["change_request_version_id"], unique=False)

    # 5. Change Estimates
    op.create_table(
        "change_estimates",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_version_id", sa.String(length=36), nullable=False),
        sa.Column("estimate_version_id", sa.String(length=36), nullable=True),
        sa.Column("optimistic_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("most_likely_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("pessimistic_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("expected_hours", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.85"),
        sa.Column("assumptions", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_version_id"], ["change_request_versions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["estimate_version_id"], ["estimate_versions.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 6. Change Commercials
    op.create_table(
        "change_commercials",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_version_id", sa.String(length=36), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="PKR"),
        sa.Column("original_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("change_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("revised_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("pricing_policy_version", sa.String(length=32), nullable=False, server_default="1.0"),
        sa.Column("estimate_version_id", sa.String(length=36), nullable=True),
        sa.Column("cost_model_version", sa.String(length=32), nullable=False, server_default="1.0"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="DRAFT"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_version_id"], ["change_request_versions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 7. Change Approvals
    op.create_table(
        "change_approvals",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_version_id", sa.String(length=36), nullable=False),
        sa.Column("approver_id", sa.String(length=255), nullable=False),
        sa.Column("approval_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="APPROVED"),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_version_id"], ["change_request_versions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 8. Change Baseline Links
    op.create_table(
        "change_baseline_links",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_id", sa.String(length=36), nullable=False),
        sa.Column("previous_baseline_id", sa.String(length=36), nullable=False),
        sa.Column("new_baseline_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_id"], ["change_requests.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["previous_baseline_id"], ["contract_baselines.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["new_baseline_id"], ["contract_baselines.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 9. Change Events
    op.create_table(
        "change_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("change_request_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=255), nullable=False),
        sa.Column("actor_type", sa.String(length=32), nullable=False, server_default="USER"),
        sa.Column("event_data", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["change_request_id"], ["change_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_change_events_change_request_id"), "change_events", ["change_request_id"], unique=False)


def downgrade() -> None:
    op.drop_table("change_events")
    op.drop_table("change_baseline_links")
    op.drop_table("change_approvals")
    op.drop_table("change_commercials")
    op.drop_table("change_estimates")
    op.drop_table("change_impacts")
    op.drop_table("change_evidence")
    op.drop_table("change_request_versions")
    op.drop_table("change_requests")
