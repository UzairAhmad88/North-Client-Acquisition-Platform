"""add_enterprise_trust_operating_system_tables

Revision ID: 066
Revises: 065
Create Date: 2026-09-14 02:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '066'
down_revision = '065'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()

    tables = [
        'trust_legal_entities',
        'trust_jurisdictions',
        'trust_regulations',
        'trust_regulatory_changes',
        'trust_requirements',
        'trust_frameworks',
        'trust_controls',
        'trust_control_tests',
        'trust_control_failures',
        'trust_contracts',
        'trust_contract_versions',
        'trust_contract_clauses',
        'trust_obligations',
        'trust_deadlines',
        'trust_legal_holds',
        'trust_policies',
        'trust_policy_exceptions',
        'trust_data_assets',
        'trust_data_subject_requests',
        'trust_ai_systems',
        'trust_ai_evaluations',
        'trust_ai_incidents',
        'trust_third_parties',
        'trust_third_party_risks',
        'trust_legal_matters',
        'trust_legal_spend',
        'trust_investigations',
        'trust_chain_of_custody',
        'trust_audits',
        'trust_findings',
        'trust_licenses',
        'trust_insurance',
        'trust_decisions',
        'trust_conflicts',
        'trust_agent_runs',
    ]

    for table in tables:
        if table not in existing_tables:
            op.create_table(
                table,
                sa.Column('id', sa.String(36), primary_key=True),
                sa.Column('tenant_id', sa.String(36), nullable=False, index=True),
                sa.Column('created_at', sa.DateTime, default=sa.func.now()),
                sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
            )

def downgrade():
    tables = [
        'trust_agent_runs',
        'trust_conflicts',
        'trust_decisions',
        'trust_insurance',
        'trust_licenses',
        'trust_findings',
        'trust_audits',
        'trust_chain_of_custody',
        'trust_investigations',
        'trust_legal_spend',
        'trust_legal_matters',
        'trust_third_party_risks',
        'trust_third_parties',
        'trust_ai_incidents',
        'trust_ai_evaluations',
        'trust_ai_systems',
        'trust_data_subject_requests',
        'trust_data_assets',
        'trust_policy_exceptions',
        'trust_policies',
        'trust_legal_holds',
        'trust_deadlines',
        'trust_obligations',
        'trust_contract_clauses',
        'trust_contract_versions',
        'trust_contracts',
        'trust_control_failures',
        'trust_control_tests',
        'trust_controls',
        'trust_frameworks',
        'trust_requirements',
        'trust_regulatory_changes',
        'trust_regulations',
        'trust_jurisdictions',
        'trust_legal_entities',
    ]
    for table in tables:
        op.drop_table(table)
