"""add_business_intelligence_analytics_tables

Revision ID: 025
Revises: 024
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "025"
down_revision = "024"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Analytics Metrics Registry
    op.create_table(
        "analytics_metrics",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("metric_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False, server_default="OPERATIONS"),
        sa.Column("formula", sa.Text(), nullable=False),
        sa.Column("source_tables", sa.JSON(), nullable=False),
        sa.Column("dimensions", sa.JSON(), nullable=False),
        sa.Column("time_window_default", sa.String(length=50), nullable=False, server_default="30d"),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("owner", sa.String(length=100), nullable=False, server_default="system"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("metric_key"),
    )
    op.create_index("ix_analytics_metrics_tenant_id", "analytics_metrics", ["tenant_id"])
    op.create_index("ix_analytics_metrics_metric_key", "analytics_metrics", ["metric_key"])

    # 2. Metric Versions
    op.create_table(
        "analytics_metric_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("metric_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("formula", sa.Text(), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=True),
        sa.Column("author", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["metric_id"], ["analytics_metrics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_metric_versions_tenant_id", "analytics_metric_versions", ["tenant_id"])
    op.create_index("ix_analytics_metric_versions_metric_id", "analytics_metric_versions", ["metric_id"])

    # 3. Analytics Dimensions
    op.create_table(
        "analytics_dimensions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("dimension_type", sa.String(length=100), nullable=False),
        sa.Column("dimension_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("attributes", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_dimensions_tenant_id", "analytics_dimensions", ["tenant_id"])
    op.create_index("ix_analytics_dimensions_dimension_type", "analytics_dimensions", ["dimension_type"])
    op.create_index("ix_analytics_dimensions_dimension_key", "analytics_dimensions", ["dimension_key"])

    # 4. Analytics Facts
    op.create_table(
        "analytics_facts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("fact_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=True),
        sa.Column("dimensions", sa.JSON(), nullable=False),
        sa.Column("numeric_values", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_facts_tenant_id", "analytics_facts", ["tenant_id"])
    op.create_index("ix_analytics_facts_fact_type", "analytics_facts", ["fact_type"])
    op.create_index("ix_analytics_facts_entity_id", "analytics_facts", ["entity_id"])
    op.create_index("ix_analytics_facts_recorded_at", "analytics_facts", ["recorded_at"])

    # 5. Snapshots & Aggregations
    op.create_table(
        "analytics_snapshots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("snapshot_type", sa.String(length=100), nullable=False),
        sa.Column("time_window", sa.String(length=50), nullable=False),
        sa.Column("metrics_data", sa.JSON(), nullable=False),
        sa.Column("sample_sizes", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_snapshots_tenant_id", "analytics_snapshots", ["tenant_id"])
    op.create_index("ix_analytics_snapshots_snapshot_type", "analytics_snapshots", ["snapshot_type"])
    op.create_index("ix_analytics_snapshots_created_at", "analytics_snapshots", ["created_at"])

    op.create_table(
        "analytics_aggregations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("aggregation_key", sa.String(length=150), nullable=False),
        sa.Column("time_window", sa.String(length=50), nullable=False),
        sa.Column("granularity", sa.String(length=50), nullable=False, server_default="daily"),
        sa.Column("results", sa.JSON(), nullable=False),
        sa.Column("sample_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("calculated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_aggregations_tenant_id", "analytics_aggregations", ["tenant_id"])
    op.create_index("ix_analytics_aggregations_aggregation_key", "analytics_aggregations", ["aggregation_key"])

    # 6. Business Insights
    op.create_table(
        "business_insights",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.String(length=64), nullable=False, server_default="MEDIUM"),
        sa.Column("sample_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("time_window", sa.String(length=50), nullable=False, server_default="30d"),
        sa.Column("affected_entities", sa.JSON(), nullable=False),
        sa.Column("recommended_action", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DRAFT"),
        sa.Column("created_by", sa.String(length=100), nullable=False, server_default="bi_learning_agent"),
        sa.Column("reviewed_by", sa.String(length=100), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_business_insights_tenant_id", "business_insights", ["tenant_id"])
    op.create_index("ix_business_insights_category", "business_insights", ["category"])
    op.create_index("ix_business_insights_status", "business_insights", ["status"])
    op.create_index("ix_business_insights_created_at", "business_insights", ["created_at"])

    # 7. Business Insight Evidence
    op.create_table(
        "business_insight_evidence",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("insight_id", sa.String(length=36), nullable=False),
        sa.Column("source_type", sa.String(length=100), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("baseline_value", sa.Float(), nullable=True),
        sa.Column("observed_value", sa.Float(), nullable=True),
        sa.Column("variance_pct", sa.Float(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["insight_id"], ["business_insights.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_business_insight_evidence_tenant_id", "business_insight_evidence", ["tenant_id"])
    op.create_index("ix_business_insight_evidence_insight_id", "business_insight_evidence", ["insight_id"])

    # 8. Business Recommendations
    op.create_table(
        "business_recommendations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("insight_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("expected_benefit", sa.Text(), nullable=False),
        sa.Column("potential_downside", sa.Text(), nullable=False),
        sa.Column("confidence", sa.String(length=64), nullable=False, server_default="MEDIUM"),
        sa.Column("affected_workflow", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="PENDING_APPROVAL"),
        sa.Column("decision_reason", sa.Text(), nullable=True),
        sa.Column("reviewed_by", sa.String(length=100), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["insight_id"], ["business_insights.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_business_recommendations_tenant_id", "business_recommendations", ["tenant_id"])
    op.create_index("ix_business_recommendations_insight_id", "business_recommendations", ["insight_id"])
    op.create_index("ix_business_recommendations_status", "business_recommendations", ["status"])
    op.create_index("ix_business_recommendations_created_at", "business_recommendations", ["created_at"])

    # 9. Recommendation Reviews
    op.create_table(
        "recommendation_reviews",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("recommendation_id", sa.String(length=36), nullable=False),
        sa.Column("reviewer", sa.String(length=100), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("policy_impact", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["recommendation_id"], ["business_recommendations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recommendation_reviews_tenant_id", "recommendation_reviews", ["tenant_id"])
    op.create_index("ix_recommendation_reviews_recommendation_id", "recommendation_reviews", ["recommendation_id"])

    # 10. Experiments
    op.create_table(
        "experiments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("target_workflow", sa.String(length=100), nullable=False),
        sa.Column("target_metric", sa.String(length=100), nullable=False),
        sa.Column("baseline_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("target_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("sample_target", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("current_sample_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="DRAFT"),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("conclusion", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_experiments_tenant_id", "experiments", ["tenant_id"])
    op.create_index("ix_experiments_status", "experiments", ["status"])

    # 11. Experiment Metrics & Results
    op.create_table(
        "experiment_metrics",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("experiment_id", sa.String(length=36), nullable=False),
        sa.Column("metric_name", sa.String(length=100), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("baseline_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("current_value", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("unit", sa.String(length=20), nullable=False, server_default="count"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiments.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_experiment_metrics_tenant_id", "experiment_metrics", ["tenant_id"])
    op.create_index("ix_experiment_metrics_experiment_id", "experiment_metrics", ["experiment_id"])

    op.create_table(
        "experiment_results",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("experiment_id", sa.String(length=36), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=True),
        sa.Column("observed_value", sa.Float(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiments.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_experiment_results_tenant_id", "experiment_results", ["tenant_id"])
    op.create_index("ix_experiment_results_experiment_id", "experiment_results", ["experiment_id"])

    # 12. Model Registry & Governance
    op.create_table(
        "model_registry",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("model_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("model_type", sa.String(length=50), nullable=False, server_default="deterministic_baseline"),
        sa.Column("features", sa.JSON(), nullable=False),
        sa.Column("training_window", sa.String(length=50), nullable=False, server_default="90d"),
        sa.Column("evaluation_metrics", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="EXPERIMENTAL"),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("model_key"),
    )
    op.create_index("ix_model_registry_tenant_id", "model_registry", ["tenant_id"])
    op.create_index("ix_model_registry_model_key", "model_registry", ["model_key"])
    op.create_index("ix_model_registry_status", "model_registry", ["status"])

    # 13. Model Evaluations & Predictions
    op.create_table(
        "model_evaluations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=False),
        sa.Column("evaluation_type", sa.String(length=50), nullable=False),
        sa.Column("sample_size", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("metrics_result", sa.JSON(), nullable=False),
        sa.Column("drift_detected", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("drift_details", sa.JSON(), nullable=False),
        sa.Column("evaluated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_evaluations_tenant_id", "model_evaluations", ["tenant_id"])
    op.create_index("ix_model_evaluations_model_id", "model_evaluations", ["model_id"])

    op.create_table(
        "model_predictions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=True),
        sa.Column("prediction_value", sa.Float(), nullable=False),
        sa.Column("confidence_interval", sa.JSON(), nullable=False),
        sa.Column("features_snapshot", sa.JSON(), nullable=False),
        sa.Column("actual_outcome", sa.Float(), nullable=True),
        sa.Column("outcome_recorded_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["model_id"], ["model_registry.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_predictions_tenant_id", "model_predictions", ["tenant_id"])
    op.create_index("ix_model_predictions_model_id", "model_predictions", ["model_id"])
    op.create_index("ix_model_predictions_entity_id", "model_predictions", ["entity_id"])
    op.create_index("ix_model_predictions_created_at", "model_predictions", ["created_at"])

    # 14. Data Quality Checks & Results
    op.create_table(
        "data_quality_checks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("check_name", sa.String(length=150), nullable=False),
        sa.Column("target_table", sa.String(length=100), nullable=False),
        sa.Column("rule_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="GOOD"),
        sa.Column("last_run_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_quality_checks_tenant_id", "data_quality_checks", ["tenant_id"])

    op.create_table(
        "data_quality_results",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("check_id", sa.String(length=36), nullable=False),
        sa.Column("total_records", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_records", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="GOOD"),
        sa.Column("anomalies", sa.JSON(), nullable=False),
        sa.Column("checked_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["check_id"], ["data_quality_checks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_data_quality_results_tenant_id", "data_quality_results", ["tenant_id"])
    op.create_index("ix_data_quality_results_check_id", "data_quality_results", ["check_id"])

    # 15. Analytics Query Runs & Reports
    op.create_table(
        "analytics_query_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("query_name", sa.String(length=150), nullable=False),
        sa.Column("parameter_payload", sa.JSON(), nullable=False),
        sa.Column("executed_by", sa.String(length=100), nullable=False),
        sa.Column("execution_time_ms", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("result_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_query_runs_tenant_id", "analytics_query_runs", ["tenant_id"])
    op.create_index("ix_analytics_query_runs_created_at", "analytics_query_runs", ["created_at"])

    op.create_table(
        "analytics_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("report_type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("time_window", sa.String(length=50), nullable=False),
        sa.Column("report_summary", sa.Text(), nullable=False),
        sa.Column("report_data", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False, server_default="bi_agent"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_analytics_reports_tenant_id", "analytics_reports", ["tenant_id"])
    op.create_index("ix_analytics_reports_created_at", "analytics_reports", ["created_at"])


def downgrade() -> None:
    op.drop_table("analytics_reports")
    op.drop_table("analytics_query_runs")
    op.drop_table("data_quality_results")
    op.drop_table("data_quality_checks")
    op.drop_table("model_predictions")
    op.drop_table("model_evaluations")
    op.drop_table("model_registry")
    op.drop_table("experiment_results")
    op.drop_table("experiment_metrics")
    op.drop_table("experiments")
    op.drop_table("recommendation_reviews")
    op.drop_table("business_recommendations")
    op.drop_table("business_insight_evidence")
    op.drop_table("business_insights")
    op.drop_table("analytics_aggregations")
    op.drop_table("analytics_snapshots")
    op.drop_table("analytics_facts")
    op.drop_table("analytics_dimensions")
    op.drop_table("analytics_metric_versions")
    op.drop_table("analytics_metrics")
