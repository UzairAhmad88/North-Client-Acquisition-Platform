"""Master Facade for Phase 63 Unified AI/ML Model Factory & Production AI Operating System."""

from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

try:
    from backend.app.services.ai_model_factory.base import (
        AttrDict,
        FrameworkType,
        ModelStage,
        ModelType,
    )
    from backend.app.services.ai_model_factory.projects_datasets_features import (
        ProjectsDatasetsFeaturesService,
    )
    from backend.app.services.ai_model_factory.experiments_training_hyperparameters import (
        ExperimentsTrainingHyperparametersService,
    )
    from backend.app.services.ai_model_factory.registry_artifacts_versions import (
        ModelRegistryArtifactsService,
    )
    from backend.app.services.ai_model_factory.evaluation_benchmarks_llm_judge import (
        EvaluationBenchmarksJudgeService,
    )
    from backend.app.services.ai_model_factory.prompts_embeddings_ragops_agentops import (
        PromptsEmbeddingsRagopsAgentopsService,
    )
    from backend.app.services.ai_model_factory.deployments_inference_routing_fallback import (
        DeploymentsInferenceRoutingService,
    )
    from backend.app.services.ai_model_factory.monitoring_drift_feedback_retraining import (
        MonitoringDriftFeedbackRetrainingService,
    )
    from backend.app.services.ai_model_factory.governance_model_cards_safety_security import (
        GovernanceModelCardsSafetyService,
    )
    from backend.app.services.ai_model_factory.gpu_queue_finops_twin_copilot import (
        GpuFinopsTwinCopilotService,
    )
except ImportError:
    from app.services.ai_model_factory.base import (
        AttrDict,
        FrameworkType,
        ModelStage,
        ModelType,
    )
    from app.services.ai_model_factory.projects_datasets_features import (
        ProjectsDatasetsFeaturesService,
    )
    from app.services.ai_model_factory.experiments_training_hyperparameters import (
        ExperimentsTrainingHyperparametersService,
    )
    from app.services.ai_model_factory.registry_artifacts_versions import (
        ModelRegistryArtifactsService,
    )
    from app.services.ai_model_factory.evaluation_benchmarks_llm_judge import (
        EvaluationBenchmarksJudgeService,
    )
    from app.services.ai_model_factory.prompts_embeddings_ragops_agentops import (
        PromptsEmbeddingsRagopsAgentopsService,
    )
    from app.services.ai_model_factory.deployments_inference_routing_fallback import (
        DeploymentsInferenceRoutingService,
    )
    from app.services.ai_model_factory.monitoring_drift_feedback_retraining import (
        MonitoringDriftFeedbackRetrainingService,
    )
    from app.services.ai_model_factory.governance_model_cards_safety_security import (
        GovernanceModelCardsSafetyService,
    )
    from app.services.ai_model_factory.gpu_queue_finops_twin_copilot import (
        GpuFinopsTwinCopilotService,
    )

logger = logging.getLogger(__name__)


