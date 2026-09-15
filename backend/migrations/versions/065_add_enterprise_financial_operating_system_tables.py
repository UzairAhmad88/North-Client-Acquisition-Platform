"""add_enterprise_financial_operating_system_tables

Revision ID: 065
Revises: 064
Create Date: 2026-09-14 02:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '065'
down_revision = '064'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'fin_entities',
        'fin_accounts',
        'fin_customers',
        'fin_vendors',
        'fin_bank_accounts',
        'fin_invoices',
        'fin_invoice_items',
        'fin_bills',
        'fin_payments',
        'fin_payment_approvals',
        'fin_bank_transactions',
        'fin_reconciliation',
        'fin_journals',
        'fin_journal_lines',
        'fin_accounting_periods',
        'fin_expenses',
        'fin_assets',
        'fin_budgets',
        'fin_cash_forecasts',
        'fin_treasury_positions',
        'fin_fraud_alerts',
        'fin_digital_twins',
        'fin_agent_runs',
    ]

    for tbl in tables:
        if tbl not in existing_tables:
            op.create_table(
                tbl,
                sa.Column('id', sa.String(length=64), nullable=False),
                sa.Column('tenant_id', sa.String(length=64), nullable=False),
                sa.Column('created_at', sa.DateTime(), nullable=True),
                sa.PrimaryKeyConstraint('id')
            )
            op.create_index(f'ix_{tbl}_tenant_id', tbl, ['tenant_id'], unique=False)

def downgrade():
    tables = [
        'fin_entities',
        'fin_accounts',
        'fin_customers',
        'fin_vendors',
        'fin_bank_accounts',
        'fin_invoices',
        'fin_invoice_items',
        'fin_bills',
        'fin_payments',
        'fin_payment_approvals',
        'fin_bank_transactions',
        'fin_reconciliation',
        'fin_journals',
        'fin_journal_lines',
        'fin_accounting_periods',
        'fin_expenses',
        'fin_assets',
        'fin_budgets',
        'fin_cash_forecasts',
        'fin_treasury_positions',
        'fin_fraud_alerts',
        'fin_digital_twins',
        'fin_agent_runs',
    ]
    for tbl in tables:
        op.drop_table(tbl)
