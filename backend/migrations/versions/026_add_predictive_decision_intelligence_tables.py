"""add_predictive_decision_intelligence_tables

Revision ID: 026
Revises: 025
Create Date: 2026-09-08
"""

import alembic.op as op
import sqlalchemy as sa

revision = "026"
down_revision = "025"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Feature Store & Feature Registry
    op.create_table(
        "feature_definitions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("feature_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("data_source", sa.String(length=100), nullable=False),
        sa.Column("formula", sa.Text(), nullable=False),
        sa.Column("data_type", sa.String(length=50), nullable=False, server_default="float"),
        sa.Column("freshness_window", sa.String(length=50), nullable=False, server_default="24h"),
        sa.Column("privacy_level", sa.String(length=50), nullable=False, server_default="INTERNAL_BUSINESS"),
        sa.Column("owner", sa.String(length=100), nullable=False, server_default="ml_engineering"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("feature_key"),
    )
    op.create_index("ix_feature_definitions_tenant_id", "feature_definitions", ["tenant_id"])
    op.create_index("ix_feature_definitions_feature_key", "feature_definitions", ["feature_key"])

    op.create_table(
        "feature_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("feature_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("transformation_logic", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["feature_id"], ["feature_definitions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_feature_versions_tenant_id", "feature_versions", ["tenant_id"])
    op.create_index("ix_feature_versions_feature_id", "feature_versions", ["feature_id"])

    op.create_table(
        "feature_values",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("feature_id", sa.String(length=36), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("value_numeric", sa.Float(), nullable=True),
        sa.Column("value_text", sa.String(length=255), nullable=True),
        sa.Column("value_json", sa.JSON(), nullable=False),
        sa.Column("as_of_timestamp", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["feature_id"], ["feature_definitions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_feature_values_tenant_id", "feature_values", ["tenant_id"])
    op.create_index("ix_feature_values_feature_id", "feature_values", ["feature_id"])
    op.create_index("ix_feature_values_entity_id", "feature_values", ["entity_id"])
    op.create_index("ix_feature_values_as_of_timestamp", "feature_values", ["as_of_timestamp"])

    # 2. Training Datasets & Runs
    op.create_table(
        "training_datasets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("dataset_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("prediction_type", sa.String(length=64), nullable=False),
        sa.Column("feature_keys", sa.JSON(), nullable=False),
        sa.Column("target_label", sa.String(length=100), nullable=False),
        sa.Column("data_window_start", sa.DateTime(), nullable=False),
        sa.Column("data_window_end", sa.DateTime(), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("leakage_check_passed", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dataset_key"),
    )
    op.create_index("ix_training_datasets_tenant_id", "training_datasets", ["tenant_id"])
    op.create_index("ix_training_datasets_dataset_key", "training_datasets", ["dataset_key"])
    op.create_index("ix_training_datasets_prediction_type", "training_datasets", ["prediction_type"])

    op.create_table(
        "training_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("dataset_id", sa.String(length=36), nullable=False),
        sa.Column("algorithm", sa.String(length=100), nullable=False),
        sa.Column("hyperparameters", sa.JSON(), nullable=False),
        sa.Column("evaluation_metrics", sa.JSON(), nullable=False),
        sa.Column("training_duration_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["dataset_id"], ["training_datasets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_training_runs_tenant_id", "training_runs", ["tenant_id"])
    op.create_index("ix_training_runs_dataset_id", "training_runs", ["dataset_id"])

    # 3. Prediction Models & Deployments
    op.create_table(
        "prediction_models",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("model_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("prediction_type", sa.String(length=64), nullable=False),
        sa.Column("algorithm", sa.String(length=100), nullable=False),
        sa.Column("current_version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="EXPERIMENTAL"),
        sa.Column("thresholds", sa.JSON(), nullable=False),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("model_key"),
    )
    op.create_index("ix_prediction_models_tenant_id", "prediction_models", ["tenant_id"])
    op.create_index("ix_prediction_models_model_key", "prediction_models", ["model_key"])
    op.create_index("ix_prediction_models_prediction_type", "prediction_models", ["prediction_type"])
    op.create_index("ix_prediction_models_status", "prediction_models", ["status"])

    op.create_table(
        "model_deployments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("deployed_by", sa.String(length=100), nullable=False),
        sa.Column("deployment_mode", sa.String(length=50), nullable=False, server_default="PRODUCTION"),
        sa.Column("deployed_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("retired_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["model_id"], ["prediction_models.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_deployments_tenant_id", "model_deployments", ["tenant_id"])
    op.create_index("ix_model_deployments_model_id", "model_deployments", ["model_id"])

    # 4. Predictions, Explanations & Outcomes
    op.create_table(
        "prediction_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("model_id", sa.String(length=36), nullable=False),
        sa.Column("prediction_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("risk_band", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("confidence_interval", sa.JSON(), nullable=False),
        sa.Column("model_version", sa.String(length=20), nullable=False),
        sa.Column("inference_timestamp", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["model_id"], ["prediction_models.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_prediction_records_tenant_id", "prediction_records", ["tenant_id"])
    op.create_index("ix_prediction_records_model_id", "prediction_records", ["model_id"])
    op.create_index("ix_prediction_records_prediction_type", "prediction_records", ["prediction_type"])
    op.create_index("ix_prediction_records_entity_id", "prediction_records", ["entity_id"])
    op.create_index("ix_prediction_records_inference_timestamp", "prediction_records", ["inference_timestamp"])

    op.create_table(
        "prediction_explanations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("prediction_id", sa.String(length=36), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("key_drivers", sa.JSON(), nullable=False),
        sa.Column("safety_notes", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["prediction_id"], ["prediction_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("prediction_id"),
    )
    op.create_index("ix_prediction_explanations_tenant_id", "prediction_explanations", ["tenant_id"])
    op.create_index("ix_prediction_explanations_prediction_id", "prediction_explanations", ["prediction_id"])

    op.create_table(
        "prediction_outcomes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("prediction_id", sa.String(length=36), nullable=False),
        sa.Column("actual_numeric_outcome", sa.Float(), nullable=False),
        sa.Column("outcome_label", sa.String(length=100), nullable=False),
        sa.Column("error_magnitude", sa.Float(), nullable=True),
        sa.Column("recorded_by", sa.String(length=100), nullable=False, server_default="system_outcome_collector"),
        sa.Column("recorded_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["prediction_id"], ["prediction_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("prediction_id"),
    )
    op.create_index("ix_prediction_outcomes_tenant_id", "prediction_outcomes", ["tenant_id"])
    op.create_index("ix_prediction_outcomes_prediction_id", "prediction_outcomes", ["prediction_id"])

    # 5. Decision Intelligence Policies, Support & Overrides
    op.create_table(
        "decision_policies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("policy_key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("prediction_type", sa.String(length=64), nullable=False),
        sa.Column("rules_logic", sa.JSON(), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False, server_default="v1.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("policy_key"),
    )
    op.create_index("ix_decision_policies_tenant_id", "decision_policies", ["tenant_id"])
    op.create_index("ix_decision_policies_policy_key", "decision_policies", ["policy_key"])

    op.create_table(
        "decision_support_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("prediction_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("recommended_action", sa.Text(), nullable=False),
        sa.Column("tradeoff_analysis", sa.Text(), nullable=False),
        sa.Column("urgency", sa.String(length=32), nullable=False, server_default="MEDIUM"),
        sa.Column("state", sa.String(length=64), nullable=False, server_default="PENDING_REVIEW"),
        sa.Column("reviewed_by", sa.String(length=100), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["prediction_id"], ["prediction_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("prediction_id"),
    )
    op.create_index("ix_decision_support_records_tenant_id", "decision_support_records", ["tenant_id"])
    op.create_index("ix_decision_support_records_prediction_id", "decision_support_records", ["prediction_id"])
    op.create_index("ix_decision_support_records_state", "decision_support_records", ["state"])
    op.create_index("ix_decision_support_records_created_at", "decision_support_records", ["created_at"])

    op.create_table(
        "decision_reviews",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("decision_record_id", sa.String(length=36), nullable=False),
        sa.Column("reviewer", sa.String(length=100), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["decision_record_id"], ["decision_support_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_decision_reviews_tenant_id", "decision_reviews", ["tenant_id"])
    op.create_index("ix_decision_reviews_decision_record_id", "decision_reviews", ["decision_record_id"])

    op.create_table(
        "decision_overrides",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("decision_record_id", sa.String(length=36), nullable=False),
        sa.Column("original_recommendation", sa.Text(), nullable=False),
        sa.Column("chosen_action", sa.Text(), nullable=False),
        sa.Column("override_reason", sa.Text(), nullable=False),
        sa.Column("operator", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["decision_record_id"], ["decision_support_records.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_decision_overrides_tenant_id", "decision_overrides", ["tenant_id"])
    op.create_index("ix_decision_overrides_decision_record_id", "decision_overrides", ["decision_record_id"])

    # 6. Forecast Runs & Model Drift Events
    op.create_table(
        "forecast_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("forecast_type", sa.String(length=100), nullable=False),
        sa.Column("time_horizon", sa.String(length=50), nullable=False, server_default="30d"),
        sa.Column("model_version", sa.String(length=20), nullable=False),
        sa.Column("predictions_payload", sa.JSON(), nullable=False),
        sa.Column("confidence_intervals", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_forecast_runs_tenant_id", "forecast_runs", ["tenant_id"])
    op.create_index("ix_forecast_runs_forecast_type", "forecast_runs", ["forecast_type"])
    op.create_index("ix_forecast_runs_created_at", "forecast_runs", ["created_at"])

    op.create_table(
        "model_drift_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("model_key", sa.String(length=100), nullable=False),
        sa.Column("drift_type", sa.String(length=50), nullable=False),
        sa.Column("drift_metric_value", sa.Float(), nullable=False),
        sa.Column("drift_status", sa.String(length=50), nullable=False, server_default="WARNING"),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("detected_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_drift_events_tenant_id", "model_drift_events", ["tenant_id"])
    op.create_index("ix_model_drift_events_model_key", "model_drift_events", ["model_key"])
    op.create_index("ix_model_drift_events_detected_at", "model_drift_events", ["detected_at"])


def downgrade() -> None:
    op.drop_table("model_drift_events")
    op.drop_table("forecast_runs")
    op.drop_table("decision_overrides")
    op.drop_table("decision_reviews")
    op.drop_table("decision_support_records")
    op.drop_table("decision_policies")
    op.drop_table("prediction_outcomes")
    op.drop_table("prediction_explanations")
    op.drop_table("prediction_records")
    op.drop_table("model_deployments")
    op.drop_table("prediction_models")
    op.drop_table("training_runs")
    op.drop_table("training_datasets")
    op.drop_table("feature_values")
    op.drop_table("feature_versions")
    op.drop_table("feature_definitions")
