"""add unified research intelligence tables

Revision ID: 047
Revises: 046
Create Date: 2026-09-10 02:46:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '047'
down_revision = '046'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. research_workspaces
    op.create_table(
        'research_workspaces',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('research_question', sa.Text(), nullable=False),
        sa.Column('objective', sa.Text(), nullable=True),
        sa.Column('research_type', sa.String(length=64), nullable=False, server_default='MARKET'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='PLANNED'),
        sa.Column('owner_id', sa.String(length=128), nullable=False),
        sa.Column('scope', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. research_tasks
    op.create_table(
        'research_tasks',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('task_type', sa.String(length=64), nullable=False, server_default='SOURCE_DISCOVERY'),
        sa.Column('priority', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('assigned_worker', sa.String(length=128), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='QUEUED'),
        sa.Column('budget_tokens', sa.Integer(), nullable=False, server_default='10000'),
        sa.Column('result_summary', sa.Text(), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_tasks_workspace_id', 'research_tasks', ['workspace_id'])

    # 3. research_sources
    op.create_table(
        'research_sources',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('url_or_reference', sa.String(length=512), nullable=False),
        sa.Column('source_type', sa.String(length=64), nullable=False, server_default='PUBLIC_WEB'),
        sa.Column('publisher', sa.String(length=255), nullable=True),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('authority_score', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('reliability', sa.String(length=32), nullable=False, server_default='MEDIUM_TRUST'),
        sa.Column('freshness', sa.String(length=32), nullable=False, server_default='CURRENT'),
        sa.Column('content_hash', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='VALIDATED'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_sources_workspace_id', 'research_sources', ['workspace_id'])

    # 4. research_entities
    op.create_table(
        'research_entities',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('entity_type', sa.String(length=64), nullable=False),
        sa.Column('canonical_id', sa.String(length=128), nullable=True),
        sa.Column('aliases', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('attributes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.9'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_entities_workspace_id', 'research_entities', ['workspace_id'])

    # 5. research_facts
    op.create_table(
        'research_facts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('source_id', sa.String(length=64), nullable=True),
        sa.Column('claim', sa.Text(), nullable=False),
        sa.Column('value_extracted', sa.Text(), nullable=True),
        sa.Column('fact_status', sa.String(length=32), nullable=False, server_default='VERIFIED'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('provenance', sa.String(length=255), nullable=True),
        sa.Column('observed_date', sa.String(length=32), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_facts_workspace_id', 'research_facts', ['workspace_id'])

    # 6. research_claims
    op.create_table(
        'research_claims',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('claim_text', sa.Text(), nullable=False),
        sa.Column('verification_status', sa.String(length=32), nullable=False, server_default='SUPPORTED'),
        sa.Column('independent_sources_count', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('supporting_evidence', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('contradicting_evidence', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_claims_workspace_id', 'research_claims', ['workspace_id'])

    # 7. research_conflicts
    op.create_table(
        'research_conflicts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('topic', sa.String(length=255), nullable=False),
        sa.Column('source_a_id', sa.String(length=64), nullable=False),
        sa.Column('claim_a', sa.Text(), nullable=False),
        sa.Column('source_b_id', sa.String(length=64), nullable=False),
        sa.Column('claim_b', sa.Text(), nullable=False),
        sa.Column('possible_explanation', sa.Text(), nullable=True),
        sa.Column('resolution_status', sa.String(length=32), nullable=False, server_default='SURFACED'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_conflicts_workspace_id', 'research_conflicts', ['workspace_id'])

    # 8. research_trends
    op.create_table(
        'research_trends',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('trend_name', sa.String(length=255), nullable=False),
        sa.Column('trend_type', sa.String(length=64), nullable=False, server_default='EMERGING'),
        sa.Column('momentum_score', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('key_drivers', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('impact_assessment', sa.Text(), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_trends_workspace_id', 'research_trends', ['workspace_id'])

    # 9. research_competitor_profiles
    op.create_table(
        'research_competitor_profiles',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('company_name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('market_position', sa.String(length=64), nullable=False, server_default='CHALLENGER'),
        sa.Column('products_offered', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('pricing_signals', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('strengths', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('weaknesses', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('recent_changes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 10. research_market_signals
    op.create_table(
        'research_market_signals',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('market_segment', sa.String(length=128), nullable=False),
        sa.Column('signal_type', sa.String(length=64), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('source_reference', sa.String(length=255), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 11. research_monitoring_rules
    op.create_table(
        'research_monitoring_rules',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('target_entity', sa.String(length=255), nullable=False),
        sa.Column('watch_frequency', sa.String(length=32), nullable=False, server_default='DAILY'),
        sa.Column('topics_monitored', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('alert_significance_threshold', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_monitoring_rules_workspace_id', 'research_monitoring_rules', ['workspace_id'])

    # 12. research_intelligence_events
    op.create_table(
        'research_intelligence_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('event_type', sa.String(length=64), nullable=False),
        sa.Column('target_entity', sa.String(length=255), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('significance', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('evidence_payload', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 13. research_syntheses
    op.create_table(
        'research_syntheses',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('executive_summary', sa.Text(), nullable=False),
        sa.Column('key_findings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('strategic_implications', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('recommended_actions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('uncertainties_and_limitations', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_syntheses_workspace_id', 'research_syntheses', ['workspace_id'])

    # 14. research_reports
    op.create_table(
        'research_reports',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('report_markdown', sa.Text(), nullable=False),
        sa.Column('citations', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence_rating', sa.String(length=32), nullable=False, server_default='HIGH'),
        sa.Column('generated_at', sa.String(length=32), nullable=False),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_reports_workspace_id', 'research_reports', ['workspace_id'])

    # 15. research_gaps
    op.create_table(
        'research_gaps',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), sa.ForeignKey('research_workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('gap_description', sa.Text(), nullable=False),
        sa.Column('importance', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('recommended_investigation', sa.Text(), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_gaps_workspace_id', 'research_gaps', ['workspace_id'])

    # 16. research_quality_scores
    op.create_table(
        'research_quality_scores',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('workspace_id', sa.String(length=64), nullable=False),
        sa.Column('source_quality_score', sa.Float(), nullable=False, server_default='0.85'),
        sa.Column('evidence_coverage_score', sa.Float(), nullable=False, server_default='0.80'),
        sa.Column('citation_accuracy_score', sa.Float(), nullable=False, server_default='0.95'),
        sa.Column('conflict_handling_score', sa.Float(), nullable=False, server_default='0.90'),
        sa.Column('composite_quality_score', sa.Float(), nullable=False, server_default='0.875'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_research_quality_scores_workspace_id', 'research_quality_scores', ['workspace_id'])


def downgrade() -> None:
    op.drop_table('research_quality_scores')
    op.drop_table('research_gaps')
    op.drop_table('research_reports')
    op.drop_table('research_syntheses')
    op.drop_table('research_intelligence_events')
    op.drop_table('research_monitoring_rules')
    op.drop_table('research_market_signals')
    op.drop_table('research_competitor_profiles')
    op.drop_table('research_trends')
    op.drop_table('research_conflicts')
    op.drop_table('research_claims')
    op.drop_table('research_facts')
    op.drop_table('research_entities')
    op.drop_table('research_sources')
    op.drop_table('research_tasks')
    op.drop_table('research_workspaces')
