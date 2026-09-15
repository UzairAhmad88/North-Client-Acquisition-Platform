"""add_solution_proposal_tables

Revision ID: 017
Revises: 016
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "017"
down_revision = "016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Solution Designs Table
    op.create_table(
        "solution_designs",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("discovery_session_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DRAFT"),
        sa.Column("overview", sa.Text(), nullable=False),
        sa.Column("architecture_summary", sa.Text(), nullable=False),
        sa.Column("complexity_tier", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("approved_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["discovery_session_id"], ["discovery_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["approved_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_solution_designs_discovery_session_id"), "solution_designs", ["discovery_session_id"], unique=False)
    op.create_index(op.f("ix_solution_designs_business_id"), "solution_designs", ["business_id"], unique=False)
    op.create_index(op.f("ix_solution_designs_lead_id"), "solution_designs", ["lead_id"], unique=False)
    op.create_index(op.f("ix_solution_designs_status"), "solution_designs", ["status"], unique=False)

    # 2. Solution Features Table
    op.create_table(
        "solution_features",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="RECOMMENDED"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_solution_features_solution_id"), "solution_features", ["solution_id"], unique=False)
    op.create_index(op.f("ix_solution_features_category"), "solution_features", ["category"], unique=False)
    op.create_index(op.f("ix_solution_features_status"), "solution_features", ["status"], unique=False)

    # 3. Solution Deliverables Table
    op.create_table(
        "solution_deliverables",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="PROPOSED"),
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_solution_deliverables_solution_id"), "solution_deliverables", ["solution_id"], unique=False)

    # 4. Solution Dependencies Table
    op.create_table(
        "solution_dependencies",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("feature_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("depends_on_feature_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("dependency_type", sa.String(length=64), nullable=False, server_default="REQUIRES"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["feature_id"], ["solution_features.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["depends_on_feature_id"], ["solution_features.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_solution_dependencies_solution_id"), "solution_dependencies", ["solution_id"], unique=False)
    op.create_index(op.f("ix_solution_dependencies_feature_id"), "solution_dependencies", ["feature_id"], unique=False)

    # 5. Solution Integrations Table
    op.create_table(
        "solution_integrations",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("purpose", sa.String(length=255), nullable=False),
        sa.Column("provider", sa.String(length=128), nullable=False),
        sa.Column("data_flow", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PROPOSED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_solution_integrations_solution_id"), "solution_integrations", ["solution_id"], unique=False)

    # 6. Solution Assumptions Table
    op.create_table(
        "solution_assumptions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("assumption_text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="UNCONFIRMED"),
        sa.Column("risk_level", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_solution_assumptions_solution_id"), "solution_assumptions", ["solution_id"], unique=False)

    # 7. Solution Requirement Links Table
    op.create_table(
        "solution_requirement_links",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("feature_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("requirement_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("relationship_type", sa.String(length=64), nullable=False, server_default="ADDRESSES"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["feature_id"], ["solution_features.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_solution_requirement_links_solution_id"), "solution_requirement_links", ["solution_id"], unique=False)
    op.create_index(op.f("ix_solution_requirement_links_feature_id"), "solution_requirement_links", ["feature_id"], unique=False)
    op.create_index(op.f("ix_solution_requirement_links_requirement_id"), "solution_requirement_links", ["requirement_id"], unique=False)

    # 8. Proposals Table
    op.create_table(
        "proposals",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("proposal_type", sa.String(length=64), nullable=False, server_default="FULL"),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DRAFT"),
        sa.Column("pricing_status", sa.String(length=64), nullable=False, server_default="PRICING_REQUIRES_HUMAN_REVIEW"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
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
    op.create_index(op.f("ix_proposals_solution_id"), "proposals", ["solution_id"], unique=False)
    op.create_index(op.f("ix_proposals_business_id"), "proposals", ["business_id"], unique=False)
    op.create_index(op.f("ix_proposals_lead_id"), "proposals", ["lead_id"], unique=False)
    op.create_index(op.f("ix_proposals_status"), "proposals", ["status"], unique=False)

    # 9. Proposal Items Table
    op.create_table(
        "proposal_items",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("proposal_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("service_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("deliverable_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("unit", sa.String(length=32), nullable=False, server_default="project"),
        sa.Column("is_optional", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["deliverable_id"], ["solution_deliverables.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_proposal_items_proposal_id"), "proposal_items", ["proposal_id"], unique=False)

    # 10. Proposal Versions Table
    op.create_table(
        "proposal_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("proposal_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("sections_json", sa.JSON(), nullable=False),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_proposal_versions_proposal_id"), "proposal_versions", ["proposal_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_proposal_versions_proposal_id"), table_name="proposal_versions")
    op.drop_table("proposal_versions")
    op.drop_index(op.f("ix_proposal_items_proposal_id"), table_name="proposal_items")
    op.drop_table("proposal_items")
    op.drop_index(op.f("ix_proposals_status"), table_name="proposals")
    op.drop_index(op.f("ix_proposals_lead_id"), table_name="proposals")
    op.drop_index(op.f("ix_proposals_business_id"), table_name="proposals")
    op.drop_index(op.f("ix_proposals_solution_id"), table_name="proposals")
    op.drop_table("proposals")
    op.drop_index(op.f("ix_solution_requirement_links_requirement_id"), table_name="solution_requirement_links")
    op.drop_index(op.f("ix_solution_requirement_links_feature_id"), table_name="solution_requirement_links")
    op.drop_index(op.f("ix_solution_requirement_links_solution_id"), table_name="solution_requirement_links")
    op.drop_table("solution_requirement_links")
    op.drop_index(op.f("ix_solution_assumptions_solution_id"), table_name="solution_assumptions")
    op.drop_table("solution_assumptions")
    op.drop_index(op.f("ix_solution_integrations_solution_id"), table_name="solution_integrations")
    op.drop_table("solution_integrations")
    op.drop_index(op.f("ix_solution_dependencies_feature_id"), table_name="solution_dependencies")
    op.drop_index(op.f("ix_solution_dependencies_solution_id"), table_name="solution_dependencies")
    op.drop_table("solution_dependencies")
    op.drop_index(op.f("ix_solution_deliverables_solution_id"), table_name="solution_deliverables")
    op.drop_table("solution_deliverables")
    op.drop_index(op.f("ix_solution_features_status"), table_name="solution_features")
    op.drop_index(op.f("ix_solution_features_category"), table_name="solution_features")
    op.drop_index(op.f("ix_solution_features_solution_id"), table_name="solution_features")
    op.drop_table("solution_features")
    op.drop_index(op.f("ix_solution_designs_status"), table_name="solution_designs")
    op.drop_index(op.f("ix_solution_designs_lead_id"), table_name="solution_designs")
    op.drop_index(op.f("ix_solution_designs_business_id"), table_name="solution_designs")
    op.drop_index(op.f("ix_solution_designs_discovery_session_id"), table_name="solution_designs")
    op.drop_table("solution_designs")
