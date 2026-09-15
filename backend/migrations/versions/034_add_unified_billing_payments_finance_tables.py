"""add_unified_billing_payments_finance_tables

Revision ID: 034
Revises: 033
Create Date: 2026-09-09
"""

import alembic.op as op
import sqlalchemy as sa

revision = "034"
down_revision = "033"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. billing_profiles
    op.create_table(
        "billing_profiles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("tax_id", sa.String(length=100), nullable=True),
        sa.Column("billing_email", sa.String(length=255), nullable=False),
        sa.Column("address_line1", sa.String(length=255), nullable=True),
        sa.Column("address_line2", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("postal_code", sa.String(length=50), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=False, server_default="US"),
        sa.Column("default_currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("payment_terms", sa.String(length=50), nullable=False, server_default="net_30"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_billing_profiles_tenant_id", "billing_profiles", ["tenant_id"])
    op.create_index("ix_billing_profiles_client_id", "billing_profiles", ["client_id"])

    # 2. currencies
    op.create_table(
        "currencies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("symbol", sa.String(length=10), nullable=False, server_default="$"),
        sa.Column("decimal_places", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_currencies_code", "currencies", ["code"])

    # 3. tax_profiles
    op.create_table(
        "tax_profiles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("tax_type", sa.String(length=50), nullable=False, server_default="sales_tax"),
        sa.Column("rate_pct", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("is_compound", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tax_profiles_tenant_id", "tax_profiles", ["tenant_id"])

    # 4. invoices
    op.create_table(
        "invoices",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("billing_profile_id", sa.String(length=36), nullable=True),
        sa.Column("project_id", sa.String(length=36), nullable=True),
        sa.Column("contract_id", sa.String(length=36), nullable=True),
        sa.Column("proposal_id", sa.String(length=36), nullable=True),
        sa.Column("invoice_number", sa.String(length=100), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("payment_terms", sa.String(length=50), nullable=False, server_default="net_30"),
        sa.Column("custom_terms_days", sa.Integer(), nullable=True),
        sa.Column("issue_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("subtotal", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("discount_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("taxable_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("tax_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("total_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("amount_paid", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("balance_due", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("tax_rate_pct", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("tax_type", sa.String(length=50), nullable=False, server_default="none"),
        sa.Column("tax_region", sa.String(length=100), nullable=True),
        sa.Column("discount_rate_pct", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("fixed_discount_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("terms_and_conditions", sa.Text(), nullable=True),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("issued_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("approved_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["billing_profile_id"], ["billing_profiles.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_invoices_tenant_id", "invoices", ["tenant_id"])
    op.create_index("ix_invoices_client_id", "invoices", ["client_id"])
    op.create_index("ix_invoices_project_id", "invoices", ["project_id"])
    op.create_index("ix_invoices_invoice_number", "invoices", ["invoice_number"])
    op.create_index("ix_invoices_status", "invoices", ["status"])

    # 5. invoice_versions
    op.create_table(
        "invoice_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("invoice_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("invoice_data_snapshot", sa.JSON(), nullable=False),
        sa.Column("changed_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("change_reason", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_invoice_versions_invoice_id", "invoice_versions", ["invoice_id"])

    # 6. invoice_items
    op.create_table(
        "invoice_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("invoice_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("quantity", sa.Numeric(precision=18, scale=2), nullable=False, server_default="1.00"),
        sa.Column("unit_price", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("subtotal", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("discount_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("taxable_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("tax_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("total_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("item_type", sa.String(length=50), nullable=False, server_default="fixed"),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reference_id", sa.String(length=36), nullable=True),
        sa.Column("contract_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_invoice_items_invoice_id", "invoice_items", ["invoice_id"])

    # 7. invoice_approvals
    op.create_table(
        "invoice_approvals",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("invoice_id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("approver_user_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_invoice_approvals_invoice_id", "invoice_approvals", ["invoice_id"])
    op.create_index("ix_invoice_approvals_tenant_id", "invoice_approvals", ["tenant_id"])

    # 8. billing_schedules
    op.create_table(
        "billing_schedules",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=True),
        sa.Column("contract_id", sa.String(length=36), nullable=True),
        sa.Column("schedule_type", sa.String(length=50), nullable=False, server_default="milestone"),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_billing_schedules_tenant_id", "billing_schedules", ["tenant_id"])
    op.create_index("ix_billing_schedules_client_id", "billing_schedules", ["client_id"])

    # 9. billing_schedule_items
    op.create_table(
        "billing_schedule_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("schedule_id", sa.String(length=36), nullable=False),
        sa.Column("milestone_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("target_billing_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("invoice_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["schedule_id"], ["billing_schedules.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_billing_schedule_items_schedule_id", "billing_schedule_items", ["schedule_id"])

    # 10. subscriptions
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("plan_name", sa.String(length=255), nullable=False),
        sa.Column("billing_interval", sa.String(length=50), nullable=False, server_default="monthly"),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cancel_at_period_end", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subscriptions_tenant_id", "subscriptions", ["tenant_id"])
    op.create_index("ix_subscriptions_client_id", "subscriptions", ["client_id"])

    # 11. payments
    op.create_table(
        "payments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("invoice_id", sa.String(length=36), nullable=True),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("provider_type", sa.String(length=50), nullable=False, server_default="mock"),
        sa.Column("provider_payment_id", sa.String(length=255), nullable=True),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="succeeded"),
        sa.Column("payment_method", sa.String(length=50), nullable=False, server_default="credit_card"),
        sa.Column("fee_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("raw_response", sa.JSON(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=True),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payments_tenant_id", "payments", ["tenant_id"])
    op.create_index("ix_payments_client_id", "payments", ["client_id"])
    op.create_index("ix_payments_invoice_id", "payments", ["invoice_id"])
    op.create_index("ix_payments_status", "payments", ["status"])

    # 12. payment_provider_events
    op.create_table(
        "payment_provider_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("provider_type", sa.String(length=50), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("provider_event_id", sa.String(length=255), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("is_processed", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payment_provider_events_tenant_id", "payment_provider_events", ["tenant_id"])
    op.create_index("ix_payment_provider_events_provider_event_id", "payment_provider_events", ["provider_event_id"])

    # 13. payment_reconciliations
    op.create_table(
        "payment_reconciliations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("payment_id", sa.String(length=36), nullable=True),
        sa.Column("provider_event_id", sa.String(length=36), nullable=True),
        sa.Column("invoice_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="matched"),
        sa.Column("matched_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("discrepancy_amount", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("discrepancy_type", sa.String(length=100), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("resolved_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["payment_id"], ["payments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payment_reconciliations_tenant_id", "payment_reconciliations", ["tenant_id"])

    # 14. refunds
    op.create_table(
        "refunds",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("payment_id", sa.String(length=36), nullable=False),
        sa.Column("invoice_id", sa.String(length=36), nullable=True),
        sa.Column("provider_refund_id", sa.String(length=255), nullable=True),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="succeeded"),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("error_code", sa.String(length=100), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["payment_id"], ["payments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_refunds_tenant_id", "refunds", ["tenant_id"])
    op.create_index("ix_refunds_payment_id", "refunds", ["payment_id"])

    # 15. credit_notes
    op.create_table(
        "credit_notes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("client_id", sa.String(length=36), nullable=False),
        sa.Column("invoice_id", sa.String(length=36), nullable=True),
        sa.Column("credit_note_number", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("balance", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="issued"),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_credit_notes_tenant_id", "credit_notes", ["tenant_id"])
    op.create_index("ix_credit_notes_client_id", "credit_notes", ["client_id"])

    # 16. financial_accounts
    op.create_table(
        "financial_accounts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("account_code", sa.String(length=50), nullable=False),
        sa.Column("account_name", sa.String(length=255), nullable=False),
        sa.Column("account_type", sa.String(length=50), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_financial_accounts_tenant_id", "financial_accounts", ["tenant_id"])

    # 17. ledger_entries
    op.create_table(
        "ledger_entries",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("entry_group_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("account_type", sa.String(length=50), nullable=True),
        sa.Column("direction", sa.String(length=20), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("reference_type", sa.String(length=50), nullable=True),
        sa.Column("reference_id", sa.String(length=36), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("is_reversed", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("reversing_entry_id", sa.String(length=36), nullable=True),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["account_id"], ["financial_accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ledger_entries_tenant_id", "ledger_entries", ["tenant_id"])
    op.create_index("ix_ledger_entries_entry_group_id", "ledger_entries", ["entry_group_id"])
    op.create_index("ix_ledger_entries_account_id", "ledger_entries", ["account_id"])

    # 18. financial_adjustments
    op.create_table(
        "financial_adjustments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("entry_group_id", sa.String(length=36), nullable=False),
        sa.Column("original_entry_group_id", sa.String(length=36), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("approved_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_financial_adjustments_tenant_id", "financial_adjustments", ["tenant_id"])

    # 19. project_costs
    op.create_table(
        "project_costs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("labor_cost", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("ai_token_cost", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("infrastructure_cost", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("subcontractor_cost", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("other_expenses", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("total_cost", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0.00"),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_project_costs_tenant_id", "project_costs", ["tenant_id"])
    op.create_index("ix_project_costs_project_id", "project_costs", ["project_id"])

    # 20. expenses
    op.create_table(
        "expenses",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="USD"),
        sa.Column("vendor", sa.String(length=255), nullable=True),
        sa.Column("receipt_file_id", sa.String(length=36), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("approved_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("incurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_expenses_tenant_id", "expenses", ["tenant_id"])
    op.create_index("ix_expenses_project_id", "expenses", ["project_id"])


def downgrade() -> None:
    op.drop_table("expenses")
    op.drop_table("project_costs")
    op.drop_table("financial_adjustments")
    op.drop_table("ledger_entries")
    op.drop_table("financial_accounts")
    op.drop_table("credit_notes")
    op.drop_table("refunds")
    op.drop_table("payment_reconciliations")
    op.drop_table("payment_provider_events")
    op.drop_table("payments")
    op.drop_table("subscriptions")
    op.drop_table("billing_schedule_items")
    op.drop_table("billing_schedules")
    op.drop_table("invoice_approvals")
    op.drop_table("invoice_items")
    op.drop_table("invoice_versions")
    op.drop_table("invoices")
    op.drop_table("tax_profiles")
    op.drop_table("currencies")
    op.drop_table("billing_profiles")
