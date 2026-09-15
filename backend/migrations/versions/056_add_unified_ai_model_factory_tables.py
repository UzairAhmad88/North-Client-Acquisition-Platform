"""add unified ai model factory tables

Revision ID: 056
Revises: 055
Create Date: 2026-09-12 23:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '056'
down_revision = '055'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. ai_projects
    op.create_table(
        'ai_projects',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('team', sa.String(length=128), nullable=False),
        sa.Column('domain', sa.String(length=64), nullable=False),
        sa.Column('objective', sa.Text(), nullable=True),
        sa.Column('budget_allocated_usd', sa.Float(), nullable=True),
        sa.Column('budget_spent_usd', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 2. ai_dataset_versions
    op.create_table(
        'ai_dataset_versions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('ai_projects.id'), nullable=False),
        sa.Column('dataset_name', sa.String(length=255), nullable=False),
        sa.Column('version', sa.String(length=32), nullable=False),
        sa.Column('source_lakehouse_dataset_id', sa.String(length=64), nullable=True),
        sa.Column('features_list', sa.JSON(), nullable=True),
        sa.Column('label_column', sa.String(length=128), nullable=True),
        sa.Column('splits', sa.JSON(), nullable=True),
        sa.Column('row_count', sa.Integer(), nullable=True),
        sa.Column('bias_check_status', sa.String(length=32), nullable=True),
        sa.Column('lineage_provenance', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 3. ai_experiments
    op.create_table(
        'ai_experiments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('ai_projects.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('model_type', sa.String(length=64), nullable=False),
        sa.Column('framework', sa.String(length=64), nullable=False),
        sa.Column('search_strategy', sa.String(length=32), nullable=True),
        sa.Column('best_metric_name', sa.String(length=64), nullable=True),
        sa.Column('best_metric_value', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 4. ai_experiment_runs
    op.create_table(
        'ai_experiment_runs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('experiment_id', sa.String(length=64), sa.ForeignKey('ai_experiments.id'), nullable=False),
        sa.Column('run_number', sa.Integer(), nullable=True),
        sa.Column('git_commit_hash', sa.String(length=64), nullable=True),
        sa.Column('dataset_version_id', sa.String(length=64), nullable=True),
        sa.Column('hyperparameters', sa.JSON(), nullable=True),
        sa.Column('metrics', sa.JSON(), nullable=True),
        sa.Column('hardware_specs', sa.JSON(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('cost_usd', sa.Float(), nullable=True),
        sa.Column('artifacts_uri', sa.String(length=512), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 5. ai_training_jobs
    op.create_table(
        'ai_training_jobs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('ai_projects.id'), nullable=False),
        sa.Column('model_name', sa.String(length=255), nullable=False),
        sa.Column('base_model_name', sa.String(length=255), nullable=True),
        sa.Column('job_type', sa.String(length=32), nullable=True),
        sa.Column('gpu_type', sa.String(length=64), nullable=True),
        sa.Column('gpu_count', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('progress_pct', sa.Float(), nullable=True),
        sa.Column('epochs_total', sa.Integer(), nullable=True),
        sa.Column('current_epoch', sa.Integer(), nullable=True),
        sa.Column('loss_history', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 6. ai_models
    op.create_table(
        'ai_models',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('ai_projects.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('model_type', sa.String(length=64), nullable=False),
        sa.Column('framework', sa.String(length=64), nullable=False),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('steward', sa.String(length=128), nullable=True),
        sa.Column('current_stage', sa.String(length=32), nullable=True),
        sa.Column('active_version', sa.String(length=32), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    # 7. ai_model_versions
    op.create_table(
        'ai_model_versions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('model_id', sa.String(length=64), sa.ForeignKey('ai_models.id'), nullable=False),
        sa.Column('version', sa.String(length=32), nullable=False),
        sa.Column('stage', sa.String(length=32), nullable=True),
        sa.Column('training_run_id', sa.String(length=64), nullable=True),
        sa.Column('dataset_version_id', sa.String(length=64), nullable=True),
        sa.Column('artifacts_manifest', sa.JSON(), nullable=True),
        sa.Column('metrics_summary', sa.JSON(), nullable=True),
        sa.Column('supply_chain_sbom', sa.JSON(), nullable=True),
        sa.Column('is_signed', sa.Boolean(), default=True),
        sa.Column('quality_gate_passed', sa.Boolean(), default=False),
        sa.Column('security_scan_passed', sa.Boolean(), default=False),
        sa.Column('governance_approved', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 8. ai_evaluation_suites
    op.create_table(
        'ai_evaluation_suites',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('suite_type', sa.String(length=64), nullable=False),
        sa.Column('target_model_type', sa.String(length=64), nullable=False),
        sa.Column('thresholds_config', sa.JSON(), nullable=True),
        sa.Column('test_cases_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 9. ai_evaluation_results
    op.create_table(
        'ai_evaluation_results',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('suite_id', sa.String(length=64), sa.ForeignKey('ai_evaluation_suites.id'), nullable=False),
        sa.Column('model_version_id', sa.String(length=64), sa.ForeignKey('ai_model_versions.id'), nullable=False),
        sa.Column('evaluator_engine', sa.String(length=64), nullable=True),
        sa.Column('judge_model', sa.String(length=128), nullable=True),
        sa.Column('passed', sa.Boolean(), default=False),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('detailed_metrics', sa.JSON(), nullable=True),
        sa.Column('failure_reasons', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 10. ai_prompts
    op.create_table(
        'ai_prompts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('version', sa.String(length=32), nullable=False),
        sa.Column('purpose', sa.String(length=128), nullable=False),
        sa.Column('system_prompt', sa.Text(), nullable=False),
        sa.Column('user_template', sa.Text(), nullable=False),
        sa.Column('variables', sa.JSON(), nullable=True),
        sa.Column('target_model_family', sa.String(length=64), nullable=True),
        sa.Column('stage', sa.String(length=32), nullable=True),
        sa.Column('token_budget_max', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 11. ai_deployments
    op.create_table(
        'ai_deployments',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('model_version_id', sa.String(length=64), sa.ForeignKey('ai_model_versions.id'), nullable=False),
        sa.Column('environment', sa.String(length=32), nullable=False),
        sa.Column('strategy', sa.String(length=32), nullable=False),
        sa.Column('traffic_weight_pct', sa.Float(), nullable=True),
        sa.Column('endpoint_url', sa.String(length=512), nullable=True),
        sa.Column('min_replicas', sa.Integer(), nullable=True),
        sa.Column('max_replicas', sa.Integer(), nullable=True),
        sa.Column('current_replicas', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('rollback_target_version_id', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 12. ai_inference_endpoints
    op.create_table(
        'ai_inference_endpoints',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('route_name', sa.String(length=128), nullable=False),
        sa.Column('primary_deployment_id', sa.String(length=64), sa.ForeignKey('ai_deployments.id'), nullable=False),
        sa.Column('fallback_deployment_id', sa.String(length=64), nullable=True),
        sa.Column('routing_policy', sa.String(length=64), nullable=True),
        sa.Column('timeout_ms', sa.Integer(), nullable=True),
        sa.Column('rate_limit_rpm', sa.Integer(), nullable=True),
        sa.Column('total_requests', sa.Integer(), nullable=True),
        sa.Column('p95_latency_ms', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 13. ai_model_monitoring
    op.create_table(
        'ai_model_monitoring',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('deployment_id', sa.String(length=64), sa.ForeignKey('ai_deployments.id'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('requests_count', sa.Integer(), nullable=True),
        sa.Column('errors_count', sa.Integer(), nullable=True),
        sa.Column('avg_latency_ms', sa.Float(), nullable=True),
        sa.Column('input_token_count', sa.Integer(), nullable=True),
        sa.Column('output_token_count', sa.Integer(), nullable=True),
        sa.Column('cost_usd', sa.Float(), nullable=True),
        sa.Column('drift_status', sa.String(length=32), nullable=True),
    )

    # 14. ai_drift_events
    op.create_table(
        'ai_drift_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('deployment_id', sa.String(length=64), sa.ForeignKey('ai_deployments.id'), nullable=False),
        sa.Column('drift_type', sa.String(length=32), nullable=False),
        sa.Column('metric_name', sa.String(length=64), nullable=False),
        sa.Column('metric_value', sa.Float(), nullable=True),
        sa.Column('threshold', sa.Float(), nullable=True),
        sa.Column('is_breached', sa.Boolean(), default=False),
        sa.Column('suggested_action', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 15. ai_feedback
    op.create_table(
        'ai_feedback',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('model_version_id', sa.String(length=64), nullable=False),
        sa.Column('user_id', sa.String(length=64), nullable=False),
        sa.Column('feedback_type', sa.String(length=32), nullable=False),
        sa.Column('rating_score', sa.Float(), nullable=True),
        sa.Column('correction_text', sa.Text(), nullable=True),
        sa.Column('quality_classification', sa.String(length=32), nullable=True),
        sa.Column('is_included_in_retraining', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 16. ai_model_cards
    op.create_table(
        'ai_model_cards',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('model_version_id', sa.String(length=64), sa.ForeignKey('ai_model_versions.id'), nullable=False),
        sa.Column('intended_use', sa.Text(), nullable=False),
        sa.Column('limitations', sa.Text(), nullable=False),
        sa.Column('training_data_summary', sa.Text(), nullable=False),
        sa.Column('evaluation_summary', sa.Text(), nullable=False),
        sa.Column('ethical_considerations', sa.Text(), nullable=False),
        sa.Column('risk_level', sa.String(length=32), nullable=True),
        sa.Column('owner', sa.String(length=128), nullable=False),
        sa.Column('steward', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 17. ai_gpu_jobs
    op.create_table(
        'ai_gpu_jobs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('training_job_id', sa.String(length=64), sa.ForeignKey('ai_training_jobs.id'), nullable=True),
        sa.Column('gpu_cluster_node', sa.String(length=128), nullable=True),
        sa.Column('gpu_type', sa.String(length=64), nullable=True),
        sa.Column('gpu_count', sa.Integer(), nullable=True),
        sa.Column('memory_requested_gb', sa.Integer(), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('allocated_at', sa.DateTime(), nullable=False),
    )

    # 18. ai_finops_costs
    op.create_table(
        'ai_finops_costs',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('project_id', sa.String(length=64), sa.ForeignKey('ai_projects.id'), nullable=False),
        sa.Column('model_id', sa.String(length=64), nullable=True),
        sa.Column('cost_category', sa.String(length=64), nullable=False),
        sa.Column('amount_usd', sa.Float(), nullable=True),
        sa.Column('units_consumed', sa.Float(), nullable=True),
        sa.Column('period_date', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # 19. ai_incidents
    op.create_table(
        'ai_incidents',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('tenant_id', sa.String(length=64), nullable=False, index=True),
        sa.Column('deployment_id', sa.String(length=64), nullable=True),
        sa.Column('incident_type', sa.String(length=64), nullable=False),
        sa.Column('severity', sa.String(length=16), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('root_cause', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('mitigation_action', sa.String(length=64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('ai_incidents')
    op.drop_table('ai_finops_costs')
    op.drop_table('ai_gpu_jobs')
    op.drop_table('ai_model_cards')
    op.drop_table('ai_feedback')
    op.drop_table('ai_drift_events')
    op.drop_table('ai_model_monitoring')
    op.drop_table('ai_inference_endpoints')
    op.drop_table('ai_deployments')
    op.drop_table('ai_prompts')
    op.drop_table('ai_evaluation_results')
    op.drop_table('ai_evaluation_suites')
    op.drop_table('ai_model_versions')
    op.drop_table('ai_models')
    op.drop_table('ai_training_jobs')
    op.drop_table('ai_experiment_runs')
    op.drop_table('ai_experiments')
    op.drop_table('ai_dataset_versions')
    op.drop_table('ai_projects')
