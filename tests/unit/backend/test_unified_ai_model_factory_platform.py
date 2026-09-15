"""Unit Test Suite for Phase 63 — Unified AI/ML Model Factory, MLOps, LLMOps, Evaluation & Production AI Operating System."""

import pytest
import pytest_asyncio
from typing import Any, Dict

from backend.app.services.ai_model_factory.service import AiModelFactoryService
from backend.app.services.ai_model_factory.base import (
    ModelType,
    FrameworkType,
    ModelStage,
    DeploymentStrategy,
    DriftType,
)
from agents.core.context import AgentContext
from agents.core.permissions import (
    AgentPermission,
    AgentPermissionDeniedError,
    validate_agent_permissions,
    check_tool_permission,
    PROHIBITED_PERMISSIONS,
)
from agents.ai_platform import (
    ExperimentAgent,
    TrainingAgent,
    EvaluationAgent,
    ModelRegistryAgent,
    DeploymentAgent,
    InferenceAgent,
    MonitoringAgent,
    DriftAgent,
    RetrainingAgent,
    ModelGovernanceAgent,
    SecuritySafetyAgent,
    PromptRagopsAgent,
    AgentOpsAgent,
    GpuCostAgent,
    AiCopilotAgent,
)


class TestProjectsDatasetsFeatures:
    """Test AI Projects, Lakehouse Datasets, and Feature Leakage Validation."""

    def test_project_creation_and_listing(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_ai_01"

        proj = service.projects_service.create_project(
            tenant_id=tenant,
            name="Revenue Churn Model",
            owner="data.scientist@uzaii.internal",
            team="ML Core",
            domain="FINANCE",
            budget_allocated_usd=25000.0,
        )
        assert proj.id.startswith("aiproj_")
        assert proj.name == "Revenue Churn Model"
        assert proj.budget_allocated_usd == 25000.0

        projects = service.projects_service.list_projects(tenant)
        assert len(projects) == 1
        assert projects[0].id == proj.id

    def test_dataset_versioning_and_splits(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_ai_02"

        proj = service.projects_service.create_project(
            tenant_id=tenant,
            name="Lead Classifier",
            owner="ml.lead@uzaii.internal",
            team="Growth AI",
        )

        ds = service.projects_service.register_dataset_version(
            tenant_id=tenant,
            project_id=proj.id,
            dataset_name="features_leads_gold",
            version="1.0.0",
            features_list=["page_views_30d", "company_size", "email_verified", "country_tier"],
            label_column="converted",
            splits={"train": 0.80, "val": 0.10, "test": 0.10},
            row_count=45000,
        )
        assert ds.id.startswith("aids_")
        assert ds.bias_check_status == "PASSED"
        assert ds.splits["train"] == 0.80

        # Invalid splits sum
        with pytest.raises(ValueError, match="must sum to 1.0"):
            service.projects_service.register_dataset_version(
                tenant_id=tenant,
                project_id=proj.id,
                dataset_name="invalid_splits",
                version="1.0.0",
                features_list=["f1"],
                splits={"train": 0.60, "val": 0.20},  # sums to 0.80
            )

    def test_feature_leakage_and_pii_validation(self):
        service = AiModelFactoryService()

        # Clean features
        res_clean = service.projects_service.validate_features_leakage(
            features_list=["tenure_days", "activity_score", "plan_tier"],
            label_column="churned",
        )
        assert res_clean["is_valid"] is True
        assert len(res_clean["leaked_features"]) == 0
        assert len(res_clean["pii_flagged_features"]) == 0

        # Leaked label feature and PII feature
        res_bad = service.projects_service.validate_features_leakage(
            features_list=["tenure_days", "churned", "user_ssn_number"],
            label_column="churned",
        )
        assert res_bad["is_valid"] is False
        assert "churned" in res_bad["leaked_features"]
        assert "user_ssn_number" in res_bad["pii_flagged_features"]


class TestExperimentsTrainingHyperparameters:
    """Test AI Experiments, Bayesian Sweeps, and Training Jobs."""

    def test_experiment_tracking_and_best_metric(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_exp_01"

        exp = service.experiments_service.create_experiment(
            tenant_id=tenant,
            project_id="aiproj_exp_01",
            name="XGBoost Classifier Bayesian Sweep",
            model_type=ModelType.CLASSIFICATION.value,
            framework=FrameworkType.XGBOOST.value,
            best_metric_name="f1_score",
        )
        assert exp.id.startswith("aiexp_")
        assert exp.best_metric_value == 0.0

        run1 = service.experiments_service.log_experiment_run(
            tenant_id=tenant,
            experiment_id=exp.id,
            run_number=1,
            hyperparameters={"max_depth": 4, "learning_rate": 0.1},
            metrics={"f1_score": 0.912, "accuracy": 0.920},
        )
        assert exp.best_metric_value == 0.912

        run2 = service.experiments_service.log_experiment_run(
            tenant_id=tenant,
            experiment_id=exp.id,
            run_number=2,
            hyperparameters={"max_depth": 6, "learning_rate": 0.05},
            metrics={"f1_score": 0.945, "accuracy": 0.950},
        )
        assert exp.best_metric_value == 0.945

    def test_training_job_submission_and_loss_history(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_train_01"

        job = service.experiments_service.create_training_job(
            tenant_id=tenant,
            project_id="aiproj_01",
            model_name="Llama-3-FineTuned-Enterprise",
            epochs_total=5,
        )
        assert job.id.startswith("aitrain_")
        assert job.status == "COMPLETED"
        assert len(job.loss_history) == 5
        assert job.loss_history[0]["loss"] > job.loss_history[-1]["loss"]


class TestModelRegistryArtifacts:
    """Test Central Model Registry, Stage Promotion Gates, and Version Manifests."""

    def test_model_registration_and_versioning(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_reg_01"

        model = service.registry_service.register_model(
            tenant_id=tenant,
            project_id="aiproj_reg_01",
            name="Customer Retention Scorer",
            owner="senior.ml@uzaii.internal",
            model_type=ModelType.CLASSIFICATION.value,
            framework=FrameworkType.PYTORCH.value,
        )
        assert model.id.startswith("aimodel_")
        assert model.current_stage == ModelStage.EXPERIMENTAL.value

        mv = service.registry_service.create_model_version(
            tenant_id=tenant,
            model_id=model.id,
            version="1.0.0",
            metrics_summary={"accuracy": 0.942, "f1_score": 0.938},
        )
        assert mv.id.startswith("aimv_")
        assert mv.is_signed is True
        assert mv.quality_gate_passed is False

    def test_stage_promotion_gates_enforcement(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_reg_02"

        model = service.registry_service.register_model(
            tenant_id=tenant,
            project_id="aiproj_reg_02",
            name="Security Threat Detector",
            owner="sec.ml@uzaii.internal",
        )
        mv = service.registry_service.create_model_version(
            tenant_id=tenant,
            model_id=model.id,
            version="1.0.0",
        )

        # Unapproved promotion to PRODUCTION must fail
        with pytest.raises(PermissionError, match="Quality gate has not passed"):
            service.registry_service.evaluate_and_promote_stage(
                tenant_id=tenant,
                version_id=mv.id,
                target_stage=ModelStage.PRODUCTION.value,
                approver="sec.ml@uzaii.internal",
            )

        # Grant quality & security passed
        mv.quality_gate_passed = True
        mv.security_scan_passed = True

        # Still requires formal governance approval
        with pytest.raises(PermissionError, match="governance sign-off required"):
            service.registry_service.evaluate_and_promote_stage(
                tenant_id=tenant,
                version_id=mv.id,
                target_stage=ModelStage.PRODUCTION.value,
                approver="sec.ml@uzaii.internal",
            )

        # Grant formal governance
        mv.governance_approved = True
        promoted = service.registry_service.evaluate_and_promote_stage(
            tenant_id=tenant,
            version_id=mv.id,
            target_stage=ModelStage.PRODUCTION.value,
            approver="ai.steward@uzaii.internal",
        )
        assert promoted.stage == ModelStage.PRODUCTION.value
        assert model.current_stage == ModelStage.PRODUCTION.value


class TestEvaluationBenchmarksJudge:
    """Test Evaluation Benchmarks, LLM-as-a-Judge, and Quality Thresholds."""

    def test_deterministic_benchmark_suite(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_eval_01"

        suite = service.evaluation_service.create_evaluation_suite(
            tenant_id=tenant,
            name="Fraud Detection Golden Benchmark",
            target_model_type=ModelType.CLASSIFICATION.value,
            thresholds_config={"min_accuracy": 0.92},
            test_cases_count=5000,
        )
        assert suite.id.startswith("aisup_")

        res = service.evaluation_service.run_evaluation(
            tenant_id=tenant,
            suite_id=suite.id,
            model_version_id="aimv_fraud_01",
        )
        assert res.passed is True
        assert res.score >= 0.92
        assert "roc_auc" in res.detailed_metrics

    def test_llm_as_a_judge_evaluation(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_eval_02"

        suite = service.evaluation_service.create_evaluation_suite(
            tenant_id=tenant,
            name="RAG Faithfulness Judge",
            target_model_type=ModelType.LLM.value,
            suite_type="LLM_JUDGE",
        )

        res = service.evaluation_service.run_evaluation(
            tenant_id=tenant,
            suite_id=suite.id,
            model_version_id="aimv_llm_01",
            evaluator_engine="LLM_AS_JUDGE",
            judge_model="claude-3-5-sonnet",
        )
        assert res.passed is True
        assert res.judge_model == "claude-3-5-sonnet"
        assert res.detailed_metrics["faithfulness"] >= 0.90
        assert res.detailed_metrics["toxicity"] <= 0.01


class TestPromptsRagopsAgentops:
    """Test Prompts, RAGOps groundedness, and AgentOps telemetry."""

    def test_prompt_registry(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_prompt_01"

        prompt = service.prompts_service.register_prompt(
            tenant_id=tenant,
            name="Executive Summary Template",
            purpose="Generate high-level summaries for leadership",
            system_prompt="You are an enterprise strategic analyst.",
            user_template="Data: {{input_data}}",
        )
        assert prompt.id.startswith("aiprompt_")
        assert prompt.stage == "APPROVED"
        assert len(service.prompts_service.list_prompts(tenant)) == 1

    def test_ragops_evaluation_and_groundedness(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_rag_01"

        eval_res = service.prompts_service.evaluate_rag_pipeline(
            tenant_id=tenant,
            query="What were the Q2 revenue figures?",
            retrieved_contexts=["Context Chunk 1: Q2 Revenue was $2.1M"],
            generated_answer="Q2 revenue totaled $2.1M.",
        )
        assert eval_res.is_grounded is True
        assert eval_res.metrics["context_groundedness"] >= 0.90

    def test_agentops_telemetry_tracking(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_agentops_01"

        record = service.prompts_service.track_agentops_run(
            tenant_id=tenant,
            agent_name="DataQualityAgent",
            task_id="task_qa_01",
            tool_calls_count=5,
            planning_steps_count=3,
            errors_count=0,
            duration_seconds=2.45,
            cost_usd=0.018,
        )
        assert record.tool_accuracy_pct == 100.0
        assert record.task_outcome == "SUCCESS"


class TestDeploymentsInferenceRouting:
    """Test Canary Deployments, Policy Inference Gateway, and Rollback."""

    def test_canary_deployment_creation_and_routing(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_depl_01"

        depl = service.deployments_service.create_deployment(
            tenant_id=tenant,
            model_version_id="aimv_prod_01",
            strategy=DeploymentStrategy.CANARY.value,
            traffic_weight_pct=20.0,
        )
        assert depl.id.startswith("aidepl_")
        assert depl.traffic_weight_pct == 20.0

        ep = service.deployments_service.create_inference_endpoint(
            tenant_id=tenant,
            route_name="predict-risk",
            primary_deployment_id=depl.id,
        )
        assert ep.id.startswith("aiinf_")

        # Execute prediction
        pred = service.deployments_service.execute_inference_predict(
            tenant_id=tenant,
            endpoint_id=ep.id,
            input_payload={"account_id": "acc_001"},
        )
        assert pred["status"] == "SUCCESS"
        assert pred["prediction"]["label"] == "HIGH_VALUE_CUSTOMER"

    def test_instant_deployment_rollback(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_depl_02"

        depl = service.deployments_service.create_deployment(
            tenant_id=tenant,
            model_version_id="aimv_new_buggy",
            rollback_target_version_id="aimv_v1_stable",
        )
        rolled_back = service.deployments_service.rollback_deployment(
            tenant_id=tenant,
            deployment_id=depl.id,
            operator="sre.oncall@uzaii.internal",
        )
        assert rolled_back.status == "ROLLED_BACK"
        assert rolled_back.model_version_id == "aimv_v1_stable"


class TestMonitoringDriftFeedback:
    """Test Drift Detection (PSI), Monitoring rollups, and Retraining Triggers."""

    def test_feature_drift_psi_breach(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_drift_01"

        # Normal event
        normal_evt = service.monitoring_service.detect_and_record_drift(
            tenant_id=tenant,
            deployment_id="aidepl_01",
            metric_name="PSI",
            metric_value=0.08,
            threshold=0.25,
        )
        assert normal_evt.is_breached is False
        assert normal_evt.suggested_action == "NO_ACTION_REQUIRED"

        # Drift breach event
        breach_evt = service.monitoring_service.detect_and_record_drift(
            tenant_id=tenant,
            deployment_id="aidepl_01",
            metric_name="PSI",
            metric_value=0.32,
            threshold=0.25,
        )
        assert breach_evt.is_breached is True
        assert breach_evt.suggested_action == "TRIGGER_RETRAINING"

    def test_feedback_quality_validation_and_retraining(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_fb_01"

        fb = service.monitoring_service.submit_feedback(
            tenant_id=tenant,
            model_version_id="aimv_01",
            user_id="user_test_01",
            feedback_type="CORRECTION",
            correction_text="Account has actually renewed for 12 months.",
        )
        assert fb.quality_classification == "VALID"
        assert fb.is_included_in_retraining is True

        retrain_job = service.monitoring_service.trigger_retraining_workflow(
            tenant_id=tenant,
            model_id="aimodel_churn_01",
            reason="FEEDBACK_THRESHOLD_REACHED",
        )
        assert retrain_job.id.startswith("retrain_")
        assert retrain_job.status == "QUEUED"


class TestGovernanceSafetyGpuFinops:
    """Test Model Cards, SBOM scans, GPU allocation, FinOps, and Digital Twin simulations."""

    def test_model_card_and_sbom_security_scan(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_gov_01"

        card = service.governance_service.create_model_card(
            tenant_id=tenant,
            model_version_id="aimv_01",
            owner="dr.sarah@uzaii.internal",
            steward="marcus@uzaii.internal",
            intended_use="Lead scoring",
            limitations="None for B2B tech sector",
            training_data_summary="100k verified leads",
            evaluation_summary="94.5% accuracy",
            ethical_considerations="No demographic attributes utilized",
        )
        assert card.id.startswith("aimcard_")

        scan = service.governance_service.run_security_and_license_scan(
            tenant_id=tenant,
            model_version_id="aimv_01",
            base_model_license="Apache-2.0",
        )
        assert scan.passed is True
        assert scan.is_license_compliant is True

    def test_gpu_scheduling_and_finops_costs(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_finops_01"

        gpu_job = service.copilot_service.allocate_gpu_job(
            tenant_id=tenant,
            training_job_id="aitrain_01",
            gpu_type="NVIDIA_H100_SXM5_80GB",
            gpu_count=4,
        )
        assert gpu_job.id.startswith("gpu_")
        assert gpu_job.gpu_count == 4

        cost = service.copilot_service.record_finops_cost(
            tenant_id=tenant,
            project_id="aiproj_01",
            cost_category="INFERENCE_TOKENS",
            amount_usd=125.40,
            units_consumed=2508000.0,
        )
        assert cost.id.startswith("finops_")
        assert cost.amount_usd == 125.40

    def test_digital_twin_failure_simulation(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_twin_01"

        sim = service.copilot_service.simulate_digital_twin_scenario(
            tenant_id=tenant,
            scenario_type="GPU_NODE_FAILURE",
        )
        assert sim["scenario"] == "GPU_NODE_FAILURE"
        assert "failover" in sim["impact_summary"]

    def test_grounded_copilot_response(self):
        service = AiModelFactoryService()
        tenant = "tenant_test_copilot_01"

        resp = service.copilot_service.query_ai_copilot(
            tenant_id=tenant,
            query="What is the accuracy and stage of Customer Churn Risk Classifier?",
        )
        assert len(resp["facts"]) > 0
        assert len(resp["inferences"]) > 0
        assert len(resp["hypotheses"]) > 0
        assert len(resp["recommendations"]) > 0
        assert resp["confidence_score"] >= 0.90


class TestAiWorkforceAndPermissions:
    """Test all 15 AI Platform Agents, least privilege scopes, and prohibited actions."""

    @pytest.mark.asyncio
    async def test_agents_permission_and_execution(self):
        ctx = AgentContext(
            workflow_id="wf_ai_01",
            task_id="task_ai_01",
            agent_run_id="run_ai_01",
            metadata={"tenant_id": "test_tenant", "name": "Churn Classifier Sweep", "query": "What is model status?"},
        )

        agents = [
            ExperimentAgent(),
            TrainingAgent(),
            EvaluationAgent(),
            ModelRegistryAgent(),
            DeploymentAgent(),
            InferenceAgent(),
            MonitoringAgent(),
            DriftAgent(),
            RetrainingAgent(),
            ModelGovernanceAgent(),
            SecuritySafetyAgent(),
            PromptRagopsAgent(),
            AgentOpsAgent(),
            GpuCostAgent(),
            AiCopilotAgent(),
        ]

        for agent in agents:
            validate_agent_permissions(agent.permissions)
            assert len(agent.permissions) > 0

            # Execute agent task
            result = await agent.execute(ctx)
            assert result["status"] == "COMPLETED"

    def test_prohibited_actions_enforcement(self):
        prohibited_sample = [
            "AUTONOMOUS_DEPLOY_MODEL",
            "AUTONOMOUS_DELETE_MODEL",
            "AUTONOMOUS_PROMOTE_STAGE",
            "AUTONOMOUS_MODIFY_SAFETY_POLICY",
            "BYPASS_MODEL_QUALITY_GATE",
            "BYPASS_MODEL_SECURITY_SCAN",
            "FABRICATE_EVALUATION_METRICS",
            "EXPOSE_TRAINING_DATA_PII",
        ]

        for perm in prohibited_sample:
            assert perm in PROHIBITED_PERMISSIONS
            with pytest.raises(AgentPermissionDeniedError, match="strictly prohibited"):
                validate_agent_permissions({perm})
