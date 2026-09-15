"""add unified decision rooms tables

Revision ID: 046
Revises: 045
Create Date: 2026-09-10 02:35:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '046'
down_revision = '045'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. decision_rooms
    op.create_table(
        'decision_rooms',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('objective', sa.Text(), nullable=True),
        sa.Column('decision_type', sa.String(length=64), nullable=False, server_default='STRATEGIC'),
        sa.Column('importance', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='OPEN'),
        sa.Column('owner_id', sa.String(length=128), nullable=False),
        sa.Column('selected_option_id', sa.String(length=64), nullable=True),
        sa.Column('decision_summary', sa.Text(), nullable=True),
        sa.Column('decided_at', sa.DateTime(), nullable=True),
        sa.Column('decided_by', sa.String(length=128), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. decision_contexts
    op.create_table(
        'decision_contexts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('background', sa.Text(), nullable=False),
        sa.Column('current_state', sa.Text(), nullable=True),
        sa.Column('constraints', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('entities_involved', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('policies_applicable', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('memory_references', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_contexts_room_id', 'decision_contexts', ['room_id'])

    # 3. decision_evidence
    op.create_table(
        'decision_evidence',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('evidence_type', sa.String(length=64), nullable=False),
        sa.Column('source', sa.String(length=255), nullable=False),
        sa.Column('claim', sa.Text(), nullable=False),
        sa.Column('provenance', sa.String(length=255), nullable=True),
        sa.Column('authority', sa.String(length=64), nullable=False, server_default='OFFICIAL'),
        sa.Column('statement_category', sa.String(length=64), nullable=False, server_default='FACT'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('freshness', sa.String(length=64), nullable=True, server_default='CURRENT'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_evidence_room_id', 'decision_evidence', ['room_id'])

    # 4. decision_assumptions
    op.create_table(
        'decision_assumptions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('statement', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.7'),
        sa.Column('validated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('validator_role', sa.String(length=64), nullable=True),
        sa.Column('validation_evidence_id', sa.String(length=64), nullable=True),
        sa.Column('impact_if_false', sa.String(length=64), nullable=False, server_default='MEDIUM'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_assumptions_room_id', 'decision_assumptions', ['room_id'])

    # 5. decision_unknowns
    op.create_table(
        'decision_unknowns',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('impact', sa.String(length=64), nullable=False, server_default='MEDIUM'),
        sa.Column('resolution_path', sa.Text(), nullable=True),
        sa.Column('resolved', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('resolved_value', sa.Text(), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_unknowns_room_id', 'decision_unknowns', ['room_id'])

    # 6. decision_hypotheses
    op.create_table(
        'decision_hypotheses',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('statement', sa.Text(), nullable=False),
        sa.Column('test_criteria', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='PROPOSED'),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_hypotheses_room_id', 'decision_hypotheses', ['room_id'])

    # 7. decision_options
    op.create_table(
        'decision_options',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('benefits', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('costs', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('risks', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('dependencies', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('resources_required', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('expected_outcome', sa.Text(), nullable=True),
        sa.Column('uncertainty_level', sa.String(length=32), nullable=False, server_default='MEDIUM'),
        sa.Column('reversibility', sa.String(length=32), nullable=False, server_default='REVERSIBLE'),
        sa.Column('composite_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_options_room_id', 'decision_options', ['room_id'])

    # 8. decision_criteria
    op.create_table(
        'decision_criteria',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('criterion_type', sa.String(length=64), nullable=False, server_default='BENEFIT'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_criteria_room_id', 'decision_criteria', ['room_id'])

    # 9. decision_scores
    op.create_table(
        'decision_scores',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('option_id', sa.String(length=64), nullable=False),
        sa.Column('criterion_id', sa.String(length=64), nullable=False),
        sa.Column('raw_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('weighted_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('justification', sa.Text(), nullable=True),
        sa.Column('scored_by', sa.String(length=128), nullable=False, server_default='AI_ANALYST'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_scores_room_id', 'decision_scores', ['room_id'])
    op.create_index('ix_decision_scores_option_id', 'decision_scores', ['option_id'])

    # 10. decision_tradeoffs
    op.create_table(
        'decision_tradeoffs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('option_a_id', sa.String(length=64), nullable=False),
        sa.Column('option_b_id', sa.String(length=64), nullable=False),
        sa.Column('tradeoff_summary', sa.Text(), nullable=False),
        sa.Column('gains_in_a', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('sacrifices_in_a', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_tradeoffs_room_id', 'decision_tradeoffs', ['room_id'])

    # 11. decision_scenarios
    op.create_table(
        'decision_scenarios',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('option_id', sa.String(length=64), nullable=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('scenario_type', sa.String(length=64), nullable=False, server_default='BASELINE'),
        sa.Column('assumptions_applied', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('projected_metrics', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('second_order_effects', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence_interval', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_scenarios_room_id', 'decision_scenarios', ['room_id'])

    # 12. decision_risks
    op.create_table(
        'decision_risks',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('option_id', sa.String(length=64), nullable=True),
        sa.Column('risk_category', sa.String(length=64), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('probability', sa.Float(), nullable=False, server_default='0.3'),
        sa.Column('impact', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('risk_score', sa.Float(), nullable=False, server_default='0.15'),
        sa.Column('mitigation', sa.Text(), nullable=True),
        sa.Column('blast_radius', sa.String(length=64), nullable=False, server_default='TEAM'),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_risks_room_id', 'decision_risks', ['room_id'])

    # 13. decision_analyses
    op.create_table(
        'decision_analyses',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('specialist_role', sa.String(length=64), nullable=False),
        sa.Column('worker_id', sa.String(length=64), nullable=True),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('recommendations', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('key_findings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, server_default='0.8'),
        sa.Column('facts', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('inferences', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_analyses_room_id', 'decision_analyses', ['room_id'])

    # 14. decision_reviews
    op.create_table(
        'decision_reviews',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reviewer_role', sa.String(length=64), nullable=False, server_default='CRITICAL_ANALYST'),
        sa.Column('target_option_id', sa.String(length=64), nullable=True),
        sa.Column('critique_summary', sa.Text(), nullable=False),
        sa.Column('weak_assumptions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('unintended_consequences', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('hidden_costs', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('data_gaps', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_reviews_room_id', 'decision_reviews', ['room_id'])

    # 15. decision_disagreements
    op.create_table(
        'decision_disagreements',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('topic', sa.String(length=255), nullable=False),
        sa.Column('disagreement_category', sa.String(length=64), nullable=False),
        sa.Column('party_a', sa.String(length=128), nullable=False),
        sa.Column('view_a', sa.Text(), nullable=False),
        sa.Column('party_b', sa.String(length=128), nullable=False),
        sa.Column('view_b', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='SURFACED'),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_disagreements_room_id', 'decision_disagreements', ['room_id'])

    # 16. decision_discussions
    op.create_table(
        'decision_discussions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('author_id', sa.String(length=128), nullable=False),
        sa.Column('author_role', sa.String(length=64), nullable=False, server_default='HUMAN_DECISION_MAKER'),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_human', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('parent_id', sa.String(length=64), nullable=True),
        sa.Column('mentions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('annotations', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_discussions_room_id', 'decision_discussions', ['room_id'])

    # 17. decision_approvals
    op.create_table(
        'decision_approvals',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('step_name', sa.String(length=128), nullable=False),
        sa.Column('required_role', sa.String(length=64), nullable=False),
        sa.Column('approver_id', sa.String(length=128), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='PENDING'),
        sa.Column('decision_notes', sa.Text(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_approvals_room_id', 'decision_approvals', ['room_id'])

    # 18. decision_actions
    op.create_table(
        'decision_actions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('target_system', sa.String(length=64), nullable=False),
        sa.Column('target_payload', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('assigned_to', sa.String(length=128), nullable=True),
        sa.Column('execution_status', sa.String(length=32), nullable=False, server_default='PENDING_APPROVAL'),
        sa.Column('dispatched_at', sa.DateTime(), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_actions_room_id', 'decision_actions', ['room_id'])

    # 19. decision_outcomes
    op.create_table(
        'decision_outcomes',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('metric_name', sa.String(length=128), nullable=False),
        sa.Column('expected_value', sa.Float(), nullable=False),
        sa.Column('actual_value', sa.Float(), nullable=False),
        sa.Column('variance_pct', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('measured_at', sa.DateTime(), nullable=False),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_outcomes_room_id', 'decision_outcomes', ['room_id'])

    # 20. decision_post_reviews
    op.create_table(
        'decision_post_reviews',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('room_id', sa.String(length=64), sa.ForeignKey('decision_rooms.id', ondelete='CASCADE'), nullable=False),
        sa.Column('decision_quality_score', sa.Float(), nullable=False, server_default='80.0'),
        sa.Column('outcome_rating', sa.String(length=32), nullable=False, server_default='NEUTRAL'),
        sa.Column('prediction_error', sa.Text(), nullable=True),
        sa.Column('assumption_error', sa.Text(), nullable=True),
        sa.Column('execution_error', sa.Text(), nullable=True),
        sa.Column('model_error', sa.Text(), nullable=True),
        sa.Column('lessons_learned', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('feed_to_organizational_memory', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('reviewed_by', sa.String(length=128), nullable=False),
        sa.Column('reviewed_at', sa.DateTime(), nullable=False),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_decision_post_reviews_room_id', 'decision_post_reviews', ['room_id'])

    # 21. decision_templates
    op.create_table(
        'decision_templates',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False, unique=True),
        sa.Column('decision_type', sa.String(length=64), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('default_criteria', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('default_specialists', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('default_approval_steps', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('meta_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('decision_templates')
    op.drop_table('decision_post_reviews')
    op.drop_table('decision_outcomes')
    op.drop_table('decision_actions')
    op.drop_table('decision_approvals')
    op.drop_table('decision_discussions')
    op.drop_table('decision_disagreements')
    op.drop_table('decision_reviews')
    op.drop_table('decision_analyses')
    op.drop_table('decision_risks')
    op.drop_table('decision_scenarios')
    op.drop_table('decision_tradeoffs')
    op.drop_table('decision_scores')
    op.drop_table('decision_criteria')
    op.drop_table('decision_options')
    op.drop_table('decision_hypotheses')
    op.drop_table('decision_unknowns')
    op.drop_table('decision_assumptions')
    op.drop_table('decision_evidence')
    op.drop_table('decision_contexts')
    op.drop_table('decision_rooms')