class AiModelFactoryService:
    """Master Orchestrator Facade for Phase 63 AI Model Factory."""

    def __init__(self):
        self.projects_service = ProjectsDatasetsFeaturesService()
        self.experiments_service = ExperimentsTrainingHyperparametersService()
        self.registry_service = ModelRegistryArtifactsService()
        self.evaluation_service = EvaluationBenchmarksJudgeService()
        self.prompts_service = PromptsEmbeddingsRagopsAgentopsService()
        self.deployments_service = DeploymentsInferenceRoutingService()
        self.monitoring_service = MonitoringDriftFeedbackRetrainingService()
        self.governance_service = GovernanceModelCardsSafetyService()
        self.copilot_service = GpuFinopsTwinCopilotService()
        self._seed_default_ecosystem("default_tenant")

    def _seed_default_ecosystem(self, tenant_id: str):
        """Seed a rich, production-grade AI Model Factory ecosystem."""
        # 1. Project
        proj = self.projects_service.create_project(
            tenant_id=tenant_id,
            name="Customer Intelligence AI Suite",
            owner="dr.sarah.chen@uzaii.internal",
            team="AI/ML Platform Team",
            domain="CUSTOMER_INTELLIGENCE",
            objective="Deliver real-time lead scoring, conversion prediction, and customer churn early warning",
            budget_allocated_usd=50000.0,
        )

        # 2. Dataset Version
        ds = self.projects_service.register_dataset_version(
            tenant_id=tenant_id,
            project_id=proj.id,
            dataset_name="gold_customer_features_v2",
            version="2.1.0",
            features_list=[
                "user_tenure_days", "mrr_usd", "login_frequency_weekly",
                "tickets_opened_30d", "nps_rating", "engagement_score",
            ],
            label_column="churned_within_90d",
            row_count=125000,
        )

        # 3. Experiment & Runs
        exp = self.experiments_service.create_experiment(
            tenant_id=tenant_id,
            project_id=proj.id,
            name="LightGBM vs XGBoost Churn Classifier",
            model_type=ModelType.CLASSIFICATION.value,
            framework=FrameworkType.LIGHTGBM.value,
            search_strategy="BAYESIAN",
        )
        run = self.experiments_service.log_experiment_run(
            tenant_id=tenant_id,
            experiment_id=exp.id,
            run_number=1,
            hyperparameters={"learning_rate": 0.03, "num_leaves": 31, "max_depth": 6},
            metrics={"accuracy": 0.948, "f1_score": 0.942, "roc_auc": 0.985},
            dataset_version_id=ds.id,
        )

        # 4. Registered Model & Version
        model = self.registry_service.register_model(
            tenant_id=tenant_id,
            project_id=proj.id,
            name="Customer Churn Risk Classifier",
            owner="dr.sarah.chen@uzaii.internal",
            model_type=ModelType.CLASSIFICATION.value,
            framework=FrameworkType.LIGHTGBM.value,
        )
        mv = self.registry_service.create_model_version(
            tenant_id=tenant_id,
            model_id=model.id,
            version="2.1.0",
            training_run_id=run.id,
            dataset_version_id=ds.id,
            metrics_summary={"accuracy": 0.948, "f1_score": 0.942, "roc_auc": 0.985},
        )
        mv.quality_gate_passed = True
        mv.security_scan_passed = True
        mv.governance_approved = True
        mv.stage = ModelStage.PRODUCTION.value
        model.current_stage = ModelStage.PRODUCTION.value

        # 5. Evaluation Suite & Result
        suite = self.evaluation_service.create_evaluation_suite(
            tenant_id=tenant_id,
            name="Churn Risk Golden Benchmark v2",
            target_model_type=ModelType.CLASSIFICATION.value,
        )
        self.evaluation_service.run_evaluation(
            tenant_id=tenant_id,
            suite_id=suite.id,
            model_version_id=mv.id,
        )

        # 6. Prompt
        self.prompts_service.register_prompt(
            tenant_id=tenant_id,
            name="Executive Decision Synthesis Prompt",
            purpose="Summarize predictive model inferences for C-level Decision Rooms",
            system_prompt="You are an executive intelligence analyst. Synthesize predictive metrics with strict fact/inference separation.",
            user_template="Customer: {{customer_name}}, Churn Risk: {{risk_score}}%, Factors: {{top_features}}",
            version="1.2.0",
        )

        # 7. Deployment & Inference Route
        depl = self.deployments_service.create_deployment(
            tenant_id=tenant_id,
            model_version_id=mv.id,
            environment="PRODUCTION",
            traffic_weight_pct=100.0,
            rollback_target_version_id=mv.id,
        )
        self.deployments_service.create_inference_endpoint(
            tenant_id=tenant_id,
            route_name="predict-churn-risk",
            primary_deployment_id=depl.id,
        )

        # 8. Monitoring Snapshot & Drift Event
        self.monitoring_service.record_monitoring_snapshot(
            tenant_id=tenant_id,
            deployment_id=depl.id,
            requests_count=85200,
            errors_count=12,
            avg_latency_ms=24.5,
            cost_usd=42.80,
        )
        self.monitoring_service.detect_and_record_drift(
            tenant_id=tenant_id,
            deployment_id=depl.id,
            metric_name="PSI",
            metric_value=0.08,
            threshold=0.25,
        )

        # 9. Model Card & Governance
        self.governance_service.create_model_card(
            tenant_id=tenant_id,
            model_version_id=mv.id,
            owner="dr.sarah.chen@uzaii.internal",
            steward="marcus.governance@uzaii.internal",
            intended_use="Predictive customer churn probability scoring to assist Customer Success managers.",
            limitations="Not calibrated for enterprise accounts with less than 14 days of tenure.",
            training_data_summary="Trained on 125,000 anonymized account quarters from Gold Customer Mart.",
            evaluation_summary="Achieved 94.8% accuracy and 0.985 ROC-AUC on 10,000 held-out test accounts.",
            ethical_considerations="Demographic features excluded. PII masked according to Phase 47/62 governance.",
        )
        self.governance_service.run_security_and_license_scan(
            tenant_id=tenant_id,
            model_version_id=mv.id,
            base_model_license="Apache-2.0",
        )
        self.governance_service.submit_governance_approval(
            tenant_id=tenant_id,
            model_version_id=mv.id,
            approver_email="marcus.governance@uzaii.internal",
        )

        # 10. GPU Job & FinOps Cost
        self.copilot_service.allocate_gpu_job(
            tenant_id=tenant_id,
            training_job_id="aitrain_seed_01",
            gpu_type="NVIDIA_A100_80GB",
            gpu_count=2,
        )
        self.copilot_service.record_finops_cost(
            tenant_id=tenant_id,
            project_id=proj.id,
            cost_category="INFERENCE_TOKENS",
            amount_usd=1420.0,
            units_consumed=28400000.0,
            model_id=model.id,
        )

    def get_platform_overview(self, tenant_id: str) -> Dict[str, Any]:
        """Aggregate high-level metrics for the AI Command Center."""
        projects = self.projects_service.list_projects(tenant_id)
        models = self.registry_service.list_models(tenant_id)
        deployments = self.deployments_service.list_deployments(tenant_id)
        suites = self.evaluation_service.list_suites(tenant_id)
        prompts = self.prompts_service.list_prompts(tenant_id)
        drift_events = self.monitoring_service.list_drift_events(tenant_id)
        gpu_jobs = self.copilot_service.list_gpu_jobs(tenant_id)
        finops = self.copilot_service.list_finops_costs(tenant_id)

        total_cost = sum(c.amount_usd for c in finops)

        return {
            "total_projects": len(projects),
            "total_models": len(models),
            "production_models": sum(1 for m in models if m.current_stage == ModelStage.PRODUCTION.value),
            "total_deployments": len(deployments),
            "evaluation_suites": len(suites),
            "governed_prompts": len(prompts),
            "active_drift_alerts": sum(1 for d in drift_events if d.is_breached),
            "active_gpu_jobs": len(gpu_jobs),
            "total_finops_cost_usd": total_cost,
            "platform_health_status": "OPTIMAL",
            "timestamp": datetime.utcnow().isoformat(),
        }
