"""add_contract_commitment_tables

Revision ID: 019
Revises: 018
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "019"
down_revision = "018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Contracts Table
    op.create_table(
        "contracts",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("proposal_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("estimate_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("solution_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("business_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("lead_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("contract_number", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DRAFT"),
        sa.Column("pricing_status", sa.String(length=64), nullable=False, server_default="PRICING_REQUIRES_HUMAN_REVIEW"),
        sa.Column("risk_status", sa.String(length=32), nullable=False, server_default="PENDING_REVIEW"),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("total_amount", sa.Float(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("content_hash", sa.String(length=64), nullable=True),
        sa.Column("is_stale", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("approved_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["proposal_id"], ["proposals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["estimate_id"], ["project_estimates.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["solution_id"], ["solution_designs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["business_id"], ["businesses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["approved_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contracts_contract_number"), "contracts", ["contract_number"], unique=True)
    op.create_index(op.f("ix_contracts_proposal_id"), "contracts", ["proposal_id"], unique=False)
    op.create_index(op.f("ix_contracts_estimate_id"), "contracts", ["estimate_id"], unique=False)
    op.create_index(op.f("ix_contracts_solution_id"), "contracts", ["solution_id"], unique=False)
    op.create_index(op.f("ix_contracts_business_id"), "contracts", ["business_id"], unique=False)
    op.create_index(op.f("ix_contracts_lead_id"), "contracts", ["lead_id"], unique=False)
    op.create_index(op.f("ix_contracts_status"), "contracts", ["status"], unique=False)

    # 2. Contract Versions Table
    op.create_table(
        "contract_versions",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("sections_json", sa.JSON(), nullable=False),
        sa.Column("source_proposal_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("source_estimate_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("source_solution_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("source_requirements_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contract_versions_contract_id"), "contract_versions", ["contract_id"], unique=False)

    # 3. Contract Templates Table
    op.create_table(
        "contract_templates",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="ACTIVE"),
        sa.Column("sections_schema", sa.JSON(), nullable=False),
        sa.Column("created_by_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 4. Contract Sections Table
    op.create_table(
        "contract_sections",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("section_type", sa.String(length=64), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contract_sections_contract_id"), "contract_sections", ["contract_id"], unique=False)

    # 5. Contract Approvals Table
    op.create_table(
        "contract_approvals",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="APPROVED"),
        sa.Column("approval_reason", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("approved_by_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["approved_by_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contract_approvals_contract_id"), "contract_approvals", ["contract_id"], unique=False)

    # 6. Contract Client Acceptances Table
    op.create_table(
        "contract_client_acceptances",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="APPROVED"),
        sa.Column("acceptance_statement", sa.Text(), nullable=False),
        sa.Column("client_email", sa.String(length=255), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contract_client_acceptances_contract_id"), "contract_client_acceptances", ["contract_id"], unique=False)

    # 7. Contract Signatures Table
    op.create_table(
        "contract_signatures",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("provider_name", sa.String(length=64), nullable=False, server_default="mock"),
        sa.Column("provider_request_id", sa.String(length=128), nullable=False),
        sa.Column("signer_email", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contract_signatures_contract_id"), "contract_signatures", ["contract_id"], unique=False)

    # 8. Contract Baselines Table
    op.create_table(
        "contract_baselines",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_version", sa.Integer(), nullable=False),
        sa.Column("requirements_version", sa.Integer(), nullable=False),
        sa.Column("solution_version", sa.Integer(), nullable=False),
        sa.Column("estimate_version", sa.Integer(), nullable=False),
        sa.Column("proposal_version", sa.Integer(), nullable=False),
        sa.Column("scope_hash", sa.String(length=64), nullable=False),
        sa.Column("commercial_hash", sa.String(length=64), nullable=False),
        sa.Column("contract_hash", sa.String(length=64), nullable=False),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contract_baselines_contract_id"), "contract_baselines", ["contract_id"], unique=False)

    # 9. Contract Discrepancies Table
    op.create_table(
        "contract_discrepancies",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("contract_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("discrepancy_type", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="HIGH"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="DETECTED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contract_discrepancies_contract_id"), "contract_discrepancies", ["contract_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_contract_discrepancies_contract_id"), table_name="contract_discrepancies")
    op.drop_table("contract_discrepancies")
    op.drop_index(op.f("ix_contract_baselines_contract_id"), table_name="contract_baselines")
    op.drop_table("contract_baselines")
    op.drop_index(op.f("ix_contract_signatures_contract_id"), table_name="contract_signatures")
    op.drop_table("contract_signatures")
    op.drop_index(op.f("ix_contract_client_acceptances_contract_id"), table_name="contract_client_acceptances")
    op.drop_table("contract_client_acceptances")
    op.drop_index(op.f("ix_contract_approvals_contract_id"), table_name="contract_approvals")
    op.drop_table("contract_approvals")
    op.drop_index(op.f("ix_contract_sections_contract_id"), table_name="contract_sections")
    op.drop_table("contract_sections")
    op.drop_table("contract_templates")
    op.drop_index(op.f("ix_contract_versions_contract_id"), table_name="contract_versions")
    op.drop_table("contract_versions")
    op.drop_index(op.f("ix_contracts_status"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_lead_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_business_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_solution_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_estimate_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_proposal_id"), table_name="contracts")
    op.drop_index(op.f("ix_contracts_contract_number"), table_name="contracts")
    op.drop_table("contracts")
