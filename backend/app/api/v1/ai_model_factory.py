"""FastAPI REST Router for Phase 63 AI Model Factory."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

try:
    from backend.app.schemas.ai_model_factory import (
        AiCopilotQueryRequest,
        AiDatasetVersionRegisterRequest,
        AiDeploymentCreateRequest,
        AiEvaluationRunRequest,
        AiEvaluationSuiteCreateRequest,
        AiExperimentCreateRequest,
        AiExperimentRunLogRequest,
        AiFeedbackSubmitRequest,
        AiInferencePredictRequest,
        AiModelCardCreateRequest,
        AiModelRegisterRequest,
        AiModelStagePromoteRequest,
        AiModelVersionCreateRequest,
        AiProjectCreateRequest,
        AiPromptRegisterRequest,
    )
    from backend.app.services.ai_model_factory.service import AiModelFactoryService
except ImportError:
    from app.schemas.ai_model_factory import (
        AiCopilotQueryRequest,
        AiDatasetVersionRegisterRequest,
        AiDeploymentCreateRequest,
        AiEvaluationRunRequest,
        AiEvaluationSuiteCreateRequest,
        AiExperimentCreateRequest,
        AiExperimentRunLogRequest,
        AiFeedbackSubmitRequest,
        AiInferencePredictRequest,
        AiModelCardCreateRequest,
        AiModelRegisterRequest,
        AiModelStagePromoteRequest,
        AiModelVersionCreateRequest,
        AiProjectCreateRequest,
        AiPromptRegisterRequest,
    )
    from app.services.ai_model_factory.service import AiModelFactoryService

router = APIRouter(prefix="/ai-factory", tags=["AI Model Factory & MLOps Platform"])

# Singleton service instance
_service = AiModelFactoryService()


def get_ai_service() -> AiModelFactoryService:
    return _service


@router.get("/overview", response_model=Dict[str, Any])
async def get_platform_overview(
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    """Retrieve top-level platform overview metrics."""
    return service.get_platform_overview(tenant_id)


# Projects & Datasets
@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(
    req: AiProjectCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.projects_service.create_project(
        tenant_id=tenant_id,
        name=req.name,
        owner=req.owner,
        team=req.team,
        domain=req.domain,
        description=req.description,
        objective=req.objective,
        budget_allocated_usd=req.budget_allocated_usd,
    )


@router.get("/projects")
async def list_projects(
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.projects_service.list_projects(tenant_id)


@router.post("/datasets", status_code=status.HTTP_201_CREATED)
async def register_dataset_version(
    req: AiDatasetVersionRegisterRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.projects_service.register_dataset_version(
        tenant_id=tenant_id,
        project_id=req.project_id,
        dataset_name=req.dataset_name,
        version=req.version,
        features_list=req.features_list,
        label_column=req.label_column,
        source_lakehouse_dataset_id=req.source_lakehouse_dataset_id,
        splits=req.splits,
        row_count=req.row_count,
    )


@router.get("/datasets")
async def list_datasets(
    tenant_id: str = Query("default_tenant"),
    project_id: Optional[str] = None,
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.projects_service.list_dataset_versions(tenant_id, project_id)


# Experiments & Training
@router.post("/experiments", status_code=status.HTTP_201_CREATED)
async def create_experiment(
    req: AiExperimentCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.experiments_service.create_experiment(
        tenant_id=tenant_id,
        project_id=req.project_id,
        name=req.name,
        model_type=req.model_type,
        framework=req.framework,
        search_strategy=req.search_strategy,
        best_metric_name=req.best_metric_name,
        description=req.description,
    )


@router.get("/experiments")
async def list_experiments(
    tenant_id: str = Query("default_tenant"),
    project_id: Optional[str] = None,
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.experiments_service.list_experiments(tenant_id, project_id)


@router.post("/runs", status_code=status.HTTP_201_CREATED)
async def log_experiment_run(
    req: AiExperimentRunLogRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.experiments_service.log_experiment_run(
        tenant_id=tenant_id,
        experiment_id=req.experiment_id,
        run_number=req.run_number,
        hyperparameters=req.hyperparameters,
        metrics=req.metrics,
        git_commit_hash=req.git_commit_hash,
        dataset_version_id=req.dataset_version_id,
        duration_seconds=req.duration_seconds,
        cost_usd=req.cost_usd,
    )


@router.get("/runs")
async def list_runs(
    tenant_id: str = Query("default_tenant"),
    experiment_id: Optional[str] = None,
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.experiments_service.list_runs(tenant_id, experiment_id)


# Model Registry & Promotion
@router.post("/models", status_code=status.HTTP_201_CREATED)
async def register_model(
    req: AiModelRegisterRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.registry_service.register_model(
        tenant_id=tenant_id,
        project_id=req.project_id,
        name=req.name,
        owner=req.owner,
        model_type=req.model_type,
        framework=req.framework,
        steward=req.steward,
        description=req.description,
        tags=req.tags,
    )


@router.get("/models")
async def list_models(
    tenant_id: str = Query("default_tenant"),
    project_id: Optional[str] = None,
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.registry_service.list_models(tenant_id, project_id)


@router.post("/models/versions", status_code=status.HTTP_201_CREATED)
async def create_model_version(
    req: AiModelVersionCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.registry_service.create_model_version(
        tenant_id=tenant_id,
        model_id=req.model_id,
        version=req.version,
        training_run_id=req.training_run_id,
        dataset_version_id=req.dataset_version_id,
        metrics_summary=req.metrics_summary,
    )


@router.post("/models/promote")
async def promote_model_stage(
    req: AiModelStagePromoteRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    try:
        return service.registry_service.evaluate_and_promote_stage(
            tenant_id=tenant_id,
            version_id=req.version_id,
            target_stage=req.target_stage,
            approver=req.approver,
        )
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Evaluations
@router.post("/evaluations/suites", status_code=status.HTTP_201_CREATED)
async def create_evaluation_suite(
    req: AiEvaluationSuiteCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.evaluation_service.create_evaluation_suite(
        tenant_id=tenant_id,
        name=req.name,
        target_model_type=req.target_model_type,
        suite_type=req.suite_type,
        thresholds_config=req.thresholds_config,
        test_cases_count=req.test_cases_count,
    )


@router.post("/evaluations/run")
async def run_evaluation(
    req: AiEvaluationRunRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.evaluation_service.run_evaluation(
        tenant_id=tenant_id,
        suite_id=req.suite_id,
        model_version_id=req.model_version_id,
        evaluator_engine=req.evaluator_engine,
        judge_model=req.judge_model,
    )


# Prompts
@router.post("/prompts", status_code=status.HTTP_201_CREATED)
async def register_prompt(
    req: AiPromptRegisterRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.prompts_service.register_prompt(
        tenant_id=tenant_id,
        name=req.name,
        purpose=req.purpose,
        system_prompt=req.system_prompt,
        user_template=req.user_template,
        version=req.version,
        variables=req.variables,
        target_model_family=req.target_model_family,
        token_budget_max=req.token_budget_max,
    )


@router.get("/prompts")
async def list_prompts(
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.prompts_service.list_prompts(tenant_id)


# Deployments & Inference
@router.post("/deployments", status_code=status.HTTP_201_CREATED)
async def create_deployment(
    req: AiDeploymentCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.deployments_service.create_deployment(
        tenant_id=tenant_id,
        model_version_id=req.model_version_id,
        environment=req.environment,
        strategy=req.strategy,
        traffic_weight_pct=req.traffic_weight_pct,
        min_replicas=req.min_replicas,
        max_replicas=req.max_replicas,
        rollback_target_version_id=req.rollback_target_version_id,
    )


@router.get("/deployments")
async def list_deployments(
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.deployments_service.list_deployments(tenant_id)


@router.post("/inference/predict")
async def execute_inference(
    req: AiInferencePredictRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    try:
        return service.deployments_service.execute_inference_predict(
            tenant_id=tenant_id,
            endpoint_id=req.endpoint_id,
            input_payload=req.input_payload,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Monitoring & Drift
@router.get("/drift")
async def list_drift_events(
    tenant_id: str = Query("default_tenant"),
    deployment_id: Optional[str] = None,
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.monitoring_service.list_drift_events(tenant_id, deployment_id)


@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    req: AiFeedbackSubmitRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.monitoring_service.submit_feedback(
        tenant_id=tenant_id,
        model_version_id=req.model_version_id,
        user_id=req.user_id,
        feedback_type=req.feedback_type,
        rating_score=req.rating_score,
        correction_text=req.correction_text,
    )


# Governance & Model Cards
@router.post("/governance/model-cards", status_code=status.HTTP_201_CREATED)
async def create_model_card(
    req: AiModelCardCreateRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.governance_service.create_model_card(
        tenant_id=tenant_id,
        model_version_id=req.model_version_id,
        owner=req.owner,
        steward=req.steward,
        intended_use=req.intended_use,
        limitations=req.limitations,
        training_data_summary=req.training_data_summary,
        evaluation_summary=req.evaluation_summary,
        ethical_considerations=req.ethical_considerations,
        risk_level=req.risk_level,
    )


# Copilot & Digital Twin
@router.post("/copilot/query")
async def query_copilot(
    req: AiCopilotQueryRequest,
    tenant_id: str = Query("default_tenant"),
    service: AiModelFactoryService = Depends(get_ai_service),
):
    return service.copilot_service.query_ai_copilot(
        tenant_id=tenant_id,
        query=req.query,
    )
